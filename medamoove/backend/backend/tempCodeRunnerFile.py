SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id':os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
    }
}