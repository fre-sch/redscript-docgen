import itertools

import pytest
from parsimonious import Grammar, IncompleteParseError

from redscript_docgen import parser


qualifiers = ("public", "protected", "private", "static", "final", "const",
              "native", "exec", "cb", "abstract", "persistent", "inline",
              "edit", "rep")
qualifier_combinations = [
    " ".join(it) for it in
    itertools.combinations(qualifiers, 3)
]


@pytest.mark.parametrize("value", qualifier_combinations)
def test_qualifier_ok(value):
    grammar = Grammar(r"""
    start = qualifierlist
    """ + parser.qualifier + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


def test_qualifier_notok():
    grammar = Grammar(r"""
        start = qualifierlist
        """ + parser.qualifier + parser.ws)
    with pytest.raises(IncompleteParseError):
        grammar.parse("public, static, final")


@pytest.mark.parametrize("value", (
    "/**/",
    "/* */",
    "/*/**/*/",
    "/*/*/**/*/*/",
    "/* */",
    "/*  */",
    "/* /*  */ */",
    "/* /*  /*   */  */ */",
    "/* word */",
    "/* word word */",
    "/* word /* word */ word */",
    "/* word /* word word */ word */",
    "/* let x: Int32 = 321321 */",
    "/* public func test(opt x: Int32) -> Void {} */",
    """/*
            /*
            comment body for func
            */ public func test(opt x: Int32) -> Void {
            }
        */""",
))
def test_block_comment_ok(value):
    grammar = Grammar(r"""
    start = comment
    """ + parser.comment + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "//\n",
    "////\n",
    "//////\n",
    "//word\n",
    "// word \n",
    "//word//\n",
    "// word //\n",
    "// word word\n",
    "//word word\n",
    "//word word//\n",
    "//word word// word\n",
    "//\r\n",
    "////\r\n",
    "//////\r\n",
    "//word\r\n",
    "// word \r\n",
    "//word//\r\n",
    "// word //\r\n",
    "// word word\r\n",
    "//word word\r\n",
    "//word word//\r\n",
    "//word word// word\r\n",
))
def test_block_line_comment_ok(value):
    grammar = Grammar(r"""
    start = line_comment
    """ + parser.line_comment + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "i",
    "I",
    "_",
    "_i",
    "_I",
    "i_",
    "I_",
    "i0",
    "_0",
    "ident",
    "_ident",
    "Ident",
    "_Ident",
    "ident_",
    "Ident_",
    "IdentIdent",
    "Ident_Ident",
    "ident01",
    "ident01ident",
))
def test_ident_ok(value):
    grammar = Grammar(r"""
        start = ident
        """ + parser.ident + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "ident",
    "ident,ident",
    "ident , ident , ident",
    "ident , ident , ident",
))
def test_annotation_params_ok(value):
    grammar = Grammar(r"""
        start = annotation_params
        """ + parser.annotation + parser.symbols + parser.ident + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "@annotation()",
    "@annotation( \n )",
    "@annotation(param)",
    "@annotation(param, param)",
    "@annotation( param )",
))
def test_annotation_ok(value):
    grammar = Grammar(parser.annotation + parser.symbols + parser.ident + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "type",
    "type<type>",
    "type<type<type>>",
    "type < type >",
    "type < type < type > >"
))
def test_type_ok(value):
    grammar = Grammar(parser.type_ + parser.symbols + parser.ident + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "ident:type",
    "ident: type",
    "ident :type",
    "ident  :  type",
    "ident:type<type>",
    "ident: type<type>",
    "ident :type<type>",
    "ident  :  type<type>",
    "opt ident:type",
    "opt ident: type",
    "opt ident :type",
    "opt ident  :  type",
    "opt ident:type<type>",
    "opt ident: type<type>",
    "opt ident :type<type>",
    "opt ident  :  type<type>",
    "out ident:type",
    "out ident: type",
    "out ident :type",
    "out ident  :  type",
    "out ident:type<type>",
    "out ident: type<type>",
    "out ident :type<type>",
    "out ident  :  type<type>",
))
def test_param_ok(value):
    grammar = Grammar(
        "start = param\n"
        + parser.params
        + parser.type_
        + parser.symbols
        + parser.ident
        + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "ident: type",
    "ident: type, ident: type",
    "ident: type, ident: type",
    "ident: type<type>",
    "ident: type<type>, ident:type<type>",
    "ident: type, out ident: type, opt ident:type, ident:type",
))
def test_param_list_ok(value):
    grammar = Grammar(
        "start = param_list\n"
        + parser.params
        + parser.type_
        + parser.symbols
        + parser.ident
        + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "()",
    "( )",
    "(ident: type)",
    "(ident: type, ident: type)",
    "( ident: type, ident: type )",
    "(ident: type<type>)",
    "(ident: type, ident: type<type>, ident:type<type>)",
    "(ident: type, out ident: type, opt ident:type, ident:type)",
))
def test_parameters_ok(value):
    grammar = Grammar(
        parser.params
        + parser.type_
        + parser.symbols
        + parser.ident
        + parser.ws)
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "IDENT = 1",
    "IDENT = 123",
    "IDENT=1",
    "IDENT=1123",
))
def test_enum_decl_ok(value):
    grammar = Grammar(
        "start=enum_decl\n"
        + parser.enum
        + parser.ws
        + parser.symbols
        + parser.ident
    )
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "One = 1, Two = 2",
    "One = 1, Two = 2,"
    "One=1,Two=2,"
))
def test_enum_list_ok(value):
    grammar = Grammar(
        "start=enum_list\n"
        + parser.enum
        + parser.ws
        + parser.symbols
        + parser.ident
    )
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "{}",
    "{ }",
    "{One = 1}",
    "{One = 1,}",
    "{One = 1, Two = 2,}",
    "{One=1,Two=2,}"
))
def test_enum_body_ok(value):
    grammar = Grammar(
        "start=enum_body\n"
        + parser.enum
        + parser.ws
        + parser.symbols
        + parser.ident
    )
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "enum ident{}",
    "enum ident { }",
    "enum ident {One = 1}",
    "enum ident {One = 1,}",
    "enum ident {One = 1, Two = 2,}",
    "enum ident{One=1,Two=2,}"
))
def test_enum_ok(value):
    grammar = Grammar(
        "start=enum\n"
        + parser.enum
        + parser.ws
        + parser.symbols
        + parser.ident
    )
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "func Name_Of_Func01",
    "public func Name_Of_Func01",
    "public static func Name_Of_Func01",
    "public static native func Name_Of_Func01",
    "public static native cb func Name_Of_Func01",
))
def test_func_start_ok(value):
    grammar = Grammar(
        "start=func_start\n"
        + parser.annotation
        + parser.function
        + parser.params
        + parser.type_
        + parser.qualifier
        + parser.ws
        + parser.symbols
        + parser.ident
    )
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "func Name_Of_Func01() -> type",
    "public func Name_Of_Func01(param: type) -> type",
    "public static func Name_Of_Func01(param: type, out param: ref<type>) -> type",
    "public static native func Name_Of_Func01(opt a: type, opt b: type) -> type<type<type>>",
    "public static native cb func Name_Of_Func01(   ) -> void",
    "@annotation() func name() -> type"
))
def test_func_sig_ok(value):
    grammar = Grammar(
        "start=func_sig\n"
        + parser.annotation
        + parser.function
        + parser.params
        + parser.type_
        + parser.qualifier
        + parser.ws
        + parser.symbols
        + parser.ident
    )
    tree = grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "{}",
    "{ }",
    "{ any thing }",
    """{ let a: type = func(); let b = obj.func("param") }""",
    """{ while 1 { print(foo) } }"""
))
def test_func_body_ok(value):
    grammar = Grammar(
        "start=func_body\n"
        + parser.annotation
        + parser.function
        + parser.params
        + parser.type_
        + parser.qualifier
        + parser.ws
        + parser.symbols
        + parser.ident
    )
    tree = grammar.parse(value)
    assert tree is not None
