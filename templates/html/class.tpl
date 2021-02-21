<div class="definition d-class" id="{{definition.id}}">
<h3>Class <span class="d-name">{{ definition.name }}</span> {% if definition.base %}extends {{ definition.base | link }}{% endif %}</h3>
<div class="d-origin">Defined in <span>`{{ definition.file_path.parts | join("/") }}`</span></div>

<div class="d-body">
    <div class="d-fields ms-3">
    <h4>Fields</h4>
{% for member in definition.members | select("is_field") -%}
    <div id="{{member.name}}-{{loop.index}}" class="d-field">
        <code class="d-field">
        {{ member.qualifiers | map("lower") | join(" ") }}
        let <a class="d-name"
                href="#{{member.id}}"
                id="{{member.id}}"
            >{{ member.name}}</a>: {{ member.type_ | link }}
        </code>
    </div>r
{% endfor %}
    </div>
    <div class="d-methods ms-3">
    <h4>Methods</h4>
{% for member in definition.members | select("is_function") -%}
    <code class="d-method-sig">
        <span class="d-none">{{ member.qualifiers | join(" ") }}
        func </span><a class="d-name"
                        href="#{{member.id}}"
                        id="{{member.id}}"
                    >{{ member.name }}</a>(
        <span class="d-params">
        {%- for param in member.parameters -%}
            <var>{{ param.qualifiers | join(" ")}} {{ param.name }}:</var><span>{{ param.type_ | link }}{{ ", " if not loop.last else " " }}</span>
            {%- endfor -%}</span>) -&gt; {{ member.return_type | link }}
    </code>
{% endfor %}
    </div>
</div>
</div>
