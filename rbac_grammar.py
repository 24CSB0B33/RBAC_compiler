#lark is used here as a python library for lexing and parsing
#to simplify trivial conditions
#here our grammar structure is developed with main identifiers as ROLE,DENY,INHERITS,PERMIT
#later additional identifiers will be added in progress of project
#EBNF form

from lark import Lark
rbac_syntax = r"""
    start : statement+

    ?statement:role_decl
            | rule_decl

    role_decl: "ROLE" IDENTIFIER [inheritance] "{" permission* "}"
    inheritance: "INHERITS" identifier_list
    permission: "PERMIT" IDENTIFIER

    rule_decl: "DENY" IDENTIFIER "," IDENTIFIER

    identifier_list: IDENTIFIER ("," IDENTIFIER)*

    %import common.CNAME -> IDENTIFIER
    %import common.WS
    %ignore WS
    %import common.CPP_COMMENT
    %ignore CPP_COMMENT
"""

rbac_parser = Lark(rbac_syntax)