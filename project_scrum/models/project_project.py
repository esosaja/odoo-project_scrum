# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    closed = fields.Boolean(u'Estado Concluído?')
    cancelled = fields.Boolean(u'Estado Cancelado?')
    

class ProjectTask(models.Model):
    _inherit = "project.task"
    _order = "sequence"

    user_id = fields.Many2one('res.users', 'Assigned to', select=True, track_visibility='onchange', default="")
    actor_ids = fields.Many2many(comodel_name='project.scrum.actors', string='Actor')
    sprint_id = fields.Many2one(comodel_name='project.scrum.sprint', string='Sprint')
    us_id = fields.Many2one(comodel_name='project.scrum.us', string='User Stories')
    use_scrum = fields.Boolean(related='project_id.use_scrum')
    closed = fields.Boolean(related='stage_id.closed')
    cancelled = fields.Boolean(related='stage_id.cancelled')
    description = fields.Html('Description')
    points = fields.Integer('Points')
    
    def _daterange(self, start_date, end_date):
        available_dates = []
        for n in range(int ((end_date - start_date).days)):
            single_date = start_date + timedelta(days=n, hours=12)
            if single_date.weekday() != 5 and single_date.weekday() != 6:
                available_dates.append(single_date)
        return available_dates
    
    def _update_projected_burndown(self, vals):  
        sprint = "sprint_id" in vals and self.env['project.scrum.sprint'].browse(vals["sprint_id"]) or self.sprint_id 
        if sprint and sprint.date_start and sprint.date_stop:
            bnd = self.env['project.burndown'].search([('sprint_id', '=', sprint.id)])
            for item in bnd:
                item.unlink()
            points = sprint.total_points
            if "points" in vals and self.id:
                points += (vals["points"] - self.points)

            start_date = datetime.strptime(sprint.date_start, DEFAULT_SERVER_DATE_FORMAT)
            end_date = datetime.strptime(sprint.date_stop, DEFAULT_SERVER_DATE_FORMAT) + timedelta(1)

            available_dates = self._daterange(start_date, end_date)
            closed_tasks = sprint.task_ids.filtered(lambda x: x.stage_id.closed)
            if "stage_id" in vals and self.id:
                stage = self.env['project.task.type'].browse(vals['stage_id'])
                if stage.closed:
                    closed_tasks |= sprint.task_ids.filtered(lambda x: x.id == self.id)
                elif self.stage_id.closed:
                    closed_tasks = closed_tasks.filtered(lambda x: x.id != self.id)

            points_day = points / float(len(available_dates) - 1 or 1)
            points_left = points
            points_real = points
            for single_date in available_dates:
                burndown = { 'type': 'projected', 'day': single_date,
                            'points': points_left, 'sprint_id': sprint.id }
                self.env['project.burndown'].create(burndown)
                points_left -= points_day
                if points_left < 0.1:
                    points_left = 0

                today_str = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                tasks_today = closed_tasks.filtered(
                    lambda x: datetime.strptime((x.date_end or today_str), DEFAULT_SERVER_DATETIME_FORMAT) >= single_date + timedelta(hours=-12) and \
                    datetime.strptime((x.date_end or today_str), DEFAULT_SERVER_DATETIME_FORMAT) < single_date + timedelta(hours=12))
                points_today = sum(task.points for task in tasks_today)
                points_real -= points_today
                burndown = { 'type': 'real', 'day': single_date,
                            'points': points_real, 'sprint_id': sprint.id }
                self.env['project.burndown'].create(burndown)
    
    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        default.update({
            'sprint_id': None,
        })
        return super(ProjectTask, self).copy(default)

    @api.model
    def create(self, values):
        result = super(ProjectTask, self).create(values)
        self._update_projected_burndown(values)
        return result

    @api.multi
    def write(self, vals):
        if self.env['project.task.type'].browse(vals.get('stage_id')).closed:
            vals['date_end'] = fields.datetime.now()
        if "points" in vals:
            self._update_projected_burndown(vals)
        if "stage_id" in vals:
            self._update_projected_burndown(vals)
                                                    
        return super(ProjectTask, self).write(vals)

    @api.model
    def _read_group_sprint_id(self, present_ids, domain, **kwargs):
        project = self.env['project.project'].browse(self._resolve_project_id_from_context())

        if project.use_scrum:
            sprints = self.env['project.scrum.sprint'].search([('project_id', '=', project.id)], order='sequence').name_get()
            return sprints, None
        else:
            return [], None

    @api.model
    def _read_group_us_id(self, present_ids, domain, **kwargs):
        project = self.env['project.project'].browse(self._resolve_project_id_from_context())

        if project.use_scrum:
            user_stories = self.env['project.scrum.us'].search([('project_id', '=', project.id)], order='sequence').name_get()
            return user_stories, None
        else:
            return [], None

    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        stage_obj = self.pool.get('project.task.type')
        order = stage_obj._order
        access_rights_uid = access_rights_uid or uid
        if read_group_order == 'stage_id desc':
            order = '%s desc' % order
        search_domain = []
        project_id = context.get('default_project_id', False)
        if project_id:
            search_domain += ['|', ('project_ids', '=', project_id)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(cr, uid, search_domain, order=order, access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x, y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))

        fold = {}
        for stage in stage_obj.browse(cr, access_rights_uid, stage_ids, context=context):
            fold[stage.id] = stage.fold or False
        return result, fold


    _group_by_full = {
        'sprint_id': _read_group_sprint_id,
        'us_id': _read_group_us_id,
        'stage_id': _read_group_stage_ids,
    }
