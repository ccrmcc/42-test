test:
	python dj42cc_test/manage.py test splash logger

pep8:
	pep8 dj42cc_test/splash dj42cc_test/logger

coverage:
	@echo Creating tests coverage report
	coverage run --source=dj42cc_test dj42cc_test/manage.py test splash logger \
	&& coverage report

pyflakes:
	@echo Executing PyFlakes checks...
	find . | grep '\.py$$' | grep -v '__init__' | \
		grep -v -E '(manage|settings|_testing)' | xargs -I {} pyflakes {}
