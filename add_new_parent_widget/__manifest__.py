# -*- coding: utf-8 -*-
{
    'name': "Add new Parent widget",
    'summary': "Add new Parent widget",
    'description': """
        This module allow a vistor parent to be able to add some info quickly .
    """,
    'version': '15.0.1',
    'author': 'AICSK Team',
    'website': 'http://www.aicks.org/',
    'support': 'AICSK Team',
    'maintainer': 'AICSK Team',
    'license': 'AGPL-3',
    'category': 'Tutorial',
    'depends': [
        'base',
        'web'
    ],
    'data': [
        'views/add_new_parent_widget_view.xml'
    ],
    'assets': {
        'web.assets_backend':[
            'add_new_parent_widget/static/src/js/add_new_parent_widget.js',
            'add_new_parent_widget/static/src/css/add_new_parent_widget.css',
        ],
        'web.assets_qweb': [
            'add_new_parent_widget/static/src/xml/add_new_parent_widget.xml',
        ],
    },
    'demo': [],
    'images': [
        'static/description/icon.png'
    ],
    'installable': True,
    'application': False,
}

