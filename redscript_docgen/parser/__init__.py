from redscript_docgen.parser import grammar
from redscript_docgen.parser.model import Type, Func, Param, Enum, EnumItem, \
    Class, Field
from redscript_docgen.parser.transform import Visitor


def parse(source_string, file_path):
    return Visitor(file_path).visit(grammar.grammar.parse(source_string))


if __name__ == '__main__':
    import sys, pathlib, pprint
    with pathlib.Path(sys.argv[1]).open("r", encoding="UTF-8") as fp:
        #pprint.pprint(parse(fp.read()))
        tree = parse(fp.read(), sys.argv[1])
        pprint.pprint(tree)
