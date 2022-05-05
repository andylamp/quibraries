============
Contributing
============

Contributions are welcome and greatly appreciated. Please ensure while contributing or interacting with
the developers that you follow our
`Code of Conduct <https://github.com/andylamp/quibraries/blob/master/code_of_conduct.md>`_.

Types of Contributions
----------------------

Report Security Vulnerabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you think you have found a security vulnerability,
please email axorl@quine.sh.

Please don't report it in an GitHub issue or in any other public discourse platform.


Report Bugs and Make Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open an issue in our `GitHub Repo <https://github.com/andylamp/quibraries/issues>`_.


Write Code
~~~~~~~~~~

Feel free to look through the GitHub issues for open issues.
Anything tagged with "help wanted" is available to fix.

Please ensure new and altered features have tests and are
documented with DocStrings.


Write Documentation
~~~~~~~~~~~~~~~~~~~

We want pybraries users to have a great experience.
Documentation is a huge part of Developer Experience.

Feel free to add to and improve the documentation.
You can contribute to official pybraries docs,
in docstrings, or by writing blog posts.

Small changes to the docs can be made by editing the code on GitHub
in the browser and opening a Pull Request (PR).

If making more substantial changes or additions:

When in the docs folder, build the docs with the command::

    make html

The built HTML docs will be created in the docs->_build folder.

Check for broken links by running the following command::

    make linkcheck


Get Started!
------------

Ready to contribute? Here's how to set up `pybraries` for local development.

#. Fork the `quibraries` repo on GitHub.
#. Clone your fork locally::

    git clone git@github.com:your_github_username_here/quibraries.git

#. Install your local copy into a virtual environment.

#. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature-branch

   Now you can make your changes locally.

#. Install requirements.txt with::

    pip install -r requirements.txt

#. To ensure code quality we use a few tools as `pre-commit hooks <https://pre-commit.com/>`_, which need to pass.

#. When you're done making changes, check that your changes pass the test suite and Flake8::

    pytest flake8

#. Commit your changes and push your branch to GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

#. Submit a Pull Request (PR) through GitHub.

If you are new to contributing to open source, check out `this guide <https://github.com/chalmerlowe/intro_to_sprinting>`_ by Chalmer Lowe.

Code Quality
------------

We use as described above few tools as `pre-commit hooks <https://pre-commit.com/>`_. Most notably, we use
`black <https://black.readthedocs.io/en/stable/the_black_code_style/index.html>`_ for code formatting and
`Flake8 <https://flake8.pycqa.org/en/latest/>`_ plus `Pylint <https://pylint.pycqa.org/en/latest/>`_ for linting.

Max line length is set to 119 characters and the following warnings/errors are ignored:

* E203 - Whitespace before, this is because it conflicts with the `black` code formatter in some instances.
* W503 - Break occurred before a binary operator, this is in the process of being `deprecated <https://www.flake8rules.com/rules/W503.html>`_.

The full list of linters can be seen in the ``pre-commit-config.yaml`` file located in the main directory
of the project.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. If code was updated, the pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The code should work for Python 3.8 and higher.

Deploying
---------

A reminder for the maintainers on how to deploy.

#. Make sure all changes are committed (including an entry in history.rst).

#. Then run::

    bumpversion2 patch      # possible: major / minor / patch
    git push
    git push --tags

#. Build with::

    python setup.py sdist bdist_wheel

#. Use twine to upload to PyPI.

#. Update the Releases section on GitHub.
