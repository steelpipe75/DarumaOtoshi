#!/bin/bashdata

script_dir="$(dirname "$0")"
pushd "$script_dir"

echo --- pip install ---
python -m pip install -e ..
python -m pip install coverage

popd
