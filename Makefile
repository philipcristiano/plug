NOSETESTS = bin/nosetests -m '([Dd]escribe|[Ww]hen|[Ss]hould|[Tt]est)' -e DingusTestCase

test:
	$(NOSETESTS) tests/*.py

clean:
	-rm -rf dist

develop:
	bin/python setup.py develop

.PHONY: dist
dist: clean
	bin/python setup.py sdist
	cp dist/plug-*.tar.gz dist/plug-latest.tar.gz

virtualenv:
	virtualenv --no-site-packages --distribute .

requirements: virtualenv
	bin/pip install -r requirements.pip
	bin/easy_install nose_machineout

create: dist
	bin/plug create --package=dist/plug-0.1.0.tar.gz
	cp plug-*.tar.gz.plug plug.plug

install: create package_puppet
	bin/fab deploy

package_puppet:
	tar cfz puppet.tgz puppet

bootstrap: package_puppet
	bin/fab bootstrap

