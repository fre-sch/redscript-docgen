<div class="definition d-func" id="{{definition.id}}">
    <span class="d-none">{{ definition.qualifiers | join(" ") }}
    func </span><a class="d-name" href="#{{definition.id}}" >{{ definition.name }}</a>(
    <span class="d-params">
    {%- for param in definition.parameters -%}
        <var>{{ param.qualifiers | join(" ")}} {{ param.name }}:</var><span>{{ param.type_ | link }}{{ ", " if not loop.last else " " }}</span>
        {%- endfor -%}</span>) -&gt; {{ definition.return_type | link }}
</div>
