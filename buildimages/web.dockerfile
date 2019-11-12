FROM gwyddion/odoo:12.0

WORKDIR /odoo-dev/addon

ENV PIPENV_PIPFILE=/odoo-dev/addon/Pipfile

COPY Pipfile Pipfile.lock .pre-commit-config.yaml /odoo-dev/addon/

# Sync python dependencies
RUN pipenv sync --dev

EXPOSE 8069

CMD pipenv run odoo -c /odoo-dev/addon/config/odoo.conf --dev=all
