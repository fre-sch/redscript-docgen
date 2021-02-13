# Class {{ def["name"] }}

``{% for qualifier in def["qualifiers"] %}{{ qualifier | lower }} {% endfor -%}
class {{ def["name"] }}{% if def["base"] %} extends {{ def["base"] }}{% endif %}``

{% if def["base"] -%}
Extends: [{{ def["base"] }}]({{ def["base"] }}.md)
{%- endif %}

## Fields

{% for member in def["members"] -%}
{% if "Field" in member -%}
### {{ member | definition_name}}
```swift
{% for qualifier in member["Field"]["qualifiers"] %}{{ qualifier | lower }} {% endfor -%}
{{ member | definition_name}}: {{ member | definition_type | type_name }}
```
{% endif -%}
{% endfor %}

## Methods

{% for member in def["members"] -%}
{% if "Function" in member -%}
### {{ member | definition_name }}
```swift
{% for qualifier in member["Function"]["declaration"]["qualifiers"] %}{{ qualifier | lower }} {% endfor -%}
func {{ member | definition_name }}(
{%- for param in member["Function"]["parameters"] -%}
{{ param["name"] }}: {{ param["type_"] | type_name }}{{ ", " if not loop.last else " " }}
{%- endfor -%}
) -> {{ member | definition_type | link }}
```
Param | Type | Notes
--- | --- | ---
{% for param in member["Function"]["parameters"] -%} 
``{{ param["name"] }}`` | ``{{ param["type_"] | type_name }}`` | 
{% endfor %}
{% endif -%}
{% endfor -%}
