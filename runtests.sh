# Building module

./build.sh

echo "Running $(python3 --version)"

python3 -m unittest discover ./tests
