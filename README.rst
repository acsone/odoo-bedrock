============================
Odoo Bedrock container image
============================

/!\ this is alpha stuff, use at your own risk, expect things to change /!\

This image is meant as a greatest common denominator foundation to run Odoo.

It is a BYOO (bring-your-own-odoo) image, which means you need
to create a derived image which adds your Odoo and addons.
This image does not mandate any particular installation method 
for Odoo and addons.

Features
========

* Ubuntu 18.04 minimal
* python
* confd
* gosu
* nano, less
* curl (TBC: to be removed, it's there only for installation
* Odoo external dependencies (wkhtmltopdf, lessc, etc),
  except python libraries which you need to provide yourself.

The entrypoint does the following:

* confd + gosu, mostly. TBC

Configuration
=============

TBC

Examples
========

These are typical Dockerfiles derived from this image.

Installing addons and Odoo from source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assume you have odoo source code in ``./src/odoo`` and your addons
in ``myaddons``. You can create the following Dockerfile::

  FROM acsone/odoo-bedrock:10.0-latest

  COPY ./src/odoo /odoo/src/odoo
  RUN python -m virtualenv /odoo \
    && /odoo/bin/pip install --no-cache-dir \
      -r /odoo/src/odoo/requirements.txt \
      -f https://wheelhouse.acsone.eu/manylinux1 \
    && /odoo/bin/pip install -e /odoo/src/odoo

  COPY ./addons /odoo/addons

  ENV ADDONS_PATH=/odoo/src/odoo/addons,/odoo/src/odoo/odoo/addons,/odoo/addons

Note the use of ``-f https://wheelhouse.acsone.eu/manylinux1`` to find binary wheels that work without additional system dependencies. This is not mandadatory but helps having an image without build tools.

Installing from pre-built manylinux wheels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your Odoo project is a regular python project with dependencies
(including Odoo itself) declared in a `requirements.txt` you can use
such a Dockerfile::

  FROM acsone/odoo-bedrock:10.0-latest

  RUN python -m virtualenv /odoo \
    && /odoo/bin/pip install --no-index --no-deps /tmp/release/*.whl

This method assumes the wheel files, including Odoo itself,
have been built outside the container before hand using, for example,
`pip wheel -r requirements.txt --wheel-dir=release/`.

Notice there is no COPY statement. That's because you can use
`buildah <https://github.com/containers/buildah>`_ to create an OCI compliant image,
using a bind mounted volume during build::

  buildah bud --volume $PWD/release:/tmp/release -t image:tag .

Credits
=======

Some inspiration has been drawn from `camptocamp/odoo-project <https://github.com/camptocamp/docker-odoo-project>`_
in particular the odoo config file templates, entrypoint.sh and the travis config.

Contributors
~~~~~~~~~~~~

* Stéphane Bidoul <stephane.bidoul@acsone.eu>
