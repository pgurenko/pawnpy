# Building module

./build.sh

cp -f build/libpawnpy.so ./pawnpy
cp -f build/pawncc ./pawnpy

echo "Running $(python3 --version)"

python3 -m unittest discover ./tests
