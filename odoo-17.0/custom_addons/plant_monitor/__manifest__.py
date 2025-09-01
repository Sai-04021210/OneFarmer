{
    'name': 'Plant Monitor',
    'version': '17.0.1.0.0',
    'category': 'Agriculture',
    'summary': 'Plant Monitoring System for Agriculture',
    'description': """
        Plant Monitoring System
        =======================
        This module provides functionality to monitor plants including:
        * Plant registration and information
        * Growth tracking
        * Health monitoring
        * Environmental data tracking
        * Irrigation and care schedules
    """,
    'author': 'OneFarmer',
    'website': 'https://www.onefarmer.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/plant_monitor_views.xml',
        'views/plant_monitor_menus.xml',
        'data/cron_jobs.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}