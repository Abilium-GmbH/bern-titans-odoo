{
    'name': 'Google Multi Calendar',
    'summary': 'Multi google calendar module for odoo',
    'version': '0.1',
    'category': 'Calendar',
    'license': 'LGPL-3', 
    'author': 'Abilium GmbH',
    'website': 'http://www.abilium.com',
    'live_test_url': '',
    'contributors': [
        'Severin Zumbrunn <severin.zumbrunn@abilium.com>',
    ],
    'depends': [
        'calendar',
        'google_calendar',
    ],
    'data': [
        'data/calendar.xml',
        'views/calendar.xml'
    ],
    'assets': {

    },
    'images': [

    ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'uninstall_hook': False,
}
