==========
levenparty
==========

LevenParty, a pseudo-port of `Translation Party`_.

Uses Levenshtein distances & random transformations to try to make words
match... BECAUSE THE INTERNET NEEDS MORE SILLY THINGS!

This is just the JSON & server-side component, a nice Ajax-y HTML page sure
would be a great addition...

A running instance can be found at http://levenparty.herokuapp.com/.

.. _`Translation Party`: http://translationparty.com/


Endpoints
=========

http://levenparty.herokuapp.com/
    Gives some meta info & includes the last 50 things that have been queried.

http://levenparty.herokuapp.com/word_1/word_2/
    Does the actual party/transforms. Substitute in your own words!


Requirements
============

* Python 2.6+
* restless
* itty
* pylev


License
=======

BSD
