CONFIG = {
    # Don't forget to remove the old database (flags.sqlite) before each competition.

    # The clients will run sploits on TEAMS and
    # fetch FLAG_FORMAT from sploits' stdout.
    'TEAMS': {
        'Team NPC' : '138.197.185.98', 
        'Team PEPPA' : '0.0.0.0',
        'Team SLAVES' : '1.1.1.1',
        'Team MASTERS' : '2.2.2.2',
        },
    'FLAG_FORMAT': r'[A-Z0-9]{31}=',

    'SYSTEM_PROTOCOL': 'ructf_http',
    'SYSTEM_URL': 'http://138.197.185.98/submit',
    'SYSTEM_TOKEN': '<TOKEN>',

    # The server will submit not more than SUBMIT_FLAG_LIMIT flags
    # every SUBMIT_PERIOD seconds. Flags received more than
    # FLAG_LIFETIME seconds ago will be skipped.
    'SUBMIT_FLAG_LIMIT': 50,
    'SUBMIT_PERIOD': 5,
    'FLAG_LIFETIME': 5 * 60,

    # Password for the web interface. You can use it with any login.
    # This value will be excluded from the config before sending it to farm clients.
    'SERVER_PASSWORD': 'adminadmin',

    # Use authorization for API requests
    'ENABLE_API_AUTH': False,
    'API_TOKEN': '00000000000000000000'
}
