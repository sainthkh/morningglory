from django.conf import settings

import configparser

config = configparser.ConfigParser()
config.read(settings.SECRET_ROOT + 'wp.conf', encoding='utf-8')

settings.DATABASES['wpdb'] = {
	'ENGINE': 'mysql.connector.django',
	'NAME': config['WP']['name'],
	'PASSWORD': config['WP']['password'],
	'USER': config['WP']['user'],
	'OPTIONS': {
          'autocommit': True,
        },
	'HOST': 'localhost',
	'PORT': '3306',
}

settings.INSTALLED_APPS += [
	'data.apps.DataConfig',
]

WP_PREFIX = config['WP']['prefix']