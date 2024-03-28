$scriptDirectory = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Push-Location $scriptDirectory

Write-Output "--- pip install ---"
python -m pip install -e ..

Pop-Location
