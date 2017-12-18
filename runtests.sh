# Building module

mkdir -p pawnpy/build-lib
cd pawnpy/build-lib
cmake ../
make -j4
cd ../../

mkdir -p pawnpy/build-cc
cd pawnpy/build-cc
cmake ../src/pawn/compiler
make -j4
cd ../../

cp -f pawnpy/build-lib/libpawnpy.so ./pawnpy
cp -f pawnpy/build-cc/pawncc ./pawnpy

echo "Running $(python3 --version)"

python3 -m unittest discover ./tests
