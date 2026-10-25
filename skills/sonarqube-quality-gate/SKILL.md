---
name: sonarqube-quality-gate
description: Enforce SonarQube Quality Gate (S3776, S1192, S107, S112, S1452) via scripts/bin/ecc-agy/sonar-audit.ps1. Not for style formatting.
metadata:
  origin: ECC-AGY
---

# SonarQube Quality Gate & Clean as You Code

Enforces SonarQube static analysis rules and Quality Gate `A` ratings across Java 25 / Spring Boot 4, Angular 21 / TypeScript, Go 1.24 LTS, and Python 3.

## When to Use

- Auditing or refactoring code to pass SonarQube / SonarCloud Quality Gates (`Clean as You Code`).
- Resolving Cognitive Complexity (`S3776`), duplicated string literals (`S1192`), parameter count (`S107`), or Java/Go/TS/Python code smells before committing.
- Running pre-commit static verification across the workspace.

## Quality Gate Thresholds (`A` Rating Baseline)

| Metric | Threshold |
| :--- | :--- |
| **Reliability / Bugs** | `0` new bugs (Rating `A`) |
| **Security / Vulnerabilities** | `0` vulnerabilities & `100%` hotspots reviewed (Rating `A`) |
| **Maintainability / Code Smells** | Technical debt ratio $\le 5\%$ (Rating `A`) |
| **Coverage on New/Overall Code** | $\ge 80\%$ (JaCoCo XML, Go `coverage.out`, LCOV, Cobertura) |
| **Duplicated Lines Density** | $\le 3\%$ |

## Non-Negotiable Multi-Language Rules

1. **`S3776` (Cognitive Complexity $\le 15$)**:
   - Extract focused private/package helper functions, use guard clauses (`return` / `continue` early), and flatten nested `if`/`for`/`try` blocks so every function/method scores $\le 15$.
2. **`S1192` (No Duplicated String Literals $\ge 3$ times)**:
   - Extract repeated string literals ($\ge 7$ chars, repeated $\ge 3$ times in a production file) into named constants (`private static final String`, `const`, `private static readonly`, or `UPPER_SNAKE_CASE`).
3. **`S107` (Max 7 Parameters)**:
   - Group related parameters into an immutable `record`, `@dataclass(frozen=True)`, Go `struct`, or TypeScript `interface` when parameter count exceeds 7.
4. **`S108` & `S2486` (No Empty Blocks or Swallowed Exceptions)**:
   - Never leave `catch`, `else`, or nested blocks empty; handle or rethrow with context.
5. **Java 25 Specific Rules (`kakebo-backend`)**:
   - **`java:S112`**: Never throw raw `RuntimeException`, `Exception`, `Throwable`, or `Error`; throw specific domain or standard exceptions (`IllegalArgumentException`, `IllegalStateException`).
   - **`java:S1452`**: Never return wildcard generic types (`ResponseEntity<?>`); return `ResponseEntity<SpecificDto>` or `ResponseEntity<Object>`.
   - **`java:S2696`**: Never assign `static` fields directly inside an instance method (`@PostConstruct`); delegate to a `private static` setter method.
   - **`java:S2142`**: Always call `Thread.currentThread().interrupt()` when catching `InterruptedException`.
   - **`java:S1068` & `java:S1128`**: Remove unused `private` fields and unused `import` statements.
   - **`java:S1066`**: Merge collapsible nested `if` statements using `&&`.

## Deterministic Audit Workflow

### 1. Run Multi-Language Static Audit (Windows 11 `pwsh`)
```powershell
pwsh -NoProfile -File scripts/bin/ecc-agy/sonar-audit.ps1
```

### 2. Run Multi-Language Static Audit (Debian 12 / WSL2 `bash`)
```bash
scripts/bin/ecc-agy/sonar-audit.sh
```

### 3. Fix & Re-Verify
- Refactor every reported `[CRITICAL]`, `[MAJOR]`, and `[MINOR]` finding at the exact `file:line`.
- Re-run `sonar-audit.ps1` and the project's unit test suite to confirm `0` issues and `100%` test pass rate.
