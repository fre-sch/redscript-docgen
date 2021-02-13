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
    qualifierlist    = (qualifier ws qualifierlist) / qualifier
"""

ident = r"""
    ident            = ~"[a-z_]\w*"ai
"""

symbols = r"""
    lbrace           = "{"
    rbrace           = "}"
    lparen           = "("
    rparen           = ")"
    listsep          = _ "," _
    gt               = ">"
    lt               = "<"
    typesep          = ":"
"""

annotation = r"""
    annotation        = "@" ident lparen _ annotation_params? _ rparen
    annotation_params = (ident listsep annotation_params) / ident
"""

type_ = r"""
    type             = ident (_ type_wrapped _)?
    type_wrapped     = lt _ type _ gt
"""

params = r"""
    parameters       = lparen _ param_list? _ rparen
    param_list       = (param listsep param_list) / param 
    param            = param_ident _ typesep _ type
    param_ident      = (param_qualifier ws ident) / ident
    param_qualifier  = "out" / "opt" 
"""

#
# grammar = Grammar(r"""
# deflist          = ( def / _ )*
# def              = func / annotation
# _                = ~"\s*"a
# ws               = ~"\s+"a
# comment_start    = "/*"
# comment_end      = "*/"
# comment_content  = comment / (!comment_start !comment_end _)
# comment          = comment_start comment_content* comment_end
# line_comment     = "//" ~".*$"
# qualifier        = "public" / "protected" / "private" / "static" / "final" /
#                    "const" / "native" / "exec" / "cb" /
#                    "abstract" / "persistent" / "inline" / "edit" / "rep"
# qualifierlist    = (qualifier ws qualifierlist) / qualifier
# ident            = ~"\w+"a
# typesep          = _ ":" _
# annotationparams = (ident listsep typeparamlist) / ident
# annotation       = "@" ident rparen _ annotationparams? _ lparen
# type             = ident ( _ type_wrapped _ )?
# type_wrapped     = lt _ type _ gt
# param            = ("out" / "opt")* _ ident typesep type
# paramlist        = (param listsep paramlist) / param
# func_sig         = qualifierlist* ws "func" _ ident _ lparen _ paramlist? _ rparen _ "->" _
# func             = func_sig
# braced           = lbrace _ ( deflist / statement )* _ rbrace
# statement        = statement_body statement_term
# statement_body   = ~"[^;]+"a*
# statement_term   = ";"
# """)
#
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
#
# tree = grammar.parse("""
# foo; bar;
# foo bar;
# let foo:bar = wusch();
# one {
#     foo; bar;
#     foo bar;
#     let foo:bar = wusch();
# }
# two {
#     let foo;
#     three {
#         let foo:bar = wusch();
#     }
#     let foo:bar = wusch();
# """)
# print(tree)
