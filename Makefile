.PHONY: clean test lint rebuild run shell destroy install package

clean:
	find . -name '*.py[co]' -delete
	find ./src -name __pycache__ |xargs rm -rf

test:
	docker-compose run --service-ports web pipenv run odoo -c /odoo-dev/addon/config/odoo.conf -u library_app --test-enable --stop
	docker-compose run --service-ports web pipenv run odoo -c /odoo-dev/addon/config/odoo.conf -u library_member --test-enable --stop

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
	docker-compose run --service-ports web pipenv run odoo -c /odoo-dev/addon/config/odoo.conf -i library_app --stop
	docker-compose run --service-ports web pipenv run odoo -c /odoo-dev/addon/config/odoo.conf -i library_member --stop

package:
	docker-compose run web /bin/bash -c "rm -rf ./dist/* && pipenv run python -B setup.py sdist && pipenv run python -B setup.py bdist_wheel"
