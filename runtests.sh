# Building module

mkdir -p build
cd build
cmake ../pawnpy
make pawncc pawnpy -j4
cd ../

cp -f build/libpawnpy.so ./pawnpy
cp -f build/pawncc ./pawnpy

echo "Running $(python3 --version)"

python3 -m unittest discover ./tests
