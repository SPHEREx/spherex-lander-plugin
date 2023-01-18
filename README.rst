#####################
spherex-lander-plugin
#####################

This plugin configures Lander, the PDF landing page static site generator, for SPHEREx documents.

Installation
============

Right now the best way to install this package is through GitHub itself::

    python -m pip install git+https://github.com/SPHEREx/spherex-lander-plugin.git@main#egg=spherex-lander-plugin

This installation is done automatically as part of the `spherex-doc-workflows <https://github.com/SPHEREx/spherex-doc-workflows>`__ reusable GitHub Actions workflows.

Configuring these plugins
=========================

These plugins are configured via the `lander.yaml` file in a TeX document's repository.
All document types use the same theme plugin (`spherex`), but different parsing plugins.
Below are examples for different document types.

SSDC-MS
-------

.. code-block:: yaml

   source_path: SSDC-MS-000.tex
   parser: spherex-ssdc-ms
   theme: spherex
   canonical_url: https://spherex-docs.ipac.caltech.edu/SSDC-MS-000/

SSDC-PM
-------

.. code-block:: yaml

   source_path: SSDC-PM-000.tex
   parser: spherex-ssdc-pm
   theme: spherex
   canonical_url: https://spherex-docs.ipac.caltech.edu/SSDC-PM-000/

SSDC-DP
-------

.. code-block:: yaml

   source_path: SSDC-DP-000.tex
   parser: spherex-ssdc-dp
   theme: spherex
   canonical_url: https://spherex-docs.ipac.caltech.edu/SSDC-DP-000/

SSDC-IF
-------

.. code-block:: yaml

   source_path: SSDC-IF-000.tex
   parser: spherex-ssdc-if
   theme: spherex
   canonical_url: https://spherex-docs.ipac.caltech.edu/SSDC-IF-000/

SSDC-OP
-------

.. code-block:: yaml

   source_path: SSDC-OP-000.tex
   parser: spherex-ssdc-op
   theme: spherex
   canonical_url: https://spherex-docs.ipac.caltech.edu/SSDC-OP-000/

SSDC-TN
-------

.. code-block:: yaml

   source_path: SSDC-TN-000.tex
   parser: spherex-ssdc-tn
   theme: spherex
   canonical_url: https://spherex-docs.ipac.caltech.edu/SSDC-TN-000/

SSDC-TR
-------

.. code-block:: yaml

   source_path: SSDC-TR-000.tex
   parser: spherex-ssdc-tr
   theme: spherex
   canonical_url: https://spherex-docs.ipac.caltech.edu/SSDC-TR-000/

Development workflow
====================

Using a virtual environment is best practice.
To install the plugin within the virtual environment, along with development dependencies, run::

    make init

To run the full suite of test and linting commands (assuming Python 3.8 is available)::

    tox
