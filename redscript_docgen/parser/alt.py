from parsimonious import Grammar, TokenGrammar

tokens = Grammar(r"""
    tokens                 = ws* (token_ws)*
    token_ws               = token ws*
    token                  = string / number / ident / symbol
    ident                  = ~"[a-z_][\w\.#]*"ai
    number                 = ~"-?\d+(\.\d*)?f?"ai
    string                 = ~r"\"(?:[^\\\"\\]|\\.)*\""
    ws                     = ~"\s*"a / comment
    symbol                 = ~"[^\w\s\"\'\.]+"a
    comment                = line_comment / block_comment
    block_comment_start    = "/*"
    block_comment_end      = "*/"
    block_comment_content  = comment / (!block_comment_start !block_comment_end ~"."s)
    block_comment          = block_comment_start block_comment_content* block_comment_end
    line_comment           = ~"//.*(\r\n|\r|\n)"
""")

qualifier = r"""
    qualifier        = "public" / "protected" / "private" / "static" / "final" /
                       "const" / "native" / "exec" / "cb" /
                       "abstract" / "persistent" / "inline" / "edit" / "rep"
    qualifierlist    = qualifier*
"""

symbols = r"""
    lbrace           = "{"
    rbrace           = "}"
    lparen           = "("
    rparen           = ")"
    listsep          = ","
    typesep          = ":"
    gt               = ">"
    lt               = "<"
    equal            = "="
    at               = "@"
    semicolon        = ";"
"""

annotation = r"""
    annotationlist       = annotation*
    annotation           = at ident lparen annotation_paramlist? rparen
    annotation_paramlist = annotation_param (listsep annotation_param)*
    annotation_param     = number / string / annotation_ident
    annotation_ident     = (!listsep !rparen ident)*
"""

type_ = r"""
    type             = ident type_wrapped?
    type_wrapped     = lt type type_arg? gt
    type_arg         = semicolon type_arg_value*
    type_arg_value   = !gt ident
"""

params = r"""
    parameters       = lparen param_list? rparen
    param_list       = param (listsep param)*
    param            = param_ident typesep type
    param_ident      = ident ident? 
"""

function = r"""
    func              = func_sig func_body?
    func_sig          = annotationlist qualifierlist "func" func_name parameters func_return_type
    func_name         = ident?
    func_return_type  = "->" type
    func_body_content = func_body / (!lbrace !rbrace ~"."s)
    func_body         = lbrace func_body_content* rbrace
"""

enum = r"""
    enum             = "enum" ident enum_body
    enum_body        = lbrace enum_list? rbrace
    enum_list        = enum_decl (listsep enum_decl)* listsep?
    enum_decl        = ident equal number
"""

class_ = r"""
    class            = qualifierlist ("class" / "struct") ident class_extends? class_body
    class_extends    = "extends" ident
    class_body       = lbrace class_member* rbrace
    class_member     = class_field / func
    class_field      = annotationlist qualifierlist "let" ident typesep type ";"
"""

grammar = TokenGrammar(
    """
    definitions = definition*
    definition = enum / func / class
    """
    + class_
    + enum
    + annotation
    + function
    + params
    + type_
    + qualifier
    + symbols
)
