$scriptDirectory = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Push-Location $scriptDirectory

Write-Output "--- pip install ---"
python -m pip install -e ..

Write-Output "--- c_cmake nomal ---"
python -m darumaotoshi -i .\data\c_cmake\bowling_game_cli\index.html -o .\work\c_cmake\nomal
Write-Output "--- c_cmake prettyprint ---"
python -m darumaotoshi -i .\data\c_cmake\bowling_game_cli\index.html -o .\work\c_cmake\prettyprint -p

Write-Output "--- cxx_cmake nomal ---"
python -m darumaotoshi -i .\data\cxx_cmake\bowling_game_cli\index.html -o .\work\cxx_cmake\nomal
Write-Output "--- cxx_cmake prettyprint ---"
python -m darumaotoshi -i .\data\cxx_cmake\bowling_game_cli\index.html -o .\work\cxx_cmake\prettyprint -p

Pop-Location
