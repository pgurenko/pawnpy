# Building module

./build.sh

cp -f build/libpawnpy.* ./pawnpy
cp -f build/pawncc ./pawnpy

python3 -m unittest discover ./tests
