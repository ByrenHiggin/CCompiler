source ./.venv/bin/activate
uv run pyinstaller main.py -y
echo "Build complete. Executable is located in the 'dist' directory."
./dist/main/main ./writing-a-c-compiler-tests/tests/chapter_1/valid/multi_digit.c
echo "Running tests with compiler now"
./writing-a-c-compiler-tests/test_compiler ./dist/main/main --chapter 3 --stage parse 