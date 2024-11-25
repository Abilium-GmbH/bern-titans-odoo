# -*- coding: utf-8 -*-
{
    'name': "QR Invoice Combined",

    'summary': """
    With this module allows to print invoices with the QR invoice attached.
    """,

    'description': """
    """,

    'author': "Abilium GmbH",
    'website': "https://www.abilium.io",

    'category': 'Uncategorized',
    'version': '0.1',
    'application': False,

    'depends': [
        'base',
        'account',
        'l10n_ch',
        'account_edi',
    ],

    'data': [
        'views/account_move.xml'
    ]
}
