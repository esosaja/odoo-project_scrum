# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class ProjectBurndown(models.Model):
    _name = 'project.burndown'

    @api.multi
    def _current_sprint(self):
        for rec in self:
            rec.current_sprint_id = 1

    current_sprint_id = fields.Many2one('project.scrum.sprint',
                                        string="Current Sprint",
                                        compute="_current_sprint")
    sprint_id = fields.Many2one('project.scrum.sprint', string='Sprint')
    type = fields.Selection([('projected', "Projected"), ("real", "Real")],
                            string="Type")
    day = fields.Datetime("Day")
    points = fields.Float("Points")
