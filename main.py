import sys
import argparse

parser = argparse.ArgumentParser(description="A sample script demonstrating argument parsing.")

def handle_argument(arg):
    if arg == '--lex':
        return "Lexical analysis selected."
    if arg == '--parse':
        return "Parsing selected."
    
def main():
    parser.add_argument('--lex', action='store_true', help='Perform lexical analysis')
    parser.add_argument('--parse', action='store_true', help='Perform parsing')
    args = parser.parse_args()
    
    if(args.lex):
        print("Lexical analysis selected.")
    if(args.parse):
        print("Parsing selected.")
    if not (args.lex or args.parse):
        print("Hello from ccompiler!")


if __name__ == "__main__":
    main()