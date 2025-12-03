"""
COMPILADOR COMPLETO
Integra las tres fases: Léxico, Sintáctico y Semántico

Para ejecutar:
  python main.py <archivo.txt>
  python main.py  (modo interactivo)
"""

import sys
from lexer_simple import Lexer, TokenType
from parser_rd import Parser
from semantic_analyzer import SemanticAnalyzer

def compile_file(filename: str):
    """Compila un archivo de código fuente"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{filename}'")
        return False
    except Exception as e:
        print(f"❌ Error al leer el archivo: {str(e)}")
        return False
    
    return compile_source(source_code, filename)

def compile_source(source_code: str, source_name: str = "<input>"):
    """Compila código fuente desde un string"""
    
    print("=" * 80)
    print(f"COMPILADOR - {source_name}")
    print("=" * 80)
    print("\n📄 CÓDIGO FUENTE:")
    print("-" * 80)
    print(source_code)
    print("-" * 80)
    
    # ========================================
    # FASE 1: ANÁLISIS LÉXICO
    # ========================================
    print("\n" + "=" * 80)
    print("-- FASE 1: ANÁLISIS LÉXICO")
    print("=" * 80)
    
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    # Verificar errores léxicos
    lex_errors = [t for t in tokens if t.type == TokenType.ERROR]
    
    if lex_errors:
        print(f"\n❌ Se encontraron {len(lex_errors)} errores léxicos:")
        for error in lex_errors:
            print(f"  Línea {error.line}, Columna {error.column}: Caracter no reconocido '{error.value}'")
        return False
    
    print(f"✅ Análisis léxico exitoso: {len(tokens)-1} tokens generados")
    
    # Mostrar tokens si hay pocos
    if len(tokens) <= 50:
        print("\nTokens generados:")
        for i, token in enumerate(tokens[:20]):  # Mostrar solo los primeros 20
            print(f"  {i+1:3}. {token.type.name:12} = '{token.value}'")
        if len(tokens) > 20:
            print(f"  ... y {len(tokens)-20} tokens más")
    
    # ========================================
    # FASE 2: ANÁLISIS SINTÁCTICO
    # ========================================
    print("\n" + "=" * 80)
    print("-- FASE 2: ANÁLISIS SINTÁCTICO")
    print("=" * 80)
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    if not ast:
        print(f"\n❌ Análisis sintáctico falló con {len(parser.errors)} errores")
        print("\nErrores encontrados:")
        for error in parser.errors:
            print(f"  • {error}")
        return False
    
    print(f"✅ Análisis sintáctico exitoso")
    print(f"Número de sentencias: {len(ast.statements)}")
    
    # ========================================
    # FASE 3: ANÁLISIS SEMÁNTICO
    # ========================================
    print("\n" + "=" * 80)
    print("-- FASE 3: ANÁLISIS SEMÁNTICO")
    print("=" * 80)
    
    semantic = SemanticAnalyzer()
    success = semantic.analyze(ast)
    
    if not success:
        print(f"\n❌ Análisis semántico falló con {len(semantic.errors)} errores")
        return False
    
    # ========================================
    # RESUMEN FINAL
    # ========================================
    print("\n" + "=" * 80)
    print("✅ COMPILACIÓN EXITOSA")
    print("=" * 80)
    print(f"Fuente: {source_name}")
    print(f"Tokens: {len(tokens)-1}")
    print(f"Sentencias: {len(ast.statements)}")
    print(f"Variables declaradas: {len(semantic.symbol_table.get_all_symbols())}")
    print(f"Advertencias: {len(semantic.warnings)}")
    
    if semantic.warnings:
        print("\nAdvertencias:")
        for warning in semantic.warnings:
            print(f"  ⚠️  {warning}")
    
    print("\n El programa es sintáctica y semánticamente correcto")
    print("=" * 80)
    
    return True

def interactive_mode():
    """Modo interactivo: permite ingresar código línea por línea"""
    print("=" * 80)
    print("MODO INTERACTIVO")
    print("=" * 80)
    print("Ingresa tu código (termina con una línea vacía o EOF):")
    print("Ejemplo: int x; x = 5; print(x);")
    print("-" * 80)
    
    lines = []
    try:
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
    except EOFError:
        pass
    
    if not lines:
        print("❌ No se ingresó código")
        return
    
    source_code = "\n".join(lines)
    compile_source(source_code, "<interactive>")

def run_tests():
    """Ejecuta casos de prueba predefinidos"""
    print("=" * 80)
    print("EJECUTANDO CASOS DE PRUEBA")
    print("=" * 80)
    
    test_cases = [
        ("Programa simple", """
int x;
x = 5;
print(x);
        """),
        
        ("Declaraciones e inicialización", """
int x = 10;
float y = 3.14;
string nombre;
        """),
        
        ("Condicional if-else", """
int edad = 18;
if (edad >= 18) {
    print(edad);
} else {
    print(0);
}
        """),
        
        ("Bucle while", """
int contador = 0;
while (contador < 5) {
    print(contador);
    contador = contador + 1;
}
        """),
        
        ("Expresiones complejas", """
int a = 5;
int b = 10;
int c;
c = (a + b) * 2 - a / 2;
print(c);
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
        
        ("ERROR: Variable no declarada", """
int x;
y = 10;
        """),
        
        ("ERROR: Redeclaración", """
int x;
int x;
        """),
        
        ("ERROR: Tipos incompatibles", """
int numero;
string texto;
numero = texto;
        """),
    ]
    
    passed = 0
    failed = 0
    
    for i, (name, code) in enumerate(test_cases, 1):
        print(f"\n{'#' * 80}")
        print(f"PRUEBA {i}: {name}")
        print('#' * 80)
        
        should_fail = "ERROR" in name
        result = compile_source(code, f"test_{i}")
        
        if should_fail:
            if not result:
                print(f"\n✅ Prueba {i} PASÓ (error detectado correctamente)")
                passed += 1
            else:
                print(f"\n❌ Prueba {i} FALLÓ (debería haber detectado error)")
                failed += 1
        else:
            if result:
                print(f"\n✅ Prueba {i} PASÓ")
                passed += 1
            else:
                print(f"\n❌ Prueba {i} FALLÓ")
                failed += 1
    
    print("\n" + "=" * 80)
    print("RESUMEN DE PRUEBAS")
    print("=" * 80)
    print(f"Total: {len(test_cases)}")
    print(f"Pasadas: {passed}")
    print(f"Falladas: {failed}")
    print(f"Tasa de éxito: {passed/len(test_cases)*100:.1f}%")
    print("=" * 80)

def print_help():
    """Muestra ayuda de uso"""
    print("""
COMPILADOR - Manual de Uso

Uso:
  python main.py [opciones] [archivo]

Opciones:
  <archivo>       Compila el archivo especificado
  -i, --interactive    Modo interactivo
  -t, --test      Ejecuta casos de prueba
  -h, --help      Muestra esta ayuda

Ejemplos:
  python main.py programa.txt
  python main.py -i
  python main.py --test

Gramática soportada:
  - Tipos: int, float, string
  - Sentencias: if-else, while, print
  - Operadores: +, -, *, /, %, ==, !=, <, <=, >, >=, &&, ||, !
  - Bloques: { ... }
  
Ejemplo de código válido:
  int x = 10;
  float y = 3.14;
  
  if (x > 5) {
      print(x);
  }
  
  while (x < 20) {
      x = x + 1;
  }
    """)

def main():
    """Función principal"""
    if len(sys.argv) == 1:
        # Sin argumentos: modo interactivo
        interactive_mode()
    
    elif sys.argv[1] in ['-h', '--help']:
        print_help()
    
    elif sys.argv[1] in ['-i', '--interactive']:
        interactive_mode()
    
    elif sys.argv[1] in ['-t', '--test']:
        run_tests()
    
    else:
        # Compilar archivo
        filename = sys.argv[1]
        compile_file(filename)

if __name__ == "__main__":
    main()