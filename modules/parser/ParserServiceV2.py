from typing import Callable, List
from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode
from modules.models.nodes.BaseNode import BaseNode 
from modules.models.nodes.AST.ProgramNode import ProgramNode
from modules.models.lexer.Token import Token
from modules.models.enums.token_type import TokenType
from modules.parser.Services.ExpressionParser import ExpressionParser
from modules.parser.Services.FunctionParser import FunctionParser
from modules.parser.Services.StatementParser import StatementParser
from modules.parser.Services.TokenIteratorService import TokenIteratorService



class ParserServiceV2():
    functions: List[FunctionDefinitionNode] = []
    expressionService: ExpressionParser
    expression_handlers: dict[TokenType, Callable[[], BaseNode]] = {}
    statement_handlers: dict[TokenType, Callable[[], BaseNode]] = {}
    token_iterator: TokenIteratorService
    
    def __init__(self):
        self.token_iterator = TokenIteratorService()
        self.expressionService = ExpressionParser(self.token_iterator)
        self.statementService = StatementParser(self.token_iterator, self.expressionService)
        self.functionService = FunctionParser(self.token_iterator, self.expressionService, self.statementService)

    
    ## Entry Point
    def parse_lex(self, lex_array: List[Token]) -> ProgramNode:
        print("Parsing lex array...")
        self.token_iterator.lex_array = lex_array
        self.token_iterator.position = 0
        self.functions = []
        while self.token_iterator.position < len(self.token_iterator.lex_array):
            self.functions.append(self.functionService.parse_declaration())
        return ProgramNode(functions=self.functions)
    