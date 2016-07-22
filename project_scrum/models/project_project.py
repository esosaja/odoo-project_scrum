# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    closed = fields.Boolean(u'Estado Concluído?')
    cancelled_state = fields.Boolean(u'Estado Cancelado?')