####
Functions
####

.. toctree::
    :maxdepth: 2

    {% for def in definitions -%}
    {{ def | definition_name }}
    {% endfor %}