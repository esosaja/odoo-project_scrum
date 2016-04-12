# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
#              Danimar Ribeiro <danimaribeiro@gmail.com>                      #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
###############################################################################

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
