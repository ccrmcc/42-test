test:
	python dj42cc_test/manage.py test \
	    splash \
	    logger \
	    settings_context \

pep8:
	pep8 dj42cc_test/splash \
	     dj42cc_test/logger \
	     dj42cc_test/settings_context
