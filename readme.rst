======
runcli
======
Run commands for your repo, easily.

``runcli`` allows you to define a ``Runfile`` at the root of your
repository, and then call that file from anywhere in your repo as a
script using the command ``run``. The rest is up to you!

See `Link the github repo <https://github.com/nalourie/runcli>` for the
source code.


------------
Installation
------------

Install ``runcli`` with ``pip``::

  pip install runcli

Currently only linux is tested, but it should also work on Mac.


----------
Quickstart
----------
To use ``run``, first write a ``Runfile`` in the root of some
repository. The ``Runfile`` is just a script, and can be any script you
like, for example::

  #! /bin/bash

  echo $1

Then, from anywhere in your repository call the ``Runfile`` script using
the ``run`` command::

  > run "hello, world!"
  hello, world!

That's all there is to it.


------------
Contributing
------------
Pull requests are welcome. All contributions should happen on `Link the
github repo <https://github.com/nalourie/runcli>`.
