{
    'name': 'Bern Titans Core Module',
    'summary': 'Customizations for bern titans',
    'version': '0.1',
    'category': '',
    'license': 'LGPL-3', 
    'author': 'Abilium GmbH',
    'website': 'http://www.abilium.com',
    'live_test_url': '',
    'contributors': [
        'Severin Zumbrunn <severin.zumbrunn@abilium.com>',
    ],
    'depends': [
        'base',
        'contacts',
        'google_multi_calendar'
    ],
    'data': [
        'views/res_partner.xml',
        'views/calendar.xml',
        'security/ir.model.access.csv',
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
