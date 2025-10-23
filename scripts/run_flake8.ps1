# Wrapper script to run flake8 with the tests/.flake8 config
# Usage: ./scripts/run_flake8.ps1

$python = "C:/Users/JinLa/AppData/Local/Microsoft/WindowsApps/python3.11.exe"
$config = "tests/.flake8"
Write-Host "Running flake8 using config: $config"
& $python -m flake8 --config=$config ; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
