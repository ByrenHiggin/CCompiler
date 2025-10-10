mkdir build
cd build 
mkdir preprocessed
mkdir compiled
cd ..
mkdir dist
export INPUT_FILE='c_programs/basic.c'
export FILE_NAME='basic'
export OUTPUT_FILE='build/preprocessed/'$FILE_NAME'.c'
export INPUT_ASSEMBLY='build/compiled/'$FILE_NAME'.s'
export OUTPUT_EXECUTABLE='dist/'$FILE_NAME

echo "INPUT: " $INPUT_FILE
echo "OUTPUT: " $OUTPUT_FILE

gcc -E -P $INPUT_FILE -o $OUTPUT_FILE
uv run main.py
gcc $INPUT_ASSEMBLY -o $OUTPUT_EXECUTABLE

echo "Running compiled application:"
dist/basic
echo '2 == '$?'? if yes, success!!!!'