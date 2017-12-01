# Building module

mkdir -p pawnpy/build
cd pawnpy/build
cmake ../
make -j4
cd ../../

cp -f pawnpy/build/pawnpy.so ./tests

python3 -m unittest discover ./tests