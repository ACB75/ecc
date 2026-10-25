#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Gestor modular de ECC-AGY para Antigravity (Windows / Multi-proyecto).
.DESCRIPTION
    Sincroniza módulos, skills o agentes desde C:\Workspace\projects\ecc-agy
    hacia el plugin global ~/.gemini/config/plugins/ecc-agy o hacia un proyecto específico (.agents/).
.PARAMETER Phase
    Fase preconfigurada según el escaneo de C:\Workspace:
      - generic    (Fase 1: 10 Skills y 9 agentes universales de ingeniería)
      - infra      (Fase 2: Docker, K8s, Homelab, Redes, Seguridad, Linux/Debian/Arch)
      - kakebo     (Fase 3: Java 25 / Spring Boot 4, Angular 21 / TypeScript, Postgres)
      - cluster    (Fase 4: Python / FastAPI, Testing, Observabilidad, SQL/Postgres)
      - token-hill (Fase 5: Python CLI, Testing, Benchmarking)
.PARAMETER TargetProject
    Ruta opcional a un proyecto (ej. C:\Workspace\projects\my-app\backend). Si se omite, actualiza el plugin global ecc-agy.
.PARAMETER Clean
    Si se especifica, limpia previamente las carpetas skills/ y agents/ del destino antes de sincronizar.
#>
param(
    [ValidateSet("generic", "infra", "kakebo", "cluster", "token-hill", "status")]
    [string]$Phase = "status",
    [string]$TargetProject = "",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$EccRoot = "C:\Workspace\projects\ecc-agy"
$GlobalPluginDir = Join-Path $HOME ".gemini\config\plugins\ecc-agy"

$PhaseConfig = @{
    "generic" = @{
        Skills = @(
            "tdd-workflow", "search-first", "verification-loop",
            "security-review", "coding-standards", "git-workflow",
            "conventional-commit-review", "architecture-decision-records",
            "error-handling", "docs-governance", "workspace-health-audit",
            "config-cleanup", "sonarqube-quality-gate"
        )
        Agents = @(
            "planner.md", "architect.md", "tdd-guide.md", "code-reviewer.md",
            "security-reviewer.md", "build-error-resolver.md", "silent-failure-hunter.md",
            "refactor-cleaner.md", "doc-updater.md"
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
    Write-Host "=== Estado de ECC-AGY ($GlobalPluginDir) ===" -ForegroundColor Cyan
    if (Test-Path "$GlobalPluginDir\skills") {
        $skills = @(Get-ChildItem "$GlobalPluginDir\skills" -Directory | Select-Object -ExpandProperty Name)
        Write-Host "Skills activas ($($skills.Count)): $($skills -join ', ')" -ForegroundColor Green
    }
    if (Test-Path "$GlobalPluginDir\agents") {
        $agents = @(Get-ChildItem "$GlobalPluginDir\agents" -File | Select-Object -ExpandProperty Name)
        Write-Host "Agentes activos ($($agents.Count)): $($agents -join ', ')" -ForegroundColor Yellow
    }
    exit 0
}

$destRoot = if ($TargetProject) { Join-Path $TargetProject ".agents" } else { $GlobalPluginDir }
if ($Clean) {
    if (Test-Path "$destRoot\skills") { Remove-Item -Path "$destRoot\skills" -Recurse -Force }
    if (Test-Path "$destRoot\agents") { Remove-Item -Path "$destRoot\agents" -Recurse -Force }
}
New-Item -ItemType Directory -Force -Path "$destRoot\skills" | Out-Null
New-Item -ItemType Directory -Force -Path "$destRoot\agents" | Out-Null

if (-not $TargetProject -and (Test-Path "$EccRoot\rules\AGENTS.md")) {
    New-Item -ItemType Directory -Force -Path "$GlobalPluginDir\rules" | Out-Null
    Copy-Item -Path "$EccRoot\rules\AGENTS.md" -Destination "$GlobalPluginDir\rules\AGENTS.md" -Force
    Write-Host "[+] Regla global sincronizada: AGENTS.md -> $GlobalPluginDir\rules\AGENTS.md" -ForegroundColor Cyan
}

$cfg = $PhaseConfig[$Phase]
foreach ($s in $cfg.Skills) {
    $src = Join-Path "$EccRoot\skills" $s
    $dst = Join-Path "$destRoot\skills" $s
    if (Test-Path $src) {
        if (Test-Path $dst) { Remove-Item -Path $dst -Recurse -Force }
        Copy-Item -Path $src -Destination $dst -Recurse -Force
        Write-Host "[+] Skill instalada ($Phase): $s -> $dst" -ForegroundColor Green
    }
}

$agentsList = ($cfg.Agents | ForEach-Object { "'$_'" }) -join ","
$destAgentsEscaped = ($destRoot -replace '\\', '/') + "/agents"
node -e "
const fs = require('fs');
const path = require('path');
const { adaptAntigravityAgent } = require('C:/Workspace/projects/ecc-agy/scripts/lib/install/antigravity-agent');
const agents = [$agentsList];
for (const a of agents) {
  const src = path.join('C:/Workspace/projects/ecc-agy/agents', a);
  const dst = path.join('$destAgentsEscaped', a);
  if (fs.existsSync(src)) {
    const raw = fs.readFileSync(src, 'utf8');
    fs.writeFileSync(dst, adaptAntigravityAgent(raw, a), 'utf8');
    console.log('[+] Agente adaptado ($Phase):', a);
  }
}
"
