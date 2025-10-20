from enum import Enum

class KeyWordPatterns(Enum):
    RETURN = r'return\b'
    IF = r'if\b'
    ELSE = r'else\b'
    WHILE = r'while\b'
    FOR = r'for\b'
    VOID = r'void\b'