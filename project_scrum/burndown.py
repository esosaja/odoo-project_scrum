'''
Created on Nov 13, 2015

@author: developer
'''
from openerp import api, fields, models


class BurnDownReport(models.Model):
    _name = 'burndown.report'
    _description = 'Project Scrum Burndown Report'

    day = fields.Integer('Day')
    points = fields.Integer('Points')
    actual = fields.Integer('Actual')
    type = fields.Integer('type')
