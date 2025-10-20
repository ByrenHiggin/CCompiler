source ./.venv/bin/activate
uv run pyinstaller main.py -y
echo "Build complete. Executable is located in the 'dist' directory."
./dist/main/main ./writing-a-c-compiler-tests/tests/chapter_1/valid/multi_digit.c
echo "Running tests with compiler now"
./writing-a-c-compiler-tests/test_compiler ./dist/main/main --chapter 1 --stage parse
# uv run main.py --parse writing-a-c-compiler-tests/tests/chapter_1/valid/multi_digit.c 
# uv run main.py --parse writing-a-c-compiler-tests/tests/chapter_1/valid/newlines.c 
# uv run main.py --parse writing-a-c-compiler-tests/tests/chapter_1/valid/no_newlines.c 
# uv run main.py --parse writing-a-c-compiler-tests/tests/chapter_1/valid/return_0.c 
# uv run main.py --parse writing-a-c-compiler-tests/tests/chapter_1/valid/return_2.c 
# uv run main.py --parse writing-a-c-compiler-tests/tests/chapter_1/valid/tabs.c
# uv run main.py --parse writing-a-c-compiler-tests/tests/chapter_1/valid/tabs.c

./dist/main/main --parse writing-a-c-compiler-tests/tests/chapter_1/valid/multi_digit.c && echo $? 
./dist/main/main --parse writing-a-c-compiler-tests/tests/chapter_1/valid/newlines.c  && echo $?  
./dist/main/main --parse writing-a-c-compiler-tests/tests/chapter_1/valid/no_newlines.c  && echo $? 
./dist/main/main --parse writing-a-c-compiler-tests/tests/chapter_1/valid/return_0.c  && echo $? 
./dist/main/main --parse writing-a-c-compiler-tests/tests/chapter_1/valid/return_2.c  && echo $? 
./dist/main/main --parse writing-a-c-compiler-tests/tests/chapter_1/valid/spaces.c  && echo $? 
./dist/main/main --parse writing-a-c-compiler-tests/tests/chapter_1/valid/tabs.c && echo $?

./dist/main/main --parse writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/end_before_expr.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/extra_junk.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/invalid_function_name.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/keyword_wrong_case.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/missing_type.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/misspelled_keyword.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/no_semicolon.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/not_expression.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/space_in_keyword.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/switched_parens.c 
Writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/unclosed_brace.c 
writing-a-c-compiler-tests/tests/chapter_1/invalid_parse/unclosed_paren.c