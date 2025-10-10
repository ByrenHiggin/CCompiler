from enum import Enum

class KeyWordPatterns(Enum):
    INT = r'int\b'
    FLOAT = r'float\b'
    CHAR = r'char\b'
    RETURN = r'return\b'
    IF = r'if\b'
    ELSE = r'else\b'
    WHILE = r'while\b'
    FOR = r'for\b'
    VOID = r'void\b'