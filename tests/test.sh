#!/bin/bashdata

script_dir="$(dirname "$0")"
pushd "$script_dir"

echo --- c_cmake nomal ---
python -m coverage run    -m darumaotoshi -i ./data/c_cmake/bowling_game_cli/index.html -o ./work/c_cmake/nomal
echo --- c_cmake prettyprint ---
python -m coverage run -a -m darumaotoshi -i ./data/c_cmake/bowling_game_cli/index.html -o ./work/c_cmake/prettyprint -p
echo --- c_cmake flat ---
python -m coverage run -a -m darumaotoshi -i ./data/c_cmake/bowling_game_cli/index.html -o ./work/c_cmake/flat -f
echo --- c_cmake embedded_css ---
python -m coverage run -a -m darumaotoshi -i ./data/c_cmake/bowling_game_cli/index.html -o ./work/c_cmake/embedded_css -e

echo --- cxx_cmake nomal ---
python -m coverage run -a -m darumaotoshi -i ./data/cxx_cmake/bowling_game_cli/index.html -o ./work/cxx_cmake/nomal
echo --- cxx_cmake prettyprint ---
python -m coverage run -a -m darumaotoshi -i ./data/cxx_cmake/bowling_game_cli/index.html -o ./work/cxx_cmake/prettyprint -p
echo --- cxx_cmake flat ---
python -m coverage run -a -m darumaotoshi -i ./data/cxx_cmake/bowling_game_cli/index.html -o ./work/cxx_cmake/flat -f
echo --- cxx_cmake embedded_css ---
python -m coverage run -a -m darumaotoshi -i ./data/cxx_cmake/bowling_game_cli/index.html -o ./work/cxx_cmake/embedded_css -e

echo --- coverage htm ---
python -m coverage html

echo --- diff ---
diff -r GoldenFile/ work/
if [ $? -eq 0 ]; then
    exit_code=0
else
    exit_code=1
fi

popd

exit "$exit_code"
