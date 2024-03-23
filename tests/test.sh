#!/bin/bashdata

echo --- pip install ---
python -m pip install -e ..

echo --- c_cmake nomal ---
python -m darumaotoshi -i ./data/c_cmake/bowling_game_cli/index.html -o ./work/c_cmake/nomal
echo --- c_cmake prettyprint ---
python -m darumaotoshi -i ./data/c_cmake/bowling_game_cli/index.html -o ./work/c_cmake/prettyprint -p

echo --- cxx_cmake nomal ---
python -m darumaotoshi -i ./data/cxx_cmake/bowling_game_cli/index.html -o ./work/cxx_cmake/nomal
echo --- cxx_cmake prettyprint ---
python -m darumaotoshi -i ./data/cxx_cmake/bowling_game_cli/index.html -o ./work/cxx_cmake/prettyprint -p

echo --- diff ---
diff -r GoldenFile/ work/
