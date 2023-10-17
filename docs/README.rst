=============
Quibraries
=============

|PyPi| |Supported Python versions| |lint| |coverage|

Quibraries is a `Python`_ wrapper for the `libraries.io`_ API which is based on `Pybraries`_.
Currently the package fully supports the searching functionality, meaning that the full range of available commands
from `libraries.io`_ is supported.

The full documentation is hosted at `Read the Docs`_.

Differences with Pybraries
___________________________

The main reason of existence of this package is that `Pybraries`_ is not *thread-safe*.
Further, the ``API`` key can be provided only as an environment variable, which makes it difficult to change
during execution. Additionally, is when a query returns multiple pages, in `Pybraries`_ the iteration has to
happen manually and by the user. This is because the returned object is not ``Iterable``, thus convenient
"pythonic" constructs cannot be used. The aforementioned reasons (and their associated pain points) sparked the
creation of this project which aims to offer what `Pybraries`_ does, but also adding these - to us - important
features.

Key Terms
_________

Below a list of the key terms if provided which is synonymous with the `libraries.io`_ concepts.

    *host*
        A repository host platform. e.g. GitHub

    *owner*
        A repository owner. e.g. pandas-dev

    *repo*
        A repository. e.g. pandas

    *user*
        A repository user  e.g. a GitHub username. e.g. discdiver

    *platform*
        A package manager platform. e.g. PyPI

    *project*
        A package or library distributed by a package manager platform. e.g. pandas


It is important to note that many repositories and projects share the same name. Additionally, many owners and repos
also share the same name. Further, many owners are also users.

Since this library is a wrapper around functionality that is already provided by `libraries.io`_ the items
returned are dependent on the API response. In normal circumstances, the answer type is defined by the number of
returned items. In the case of a single element returned, then it is a dictionary. If the result contains more than
one item, then the result is a list of dictionaries.

Docs
____

* Check out the full quibraries `documentation`_.

Getting Help
____________

#. Check out the quibraries documentation_.
#. Check out the `libraries.io`_ docs.
#. Open an issue on `GitHub`_ or tag a question on `Stack Overflow`_ with "quibraries".

Contributing
____________

* Contributions are welcome and appreciated! See `Contributing`_.

License
_______

This software package is governed by the terms and conditions of the `MIT license`_

.. |lint| image:: https://github.com/andylamp/quibraries/actions/workflows/lint.yml/badge.svg
.. |coverage| image:: ../coverage.svg
.. |PyPi| image:: https://img.shields.io/pypi/v/quibraries?style=round-square
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/quibraries?style=round-square
.. _MIT License: https://github.com/andylamp/quibraries/blob/master/LICENSE
.. _Contributing: https://quibraries.readthedocs.io/en/latest/CONTRIBUTING.html
.. _Read the Docs: https://quibraries.readthedocs.io/en/latest/README.html
.. _documentation: https://quibraries.readthedocs.io/en/latest/README.html
.. _libraries.io: https://libraries.io
.. _GitHub: https://github.com/andylamp/quibraries/issues
.. _Stack Overflow: https://stackoverflow.com/questions/ask
.. _Pybraries: https://github.com/pybraries/pybraries
.. _Python: https://www.python.org
