# Xudos

## Installation

MySQL

Python Version 2.7

`pip install -r requirements.txt`

## Config

`config.cfg`

	DEBUG = True
	HOST = '0.0.0.0'
	PORT = 5000
	SLIDESHOW_DELAY = 20000
	SECRET_KEY = ''
	SESSION_TYPE = 'filesystem'
	SESSION_FILE_DIR = 'xudos/storage/sessions'
	SESSION_FILE_THRESHOLD = 500
	LOG_FILE_APPLICATION = 'xudos/storage/logs/app.log'
	LOG_FILE_ACCESS = 'xudos/storage/logs/access.log'
	LOG_ACCESS_FORMAT = '%(asctime)s %(process)d %(message)s'
	LOG_APP_FORMAT = '%(asctime)s %(levelname)s %(process)d %(message)s %(pathname)s:%(lineno)d:%(funcName)s()'
	LOG_WHEN = 'midnight'
	LOG_INTERVAL = 1
	LOG_BACKUP_COUNT = 14
	MAIL_ENABLED = False
	MAIL_SERVER = ''
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = ''
	MAIL_PASSWORD = ''
	MAIL_FROM_NAME = 'Xpanxion Xudos'
	MAIL_FROM_EMAIL = ''

`dbconfig.cfg`

	[db]
	mysql_username = username
	mysql_password = password
	mysql_host = localhost
	mysql_database = xudos
	pool_recycle = 3600
	autocommit = False
	autoflush = False
