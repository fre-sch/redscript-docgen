####
Class {{ def["name"] }}
####

.. py:class:: {{ def["name"] }}{% if def["base"] %}({{ def["base"] }}{% endif %})

    {% for qualifier in def["qualifiers"] %}{{ qualifier | lower }}, {% endfor %}

    {% for member in def["members"] -%}
    {% if "Field" in member -%}
    .. py:attribute:: {{ member | definition_name}}: {{ member | definition_type | type_name }}
    {% endif -%}
    {% endfor %}

    {% for member in def["members"] -%}
    {% if "Function" in member -%}
    .. py::method:: {{ member | definition_name }}(
        {%- for param in member["Function"]["parameters"] -%}
        {{ param["name"] }}: {{ param["type_"] | type_name }},
        {%- endfor -%}
        ) -> {{ member | definition_type | link }}
    {% endif -%}
    {% endfor -%}
