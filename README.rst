.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black

Motivation
----------

The main motivation for the project is to be able to use structlog as a standard logging
solution for both applications and packages, while a the end our application logs are
sent to a Seq server.
Keeping in mind the Twelve Factor App's guide on logging: https://12factor.net/logs.

Obstacles to overcome:

* If using Seq's official logging solution `seqlog <https://seqlog.readthedocs.io/>`_
you have to rely on the full robust solution, with logging, handlers and a server.
This makes logging too robust for my taste.
* with containerized python applications using structlog for creating log entries,
and Seq server ingesting log events.

Use case
--------

Application and package logs are collected and formatted with a structlog formatter chain,
where the structlog_seq_formatters are added towards the end of the chain.
For docker container based applications using structlog JsonRenderer as the final formatter is sufficient,
after that, docker's GELF log-driver forwards the event to the Seq server, thus the application only logs to stdout.
Docker gelf docs: https://docs.docker.com/config/containers/logging/gelf/

For local development, instead of rendering an event to JSON, the CLEF renderer can be used.

Demo
----

Prerequisites
*************
* `Docker <https://docs.docker.com/get-started/>`_
* `Docker-compose <https://docs.docker.com/compose/>`_

Run the demo
************

* Run the SEQ server: ``docker-compose -f seq_test_server/docker-compose.yml up -d``
* Run the demo script: ``docker-compose -up``
* Open local `Seq server <http://localhost>`_


Goals
-----

- [ ] a formatter implementation that can be added to the structlog formatter chain. Its purpose is
      to convert the event dictionary to the CLEF format.
- [ ] a formatter that adds renderings for the message template tokens, ie.: round float values.
      A basic rendering should be to call __str__() on the object.
      This implementation should take type specific formatters as external dependencies.
- [ ] a renderer implementation that can be added to the end of the formatter chain, that provides readable
      rendered format from CLEF. This is mainly useful for local testing.


Ideas
-----
- [ ] Exception message formatter, where the exception object itself can be the body of the message. or it is part of a
      message template. Take some form of string representation of the exception, and add traceback as exc_info to the
      event dict.

Not in scope
------------

* Log handler that uses tcp/udp connection to deliver events to the Seq server.


Contribute
----------

All contributions are welcome.


Getting started
---------------
This package uses Poetry for package and dependency management. I recommend reading the official documentation first:
https://python-poetry.org/docs/

Place Celf format spec here
---------------------------


Python 2.x
----------

Sorry but no python 2.x support is planned, its 2020. Python 2.7 support ended on the 1st of January 2020.
