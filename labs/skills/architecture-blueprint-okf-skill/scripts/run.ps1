$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (-not (Test-Path "$Root/.runtime-python")) { throw "Skill environment not configured. Run scripts/setup.ps1 first." }
$Python = (Get-Content "$Root/.runtime-python" -Raw).Trim()
$env:PYTHONPATH = "$Root/src" + $(if ($env:PYTHONPATH) { ";$env:PYTHONPATH" } else { "" })
& $Python -m architecture_blueprint_okf.cli @args
