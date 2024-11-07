
prod:
	poetry run python ./manage.py migrate
	poetry run python ./manage.py createcachetable
	nginx &
	poetry run gunicorn --bind=0.0.0.0:${PORT} --workers=4 --threads 2 discord_bot_project.wsgi

debug:
	poetry run python manage.py runserver

autoformat:
	autopep8 --in-place --aggressive --aggressive ./**/*.py

lint:
	poetry run pylint ./

discord-bot:
	poetry run python ./manage.py discord_bot
