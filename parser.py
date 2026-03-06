from typing import List, TypedDict, Tuple

class Role(TypedDict):
    name: str
    parents: List[str]
    permissions: List[str]

Conflict = Tuple[str, str]

class AST(TypedDict):
    roles: List[Role]
    conflicts: List[Conflict]

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type):
        current_type, current_value = self.tokens[self.pos]
        if current_type == expected_type:
            self.pos += 1
            return current_value
        else:
            raise SyntaxError(f"Expected {expected_type}, got {current_type} ('{current_value}')")

    def parse(self) -> AST:
        ast: AST = {"roles": [], "conflicts": []}
        while self.tokens[self.pos][0] != 'EOF':
            kind = self.tokens[self.pos][0]
            if kind == 'ROLE':
                ast["roles"].append(self.parse_role())
            elif kind == 'CONFLICT':
                ast["conflicts"].append(self.parse_conflict())
            else:
                raise SyntaxError(f"Unexpected token: {kind}")
        return ast

    def parse_role(self) -> Role:
        self.consume('ROLE')
        name = self.consume('ID')
        parents = []
        if self.tokens[self.pos][0] == 'INHERITS':
            self.consume('INHERITS')
            parents.append(self.consume('ID'))
            while self.tokens[self.pos][0] == 'COMMA':
                self.consume('COMMA')
                parents.append(self.consume('ID'))

        self.consume('LBRACE')
        perms = []
        while self.tokens[self.pos][0] == 'PERMIT':
            self.consume('PERMIT')
            perms.append(self.consume('ID'))
            while self.tokens[self.pos][0] == 'COMMA':
                self.consume('COMMA')
                perms.append(self.consume('ID'))
        self.consume('RBRACE')

        return {"name": name, "parents": parents, "permissions": perms}

    def parse_conflict(self) -> Conflict:
        self.consume('CONFLICT')
        r1 = self.consume('ID')
        self.consume('COMMA')
        r2 = self.consume('ID')
        return (r1, r2)
