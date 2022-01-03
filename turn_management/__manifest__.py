# -*- coding: utf-8 -*-
{
    'name': "Turn management",
    'summary': "Turn management module",
    'description': """
        This module allow a manage visitor turn .
    """,
    'version': '15.0.1',
    'author': 'AICSK Team',
    'website': 'http://www.aicks.org/',
    'support': 'AICSK Team',
    'maintainer': 'AICSK Team',
    'license': 'AGPL-3',
     'depends': [
        'base',
        'web',
        'mail'
    ],
    'data': [],
    'assets': {
        'web.assets_backend':[
            'turn_management/static/src/js/systray_turn.js',
        ],
        'web.assets_qweb': [
            'turn_management/static/src/xml/systray_turn.xml',
        ],
    },
    'demo': [],
    'images': [
        'static/description/icon.png'
    ],
    'installable': True,
    'application': True,
}

