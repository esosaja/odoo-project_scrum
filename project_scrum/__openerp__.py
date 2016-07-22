# -*- coding: utf-8 -*-

{
    'name': 'Project Scrum',
    'version': '10.0.2.0.0',
    'category': 'Project Management',
    'author': 'Vertel AB, Trustcode',
    'website': 'http://www.trustcode.com.br',
    'depends': ['project', 'mail'],
    'data': ['views/burndown_view.xml',
             'project_scrum_view.xml',
             'wizard/project_scrum_test_task_view.xml',
             'security/ir.model.access.csv',
             'security/project_security.xml',
             'security/project_task.xml',
             'views/project_config_settings_view.xml',
             'views/project_project.xml',
    ],
    'demo': ['project_scrum_demo.xml'],
    'installable': True,
}
