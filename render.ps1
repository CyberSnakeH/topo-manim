param(
    [ValidateSet(
        "all",
        "hq",
        "help",
        "connexe_vs_arcs",
        "invariance",
        "sin1x",
        "borel_lebesgue",
        "baire",
        "connexite",
        "compacite",
        "completude",
        "check",
        "test",
        "lint",
        "format",
        "format-check",
        "install",
        "clean"
    )]
    [string] $Target = "all",

    [ValidateSet("ql", "qm", "qh", "qk")]
    [string] $Quality = "ql",

    [switch] $Help
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = $ProjectRoot
$StartTime = Get-Date

function Write-Info {
    param([string] $Message)
    Write-Host "[INFO]  $Message" -ForegroundColor Cyan
}

function Write-Step {
    param([string] $Message)
    Write-Host "[RUN]   $Message" -ForegroundColor Yellow
}

function Write-Success {
    param([string] $Message)
    Write-Host "[OK]    $Message" -ForegroundColor Green
}

function Write-Failure {
    param([string] $Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-RenderHelp {
    Write-Host ""
    Write-Host "topo-manim Windows runner" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\render.ps1 [target] [-Quality ql|qm|qh|qk]"
    Write-Host "  .\render.ps1 -Help"
    Write-Host ""
    Write-Host "Scene targets:" -ForegroundColor Yellow
    Write-Host "  connexe_vs_arcs     Render ConnexeVsArcs"
    Write-Host "  invariance          Render InvarianceTopologique"
    Write-Host "  sin1x               Render ContreExempleSin1x"
    Write-Host "  borel_lebesgue      Render BorelLebesgue"
    Write-Host "  baire               Render Baire"
    Write-Host ""
    Write-Host "Group targets:" -ForegroundColor Yellow
    Write-Host "  connexite           Render connexe_vs_arcs, invariance, sin1x"
    Write-Host "  compacite           Render borel_lebesgue"
    Write-Host "  completude          Render baire"
    Write-Host "  all                 Render every scene in the selected quality"
    Write-Host "  hq                  Render every scene in high quality (-qh)"
    Write-Host ""
    Write-Host "Utility targets:" -ForegroundColor Yellow
    Write-Host "  install             Run uv sync"
    Write-Host "  check               Run python compileall on src, scenes, tests"
    Write-Host "  test                Run pytest"
    Write-Host "  lint                Run ruff check"
    Write-Host "  format              Run ruff format then ruff check --fix"
    Write-Host "  format-check        CI-friendly: fail if anything would be reformatted"
    Write-Host "  clean               Remove media/"
    Write-Host "  help                Show this help"
    Write-Host ""
    Write-Host "Quality:" -ForegroundColor Yellow
    Write-Host "  ql                  Low quality, fastest"
    Write-Host "  qm                  Medium quality"
    Write-Host "  qh                  High quality, 1080p"
    Write-Host "  qk                  4K quality, slow"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\render.ps1 check"
    Write-Host "  .\render.ps1 test"
    Write-Host "  .\render.ps1 all"
    Write-Host "  .\render.ps1 connexe_vs_arcs -Quality qh"
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\render.ps1 all"
    Write-Host ""
}

function Invoke-CommandChecked {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Program,

        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]] $Arguments
    )

    Write-Step "$Program $($Arguments -join ' ')"
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $Program $($Arguments -join ' ')"
    }
    Write-Success "Done"
}

function Invoke-ManimScene {
    param(
        [Parameter(Mandatory = $true)]
        [string] $ScenePath,

        [Parameter(Mandatory = $true)]
        [string] $SceneClass
    )

    Write-Info "Rendering $SceneClass with -$Quality"
    Invoke-CommandChecked uv run manim render "-$Quality" $ScenePath $SceneClass
}

function Invoke-Target {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Name
    )

    switch ($Name) {
        "connexe_vs_arcs" {
            Invoke-ManimScene "scenes/01_connexite/connexe_vs_arcs.py" "ConnexeVsArcs"
        }
        "invariance" {
            Invoke-ManimScene "scenes/01_connexite/invariance_topologique.py" "InvarianceTopologique"
        }
        "sin1x" {
            Invoke-ManimScene "scenes/01_connexite/contre_exemple_sin1x.py" "ContreExempleSin1x"
        }
        "borel_lebesgue" {
            Invoke-ManimScene "scenes/02_compacite/borel_lebesgue.py" "BorelLebesgue"
        }
        "baire" {
            Invoke-ManimScene "scenes/03_completude/baire.py" "Baire"
        }
        "help" {
            Write-RenderHelp
        }
        "connexite" {
            Write-Info "Rendering chapter: connexite"
            Invoke-Target "connexe_vs_arcs"
            Invoke-Target "invariance"
            Invoke-Target "sin1x"
        }
        "compacite" {
            Write-Info "Rendering chapter: compacite"
            Invoke-Target "borel_lebesgue"
        }
        "completude" {
            Write-Info "Rendering chapter: completude"
            Invoke-Target "baire"
        }
        "all" {
            Write-Info "Rendering all scenes with -$Quality"
            Invoke-Target "connexite"
            Invoke-Target "compacite"
            Invoke-Target "completude"
        }
        "hq" {
            Write-Info "Switching to high quality (-qh)"
            $script:Quality = "qh"
            Invoke-Target "all"
        }
        "check" {
            Invoke-CommandChecked uv run python -m compileall src scenes tests
        }
        "test" {
            Invoke-CommandChecked uv run pytest
        }
        "lint" {
            Invoke-CommandChecked uv run ruff check .
        }
        "format" {
            Invoke-CommandChecked uv run ruff format .
            Invoke-CommandChecked uv run ruff check --fix .
        }
        "format-check" {
            Invoke-CommandChecked uv run ruff format --check .
            Invoke-CommandChecked uv run ruff check .
        }
        "install" {
            Invoke-CommandChecked uv sync
        }
        "clean" {
            Write-Step "Removing media/"
            Remove-Item -LiteralPath (Join-Path $ProjectRoot "media") -Recurse -Force -ErrorAction SilentlyContinue
            Write-Success "Cleaned media/"
        }
    }
}

Push-Location $ProjectRoot
try {
    if ($Help) {
        Write-RenderHelp
    }
    else {
        Write-Info "Project root: $ProjectRoot"
        Invoke-Target $Target
        $Elapsed = (Get-Date) - $StartTime
        Write-Success ("Finished in {0:mm\:ss}" -f $Elapsed)
    }
}
catch {
    Write-Failure $_.Exception.Message
    exit 1
}
finally {
    Pop-Location
}
