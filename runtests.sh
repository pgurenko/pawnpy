# Building module

mkdir -p pawnpy/build
cd pawnpy/build
cmake ../
make -j4
cd ../../

cp -f pawnpy/build/libpawnpy.so ./pawnpy

echo "Running $(python3 --version)"

python3 -m unittest discover ./tests