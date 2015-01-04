===============================
dgim
===============================

.. image:: https://badge.fury.io/py/dgim.png
    :target: http://badge.fury.io/py/dgim

.. image:: https://travis-ci.org/simondolle/dgim.png?branch=master
        :target: https://travis-ci.org/simondolle/dgim

.. image:: https://pypip.in/d/dgim/badge.png
        :target: https://pypi.python.org/pypi/dgim


Python implementation of the dgim algorithm: Compact datastructure to estimate the number of "True" in the last N elements of a boolean stream.

Features
--------

* Estimation of the number of "True" statements in the last N element of a boolean stream
* Configurable error rate

Usage
-----

Basic::

  from dgim.dgim import Dgim
  dgim = Dgim(N=32)
  for i in range(100):
      dgim.update(True)
  print "Number of 'True' statements in the last 32 elements"
  exact_result = 32
  print "- Exact result : {}".format(exact_result)
  dgim_result = dgim.get_count() # 28
  print "- Dgim estimation: {}".format(dgim_result)


Custom error rate::

  from dgim.dgim import Dgim
  dgim = Dgim(N=32, error_rate=0.1)
  for i in range(100):
      dgim.update(True)
  print "Number of 'True' statements in the last 32 elements"
  exact_result = 32
  print "- Exact result : {}".format(exact_result)
  dgim_result = dgim.get_count() # 30
  print "- Dgim estimation: {}".format(dgim_result)


Documentation
-------------

* Documentation: https://dgim.readthedocs.org.


License
-------

The project is licensed under the BSD license.

References
----------
- Datar, Mayur, et al. "Maintaining stream statistics over sliding windows."
  SIAM Journal on Computing 31.6 (2002): 1794-1813.
- Rajaraman, Anand, and Jeffrey David Ullman. Mining of massive datasets. Cambridge University Press, 2011. Chapter 4. http://infolab.stanford.edu/~ullman/mmds/ch4.pdf
- Mining of Massive Datasets Coursera MOOC: http://infolab.stanford.edu/~ullman/mmds/ch4.pdf
