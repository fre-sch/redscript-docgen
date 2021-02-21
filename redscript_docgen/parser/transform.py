from collections.abc import Iterable, Mapping

from parsimonious import NodeVisitor
from parsimonious.nodes import Node

from redscript_docgen.parser.model import (
    Func, Param, Type, Enum, EnumItem, Class, Field)


def flatten(x):
    if isinstance(x, Iterable) \
            and not isinstance(x, (str, bytes, bytearray)) \
            and not isinstance(x, Mapping):
        return [a
                for i in x
                for a in flatten(i)]
    else:
        return [x]


def lff(value):
    return list(filter(None, flatten(value)))


class Visitor(NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path

    def visit__(self, n, vc): return None
    def visit_ws(self, n, vc): return None
    def visit_le(self, n, vc): return None
    def visit_comment(self, n, vc): return None
    def visit_line_comment(self, n, vc): return None
    def visit_lt(self, n, vc): return None
    def visit_gt(self, n, vc): return None
    def visit_type_arg_sep(self, n, vc): return None
    def visit_lparen(self, n, vc): return None
    def visit_rparen(self, n, vc): return None

    def visit_qualifier(self, n, vc):
        return n.text

    def visit_qualifierlist(self, n, vc):
        return [i[0] for i in vc]

    # def visit_annotation_ident_fix(self, n, vc):
    #     return n.text
    #
    # def visit_annotation_ident(self, n, vc):
    #     return [vc[0], *[it[0] for it in vc]]
    #
    # def visit_annotation_param(self, n, vc):
    #     return vc

    def visit_annotation(self, n, vc):
        return n.text

    def visit_annotationlist(self, n, vc):
        return [i[0] for i in vc]

    def visit_func(self, n, vc):
        return vc[0]

    def visit_func_sig(self, n, vc):
        return Func(
            self.file_path,
            n.start,
            vc[0],
            vc[1],
            vc[4],
            lff(vc[6]),
            vc[8]
        )

    def visit_func_name(self, n, vc):
        return n.text

    def visit_func_return_type(self, n, vc):
        return vc[2]

    def visit_parameters(self, n, vc):
        return [] if isinstance(vc[2], Node) else vc[2][0]

    def visit_param_list(self, n, vc):
        return [
            vc[0],
            *[it[1] for it in vc[1]]
        ]

    def visit_param(self, n, vc):
        qualifier, ident = vc[0]
        type_ = vc[2]
        return Param(ident, type_, [qualifier])

    def visit_param_ident(self, n, vc):
        return vc

    def visit_param_qualifier(self, n, vc):
        return n.text.strip()

    def visit_ident(self, n, vc):
        return n.text

    def visit_type_arg_value(self, n, vc):
        return n.text

    def visit_type_arg(self, n, vc):
        return vc[0]

    def visit_type_wrapped(self, n, vc):
        return vc[2]

    def visit_type(self, n, vc):
        type_ident = vc[0]
        type_wrapped = [] if isinstance(vc[2], Node) else vc[2]
        return Type(type_ident, type_wrapped)

    def visit_enum(self, n, vc):
        return Enum(
            self.file_path,
            n.start,
            vc[2], vc[4][0]
        )

    def visit_enum_body(self, n, vc):
        return vc[2]

    def visit_enum_list(self, n, vc):
        first = EnumItem(*vc[0])
        rest = [
            EnumItem(*it[1]) for it in vc[1]
        ]
        return [first, *rest]

    def visit_enum_decl(self, n, vc):
        return vc[0], vc[4]

    def visit_enum_value(self, n, vc):
        return n.text

    def visit_class_extends(self, n, vc):
        return vc[2]

    def visit_class_body(self, n, vc):
        return lff(vc[1])

    def visit_class_member(self, n, vc):
        return flatten(vc[0])

    def visit_class(self, n, vc):
        return Class(
            self.file_path,
            n.start,
            vc[0],
            vc[3],
            None if isinstance(vc[5], Node) else vc[5][0],
            lff(vc[7]),
            vc[1][0].text == "struct"
        )

    def visit_class_member(self, n, vc):
        return vc[0]

    def visit_class_body(self, n, vc):
        return vc[1]

    def visit_class_extends(self, n, vc):
        return vc[2]

    def visit_class_field(self, n, vc):
        return Field(
            self.file_path,
            n.start,
            vc[0],
            vc[1],
            vc[4],
            vc[8]
        )

    def visit_definition(self, n, vc):
        return vc[0]

    def visit_definitions(self, n, vc):
        return vc[1]

    def generic_visit(self, node, visited_children):
        return list(filter(None, visited_children)) or node