from parsimonious import Grammar
from parsimonious.nodes import NodeVisitor

ws = r"""
    _                = ~"\s*"
    ws               = ~"\s+"
    le               = ~"(\r\n|\r|\n)"
"""

comment = r"""
    comment_start    = "/*"
    comment_end      = "*/"
    comment_content  = comment / (!comment_start !comment_end ~"."s)
    comment          = comment_start comment_content* comment_end
"""

line_comment = r"""
    line_comment     = ~"//.*" le
"""

qualifier = r"""
    qualifier        = "public" / "protected" / "private" / "static" / "final" /
                       "const" / "native" / "exec" / "cb" /
                       "abstract" / "persistent" / "inline" / "edit" / "rep"
    qualifierlist    = qualifier (ws qualifierlist)?
"""

ident = r"""
    ident            = ~"[a-z_]\w*"ai
"""

symbols = r"""
    lbrace           = "{"
    rbrace           = "}"
    lparen           = "("
    rparen           = ")"
    listsep          = ","
    gt               = ">"
    lt               = "<"
    typesep          = ":"
    equal            = "="
"""

annotation = r"""
    annotation        = "@" ident lparen _ annotation_params? _ rparen
    annotation_params = ident (_ listsep _ annotation_params)?
"""

type_ = r"""
    type             = ident (_ type_wrapped _)?
    type_wrapped     = lt _ type _ gt
"""

params = r"""
    parameters       = lparen _ param_list? _ rparen
    param_list       = param (_ listsep _ param_list)? 
    param            = param_ident _ typesep _ type
    param_ident      = (param_qualifier ws ident) / ident
    param_qualifier  = "out" / "opt" 
"""

function = r"""
    func              = func_sig _ func_body
    func_sig          = (annotation _)? func_start func_parameters _ func_return_type
    func_start        = (qualifierlist ws)? "func" _ ident _ 
    func_parameters   = _ parameters _
    func_return_type  = "->" _ type
    func_body_start   = lbrace
    func_body_end     = rbrace
    func_body_content = func_body / (!func_body_start !func_body_end ~"."s)
    func_body         = func_body_start func_body_content* func_body_end
"""

enum = r"""
    enum             = "enum" ws ident _ enum_body
    enum_body        = lbrace _ enum_list? _ rbrace
    enum_list        = enum_decl (_ listsep _ enum_list)? listsep?
    enum_decl        = ident _ equal _ enum_value
    enum_value       = ~"\d+"a
"""

braced_body = r"""
    braced           = lbrace _ braced_body* _ rbrace
    braced_body      = deflist / statement
    statement        = statement_body statement_term
    statement_body   = ~"[^;]+"a*
    statement_term   = ";"
"""

# grammar = Grammar(r"""
# start = ( def / statement / _ )*
# lp = "("
# rp = ")"
# lb = "{"
# rb = "}"
# def = ident _ def_body
# def_body = lb _ (def / statement)* _ rb
# statement = statement_body statement_term
# statement_body = ~"[^;]+"a*
# statement_term = ";"
# ident = ~"[a-zA-Z_]\w*"ia
# _ = ~"\s*"a
# """)
