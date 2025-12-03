# REPORTE TÉCNICO DEL COMPILADOR

**Proyecto:** Compilador de Lenguaje de Programación Simplificado  
**Autor:** Equipo de Desarrollo  
**Fecha:** Diciembre 2025  
**Versión:** 1.0

---

## TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Descripción del Diseño del Lenguaje](#descripción-del-diseño-del-lenguaje)
3. [Arquitectura del Compilador](#arquitectura-del-compilador)
4. [Mecanismos de Manejo de Errores](#mecanismos-de-manejo-de-errores)
5. [Conclusiones](#conclusiones)
6. [Áreas de Mejora](#áreas-de-mejora)

---

## RESUMEN EJECUTIVO

Este documento presenta el diseño e implementación de un compilador completo para un lenguaje de programación imperativo simplificado. El compilador está desarrollado en Python y consta de tres fases principales: análisis léxico, análisis sintáctico y análisis semántico. El proyecto demuestra los principios fundamentales de la teoría de compiladores, incluyendo el procesamiento de tokens, análisis sintáctico mediante descenso recursivo (LL(1)), construcción de árboles sintácticos abstractos (AST), y validación semántica con tabla de símbolos.

---

## DESCRIPCIÓN DEL DISEÑO DEL LENGUAJE

### 1.1 Características Generales

El lenguaje implementado es de tipo **imperativo**, **estáticamente tipado** y con **sintaxis inspirada en C/Java**. Está diseñado para ser simple pero suficientemente expresivo para demostrar conceptos fundamentales de compiladores.

### 1.2 Sistema de Tipos

El lenguaje soporta tres tipos de datos primitivos:

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `int` | Números enteros | `42`, `-10`, `0` |
| `float` | Números de punto flotante | `3.14`, `-0.5`, `2.0` |
| `string` | Cadenas de texto (declarativo) | `"hola"` |

**Características del sistema de tipos:**
- **Tipado estático:** Las variables deben declararse con un tipo explícito
- **Conversión implícita:** Se permite conversión automática de `int` a `float`
- **Inferencia de tipos:** El compilador infiere tipos de expresiones basándose en operandos

### 1.3 Palabras Reservadas

```
int, float, string, if, else, while, print
```

### 1.4 Operadores

#### Operadores Aritméticos (precedencia descendente)
- Multiplicación, División, Módulo: `*`, `/`, `%`
- Suma, Resta: `+`, `-`
- Negación unaria: `-`

#### Operadores Relacionales
```
==  (igual a)
!=  (diferente de)
<   (menor que)
<=  (menor o igual)
>   (mayor que)
>=  (mayor o igual)
```

#### Operadores Lógicos
- OR: `||`
- AND: `&&`
- NOT: `!`

**Precedencia de operadores (mayor a menor):**
1. Operadores unarios: `!`, `-`
2. Multiplicativos: `*`, `/`, `%`
3. Aditivos: `+`, `-`
4. Relacionales: `==`, `!=`, `<`, `<=`, `>`, `>=`
5. AND lógico: `&&`
6. OR lógico: `||`

### 1.5 Estructuras de Control

#### Declaración de Variables
```c
int x;                 // Declaración simple
float pi = 3.14;       // Declaración con inicialización
```

#### Asignación
```c
x = 10;
y = x + 5;
```

#### Condicional if-else
```c
if (condicion) {
    // código
} else {
    // código alternativo
}
```

#### Bucle while
```c
while (condicion) {
    // código repetitivo
}
```

#### Impresión
```c
print(x);              // Un argumento
print(x, y, z);        // Múltiples argumentos
```

#### Bloques
```c
{
    // Nuevo ámbito
    int variable_local;
}
```

### 1.6 Gramática Formal

La gramática es **LL(1)** (analizable mediante descenso recursivo):

```
Program     → StmtList
StmtList    → Stmt StmtList | ε
Stmt        → Decl ';' | Assign ';' | IfStmt | WhileStmt | PrintStmt ';' | Block

Decl        → Type id DeclInit
DeclInit    → '=' Expr | ε
Type        → int | float | string

Assign      → id '=' Expr

IfStmt      → if '(' Expr ')' Stmt ElseOpt
ElseOpt     → else Stmt | ε

WhileStmt   → while '(' Expr ')' Stmt

PrintStmt   → print '(' ArgListOpt ')'
ArgListOpt  → ArgList | ε
ArgList     → Expr ArgList'
ArgList'    → ',' Expr ArgList' | ε

Block       → '{' StmtList '}'

Expr        → OrExpr
OrExpr      → AndExpr OrTail
OrTail      → '||' AndExpr OrTail | ε
AndExpr     → RelExpr AndTail
AndTail     → '&&' RelExpr AndTail | ε
RelExpr     → AddExpr RelTail
RelTail     → RelOp AddExpr | ε
RelOp       → '==' | '!=' | '<' | '<=' | '>' | '>='
AddExpr     → MulExpr AddTail
AddTail     → ('+' | '-') MulExpr AddTail | ε
MulExpr     → Unary MulTail
MulTail     → ('*' | '/' | '%') Unary MulTail | ε
Unary       → '!' Unary | '-' Unary | Primary
Primary     → id | NUM | '(' Expr ')'
```

### 1.7 Comentarios

El lenguaje soporta dos tipos de comentarios:

```c
// Comentario de línea

/* Comentario
   de múltiples
   líneas */
```

---

## ARQUITECTURA DEL COMPILADOR

### 2.1 Visión General

El compilador sigue el **modelo de tres fases clásico**, donde cada fase procesa la salida de la anterior:

```
Código Fuente → [Léxico] → Tokens → [Sintáctico] → AST → [Semántico] → AST Validado
```

### 2.2 Componentes Principales

#### Módulo 1: Analizador Léxico (`lexer_simple.py`)

**Responsabilidades:**
- Convertir el código fuente (stream de caracteres) en tokens
- Identificar palabras reservadas, identificadores, literales y operadores
- Eliminar espacios en blanco y comentarios
- Detectar caracteres inválidos

**Clases Principales:**
- `TokenType`: Enumeración de todos los tipos de tokens
- `Token`: Dataclass que representa un token con tipo, valor y posición
- `Lexer`: Implementa el análisis léxico mediante autómata finito

**Algoritmo:**
```python
while not EOF:
    skip_whitespace()
    skip_comments()
    
    if current_char is digit:
        read_number()
    elif current_char is letter or '_':
        read_identifier()
    else:
        read_operator()
```

**Manejo de Números:**
- Reconoce enteros: `42`, `123`
- Reconoce decimales: `3.14`, `0.5`
- Utiliza lookahead para distinguir `.` como punto decimal vs. operador

**Manejo de Identificadores:**
- Primer carácter: letra o `_`
- Siguientes: letras, dígitos o `_`
- Verifica en tabla de palabras reservadas

#### Módulo 2: Analizador Sintáctico (`parser_rd.py`)

**Responsabilidades:**
- Verificar que la secuencia de tokens cumple con la gramática
- Construir el Árbol Sintáctico Abstracto (AST)
- Detectar errores sintácticos
- Implementar recuperación de errores

**Técnica:** Parser de **Descenso Recursivo** (Recursive Descent Parser)
- Cada no-terminal de la gramática → método en la clase
- Método LL(1): decisiones basadas en 1 token de lookahead

**Clases del AST:**

```python
- ASTNode (clase base)
  ├── Program
  ├── DeclStmt (declaración)
  ├── AssignStmt (asignación)
  ├── IfStmt (condicional)
  ├── WhileStmt (bucle)
  ├── PrintStmt (impresión)
  ├── Block (bloque)
  ├── BinaryOp (operación binaria)
  ├── UnaryOp (operación unaria)
  ├── Identifier (variable)
  └── Literal (constante)
```

**Ejemplo de método de parsing:**
```python
def parse_if_stmt(self):
    consume('if')
    consume('(')
    condition = parse_expr()
    consume(')')
    then_stmt = parse_stmt()
    if match('else'):
        else_stmt = parse_stmt()
    return IfStmt(condition, then_stmt, else_stmt)
```

**Manejo de Precedencia:**
- Implementado mediante niveles de recursión
- Cada nivel de precedencia → método separado
- Mayor precedencia → llamadas más profundas

#### Módulo 3: Analizador Semántico (`semantic_analyzer.py`)

**Responsabilidades:**
- Construir y mantener la tabla de símbolos
- Validar declaraciones antes de uso
- Verificar compatibilidad de tipos
- Detectar redeclaraciones
- Inferir tipos de expresiones
- Gestionar ámbitos (scopes)

**Componentes:**

1. **Tabla de Símbolos (`SymbolTable`)**
   - Stack de ámbitos (scopes)
   - Soporte para bloques anidados
   - Búsqueda desde el ámbito más interno al más externo

2. **Símbolos (`Symbol`)**
   ```python
   Symbol:
       - name: str
       - type: str (int, float, string, bool)
       - line, column: int
       - initialized: bool
   ```

3. **Analizador (`SemanticAnalyzer`)**
   - Visita recursiva del AST (patrón Visitor)
   - Validaciones en cada nodo
   - Acumulación de errores y advertencias

**Validaciones Implementadas:**

| ID | Validación | Descripción |
|----|------------|-------------|
| V1 | Declaración antes de uso | Toda variable debe declararse antes de usarse |
| V2 | No redeclaración | No se puede redeclarar una variable en el mismo ámbito |
| V3 | Compatibilidad de tipos | Las asignaciones deben respetar tipos |
| V4 | Tipos en operaciones | Operadores requieren tipos compatibles |
| V5 | Condiciones booleanas | Condiciones de if/while deben ser booleanas |
| V6 | Variables inicializadas | Advertencia si se usa variable no inicializada |

**Inferencia de Tipos:**
```python
- Literal numérico:
    '.' en valor → float
    sin '.' → int
    
- Operación aritmética:
    int op int → int
    int op float → float
    float op float → float
    
- Operación relacional:
    cualquier op cualquier → bool
    
- Operación lógica:
    bool op bool → bool
```

#### Módulo 4: Programa Principal (`main_compiler.py`)

**Responsabilidades:**
- Integrar las tres fases
- Manejar entrada/salida de archivos
- Proporcionar interfaz de línea de comandos
- Generar reportes de compilación

**Modos de Operación:**
1. **Modo archivo:** `python main_compiler.py programa.txt`
2. **Modo interactivo:** `python main_compiler.py -i`
3. **Modo pruebas:** `python main_compiler.py -t`

### 2.3 Flujo de Compilación

```
┌─────────────────────────────────────────────────────────┐
│                    CÓDIGO FUENTE                        │
│                  (archivo .txt)                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────────┐
    │     FASE 1: ANÁLISIS LÉXICO            │
    │  ┌──────────────────────────────────┐  │
    │  │  Lexer.tokenize()                │  │
    │  │  - Eliminar whitespace           │  │
    │  │  - Eliminar comentarios          │  │
    │  │  - Identificar tokens            │  │
    │  │  - Detectar errores léxicos      │  │
    │  └──────────────────────────────────┘  │
    └────────────────┬───────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Lista Tokens │
              └──────┬───────┘
                     │
                     ▼
    ┌────────────────────────────────────────┐
    │   FASE 2: ANÁLISIS SINTÁCTICO          │
    │  ┌──────────────────────────────────┐  │
    │  │  Parser.parse()                  │  │
    │  │  - Verificar gramática           │  │
    │  │  - Construir AST                 │  │
    │  │  - Detectar errores sintácticos  │  │
    │  │  - Recuperación de errores       │  │
    │  └──────────────────────────────────┘  │
    └────────────────┬───────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │     AST      │
              └──────┬───────┘
                     │
                     ▼
    ┌────────────────────────────────────────┐
    │   FASE 3: ANÁLISIS SEMÁNTICO           │
    │  ┌──────────────────────────────────┐  │
    │  │  SemanticAnalyzer.analyze()      │  │
    │  │  - Construir tabla de símbolos   │  │
    │  │  - Verificar declaraciones       │  │
    │  │  - Validar tipos                 │  │
    │  │  - Gestionar ámbitos             │  │
    │  │  - Detectar errores semánticos   │  │
    │  └──────────────────────────────────┘  │
    └────────────────┬───────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ AST Validado │
              │ + Tabla Símb │
              └──────────────┘
```

### 2.4 Estructuras de Datos Principales

#### Token
```python
@dataclass
class Token:
    type: TokenType      # Tipo de token (ENUM)
    value: str          # Valor literal
    line: int           # Línea en código fuente
    column: int         # Columna en código fuente
```

#### AST Node (ejemplo: IfStmt)
```python
@dataclass
class IfStmt(ASTNode):
    condition: ASTNode   # Expresión booleana
    then_stmt: ASTNode   # Rama verdadera
    else_stmt: ASTNode   # Rama falsa (opcional)
    line: int
    column: int
```

#### Symbol
```python
@dataclass
class Symbol:
    name: str           # Nombre de la variable
    type: str          # Tipo (int, float, string)
    line: int          # Ubicación de declaración
    column: int
    initialized: bool  # ¿Tiene valor inicial?
```

---

## MECANISMOS DE MANEJO DE ERRORES

### 3.1 Filosofía General

El compilador implementa un enfoque de **"reportar múltiples errores"** en lugar de detenerse en el primer error. Esto mejora la productividad del programador al identificar múltiples problemas en una sola compilación.

### 3.2 Errores Léxicos

**Tipos de errores detectados:**
1. Caracteres no reconocidos
2. Secuencias inválidas

**Estrategia:**
```python
def read_operator(self):
    if char not in valid_operators:
        return Token(TokenType.ERROR, char, line, column)
```

**Ejemplo:**
```
Código:  int x = 5 @ 3;
Error:   Línea 1, Columna 11: Caracter no reconocido '@'
```

**Recuperación:**
- Se registra el error
- Se continúa con el siguiente carácter
- Se acumulan todos los errores léxicos
- La compilación se detiene después de la fase léxica si hay errores

### 3.3 Errores Sintácticos

**Tipos de errores detectados:**
1. Token inesperado
2. Falta de delimitadores (`;`, `)`, `}`)
3. Estructura sintáctica inválida
4. EOF prematuro

**Estrategia de Recuperación: Modo Pánico**

El parser implementa **sincronización en puntos seguros:**

```python
def synchronize(self):
    """Avanza hasta encontrar un punto de sincronización"""
    sync_tokens = {SEMICOLON, RBRACE, INT, FLOAT, 
                   STRING, IF, WHILE, PRINT, EOF}
    
    while current_token not in sync_tokens:
        advance()
    
    if current_token == SEMICOLON:
        advance()  # Consumir el punto y coma
```

**Puntos de sincronización:**
- `;` (fin de sentencia)
- `}` (fin de bloque)
- Inicio de nueva sentencia (`int`, `if`, `while`, etc.)

**Ejemplo:**
```
Código:  int x
         x = 5;
         
Error:   Línea 1: Se esperaba ';', se encontró 'x'
Acción:  Se sincroniza en el siguiente ';'
         Continúa compilación desde 'x = 5;'
```

### 3.4 Errores Semánticos

**Categorías de errores:**

| Error | Descripción | Ejemplo |
|-------|-------------|---------|
| **E1: Variable no declarada** | Uso de variable sin declaración previa | `x = 5;` sin `int x;` |
| **E2: Redeclaración** | Declarar la misma variable dos veces en un ámbito | `int x; int x;` |
| **E3: Tipo incompatible** | Asignación de tipo incorrecto | `int x; string s; x = s;` |
| **E4: Operación inválida** | Operador con tipos incompatibles | `int x; string s; x = x + s;` |
| **E5: Condición no booleana** | Condición if/while no booleana | `if ("texto") {...}` |

**Estrategia:**
- Todos los errores semánticos se reportan
- Se continúa el análisis para encontrar más errores
- Uso de tipo `unknown` para errores de tipo
- La compilación falla si hay al menos un error semántico

**Ejemplo completo:**
```
Código:
    int x;
    y = 10;
    int x;
    
Errores:
    ❌ Error semántico [2:1]: La variable 'y' no ha sido declarada
    ❌ Error semántico [3:5]: La variable 'x' ya fue declarada en este ámbito
```

### 3.5 Advertencias (Warnings)

El compilador también genera **advertencias** para situaciones sospechosas pero no erróneas:

**W1: Variable posiblemente no inicializada**
```python
int x;
print(x);  // ⚠️ Advertencia: 'x' podría no estar inicializada
```

**Tratamiento:**
- Las advertencias no detienen la compilación
- Se muestran al final del proceso
- Ayudan a identificar posibles bugs

### 3.6 Formato de Mensajes de Error

**Estructura estándar:**
```
[Tipo] [Ubicación]: [Mensaje descriptivo]
```

**Ejemplos:**
```
Error léxico [5:12]: Caracter no reconocido '#'
Error sintáctico [8:1]: Se esperaba ';', se encontró 'if'
Error semántico [10:5]: La variable 'contador' no ha sido declarada
Advertencia [15:10]: La variable 'temp' podría no estar inicializada
```

**Información de contexto:**
- Número de línea y columna
- Descripción clara del problema
- Sugerencia implícita de solución

### 3.7 Resumen de Errores

Al final de cada fase, se muestra un resumen:

```
================================================================================
RESUMEN DEL ANÁLISIS SEMÁNTICO
================================================================================
Errores encontrados: 2
Advertencias: 1

❌ El análisis semántico falló
```

---

## CONCLUSIONES

### 4.1 Logros del Proyecto

1. **Implementación Completa de las Tres Fases:**
   - Se desarrolló exitosamente un compilador funcional que cubre análisis léxico, sintáctico y semántico.
   - Cada fase está claramente separada y puede probarse independientemente.

2. **Gramática LL(1) Efectiva:**
   - La gramática diseñada es no ambigua y permite análisis eficiente.
   - El parser de descenso recursivo es claro, mantenible y extensible.

3. **Manejo Robusto de Errores:**
   - El compilador no solo detecta errores, sino que proporciona mensajes claros con ubicación exacta.
   - La recuperación de errores permite reportar múltiples problemas en una sola ejecución.

4. **Tabla de Símbolos con Ámbitos:**
   - Implementación correcta de scoping mediante stack de ámbitos.
   - Soporte para bloques anidados y shadowing de variables.

5. **Sistema de Tipos:**
   - Verificación estática de tipos con conversiones implícitas razonables.
   - Inferencia de tipos en expresiones complejas.

6. **Código Limpio y Documentado:**
   - Uso de Python moderno (dataclasses, type hints, enums).
   - Código bien estructurado y comentado.
   - Separación clara de responsabilidades.

### 4.2 Aplicaciones Prácticas

Este compilador sirve como:
- **Herramienta educativa:** Para enseñar conceptos de compiladores
- **Base para extensión:** Framework para agregar nuevas características
- **Referencia de diseño:** Ejemplo de buenas prácticas en construcción de compiladores

### 4.3 Desafíos Superados

1. **Diseño de Gramática LL(1):**
   - Eliminación de recursión izquierda
   - Factorización para evitar backtracking

2. **Precedencia de Operadores:**
   - Implementación mediante niveles de recursión
   - Mantenimiento de asociatividad correcta

3. **Gestión de Ámbitos:**
   - Stack de scopes para bloques anidados
   - Búsqueda correcta desde ámbito interno a externo

### 4.4 Limitaciones Actuales

1. **Sin Generación de Código:**
   - El compilador solo realiza análisis (frontend)
   - No genera código objeto ni ejecutable

2. **Sistema de Tipos Básico:**
   - No soporta arrays, structs ni tipos definidos por el usuario
   - No hay funciones ni parámetros

3. **Strings Solo Declarativos:**
   - Se pueden declarar variables string pero no hay literales
   - No hay operaciones con cadenas

4. **Sin Optimizaciones:**
   - No hay optimización del AST
   - No se evalúan expresiones constantes

---

## ÁREAS DE MEJORA

### 5.1 Extensiones del Lenguaje

#### A. Funciones y Procedimientos
```c
int suma(int a, int b) {
    return a + b;
}

void saludar(string nombre) {
    print("Hola", nombre);
}
```

**Requerimientos:**
- Extender gramática para definiciones de función
- Implementar tabla de símbolos de funciones
- Validar tipos de retorno y parámetros
- Gestionar ámbito de parámetros

#### B. Arrays y Estructuras de Datos
```c
int[10] numeros;
numeros[0] = 5;

struct Persona {
    string nombre;
    int edad;
}
```

**Requerimientos:**
- Sintaxis para declaración de arrays
- Indexación y verificación de límites
- Tipos compuestos (structs)

#### C. Literales de String
```c
string mensaje = "Hola Mundo";
string nombre = "Juan";
print(mensaje, nombre);
```

**Requerimientos:**
- Agregar TokenType.STRING_LITERAL
- Lexer debe reconocer strings entre comillas
- Operaciones básicas (concatenación)

#### D. Operador for y break/continue
```c
for (int i = 0; i < 10; i = i + 1) {
    if (i == 5) continue;
    print(i);
    if (i > 7) break;
}
```

#### E. Operadores Adicionales
- Incremento/decremento: `++`, `--`
- Asignación compuesta: `+=`, `-=`, `*=`, `/=`
- Operador ternario: `? :`

### 5.2 Mejoras en Análisis y Validación

#### A. Análisis de Flujo de Control
- Detectar código inalcanzable
- Verificar que todas las rutas retornen valor (en funciones)
- Advertir sobre bucles infinitos evidentes

#### B. Análisis de Uso de Variables
- Detectar variables declaradas pero nunca usadas
- Identificar asignaciones redundantes
- Advertir sobre múltiples asignaciones sin uso

#### C. Tipos Más Estrictos
- Prohibir conversiones implícitas riesgosas
- Requerir casts explícitos
- Validar overflow en constantes

### 5.3 Generación de Código (Backend)

#### A. Generación de Código Intermedio
- **Código de tres direcciones:**
  ```
  t1 = x + y
  t2 = t1 * 2
  z = t2
  ```
- **Bytecode:** Secuencia de instrucciones de máquina virtual
- **LLVM IR:** Integración con infraestructura LLVM

#### B. Máquina Virtual Simple
```python
class VM:
    def __init__(self):
        self.stack = []
        self.memory = {}
        
    def execute(self, bytecode):
        for instr in bytecode:
            if instr.op == 'PUSH':
                self.stack.append(instr.value)
            elif instr.op == 'ADD':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            # ...
```

#### C. Generación de Código Nativo
- Ensamblador x86-64
- ARM assembly
- Uso de herramientas como LLVM

### 5.4 Optimizaciones

#### A. Optimizaciones en el Frontend
| Optimización | Ejemplo | Resultado |
|--------------|---------|-----------|
| Constant folding | `x = 2 + 3` | `x = 5` |
| Constant propagation | `x = 5; y = x + 1` | `y = 6` |
| Dead code elimination | `if (false) {...}` | (eliminado) |
| Strength reduction | `x * 2` | `x + x` |

#### B. Optimizaciones en el Backend
- Asignación eficiente de registros
- Eliminación de instrucciones redundantes
- Inline de funciones pequeñas

### 5.5 Herramientas y Utilidades

#### A. Debugger Integrado
```python
# Modo debug
python compiler.py --debug programa.txt

# Muestra:
# - AST en cada fase
# - Estado de tabla de símbolos
# - Stack de ámbitos
# - Paso a paso del análisis
```

#### B. Visualización del AST
```python
# Generar árbol visual
python compiler.py --visualize programa.txt

# Salida: programa_ast.png con árbol gráfico
```

#### C. Pretty Printer
```python
# Reformatear código
python compiler.py --format programa.txt

# Salida: código formateado con indentación consistente
```

#### D. Análisis Estadístico
```python
# Métricas del código
python compiler.py --stats programa.txt

# Salida:
# - Líneas de código
# - Complejidad ciclomática
# - Número de variables
# - Profundidad de anidamiento
```

### 5.6 Mejoras en Manejo de Errores

#### A. Mensajes de Error Más Descriptivos
```
Error actual:
  Error semántico [10:5]: Tipos incompatibles

Error mejorado:
  Error semántico [10:5]: Tipos incompatibles en asignación
    Se esperaba: int
    Se encontró: string
    
    10 | numero = texto;
       |          ^^^^^
    
  Sugerencia: ¿Olvidaste convertir el tipo?
```

#### B. Sugerencias de Corrección
- Detectar typos en nombres de variables
- Sugerir funciones similares
- Recomendar inclusión de bibliotecas

#### C. Mejor Recuperación de Errores
- Intentar múltiples estrategias de sincronización
- Proponer correcciones automáticas
- Modo "linter" que continúa a pesar de errores

### 5.7 Testing y Calidad

#### A. Suite de Tests Ampliada
```python
# Agregar más casos:
- Tests de regresión
- Tests de rendimiento
- Tests de casos límite
- Fuzzing para encontrar bugs
```

#### B. Cobertura de Código
```bash
pytest --cov=. --cov-report=html
# Asegurar >95% de cobertura
```

#### C. Integración Continua
```yaml
# GitHub Actions / GitLab CI
on: [push, pull_request]
jobs:
  test:
    - run: pytest
    - run: mypy .
    - run: pylint .
```

### 5.8 Documentación y Usabilidad

#### A. Documentación Completa
- Manual del lenguaje con todos los features
- Tutorial paso a paso
- Ejemplos de código comentados
- Documentación API del compilador

#### B. IDE Integration
- Extension para VSCode
- Syntax highlighting
- Auto-complete
- Error squiggles en tiempo real

#### C. REPL (Read-Eval-Print-Loop)
```bash
$ compiler repl
> int x = 5;
> x = x + 1;
> print(x);
6
```

### 5.9 Performance

#### A. Paralelización
- Análisis léxico en paralelo (para archivos grandes)
- Cache de módulos compilados
- Compilación incremental

#### B. Optimización del Parser
- Tabla de parsing pre-calculada
- Memoización de subexpresiones
- Uso de parsers generados (PLY, ANTLR)

---

## REFERENCIAS

### Bibliografía Técnica
1. **Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D.** (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson.

2. **Grune, D., Van Reeuwijk, K., Bal, H. E., Jacobs, C. J., & Langendoen, K.** (2012). *Modern Compiler Design* (2nd ed.). Springer.

3. **Appel, A. W., & Palsberg, J.** (2002). *Modern Compiler Implementation in Java* (2nd ed.). Cambridge University Press.

4. **Levine, J. R., Mason, T., & Brown, D.** (1992). *Lex & Yacc* (2nd ed.). O'Reilly Media.

### Recursos Online
- Python Documentation: https://docs.python.org/3/
- LLVM Documentation: https://llvm.org/docs/
- Compiler Explorer: https://godbolt.org/

---

## APÉNDICES

### Apéndice A: Instalación y Uso

#### Requisitos
- Python 3.8 o superior
- No requiere dependencias externas

#### Instalación
```bash
git clone <repository>
cd compilador
```

#### Uso Básico
```bash
# Compilar un archivo
python main_compiler.py programa.txt

# Modo interactivo
python main_compiler.py -i

# Ejecutar tests
python main_compiler.py -t
python ejecutar_tests.py
```

### Apéndice B: Ejemplos de Programas

#### Programa 1: Cálculo Factorial (simulado)
```c
int n = 5;
int factorial = 1;
int contador = 1;

while (contador <= n) {
    factorial = factorial * contador;
    contador = contador + 1;
}

print(factorial);
```

#### Programa 2: Números Pares
```c
int i = 0;
while (i < 10) {
    if (i % 2 == 0) {
        print(i);
    }
    i = i + 1;
}
```

#### Programa 3: Máximo de Dos Números
```c
int a = 15;
int b = 20;
int max;

if (a > b) {
    max = a;
} else {
    max = b;
}

print(max);
```

### Apéndice C: Tabla de Tokens

| Token | Regex | Ejemplo |
|-------|-------|---------|
| INT | `int` | `int` |
| FLOAT | `float` | `float` |
| STRING | `string` | `string` |
| ID | `[a-zA-Z_][a-zA-Z0-9_]*` | `variable1` |
| NUM | `[0-9]+(\.[0-9]+)?` | `42`, `3.14` |
| PLUS | `\+` | `+` |
| MINUS | `-` | `-` |
| MULT | `\*` | `*` |
| DIV | `/` | `/` |
| MOD | `%` | `%` |
| EQ | `==` | `==` |
| NEQ | `!=` | `!=` |
| LT | `<` | `<` |
| LTE | `<=` | `<=` |
| GT | `>` | `>` |
| GTE | `>=` | `>=` |
| AND | `&&` | `&&` |
| OR | `\|\|` | `||` |
| NOT | `!` | `!` |
| ASSIGN | `=` | `=` |
| SEMICOLON | `;` | `;` |
| LPAREN | `\(` | `(` |
| RPAREN | `\)` | `)` |
| LBRACE | `\{` | `{` |
| RBRACE | `\}` | `}` |
| COMMA | `,` | `,` |

---

## CONCLUSIÓN FINAL

Este proyecto demuestra exitosamente la implementación de un compilador completo en sus fases de análisis. El diseño modular, la claridad del código y el manejo robusto de errores proporcionan una base sólida para futuras extensiones.

El compilador cumple con los objetivos educativos de ilustrar los conceptos fundamentales de la teoría de compiladores, mientras mantiene un código limpio y profesional que puede servir como referencia para proyectos similares.

Las áreas de mejora identificadas ofrecen un camino claro para evolucionar este compilador hacia una herramienta más completa y poderosa, ya sea agregando generación de código, optimizaciones, o características adicionales del lenguaje.

---

**Fin del Reporte Técnico**

---

*Documento generado el: Diciembre 2025*  
*Versión: 1.0*  
*Estado: Completo*

