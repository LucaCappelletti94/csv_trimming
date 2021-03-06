csv_trimming
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

Package python to remove common ugliness from a csv-like file.

Sometimes when working with CSVs that are exported from excel
or generally from software that do not primarily focus
on exporting well formatted CSVs, CSV files are exported
with empty columns or padding around.

This package is to fix that kind of issues.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install csv_trimming

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime
get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Package python to remove common ugliness from a csv-like file


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/csv_trimming.png
   :target: https://travis-ci.org/LucaCappelletti94/csv_trimming
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_csv_trimming&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_csv_trimming
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_csv_trimming&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_csv_trimming
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_csv_trimming&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_csv_trimming
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/csv_trimming/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/csv_trimming?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/csv-trimming.svg
    :target: https://badge.fury.io/py/csv-trimming
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/csv-trimming
    :target: https://pepy.tech/badge/csv-trimming
    :alt: Pypi total project downloads

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/0968ff39b133475da3a9c528b8ae2c9d
    :target: https://www.codacy.com/manual/LucaCappelletti94/csv_trimming?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/csv_trimming&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/1e95e0c5b6331cbf85aa/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/csv_trimming/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/1e95e0c5b6331cbf85aa/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/csv_trimming/test_coverage
    :alt: Code Climate Coverate
