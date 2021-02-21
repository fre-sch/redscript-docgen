# coding: utf-8
import logging
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from pathlib import Path
import pickle
import click

from redscript_docgen.parser import parse, Class, Enum, Func, Field
from redscript_docgen.template_env import init_env

logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s %(asctime)s %(threadName)s %(message)s")
log = logging.getLogger()


class Namespace:
    def __init__(self, name):
        self.name = name
        self.forward_map = defaultdict(list)
        self.reverse_map = {}

    def add_definition(self, definition):
        parts = definition.file_path.parent.parts
        self.forward_map[parts].append(definition)
        self.reverse_map[definition.name] = definition
        if hasattr(definition, "members"):
            for member in definition.members:
                self.reverse_map[definition.name, member.name] = member

    def __contains__(self, item):
        return item in self.reverse_map

    def __getitem__(self, item):
        return self.reverse_map[item]


def definition_name_sort(definition):
    if isinstance(definition, Enum):
        return 1, definition.name
    if isinstance(definition, Class):
        return 2, definition.name
    if isinstance(definition, Func):
        return 1, definition.name
    if isinstance(definition, Field):
        return 1, definition.name


def load_parse_source(cache_path, file_arg):
    abs_path, rel_path = file_arg
    item_cache_path = cache_path / rel_path

    try:
        with item_cache_path.open("rb") as fp:
            return pickle.load(fp)
    except Exception:
        pass

    with abs_path.open("r", encoding="UTF-8") as fp:
        try:
            log.debug(f"parsing: {abs_path}")
            result = parse(fp.read(), rel_path)

            item_cache_path.parent.mkdir(parents=True, exist_ok=True)
            with item_cache_path.open("wb") as cache_fp:
                pickle.dump(result, cache_fp)

            return result
        except Exception as e:
            log.error("processing: %s failed: %s", abs_path.as_uri(), e)
            return []


@click.command()
@click.argument("directory", type=click.Path(
    exists=True, file_okay=False, readable=True, resolve_path=True))
@click.argument("output_dir")
@click.option("--base-uri", type=str, default=None)
@click.option("--mode", type=click.Choice(["html", "rst", "md"], case_sensitive=False), default="html")
def main(directory, output_dir, base_uri, mode):
    directory = Path(directory)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    if base_uri is None:
        base_uri = output_path.absolute().as_uri()
    namespace_root = Namespace("global")
    env, mode_ext = init_env(mode, base_uri, namespace_root)
    cache_path = output_path / "__cache__"
    files = [
        (it, it.relative_to(directory))
        for it in directory.glob("**/*.script")
        if it.is_file()
    ]
    log.info("found %s files to process", len(files))
    with ThreadPoolExecutor() as executor:
        for file_definitions in executor.map(partial(load_parse_source, cache_path), files):
            for definition in file_definitions:
                namespace_root.add_definition(definition)
    log.info("finished parsing")

    template = env.get_template("definition.tpl")
    for namespace, definition_group in namespace_root.forward_map.items():
        if namespace:
            definition_output_path = output_path / Path(*namespace[:-1], namespace[-1] + mode_ext)
        else:
            definition_output_path = output_path / ("global" + mode_ext)
        definition_output_path.parent.mkdir(parents=True, exist_ok=True)
        with definition_output_path.open("w", encoding="UTF-8") as fp:
            fp.write(template.render(namespace=namespace, definitions=definition_group))

    log.info("generation complete")


if __name__ == '__main__':
    main()