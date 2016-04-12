# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 Trustcode - www.trustcode.com.br                         #
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


class ResCompany(models.Model):
    _inherit = 'res.company'

    cancel_open_tasks_scrum = fields.Boolean(
        u'Cancelar tarefas abertas ao finalizar sprint')


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'project.config.settings'

    cancel_open_tasks_scrum = fields.Boolean(
        u'Cancelar tarefas abertas ao finalizar sprint', help="""
        Ao cancelar as tarefas abertas ele faz um cópia da mesma e adiciona
        a cópia ao primeiro estágio e muda a tarefa original para cancelada
        """)

    def get_default_cancel_open_tasks_scrum(
            self, cr, uid, fields, context=None):
        user = self.pool['res.users'].browse(cr, uid, uid, context)
        return {'cancel_open_tasks_scrum':
                user.company_id.cancel_open_tasks_scrum}

    @api.multi
    def set_cancel_open_tasks_scrum(self):
        self.env.user.company_id.cancel_open_tasks_scrum = \
            self.cancel_open_tasks_scrum
