# coding: utf-8
import json
import logging
import time
from itertools import groupby
from operator import itemgetter
from pathlib import Path

import click
from jinja2 import Environment, select_autoescape, FileSystemLoader, evalcontextfilter, contextfilter
from markupsafe import Markup, escape as markup_escape

log = logging.getLogger()


def is_class(definition):
    return "Class" in definition


def is_function(definition):
    return "Function" in definition


def is_field(definition):
    return "Field" in definition


def definition_name(definition, full=False):
    if is_class(definition):
        return definition["Class"]["name"]
    if is_function(definition):
        f_name = definition["Function"]["declaration"]["name"]
        if full:
            params = [
                f"""{p["name"]}: {type_name(p["type_"])}"""
                for p in definition["Function"]["parameters"]
            ]
            return f"""{f_name}({", ".join(params)}) -> {type_name(definition["Function"]["type_"])}"""
        return f_name
    if is_field(definition):
        return definition["Field"]["name"]


def type_name(type_def):
    args = ""
    if type_def.get("arguments"):
        args = "<" + " | ".join(type_name(arg) for arg in type_def["arguments"]) + ">"
    return type_def["name"] + args


def type_name_unwrap(type_def):
    if type_def.get("arguments"):
        for arg in type_def["arguments"]:
            return type_name_unwrap(arg)
    return type_def["name"]


def definition_type(definition):
    if is_function(definition):
        return definition["Function"]["type_"]
    elif is_field(definition):
        return definition["Field"]["type_"]
    return ""


def definition_name_sort(definition):
    if is_class(definition):
        return 1, definition["Class"]["name"]
    if is_function(definition):
        return 2, definition["Function"]["declaration"]["name"]
    if is_field(definition):
        return 1, definition["Field"]["name"]


def fix_field_members(members):
    for member_definition in members:
        if "Field" in member_definition:
            yield {"Field": {
                **member_definition["Field"][0],
                "type_": member_definition["Field"][1]
            }}
        else:
            yield member_definition


def init_definitions(definitions):
    for i, definition in enumerate(definitions):

        if "Class" in definition:
            if "members" in definition["Class"]:
                definitions[i]["Class"]["members"] = sorted(list(
                    fix_field_members(definition["Class"]["members"])
                ), key=definition_name_sort)
    return definitions


def create_definitions_map(definitions):
    definitions_map = {}
    for definition in definitions:
        if "Class" in definition:
            definitions_map[definition_name(definition)] = definition
            if "members" in definition["Class"]:
                for member in definition["Class"]["members"]:
                    definitions_map[
                        definition_name(definition), definition_name(member)
                    ] = member
        elif "Function" in definition:
            definitions_map[definition_name(definition)] = definition
    return definitions_map


def make_link_filter(definitions_map):
    @contextfilter
    def link_filter(ctx, value):
        if isinstance(value, dict):
            inner_type = type_name_unwrap(value)
            name = type_name(value)
        else:
            inner_type = value
            name = value

        if inner_type not in definitions_map:
            return name

        sub_dir = ""
        if is_function(definitions_map[inner_type]):
            sub_dir = "functions"
        elif is_class(definitions_map[inner_type]):
            sub_dir = "classes"
        mode = ctx.environment.globals["mode"]
        base_uri = ctx.environment.globals["base_uri"]
        if mode == "html":
            path = f"""{base_uri}/{sub_dir}/{(inner_type + ".html")}"""
            result = f"""<a href="{path}">{markup_escape(name)}</a>"""
            if ctx.eval_ctx.autoescape:
                return Markup(result)
            return result
        elif mode == "rst":
            path = f"""{sub_dir}/{inner_type}"""
            return f"""`{name} <{path}>`_"""

    return link_filter


def init_html_env():
    return Environment(
        loader=FileSystemLoader("templates/html"),
        autoescape=select_autoescape(['html', 'xml']),
    )


def init_rst_env():
    return Environment(
        loader=FileSystemLoader("templates/rst"),
    )


def init_md_env():
    return Environment(
        loader=FileSystemLoader("templates/md"),
    )


def definition_inheritance_tree(definition, definitions_map):
    if "Class" not in definition:
        return []
    base = definition["Class"]["base"]
    bases = []
    while base:
        bases.append(base)
        parent = definitions_map[base]
        base = parent["Class"]["base"]
    return reversed(bases)


@click.command()
@click.argument("filename", type=click.File("r", encoding="UTF-8"))
@click.argument("output_dir")
@click.option("--base-uri", type=str, default=None)
@click.option("--mode", type=click.Choice(["html", "rst", "md"], case_sensitive=False), default="html")
def main(filename, output_dir, base_uri, mode):
    logging.basicConfig(level=logging.DEBUG,
                        format="%s(levelname)s %s(name)s %(message)s")
    definitions = json.load(filename)
    definitions = init_definitions(definitions)
    definitions.sort(key=definition_name_sort)
    definitions_map = create_definitions_map(definitions)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if base_uri is None:
        base_uri = output_path.absolute().as_uri()

    if mode == "html":
        env = init_html_env()
        mode_ext = "html"
    elif mode == "rst":
        env = init_rst_env()
        mode_ext = "rst"
    elif mode == "md":
        env = init_md_env()
        mode_ext = "md"

    env.filters["link"] = make_link_filter(definitions_map)
    env.filters["definition_name"] = definition_name
    env.filters["definition_type"] = definition_type
    env.filters["type_name"] = type_name
    env.filters["is_class"] = is_class
    env.filters["is_function"] = is_function
    env.filters["is_field"] = is_field
    env.tests["is_class"] = is_class
    env.tests["is_function"] = is_function
    env.tests["is_field"] = is_field
    env.globals["base_uri"] = base_uri
    env.globals["mode"] = mode
    env.globals["definitions_map"] = definitions_map

    class_template = env.get_template("class." + mode)
    function_template = env.get_template("function." + mode)

    index_path = output_path / ("index." + mode_ext)
    with index_path.open("w", encoding="UTF-8") as fp:
        fp.write(env.get_template("index." + mode).render(definitions=definitions))

    (output_path / "classes").mkdir(parents=True, exist_ok=True)
    with (output_path / ("classes/index." + mode_ext)).open("w", encoding="UTF-8") as fp:
        fp.write(
            env.get_template("class_index." + mode)
                .render(definitions=filter(is_class, definitions))
        )

    (output_path / "functions").mkdir(parents=True, exist_ok=True)
    with (output_path / ("functions/index." + mode_ext)).open("w", encoding="UTF-8") as fp:
        fp.write(
            env.get_template("function_index." + mode)
                .render(definitions=filter(is_function, definitions))
        )

    class_definitions = (it for it in definitions if "Class" in it)
    func_definitions = (
        (key, list(grouped))
        for key, grouped in groupby(
            (it for it in definitions if "Function" in it),
            key=definition_name)
    )

    for class_def in class_definitions:
        _name = definition_name(class_def)
        output_path_result = output_path / "classes"
        output_path_result.mkdir(parents=True, exist_ok=True)
        output_path_result = output_path_result / f"{_name}.{mode_ext}"
        with output_path_result.open("w", encoding="UTF-8") as fp:
            fp.write(
                class_template.render(**{
                    "def": class_def["Class"],
                    "bases": definition_inheritance_tree(class_def, definitions_map)
                })
            )
    for func_name, func_defs in func_definitions:
        output_path_result = output_path / "functions"
        output_path_result.mkdir(parents=True, exist_ok=True)
        output_path_result = output_path_result / f"{func_name}.{mode_ext}"
        with output_path_result.open("w", encoding="UTF-8") as fp:
            fp.write(
                function_template.render(**{"name": func_name, "overloads": func_defs})
            )


if __name__ == '__main__':
    main()