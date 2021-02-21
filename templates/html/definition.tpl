{% extends "layout.tpl" %}

{% block title %}
{{ namespace | join(":") }}
{% endblock %}

{% block body %}

<h2>Classes</h2>
{% for definition in definitions|select("is_class") %}
{% include "class.tpl" %}
{% endfor %}

<h2>Functions</h2>
{% for definition in definitions|select("is_function") %}
{% include "function.tpl" %}
{% endfor %}

<h2>Enums</h2>
{% for definition in definitions|select("is_enum") %}
{{ definition.name }}
{% endfor %}

{% endblock %}