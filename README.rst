============================
Odoo Bedrock container image
============================

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
* nano, less, curl
* Odoo external dependencies (wkhtmltopdf, lessc, etc),
  except python libraries which you need to provide yourself.

The entrypoint does the following:

* confd + gosu, mostly. TBC

Configuration
=============

TBC

Credits
=======

Some inspiration has been drawn from camptocamp's odoo-project image.

Contributors
~~~~~~~~~~~~

* Stéphane Bidoul <stephane.bidoul@acsone.eu>
