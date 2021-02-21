import itertools

import pytest
from parsimonious import Grammar, IncompleteParseError

from redscript_docgen.parser import grammar

qualifiers = ("public", "protected", "private", "static", "final", "const",
              "native", "exec", "cb", "abstract", "persistent", "inline",
              "edit", "rep")
qualifier_combinations = [
    " ".join(it) + " " for it in
    itertools.combinations(qualifiers, 3)
]


@pytest.mark.parametrize("value", qualifier_combinations)
def test_qualifier_ok(value):
    test_grammar = Grammar(r"""
    start = qualifierlist
    """ + grammar.qualifier + grammar.ws)
    tree = test_grammar.parse(value)
    assert tree is not None


def test_qualifier_notok():
    test_grammar = Grammar(r"""
        start = qualifierlist
        """ + grammar.qualifier + grammar.ws)
    with pytest.raises(IncompleteParseError):
        test_grammar.parse("public, static, final")


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
    test_grammar = Grammar(r"""
    start = comment
    """ + grammar.ws)
    tree = test_grammar.parse(value)
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
    test_grammar = Grammar(r"""
    start = line_comment
    """ + grammar.ws)
    tree = test_grammar.parse(value)
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
    "Ident.Ident",
))
def test_ident_ok(value):
    test_grammar = Grammar(r"""
        start = ident
        """ + grammar.ident + grammar.ws)
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "ident",
    "ident,ident",
    "ident , ident , ident",
    "ident , ident , ident",
    "1",
    "123",
    "1.23",
    "-1",
    "-123",
    "ident, -1",
    "-1, ident",
    "-1, -1",
))
def test_annotation_params_ok(value):
    test_grammar = Grammar(r"""
        start = annotation_paramlist
        """ + grammar.annotation + grammar.symbols + grammar.ident + grammar.ws)
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "@annotation()",
    "@annotation( \n )",
    "@annotation(param)",
    "@annotation(param, param)",
    "@annotation( param )",
    "@annotation(123)",
    "@annotation(12.3)",
    "@annotation(-123)",
    "@annotation(-12.345)",
    """@annotation("string value")""",
    """@attrib(customEditor, "TweakDBGroupInheritance;DeviceAreaAttack")""",
    """@default(AOEAreaSetup, -1.f)""",
))
def test_annotation_ok(value):
    test_grammar = Grammar(
        "start = annotation\n"
        + grammar.annotation
        + grammar.symbols
        + grammar.ident
        + grammar.ws)
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "@one() @two() ",
    "@one()\t@two() ",
    "@one()\n@two() ",
    """@attrib(tooltip, "determines how long the effects are active. """
    """It does not impact how long status effect (e.g. blindness) is applied """
    """on npc. This is determined by RPG for balance reasons Negative values """
    """are interpreted as infinity. Set to -1.0f by default.") """
    """@default(AOEAreaSetup, -1.f) """,
))
def test_annotationlist_ok(value):
    test_grammar = Grammar(
        "start = annotationlist\n"
        + grammar.annotation
        + grammar.symbols
        + grammar.ident
        + grammar.ws)
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "type",
    "type<type>",
    "type<type<type>>",
    "type < type >",
    "type < type < type > >"
))
def test_type_ok(value):
    test_grammar = Grammar(
        grammar.type_ + grammar.symbols + grammar.ident + grammar.ws)
    tree = test_grammar.parse(value)
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
    test_grammar = Grammar(
        "start = param\n"
        + grammar.params
        + grammar.type_
        + grammar.symbols
        + grammar.ident
        + grammar.ws)
    tree = test_grammar.parse(value)
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
    test_grammar = Grammar(
        "start = param_list\n"
        + grammar.params
        + grammar.type_
        + grammar.symbols
        + grammar.ident
        + grammar.ws)
    tree = test_grammar.parse(value)
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
    test_grammar = Grammar(
        grammar.params
        + grammar.type_
        + grammar.symbols
        + grammar.ident
        + grammar.ws)
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "IDENT = 1",
    "IDENT = 123",
    "IDENT=1",
    "IDENT=1123",
))
def test_enum_decl_ok(value):
    test_grammar = Grammar(
        "start=enum_decl\n"
        + grammar.enum
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "One = 1, Two = 2",
    "One = 1, Two = 2,"
    "One=1,Two=2,"
))
def test_enum_list_ok(value):
    test_grammar = Grammar(
        "start=enum_list\n"
        + grammar.enum
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
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
    test_grammar = Grammar(
        "start=enum_body\n"
        + grammar.enum
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
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
    test_grammar = Grammar(
        "start=enum\n"
        + grammar.enum
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "func Name_Of_Func01() -> type",
    "public func Name_Of_Func01(param: type) -> type",
    "public static func Name_Of_Func01(param: type, out param: ref<type>) -> type",
    "public static native func Name_Of_Func01(opt a: type, opt b: type) -> type<type<type>>",
    "public static native cb func Name_Of_Func01(   ) -> void",
    "@annotation() func name() -> type",
    "@one() @two() public static native func name() -> type"
))
def test_func_sig_ok(value):
    test_grammar = Grammar(
        "start=func_sig\n"
        + grammar.annotation
        + grammar.function
        + grammar.params
        + grammar.type_
        + grammar.qualifier
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "func Name()->type{}",
    "func Name() -> type {}",
    "func Name()->type\n{}",
    "func Name()->type\n",
    "func Name()->type\n{}",
))
def test_func_ok(value):
    test_grammar = Grammar(
        "start=func\n"
        + grammar.annotation
        + grammar.function
        + grammar.params
        + grammar.type_
        + grammar.qualifier
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "{}",
    "{ }",
    "{ any thing }",
    """{ let a: type = func(); let b = obj.func("param") }""",
    """{ while 1 { print(foo) } }"""
))
def test_func_body_ok(value):
    test_grammar = Grammar(
        "start=func_body\n"
        + grammar.annotation
        + grammar.function
        + grammar.params
        + grammar.type_
        + grammar.qualifier
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "let ident:type;",
    "let ident: type;",
    "let ident :type;",
    "let ident  :  type;",
    "let ident:type<type>;",
    "let ident: type<type>;",
    "let ident :type<type>;",
    "let ident  :  type<type>;",
    "private let ident:type;",
    "private let ident: type;",
    "public let ident :type;",
    "protected let ident  :  type;",
    "public edit let ident:type<type>;",
    "private edit let ident: type<type>;",
    "@annotation(type, 1) public let m_currentInterval: Int32;"
))
def test_class_field_ok(value):
    test_grammar = Grammar(
        "start = class_field\n"
        + grammar.class_
        + grammar.annotation
        + grammar.function
        + grammar.params
        + grammar.type_
        + grammar.qualifier
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "{}",
    "{\n \t\t\n}",
    "{\n\t  //comment comment\n \t\n}",
    "{\n\t/* \n\tcomment\n\tcomment2\n*/\n\t\t\n }",
))
def test_class_body_ok(value):
    test_grammar = Grammar(
        "start=class_body\n"
        + grammar.class_
        + grammar.annotation
        + grammar.function
        + grammar.params
        + grammar.type_
        + grammar.qualifier
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
    assert tree is not None


@pytest.mark.parametrize("value", (
    "public native class ClassName {}",
    "struct StructName{}",
    "class Name { //comment\n}",
    "class Name { /* comment */ }",
    "class ClassName{let ident :type;}",
    """public native class ClassName {
      let ident: type<type<type>>;
      let ident: type<type<type>>;
      // let ident: type<type<type>>;
      /* let ident: type<type<type>>; */
      private func GetIdent() -> type<type<type>> {
        while true {
          this.print("foo");
        }
      }
      private func SetIdent(ident: type) -> void {}
      @annotation(foo)
      public static func Dothing(ident: type) -> void {}
    }"""
))
def test_class_ok(value):
    test_grammar = Grammar(
        grammar.class_
        + grammar.annotation
        + grammar.function
        + grammar.params
        + grammar.type_
        + grammar.qualifier
        + grammar.ws
        + grammar.symbols
        + grammar.ident
    )
    tree = test_grammar.parse(value)
    assert tree is not None


def test_grammar_ok():
    tree = grammar.grammar.parse(
"""
enum gameEActionStatus {
  STATUS_INVALID = 0,
  STATUS_BOUND = 1,
  STATUS_READY = 2,
  STATUS_PROGRESS = 3,
  STATUS_COMPLETE = 4,
  STATUS_FAILURE = 5,
}

enum AIEExecutionOutcome {
  OUTCOME_FAILURE = 0,
  OUTCOME_SUCCESS = 1,
  OUTCOME_IN_PROGRESS = 2,
}

public native struct InventoryItemAbility {
  public native let IconPath: CName;
  public native let Title: String;
  public native let Description: String;
  public native let LocalizationDataPackage: ref<UILocalizationDataPackage>;
}

public static native func OperatorEqual(a: Float, b: Float) -> Bool
public static native func FloorF(a: Float) -> Int32

public native class WeaponEvolution_Record extends TweakDBRecord {
  public final native func Name() -> String
  public final native func Type() -> gamedataWeaponEvolution
}
public class PingCachedData extends IScriptable {}
 """)
    assert tree is not None

