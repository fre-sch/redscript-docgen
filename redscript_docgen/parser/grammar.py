from parsimonious import Grammar


ws = r"""
    _                = comment / line_comment / ~"\s*"
    ws               = ~"\s+"
    le               = ~"(\r\n|\r|\n)"
    comment_start    = "/*"
    comment_end      = "*/"
    comment_content  = comment / (!comment_start !comment_end ~"."s)
    comment          = comment_start comment_content* comment_end
    line_comment     = ~"//.*" le
"""

qualifier = r"""
    qualifier        = "public" / "protected" / "private" / "static" / "final" /
                       "const" / "native" / "exec" / "cb" /
                       "abstract" / "persistent" / "inline" / "edit" / "rep"
    qualifierlist    = (qualifier ws)*
"""

ident = r"""
    ident            = ~"[a-z_][\w\.]*"ai
    number           = ~"-?\d+(\.\d*)?f?"ai
    string           = ~r"\"(?:[^\\\"\\]|\\.)*\""
"""

symbols = r"""
    lbrace           = "{"
    rbrace           = "}"
    lparen           = "("
    rparen           = ")"
    listsep          = _ "," _
    typesep          = _ ":" _
    gt               = ">"
    lt               = "<"
    equal            = "="
"""

annotation = r"""
    annotationlist       = (annotation ws)*
    annotation           = "@" ident lparen _ annotation_paramlist? _ rparen
    annotation_paramlist = annotation_param (listsep annotation_param)*
    annotation_param     = number / string / annotation_ident
    annotation_ident     = ~"[^\,\)]+"ai
"""

type_ = r"""
    type             = ident _ type_wrapped? _
    type_wrapped     = lt _ type _ type_arg? _ gt
    type_arg_sep     = ";" _
    type_arg         = type_arg_sep type_arg_value*
    type_arg_value   = !gt ~"."
"""

params = r"""
    parameters       = lparen _ param_list? _ rparen
    param_list       = param (listsep param)*
    param            = param_ident typesep type _
    param_ident      = param_qualifier ident
    param_qualifier  = (("out" / "opt") ws)? 
"""

function = r"""
    func              = func_sig _ func_body?
    func_sig          = annotationlist qualifierlist "func" _ func_name _ parameters _ func_return_type
    func_name         = ident?
    func_return_type  = "->" _ type
    func_body_start   = lbrace
    func_body_end     = rbrace
    func_body_content = func_body / (!func_body_start !func_body_end ~"."s)
    func_body         = func_body_start func_body_content* func_body_end _
"""

enum = r"""
    enum             = "enum" ws ident _ enum_body _
    enum_body        = lbrace _ enum_list? _ rbrace
    enum_list        = enum_decl (_ listsep _ enum_decl)* listsep?
    enum_decl        = ident _ equal _ enum_value
    enum_value       = ~"-?\d+"a
"""

class_ = r"""
    class            = qualifierlist ("class" / "struct") ws ident _ class_extends? _ class_body
    class_extends    = "extends" ws ident
    class_body       = lbrace class_member* rbrace _
    class_member     = class_field / func / _
    class_field      = annotationlist qualifierlist "let" ws ident _ typesep _ type _ ";"
"""

grammar = Grammar(
    """
    definitions = _ definition*
    definition = enum / func / class
    """
    + class_
    + enum
    + annotation
    + function
    + params
    + type_
    + qualifier
    + ws
    + symbols
    + ident
)
