CONFIG = {
    'TEAMS': {
        "Team NPC" : {"token" : "asdfx321", "ip" : "host.docker.internal"},
     },

     'TOKEN2TEAM': {
        "asdfx321" : "Team NPC",
     },

    'FLAG_FORMAT': r'[A-Z0-9]{31}=',

    'FLAGS_PER_ROUND' : 5,
    'SUBMIT_FLAG_LIMIT': 50,
    'SUBMIT_PERIOD': 5,
    'FLAG_LIFETIME': 5 * 60,
    'ROUND_DURATION': 60,

    'CODE2STATUS' : {101 : "OK", 102 : "CORRUPT", 103 : "MUMBLE", 104 : "DOWN"},
}