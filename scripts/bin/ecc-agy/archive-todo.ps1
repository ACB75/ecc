<#
.SYNOPSIS
    Archiva tareas completadas (- [x]) desde doc/TODO.md hacia doc/TODO_DONE/TODO_<title>_TS.md.
.DESCRIPTION
    Script rutinario para Windows 11 (pwsh) que delega en scripts/ecc-agy/archive_todo.py.
.PARAMETER TodoPath
    Ruta al archivo TODO principal (por defecto: doc/TODO.md).
.PARAMETER DoneDir
    Directorio destino de archivo (por defecto: doc/TODO_DONE).
.PARAMETER Complete
    Título o substring de la tarea específica a archivar.
.PARAMETER AllCompleted
    Archiva todas las tareas marcadas como completadas (- [x]).
.PARAMETER Notes
    Notas adicionales de entregables o verificación a registrar.
.PARAMETER DryRun
    Muestra qué tareas se archivarían sin alterar el disco.
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/archive-todo.ps1 -AllCompleted
#>
param(
    [string]$TodoPath = "doc/TODO.md",
    [string]$DoneDir = "doc/TODO_DONE",
    [string]$Complete,
    [switch]$AllCompleted,
    [string]$Notes,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = (Resolve-Path "$ScriptDir\..\..\..").Path
$PyScript = Join-Path $WorkspaceRoot "scripts\ecc-agy\archive_todo.py"

if (-not (Test-Path $PyScript)) {
    Write-Error "[ERROR] No se encuentra el script en $PyScript"
    exit 1
}

$ResolvedTodo = Join-Path $WorkspaceRoot $TodoPath
$ResolvedDone = Join-Path $WorkspaceRoot $DoneDir

$ArgsList = @($PyScript, "--todo", $ResolvedTodo, "--done-dir", $ResolvedDone)

if ($Complete) {
    $ArgsList += @("--complete", $Complete)
}
if ($AllCompleted) {
    $ArgsList += "--all-completed"
}
if ($Notes) {
    $ArgsList += @("--notes", $Notes)
}
if ($DryRun) {
    $ArgsList += "--dry-run"
}

python @ArgsList
$pyExit = $LASTEXITCODE

if ($pyExit -eq 0 -and -not $DryRun) {
    $lintScript = Join-Path $ScriptDir "lint-markdown.ps1"
    if (Test-Path $lintScript) {
        pwsh -NoProfile -File $lintScript -Target $ResolvedDone -Fix >$null 2>&1
        pwsh -NoProfile -File $lintScript -Target $ResolvedTodo -Fix >$null 2>&1
    }
}

exit $pyExit
