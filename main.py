import sys
import argparse
from modules.lexer.lexer import LexerInstance

parser = argparse.ArgumentParser(description="A sample script demonstrating argument parsing.")

def handle_argument(arg):
    if arg == '--lex':
        return "Lexical analysis selected."
    if arg == '--parse':
        return "Parsing selected."
    
def main():
    parser.add_argument('--lex',"-l", action='store_true', help='Perform lexical analysis')
    parser.add_argument('--parse',"-p", action='store_true', help='Perform parsing')
    parser.add_argument('--codegen',"-c", action='store_true', help='Perform codegen')
    parser.add_argument('file', type=ascii, help='File to process')
    args = parser.parse_args()
    if(args.file):
        lexer = LexerInstance()
        lexer.lex_file(args.file.strip("'"))
        if(args.lex):
            sys.exit(0)
        print("parsing now")
        if(args.parse):
            print("Parsing selected.")
            sys.exit(0)
        print("codegen now")
        if(args.codegen):
            print("Hello from ccompiler!")
        sys.exit(0)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()