$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Python = (Get-Command python).Source
& $Python -c "import yaml, jsonschema, jinja2" 2>$null
if ($LASTEXITCODE -eq 0) {
  Set-Content -Path "$Root/.runtime-python" -Value $Python
  Write-Host "Using existing Python runtime: $Python"
} else {
  if (Test-Path "$Root/.venv") { Remove-Item -Recurse -Force "$Root/.venv" }
  & $Python -m venv "$Root/.venv"
  $Python = "$Root/.venv/Scripts/python.exe"
  & $Python -m pip install -r "$Root/requirements.txt"
  Set-Content -Path "$Root/.runtime-python" -Value $Python
}
& $Python -c "import yaml, jsonschema, jinja2; print('Dependencies available')"
Write-Host "Ready. Run scripts/run.ps1 --help"
