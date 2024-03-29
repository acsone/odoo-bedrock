* 2023-04-24: remove ``confd`` and generate ``odoo.cfg`` using ``envsubst``
* 2023-04-24: add support for ``ODOO_BASE_URL`` to set the ``web.base.url`` and
  ``web.base.url.freeze`` system parameters, and ``ODOO_REPORT_URL`` environment
  variables to set the ``report.url`` system parameter
* 2022-05-13: preliminary Odoo 16 support
* 2021-08-31: add warning banner when entering root shell
* 2021-08-31: build with github actions to ghcr.io
* 2020-06-12: postgres `apt repo <https://wiki.postgresql.org/wiki/Apt>`_ for easy installation
  of the latest postgres client tools if needed
* 2019-03-17: use go version of `kwkhtmltopdf <https://github.com/acsone/kwkhtmltopdf>`_ client instead python version
* 2019-03-07: use `kwkhtmltopdf <https://github.com/acsone/kwkhtmltopdf>`_ client instead of native wkhtmltopdf
* 2019-01-28: smarter default db_filter when db_name lists multiple dbs
* 2019-01-07: configurable db filter
* 2018-12-27: run start-entrypoint.d parts as odoo user instead of root
