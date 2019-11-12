.PHONY: clean test lint rebuild run shell destroy install package repl debug

clean:
	find . -name '*.py[co]' -delete
	find ./src -name __pycache__ |xargs rm -rf

test:
	docker-compose run --service-ports web pipenv run odoo -c /odoo-dev/addon/config/odoo.conf -u library_checkout --test-enable --stop

lint:
	docker-compose run web pipenv run pre-commit run --all-files

rebuild:
	docker-compose build

run:
	docker-compose up

shell:
	docker-compose run --service-ports web env SHELL=/bin/bash /bin/bash -c "pipenv shell"

destroy:
	docker-compose down -v

install:
	docker-compose run --service-ports web pipenv run odoo -c /odoo-dev/addon/config/odoo.conf -i library_checkout --stop

package:
	docker-compose run web /bin/bash -c "rm -rf ./dist/* && pipenv run python -B setup.py sdist && pipenv run python -B setup.py bdist_wheel"

repl:
	docker-compose run --service-ports web pipenv run odoo shell -c /odoo-dev/addon/config/odoo.conf

debug:
	docker-compose run --service-ports web pipenv run odoo -c /odoo-dev/addon/config/odoo.conf --dev=all
