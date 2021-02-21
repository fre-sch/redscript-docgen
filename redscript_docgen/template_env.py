import os

from jinja2 import contextfilter, Environment, FileSystemLoader
from markupsafe import escape as markup_escape

from redscript_docgen.parser import Class, Func, Field, Enum, Type


def is_class(definition):
    return isinstance(definition, Class)


def is_function(definition):
    return isinstance(definition, Func)


def is_field(definition):
    return isinstance(definition, Field)


def is_enum(definition):
    return isinstance(definition, Enum)


def type_name(type_def):
    args = ""
    if type_def.arguments:
        args = "<" + " | ".join(
            type_name(arg)
            for arg in type_def.arguments
        ) + ">"
    return type_def.name + args


def type_name_unwrap(type_def):
    for arg in type_def.arguments:
        return type_name_unwrap(arg)
    return type_def.name


def make_link_filter(namespace_root):
    @contextfilter
    def link_filter(ctx, value):
        if isinstance(value, Type):
            inner_type = type_name_unwrap(value)
            name = type_name(value)
        else:
            inner_type = value
            name = value

        if inner_type not in namespace_root:
            return markup_escape(name)

        target = namespace_root[inner_type]
        target_path = target.file_path.parent.parts or ("global", )
        base_uri = ctx.environment.globals["base_uri"]
        target_path = os.path.join(base_uri, *target_path) + ".html"
        mode = ctx.environment.globals["mode"]
        if mode == "html":
            result = f"""<a href="{target_path}#{target.id}">{markup_escape(name)}</a>"""
            return result

    return link_filter


def init_env(mode, base_uri, namespace):
    env = Environment(
        loader=FileSystemLoader(os.path.join("templates", mode))
    )
    mode_ext = "." + mode
    env.filters["link"] = make_link_filter(namespace)
    env.filters["type_name"] = type_name
    env.filters["is_class"] = is_class
    env.filters["is_function"] = is_function
    env.filters["is_field"] = is_field
    env.filters["is_enum"] = is_enum
    env.tests["is_class"] = is_class
    env.tests["is_function"] = is_function
    env.tests["is_field"] = is_field
    env.tests["is_enum"] = is_enum
    env.globals["base_uri"] = base_uri
    env.globals["mode"] = mode
    env.globals["definitions_map"] = namespace
    return env, mode_ext


def definition_inheritance_tree(definition, namespace):
    if not isinstance(definition, Class):
        return []
    base = definition.base
    bases = []
    while base:
        bases.append(base)
        parent = namespace[base]
        base = parent.base
    return bases
