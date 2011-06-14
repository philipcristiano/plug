NOSETESTS = nosetests -m '([Dd]escribe|[Ww]hen|[Ss]hould|[Tt]est)' -e DingusTestCase

unit-test:
	$(NOSETESTS) tests/unit/*.py

acceptance-test:
	$(NOSETESTS) tests/acceptance/*.py

develop:
	bin/python setup.py develop

.PHONY: dist
dist:
	bin/python setup.py sdist

virtualenv:
	virtualenv --no-site-packages --distribute .
