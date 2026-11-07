#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Gestor modular de sincronización de ECC para Antigravity (Two-Tier Architecture / ADR-0001).
.DESCRIPTION
    Sincroniza módulos, skills o agentes desde C:\Workspace\projects\ecc
    hacia el plugin global ~/.gemini/config/plugins/ecc-agy (Nivel 1: Transversal)
    o hacia un proyecto específico (.agents/) (Nivel 2: Específico de Dominio).
.PARAMETER Phase
    Fase preconfigurada según la arquitectura en dos niveles:
      - generic    (Nivel 1 Global: ~23 Skills y 11 agentes universales de ingeniería - ~800 tokens)
      - infra      (Nivel 2 Proyecto: Docker, K8s, Homelab, Redes, Seguridad)
      - kakebo     (Nivel 2 Proyecto: Java 25 / Spring Boot 4, Angular 21 / TypeScript, Postgres)
      - cluster    (Nivel 2 Proyecto: Go, Docker, K8s, Latencia, Postgres)
      - token-hill (Nivel 2 Proyecto: Python CLI, Testing, Benchmarking)
      - all        (Catálogo completo optimizado: 320 skills, 76 agentes)
      - status     (Muestra el estado actual del plugin o proyecto destino)
.PARAMETER TargetProject
    Ruta opcional a un proyecto (ej. C:\Workspace\projects\home-lab\app\kakebo). Si se omite, actualiza el plugin global ecc-agy.
.PARAMETER Clean
    Si se especifica, limpia previamente las carpetas skills/ y agents/ del destino antes de sincronizar.
.EXAMPLE
    # Desplegar Tier 1 Global (Universal Engineering - 98% ahorro tokens):
    pwsh -File ecc-agy-sync.ps1 -Phase generic -Clean
    
    # Desplegar Tier 2 a proyecto kakebo:
    pwsh -File ecc-agy-sync.ps1 -Phase kakebo -TargetProject C:\Workspace\projects\home-lab\app\kakebo
#>
param(
    [ValidateSet("generic", "infra", "kakebo", "cluster", "token-hill", "all", "status")]
    [string]$Phase = "status",
    [string]$TargetProject = "",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$EccRoot = (Resolve-Path "$ScriptDir").Path
$GlobalPluginDir = Join-Path $HOME ".gemini\config\plugins\ecc-agy"

$SkillsSource = if (Test-Path (Join-Path $EccRoot "skills")) { Join-Path $EccRoot "skills" } else { Join-Path $EccRoot "ecc-agy\skills" }
$AgentsSource = if (Test-Path (Join-Path $EccRoot "agents")) { Join-Path $EccRoot "agents" } else { Join-Path $EccRoot "ecc-agy\agents" }

$PhaseConfig = @{
    "generic" = @{
        Skills = @(
            "tdd-workflow", "search-first", "verification-loop",
            "security-review", "coding-standards", "git-workflow",
            "conventional-commit-review", "architecture-decision-records",
            "error-handling", "docs-governance", "workspace-health-audit",
            "config-gc", "sonarqube-quality-gate", "sync-microservice-sdk",
            "todo-lifecycle", "sre-reliability", "agent-sort",
            "agent-self-evaluation", "strategic-compact",
            "context-budget", "safety-guard"
        )
        Agents = @(
            "planner.md", "architect.md", "tdd-guide.md", "code-reviewer.md",
            "security-reviewer.md", "build-error-resolver.md", "silent-failure-hunter.md",
            "refactor-cleaner.md", "doc-updater.md", "todo-archiver.md",
            "sync-aligner.md"
        )
    }
    "infra" = @{
        Skills = @(
            "docker-patterns", "deployment-patterns", "kubernetes-patterns",
            "homelab-network-readiness", "homelab-network-setup", "homelab-pihole-dns",
            "homelab-vlan-segmentation", "homelab-wireguard-vpn", "network-config-validation",
            "network-interface-health", "netmiko-ssh-automation", "security-scan", "safety-guard"
        )
        Agents = @(
            "homelab-architect.md", "network-architect.md", "network-config-reviewer.md",
            "network-troubleshooter.md"
        )
    }
    "kakebo" = @{
        Skills = @(
            "springboot-patterns", "springboot-security", "springboot-tdd",
            "springboot-verification", "java-coding-standards", "angular-developer",
            "e2e-testing", "postgres-patterns", "database-migrations", "api-design",
            "sonarqube-quality-gate"
        )
        Agents = @(
            "java-reviewer.md", "java-build-resolver.md", "typescript-reviewer.md",
            "database-reviewer.md", "e2e-runner.md"
        )
    }
    "cluster" = @{
        Skills = @(
            "golang-patterns", "golang-testing", "docker-patterns",
            "kubernetes-patterns", "postgres-patterns", "latency-critical-systems",
            "data-throughput-accelerator", "benchmark-optimization-loop",
            "sonarqube-quality-gate"
        )
        Agents = @(
            "go-reviewer.md", "go-build-resolver.md", "performance-optimizer.md",
            "database-reviewer.md"
        )
    }
    "token-hill" = @{
        Skills = @(
            "python-patterns", "python-testing", "benchmark-optimization-loop",
            "sonarqube-quality-gate"
        )
        Agents = @(
            "python-reviewer.md", "performance-optimizer.md"
        )
    }
}

if ($Phase -eq "status") {
    $targetInfo = if ($TargetProject) { "$TargetProject\.agents" } else { $GlobalPluginDir }
    Write-Host "=== Estado de ECC-AGY ($targetInfo) ===" -ForegroundColor Cyan
    if (Test-Path "$targetInfo\skills") {
        $skills = @(Get-ChildItem "$targetInfo\skills" -Directory | Select-Object -ExpandProperty Name)
        Write-Host "Skills activas ($($skills.Count)): $($skills -join ', ')" -ForegroundColor Green
    } else {
        Write-Host "Skills activas (0)" -ForegroundColor Gray
    }
    if (Test-Path "$targetInfo\agents") {
        $agents = @(Get-ChildItem "$targetInfo\agents" -File -Filter "*.md" | Select-Object -ExpandProperty Name)
        Write-Host "Agentes activos ($($agents.Count)): $($agents -join ', ')" -ForegroundColor Yellow
    } else {
        Write-Host "Agentes activos (0)" -ForegroundColor Gray
    }
    exit 0
}

$destRoot = if ($TargetProject) { Join-Path $TargetProject ".agents" } else { $GlobalPluginDir }
if ($Clean) {
    Write-Host "[+] Limpiando directorio destino: $destRoot" -ForegroundColor Cyan
    if (Test-Path "$destRoot\skills") { Remove-Item -Path "$destRoot\skills" -Recurse -Force }
    if (Test-Path "$destRoot\agents") { Remove-Item -Path "$destRoot\agents" -Recurse -Force }
}
New-Item -ItemType Directory -Force -Path "$destRoot\skills" | Out-Null
New-Item -ItemType Directory -Force -Path "$destRoot\agents" | Out-Null

# Sincronizar reglas si es destino global
if (-not $TargetProject) {
    New-Item -ItemType Directory -Force -Path "$GlobalPluginDir\rules" | Out-Null
    $ruleSrc = Join-Path $EccRoot "rules\AGENTS.md"
    if (Test-Path $ruleSrc) {
        Copy-Item -Path $ruleSrc -Destination "$GlobalPluginDir\rules\AGENTS.md" -Force
        Write-Host "[+] Regla global sincronizada: AGENTS.md -> $GlobalPluginDir\rules\AGENTS.md" -ForegroundColor Cyan
    }
    $pluginJsonSrc = Join-Path $EccRoot "plugin.json"
    if (-not (Test-Path $pluginJsonSrc)) {
        $pluginJsonSrc = Join-Path $EccRoot "ecc-agy\plugin.json"
    }
    if (Test-Path $pluginJsonSrc) {
        Copy-Item -Path $pluginJsonSrc -Destination "$GlobalPluginDir\plugin.json" -Force
    }
}

if ($Phase -eq "all") {
    Write-Host "[+] Sincronizando catálogo completo optimizado (320 skills, 76 agentes)..." -ForegroundColor Cyan
    Copy-Item -Path (Join-Path $SkillsSource "*") -Destination (Join-Path $destRoot "skills") -Recurse -Force
    Copy-Item -Path (Join-Path $AgentsSource "*.md") -Destination (Join-Path $destRoot "agents") -Force
    Write-Host "[OK] Catálogo completo optimizado sincronizado en $destRoot." -ForegroundColor Green
    exit 0
}

$cfg = $PhaseConfig[$Phase]
foreach ($s in $cfg.Skills) {
    $src = Join-Path $SkillsSource $s
    $dst = Join-Path "$destRoot\skills" $s
    if (Test-Path $src) {
        if (Test-Path $dst) { Remove-Item -Path $dst -Recurse -Force }
        Copy-Item -Path $src -Destination $dst -Recurse -Force
        Write-Host "[+] Skill instalada ($Phase): $s" -ForegroundColor Green
    }
}

$adaptScript = Join-Path $EccRoot "scripts\lib\install\antigravity-agent.js"
$adaptScriptEscaped = ($adaptScript -replace '\\', '/')
$destAgentsEscaped = ($destRoot -replace '\\', '/') + "/agents"
$agentsSrcEscaped = ($AgentsSource -replace '\\', '/')

$agentsList = ($cfg.Agents | ForEach-Object { "'$_'" }) -join ","
$nodeHasYaml = $false
try {
    $null = node -e "require('js-yaml')" 2>&1
    if ($LASTEXITCODE -eq 0) { $nodeHasYaml = $true }
} catch {
    $nodeHasYaml = $false
}

if ($nodeHasYaml -and (Test-Path $adaptScript)) {
    node -e "
    const fs = require('fs');
    const path = require('path');
    const { adaptAntigravityAgent } = require('$adaptScriptEscaped');
    const agents = [$agentsList];
    for (const a of agents) {
      const src = path.join('$agentsSrcEscaped', a);
      const dst = path.join('$destAgentsEscaped', a);
      if (fs.existsSync(src)) {
        const raw = fs.readFileSync(src, 'utf8');
        fs.writeFileSync(dst, adaptAntigravityAgent(raw, a), 'utf8');
        console.log('[+] Agente adaptado ($Phase):', a);
      }
    }
    "
} else {
    foreach ($a in $cfg.Agents) {
        $src = Join-Path $AgentsSource $a
        $dst = Join-Path "$destRoot\agents" $a
        if (Test-Path $src) {
            Copy-Item -Path $src -Destination $dst -Force
            Write-Host "[+] Agente instalado ($Phase): $a" -ForegroundColor Green
        }
    }
}

Write-Host "[OK] Sincronización finalizada para fase '$Phase' en $destRoot." -ForegroundColor Green
