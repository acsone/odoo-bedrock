============================
Odoo Bedrock container image
============================

``/!\ this is alpha stuff, use at your own risk, expect things to change /!\``

This image is meant as a greatest common denominator foundation to run Odoo.

It is a BYOO (bring-your-own-odoo) image, which means you need
to create a derived image that adds your Odoo and addons.
This image does not mandate any particular installation method
for Odoo and addons, nor does it impose any constraint on your project
structure.

.. contents::

Features
========

* Ubuntu minimal because it's small and has recent pythons
  
  * 20.04 for Odoo 14 images
  * 18.04 for Odoo <= 13 images

* ``python``, obviously. 
* `confd <https://github.com/kelseyhightower/confd>`_ to generate
  the Odoo configuration file from environment variables or any other source
* `gosu <https://github.com/tianon/gosu>`_ to step down from root in the entrypoint
* ``nano``, ``less``, for some rudimentary comfort when the time comes to investigate
  the container on the terminal
* ``/usr/local/bin/wkhtmltopdf`` is the `kwkhtmltopdf
  <https://github.com/acsone/kwkhtmltopdf>`_ client. The default
  KWKHTMLTOPDF_SERVER_URL environment variable is set to http://kwkhtmltopdf.
* Odoo mandatory external dependencies (i.e. ``lessc`` for Odoo < 12)
* postgres `apt repo <https://wiki.postgresql.org/wiki/Apt>`_ for easy installation
  of the latest postgres client tools if needed

Note **Odoo's python dependencies are not included**: you need to pip install
Odoo's ``requirements.txt``, or apt install them.
This is not done in the base image as different projects
may require different versions of these libraries.

Other dependencies are also notably absent (graphviz, antiword, poppler-utils),
these being unused in the latest Odoo version and infrequently used in older
versions.

The entrypoint does the following:

* confd + gosu, `mostly <./bin/entrypoint.sh>`_.
* run scripts in /odoo/start-entrypoint.d/

Configuration
=============

TBC

Required environment variables:

* ``DB_HOST``, ``DB_USER``, ``DB_PASSWORD``, ``DB_NAME``

Examples
========

These are typical Dockerfiles derived from this image, provided here
for inspiration.

Installing addons and Odoo from source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assume you have odoo source code in ``./src/odoo`` and your addons
in ``myaddons``. You can create the following Dockerfile:

.. code:: dockerfile

  FROM quay.io/acsone/odoo-bedrock:10.0-latest

  COPY ./src/odoo /odoo/src/odoo
  RUN \
    pip install --no-cache-dir \
      -r /odoo/src/odoo/requirements.txt \
      -f https://wheelhouse.acsone.eu/manylinux1 \
    && pip install -e /odoo/src/odoo

  COPY ./myaddons /odoo/myaddons

  ENV ADDONS_PATH=/odoo/src/odoo/addons,/odoo/src/odoo/odoo/addons,/odoo/myaddons

Note the use of ``-f https://wheelhouse.acsone.eu/manylinux1`` to
find binary wheels that work without additional system dependencies.
This is not mandadatory but helps having an image without build tools.

Installing from pre-built manylinux wheels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your Odoo project is a regular python project with dependencies
(including Odoo itself) declared in a ``requirements.txt`` you can use
such a Dockerfile:

.. code:: dockerfile

  FROM quay.io/acsone/odoo-bedrock:10.0-latest

  RUN pip install --no-index --no-deps /tmp/release/*.whl

This method assumes the wheel files, including Odoo itself,
have been built outside the container before hand using, for example:

.. code:: bash

  pip wheel -r requirements.txt --wheel-dir=release/

Notice there is no COPY statement. That's because you can use
`buildah <https://github.com/containers/buildah>`_ to create an OCI compliant image,
using a bind mounted volume during build:

.. code:: bash

  buildah bud --volume $PWD/release:/tmp/release -t image:tag .

Credits
=======

Inspiration has been drawn from
`camptocamp/docker-odoo-project <https://github.com/camptocamp/docker-odoo-project>`_
for most environment variables, the odoo config file templates,
entrypoint.sh and the travis config.
This is by design, in order to facilitate possible future convergence.

Contributors
~~~~~~~~~~~~

* Stéphane Bidoul <stephane.bidoul@acsone.eu>
