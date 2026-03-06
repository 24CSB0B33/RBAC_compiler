import re

# Token definitions
TOKEN_TYPES = [
    ('ROLE',      r'\brole\b'),
    ('INHERITS',  r'\binherits\b'),
    ('PERMIT',    r'\bpermit\b'),
    ('CONFLICT',  r'\bconflict\b'),  # Changed from DENY to CONFLICT for clarity
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('COMMA',     r','),
    ('ID',        r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('SKIP',      r'[ \t\n]+'),
    ('MISMATCH',  r'.')
]

class Lexer:
    def __init__(self, text): 
        self.text = text
        self.tokens = []

    def tokenize(self):
        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_TYPES)
        for mo in re.finditer(token_regex, self.text, re.IGNORECASE):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f"Unexpected character: {value}")
            self.tokens.append((kind, value))
        self.tokens.append(('EOF', None))
        return self.tokens
