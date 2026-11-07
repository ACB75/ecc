"""
Tests unitarios para la auditoría estática de SonarQube Quality Gate A (sonar_audit.py).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sonar_audit import (
    calculate_python_cognitive_complexity,
    check_python_parameters,
    check_string_literal_duplicates,
    check_empty_blocks,
)


def test_python_cognitive_complexity():
    # Función simple: complejidad 0 o 1
    simple_code = """
def add(a, b):
    return a + b
"""
    comp_simple = calculate_python_cognitive_complexity(simple_code)
    assert comp_simple <= 1

    # Función compleja con ifs y loops anidados
    complex_code = """
def complex_fn(x, y, z):
    if x > 0:
        for i in range(x):
            if y > i:
                while z > 0:
                    z -= 1
            elif y == 0:
                pass
    else:
        return -1
"""
    comp_complex = calculate_python_cognitive_complexity(complex_code)
    assert comp_complex > 5


def test_check_python_parameters():
    # <= 7 params
    valid_fn = """
def valid_fn(p1, p2, p3, p4):
    return p1
"""
    issues_valid = check_python_parameters("test.py", valid_fn)
    assert len(issues_valid) == 0

    # > 7 params (S107 violation)
    too_many_params = """
def bad_fn(p1, p2, p3, p4, p5, p6, p7, p8, p9):
    return p1
"""
    issues_bad = check_python_parameters("test.py", too_many_params)
    assert len(issues_bad) == 1
    assert "S107" in issues_bad[0].rule_id


def test_check_string_literal_duplicates():
    # String repetido 3 veces (S1192)
    code = """
def msg():
    a = "duplicate string literal here"
    b = "duplicate string literal here"
    c = "duplicate string literal here"
    return a + b + c
"""
    findings = check_string_literal_duplicates("test.py", code)
    assert len(findings) == 1
    assert "S1192" in findings[0].rule_id


def test_check_empty_blocks():
    # Except vacío (S108)
    code_with_empty_block = """
def run():
    try:
        x = 1
    except Exception:
        pass
"""
    findings = check_empty_blocks("test.py", code_with_empty_block)
    assert len(findings) == 1
    assert "S108" in findings[0].rule_id
