import sys
import argparse
import logging
from modules.codeGenerator.AssemblyGenerator import AssemblyGenerator
from modules.lexer.LexerService import LexerService
from modules.parser.ParserServiceV2 import ParserServiceV2
from modules.IntermediateGenerator.IRGenerator import IRGenerator, TackyGenerator
from modules.utils import logger

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
	
	# Setup global logger based on arguments
	log_level = logging.DEBUG if args.verbose else logging.INFO
	log_file = args.log_file if hasattr(args, 'log_file') and args.log_file else None
	logger.setup_logger(level=log_level, log_file=log_file)
	_logger = logger.get_logger()
	
	_logger.info("Compiler starting...")
	_logger.debug(f"Arguments: {args}")
	
	if(args.file):
		try:
			file_path = args.file.strip("'")
			_logger.info(f"Processing file: {file_path}")
			
			# Lexical analysis
			_logger.debug("Starting lexical analysis...")
			lexer = LexerService()
			tokens = lexer.lex_file(file_path)
			_logger.info(f"Lexical analysis complete. Generated {len(tokens)} tokens.")
			if(args.lex):
				_logger.debug("Stopping after lexical analysis as requested.")
				sys.exit(0)
			
			# Parsing
			_logger.debug("Starting parsing...")
			#parser = ParserService()
			parserV2 = ParserServiceV2()
			#ast = parser.parse_lex(tokens) # type: ignore
			ast = parserV2.parse_lex(tokens) # type: ignore
			_logger.info("Parsing complete. AST generated.")
			if(args.parse):
				_logger.debug("Stopping after parsing as requested.")
				sys.exit(0)
			
			# Tacky intermediate representation
			_logger.debug("Converting to Tacky IR...")
			ir_Generator = IRGenerator()
			intermediate_representation = ir_Generator.parse_ast(ast)
			_logger.info("Tacky IR generation complete.")
			if(args.tacky):
				_logger.debug("Stopping after Tacky IR generation as requested.")
				sys.exit(0)
			
			# Assembly generation
			_logger.debug("Generating assembly code...")
			assembly_generator = AssemblyGenerator()
			asm: list[str] = []
			assembly_generator.generate(intermediate_representation, asm)
			_logger.info(f"Assembly generation complete. Writing to {args.output}")
			
			with open(args.output, "w") as file_object:
				file_object.writelines(asm)

			_logger.info("Compilation completed successfully!")
			if(args.codegen):
				sys.exit(0)
		except Exception as e:
			_logger.error(f"Compilation failed: {e}")
			_logger.debug("Exception details:", exc_info=True)
			sys.exit(1)
	else:
		argparser.print_help()

if __name__ == "__main__":
	main()