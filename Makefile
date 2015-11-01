run: clean
	python manage.py runserver --settings=tcc.settings_local

test: clean
	python manage.py test --settings=tcc.settings_test

coverage: clean
	python manage.py test --settings=tcc.settings_coverage

shell: clean
	python manage.py shell --settings=tcc.settings_local


clean:
	find . -name "*.pyc" -exec rm -rf {} \;
