=======
History
=======

1.0.7 (2023-10-17)
------------------

* Release in PyPi.
* Minor tweaks in typos, link fixes, and other bits.

0.2.0 (2023-10-16)
------------------

* Complete refactor of how the functionality is provided under the hood; however, external API remains unchanged.
* Drop support for Python versions _less_ than 3.10 due to maintenance overhead.
* Bumped requirements, pre-commit hook versions.

0.0.4 (2023-04-24)
------------------

* Drop support for Python versions 3.8 and 3.9 due to maintenance overhead.
* Bumped requirements, pre-commit hook versions.
* Fixed an issue with the pagination tests as live data changed from the remote API.

0.0.3 (2022-06-21)
------------------

* Encode args before constructing the url, to fix issue when searching for some libraries.

0.0.1 (2022-05-06)
------------------

* Initial release with Search API wrapper.
