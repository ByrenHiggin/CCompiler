import sys
import argparse
from modules.lexer.LexerService import LexerService
from modules.parser.ParserService import ParserService

argparser = argparse.ArgumentParser(description="A sample script demonstrating argument parsing.")

def handle_argument(arg: str) -> str:
    if arg == '--lex':
        return "Lexical analysis selected."
    if arg == '--parse':
        return "Parsing selected."
    else:
        return "No valid argument selected."
    
def main():
    argparser.add_argument('--lex',"-l", action='store_true', help='Perform lexical analysis')
    argparser.add_argument('--parse',"-p", action='store_true', help='Perform parsing')
    argparser.add_argument('--codegen',"-c", action='store_true', help='Perform codegen')
    argparser.add_argument('--output', "-S", type=str, help='File location to process', default="output.s")
    argparser.add_argument('file', type=ascii, help='File to process')
    args = argparser.parse_args()
    print("Compiler starting...")
    if(args.file):
        try:
            lexer = LexerService()
            parser = ParserService()
            tokens = lexer.lex_file(args.file.strip("'"))
            if(args.lex):
                sys.exit(0)
            ast = parser.parse_lex(tokens) # type: ignore
            if(args.parse):
                sys.exit(0)
            print("codegen now")
            asm = ast.toAsm()
            with open(args.output, "w") as file_object:
                file_object.write(asm)
            if(args.codegen):
                print("Hello from ccompiler!")
            sys.exit(0)
        except Exception as e:
            print(f"{e}")
            sys.exit(1)
    else:
        argparser.print_help()

if __name__ == "__main__":
    main()