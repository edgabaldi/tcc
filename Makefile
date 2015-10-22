run: clean
	python manage.py runserver --settings=tcc.settings_local

test: clean
	python manage.py test --settings=tcc.settings_test

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
