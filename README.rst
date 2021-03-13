My new CDN.
-----------

Made in Python with love by kal.

Only thing you'll need in your environment is `SECRET_KEY`.


Running the CDN
---------------

.. code-block:: sh

    $ hypercorn --bind '0.0.0.0:5000' --bind '[::]:5000' ...
