"""
Script de pruebas automatizado para el compilador
Ejecuta todos los casos de prueba y genera un reporte
"""

import sys
import os

# Importar el módulo main_compiler
from main_compiler import compile_source

# Colores para la salida (compatible con Windows)
try:
    import colorama
    colorama.init()
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
except:
    GREEN = RED = YELLOW = BLUE = RESET = ''

def print_header(text):
    """Imprime un encabezado decorado"""
    print(f"\n{'='*80}")
    print(f"{BLUE}{text}{RESET}")
    print('='*80)

def run_test(test_name, code, should_pass=True):
    """
    Ejecuta un caso de prueba
    Returns: True si el resultado es el esperado, False en caso contrario
    """
    print(f"\n{'─'*80}")
    print(f"📝 Test: {test_name}")
    print(f"Esperado: {'✅ ÉXITO' if should_pass else '❌ ERROR DETECTADO'}")
    print('─'*80)
    
    result = compile_source(code, f"<test: {test_name}>")
    
    # Verificar si el resultado es el esperado
    passed = (result == should_pass)
    
    if passed:
        print(f"\n{GREEN}✅ TEST PASÓ{RESET}")
    else:
        print(f"\n{RED}❌ TEST FALLÓ{RESET}")
        if should_pass:
            print("   Se esperaba éxito pero hubo error")
        else:
            print("   Se esperaba error pero tuvo éxito")
    
    return passed

def main():
    """Ejecuta todos los tests"""
    print_header("🧪 SUITE DE PRUEBAS DEL COMPILADOR")
    
    # Contadores
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    # ========================================
    # PRUEBAS VÁLIDAS
    # ========================================
    print_header("✅ CASOS VÁLIDOS (Deben compilar correctamente)")
    
    valid_tests = [
        ("Declaraciones básicas", """
int x;
float y;
string nombre;
        """),
        
        ("Declaraciones con inicialización", """
int x = 10;
float pi = 3.14;
int resultado = 0;
        """),
        
        ("Asignaciones", """
int x;
x = 5;
int y;
y = x + 10;
        """),
        
        ("Expresiones aritméticas", """
int a = 5;
int b = 10;
int suma = a + b;
int resta = b - a;
int mult = a * b;
        """),
        
        ("Expresiones con paréntesis", """
int resultado;
resultado = (5 + 3) * 2;
        """),
        
        ("If simple", """
int x = 10;
if (x > 5) {
    x = x + 1;
}
        """),
        
        ("If-Else", """
int edad = 18;
if (edad >= 18) {
    print(edad);
} else {
    edad = 0;
}
        """),
        
        ("While loop", """
int contador = 0;
while (contador < 5) {
    print(contador);
    contador = contador + 1;
}
        """),
        
        ("Operadores relacionales", """
int a = 5;
int b = 10;
if (a < b) {
    print(a);
}
if (a != b) {
    print(b);
}
        """),
        
        ("Operadores lógicos", """
int x = 5;
int y = 10;
if (x > 0 && y > 0) {
    print(x);
}
if (x < 0 || y > 0) {
    print(y);
}
        """),
        
        ("Operador unario negación", """
int x = 5;
int y;
y = -x;
        """),
        
        ("Print con múltiples argumentos", """
int x = 5;
int y = 10;
float z = 3.14;
print(x, y, z);
        """),
        
        ("Bloques anidados", """
int x = 1;
{
    int y = 2;
    {
        int z = 3;
        print(x, y, z);
    }
}
        """),
        
        ("Programa completo", """
int x = 10;
float y = 3.14;
int contador = 0;

if (x > 5) {
    while (contador < x) {
        if (contador % 2 == 0) {
            print(contador);
        }
        contador = contador + 1;
    }
}
        """),
    ]
    
    for name, code in valid_tests:
        total_tests += 1
        if run_test(name, code, should_pass=True):
            passed_tests += 1
        else:
            failed_tests += 1
    
    # ========================================
    # PRUEBAS INVÁLIDAS (Errores)
    # ========================================
    print_header("❌ CASOS INVÁLIDOS (Deben detectar errores)")
    
    invalid_tests = [
        ("Variable no declarada", """
int x;
x = 10;
y = 5;
        """),
        
        ("Redeclaración de variable", """
int x;
int x;
        """),
        
        ("Tipos incompatibles", """
int numero;
string texto;
numero = texto;
        """),
        
        ("Falta punto y coma", """
int x
x = 5;
        """),
        
        ("Operador inválido", """
int x = 5;
int y = x @ 10;
        """),
    ]
    
    for name, code in invalid_tests:
        total_tests += 1
        if run_test(name, code, should_pass=False):
            passed_tests += 1
        else:
            failed_tests += 1
    
    # ========================================
    # RESUMEN FINAL
    # ========================================
    print_header("📊 RESUMEN DE RESULTADOS")
    print(f"\n{'─'*80}")
    print(f"Total de pruebas:     {total_tests}")
    print(f"{GREEN}✅ Pruebas pasadas:   {passed_tests}{RESET}")
    print(f"{RED}❌ Pruebas falladas:  {failed_tests}{RESET}")
    print(f"Tasa de éxito:        {(passed_tests/total_tests)*100:.1f}%")
    print('─'*80)
    
    if failed_tests == 0:
        print(f"\n{GREEN}🎉 ¡TODOS LOS TESTS PASARON!{RESET}")
        return 0
    else:
        print(f"\n{YELLOW}⚠️  Algunos tests fallaron. Revisa los resultados arriba.{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
