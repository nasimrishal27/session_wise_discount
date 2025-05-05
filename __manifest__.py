# -*- coding: utf-8 -*-
{
    'name': "POS Session Wise Discount",
    'version': '1.0',
    'depends': ['base', 'point_of_sale'],
    'author': "Suni",
    'description': """
    POS Session Wise Discount
    """,
    # data files always loaded at installation
    'data': [
        'views/res_config_settings_views.xml',
        "views/pos_session_discount_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "session_wise_discount/static/src/js/payment_button_override.js",
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}

