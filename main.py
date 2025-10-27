import sys
import argparse
import logging
from modules.lexer.LexerService import LexerService
from modules.parser.ParserService import ParserService
from modules.utils.logger import setup_logger, get_logger, info, debug, error

argparser = argparse.ArgumentParser(description="A C Compiler implementation.")

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
    argparser.add_argument('--tacky',"-t", action='store_true', help='Perform tacky')
    argparser.add_argument('--output', "-S", type=str, help='File location to process', default="output.s")
    argparser.add_argument('--verbose', "-v", action='store_true', help='Enable verbose logging')
    argparser.add_argument('--log-file', type=str, help='Log to file instead of console')
    argparser.add_argument('file', type=ascii, help='File to process')
    args = argparser.parse_args()
    
    # Setup logger based on arguments
    log_level = logging.DEBUG if args.verbose else logging.INFO
    log_file = args.log_file if hasattr(args, 'log_file') and args.log_file else None
    setup_logger(level=log_level, log_file=log_file)
    
    info("Compiler starting...")
    debug(f"Arguments: {args}")
    
    if(args.file):
        try:
            file_path = args.file.strip("'")
            info(f"Processing file: {file_path}")
            
            # Lexical analysis
            debug("Starting lexical analysis...")
            lexer = LexerService()
            tokens = lexer.lex_file(file_path)
            info(f"Lexical analysis complete. Generated {len(tokens)} tokens.")
            if(args.lex):
                debug("Stopping after lexical analysis as requested.")
                sys.exit(0)
            
            # Parsing
            debug("Starting parsing...")
            parser = ParserService()
            ast = parser.parse_lex(tokens) # type: ignore
            info("Parsing complete. AST generated.")
            if(args.parse):
                debug("Stopping after parsing as requested.")
                sys.exit(0)
            
            # Tacky intermediate representation
            debug("Converting to Tacky IR...")
            ast = ast.toTacky()
            info("Tacky IR generation complete.")
            if(args.tacky):
                debug("Stopping after Tacky IR generation as requested.")
                sys.exit(0)
            
            # Assembly generation
            debug("Generating assembly code...")
            asm = ast.toAsm()
            info(f"Assembly generation complete. Writing to {args.output}")
            
            with open(args.output, "w") as file_object:
                file_object.write(asm)
            
            info("Compilation completed successfully!")
            if(args.codegen):
                sys.exit(0)
        except Exception as e:
            error(f"Compilation failed: {e}")
            debug("Exception details:", exc_info=True)
            sys.exit(1)
    else:
        argparser.print_help()

if __name__ == "__main__":
    main()