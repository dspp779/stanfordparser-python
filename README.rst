==================
stanfordparser-python
==================

Python Wrapper for `Stanford Parser`_ (only part-of-speech tagging)

--------
Features
--------

- Python interface for calling `Stanford Parser`_
- Convert tab separated text to python tuples.

.. _Stanford Parser: http://nlp.stanford.edu/software/lex-parser.html

--------------------------
Compatibility/Requirements
--------------------------

- StanfordParser class is Py2/3 compatible


-------
License
-------

The MIT License (MIT). Please read ``LICNESE``.


----------
How to use
----------

.. code:: python

  # python
  from stanfordparser import StanfordTagger
  
  tagger = StanfordTagger('.../path_to_stanford_parser')
  print tagger.parse('This is a pen.')
  # output:
  #([(u'This', u'DT'), (u'is', u'VBZ'), (u'a', u'DT'), (u'pen', u'NN'), (u'.', u'.')]
  