# Building module

mkdir -p pawnpy/build
cd pawnpy/build
cmake ../
make pawncc pawnpy -j4
cd ../../

cp -f pawnpy/build/libpawnpy.so ./pawnpy
cp -f pawnpy/build/pawncc ./pawnpy

echo "Running $(python3 --version)"

python3 -m unittest discover ./tests
