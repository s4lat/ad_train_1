CONFIG = {
    # Don't forget to remove the old database (flags.sqlite) before each competition.

    # The clients will run sploits on TEAMS and
    # fetch FLAG_FORMAT from sploits' stdout.
    'TEAMS': {
        "Team KEK" : {"token" : "asdfx321", "ip" : "0.0.0.0"},
        "Team LOL" : {"token" : "eshkerelol", "ip" : "138.197.185.98"}
     },

     'TOKEN2TEAM': {
        "asdfx321" : "Team KEK",
        "eshkerelol" : "Team LOL",
     },

    'FLAG_FORMAT': r'[A-Z0-9]{31}=',
    'FLAGS_PER_ROUND' : 5

    'SUBMIT_FLAG_LIMIT': 50,
    'SUBMIT_PERIOD': 5,
    'FLAG_LIFETIME': 5 * 60,
    'ROUND_DURATION': 60,

    # Password for the web interface. You can use it with any login.
    # This value will be excluded from the config before sending it to farm clients.
    'SERVER_PASSWORD': '1234',

    # Use authorization for API requests
    'ENABLE_API_AUTH': False,
    'API_TOKEN': '00000000000000000000'
}