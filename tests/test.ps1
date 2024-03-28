$scriptDirectory = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Push-Location $scriptDirectory

Write-Output "--- c_cmake nomal ---"
python -m darumaotoshi -i .\data\c_cmake\bowling_game_cli\index.html -o .\work\c_cmake\nomal
Write-Output "--- c_cmake prettyprint ---"
python -m darumaotoshi -i .\data\c_cmake\bowling_game_cli\index.html -o .\work\c_cmake\prettyprint -p
Write-Output "--- c_cmake flat ---"
python -m darumaotoshi -i .\data\c_cmake\bowling_game_cli\index.html -o .\work\c_cmake\flat -f
Write-Output "--- c_cmake embedded_css ---"
python -m darumaotoshi -i .\data\c_cmake\bowling_game_cli\index.html -o .\work\c_cmake\embedded_css -e
Write-Output "--- c_cmake verbose ---"
python -m darumaotoshi -i .\data\c_cmake\bowling_game_cli\index.html -o .\work\c_cmake\verbose -v
Write-Output "--- c_cmake option-all ---"
python -m darumaotoshi -i .\data\c_cmake\bowling_game_cli\index.html -o .\work\c_cmake\option-all -p -f -e -v

Write-Output "--- cxx_cmake nomal ---"
python -m darumaotoshi -i .\data\cxx_cmake\bowling_game_cli\index.html -o .\work\cxx_cmake\nomal
Write-Output "--- cxx_cmake prettyprint ---"
python -m darumaotoshi -i .\data\cxx_cmake\bowling_game_cli\index.html -o .\work\cxx_cmake\prettyprint -p
Write-Output "--- cxx_cmake flat ---"
python -m darumaotoshi -i .\data\cxx_cmake\bowling_game_cli\index.html -o .\work\cxx_cmake\flat -f
Write-Output "--- cxx_cmake embedded_css ---"
python -m darumaotoshi -i .\data\cxx_cmake\bowling_game_cli\index.html -o .\work\cxx_cmake\embedded_css -e
Write-Output "--- cxx_cmake verbose ---"
python -m darumaotoshi -i .\data\cxx_cmake\bowling_game_cli\index.html -o .\work\cxx_cmake\verbose -v
Write-Output "--- cxx_cmake option-all ---"
python -m darumaotoshi -i .\data\cxx_cmake\bowling_game_cli\index.html -o .\work\cxx_cmake\option-all -p -f -e -v

Pop-Location
