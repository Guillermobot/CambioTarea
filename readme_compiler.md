# Compilador - Proyecto Final

## 📋 Descripción

Compilador completo que implementa las tres fases principales de análisis:
- **Análisis Léxico**: Tokenización del código fuente
- **Análisis Sintáctico**: Parser recursivo descendente LL(1)
- **Análisis Semántico**: Tabla de símbolos y validaciones de tipos

## 🎯 Características del Lenguaje

### Tipos de Datos
- `int` - Números enteros
- `float` - Números decimales
- `string` - Cadenas de texto (declaración)

### Palabras Reservadas
- `int`, `float`, `string` - Declaración de tipos
- `if`, `else` - Condicionales
- `while` - Bucles
- `print` - Salida

### Operadores

**Aritméticos**: `+`, `-`, `*`, `/`, `%`

**Relacionales**: `==`, `!=`, `<`, `<=`, `>`, `>=`

**Lógicos**: `&&`, `||`, `!`

**Asignación**: `=`

### Delimitadores
- `(`, `)` - Paréntesis
- `{`, `}` - Llaves (bloques)
- `;` - Punto y coma (fin de sentencia)
- `,` - Coma (separador)

## 📁 Estructura del Proyecto

```
compilador/
├── lexer_simple.py          # Analizador léxico
├── parser.py                # Analizador sintáctico
├── semantic_analyzer.py     # Analizador semántico
├── main.py                  # Programa principal
├── README.md                # Este archivo
├── ejemplos/                # Carpeta de ejemplos
│   ├── ejemplo1.txt         # Programa simple
│   ├── ejemplo2.txt         # Con errores
│   └── ejemplo3.txt         # Complejo
└── tests/                   # Casos de prueba
```

## 🚀 Instalación y Uso

### Requisitos
- Python 3.7 o superior
- No requiere librerías externas

### Ejecución

**1. Compilar un archivo:**
```bash
python main.py programa.txt
```

**2. Modo interactivo:**
```bash
python main.py -i
```
Luego ingresa tu código y presiona Enter dos veces para compilar.

**3. Ejecutar casos de prueba:**
```bash
python main.py --test
```

**4. Ver ayuda:**
```bash
python main.py --help
```

## 📝 Ejemplos de Código

### Ejemplo 1: Programa Básico
```c
int x;
float y;
x = 10;
y = 3.14;
print(x, y);
```

### Ejemplo 2: Condicional
```c
int edad = 18;

if (edad >= 18) {
    print(edad);
} else {
    edad = 0;
}
```

### Ejemplo 3: Bucle
```c
int contador = 0;

while (contador < 5) {
    print(contador);
    contador = contador + 1;
}
```

### Ejemplo 4: Expresiones Complejas
```c
int a = 5;
int b = 10;
int resultado;

resultado = (a + b) * 2 - a / 2;

if (resultado > 20 && a < b) {
    print(resultado);
}
```

### Ejemplo 5: Bloques Anidados
```c
int x = 1;

{
    int y = 2;
    {
        int z = 3;
        print(x, y, z);
    }
}
```

## 🔍 Gramática

### Programa y Sentencias
```
Program      → StmtList
StmtList     → Stmt StmtList | ε
Stmt         → Decl ';' | Assign ';' | IfStmt | WhileStmt | PrintStmt ';' | Block
```

### Declaraciones
```
Decl         → Type id DeclInit
DeclInit     → '=' Expr | ε
Type         → int | float | string
```

### Sentencias de Control
```
Assign       → id '=' Expr
IfStmt       → if '(' Expr ')' Stmt ElseOpt
ElseOpt      → else Stmt | ε
WhileStmt    → while '(' Expr ')' Stmt
PrintStmt    → print '(' ArgListOpt ')'
Block        → '{' StmtList '}'
```

### Expresiones
```
Expr         → OrExpr
OrExpr       → AndExpr OrTail
OrTail       → '||' AndExpr OrTail | ε
AndExpr      → RelExpr AndTail
AndTail      → '&&' RelExpr AndTail | ε
RelExpr      → AddExpr RelTail
RelTail      → RelOp AddExpr | ε
RelOp        → '==' | '!=' | '<' | '<=' | '>' | '>='
AddExpr      → MulExpr AddTail
AddTail      → ('+' | '-') MulExpr AddTail | ε
MulExpr      → Unary MulTail
MulTail      → ('*' | '/' | '%') Unary MulTail | ε
Unary        → '!' Unary | '-' Unary | Primary
Primary      → id | NUM | '(' Expr ')'
```

## ✅ Validaciones Semánticas

El compilador realiza las siguientes validaciones:

1. **Declaración antes de uso**: Las variables deben declararse antes de usarse
2. **Tipos compatibles**: Las asignaciones y operaciones deben respetar los tipos
3. **No redeclaración**: No se puede declarar la misma variable dos veces en el mismo ámbito
4. **Condiciones válidas**: Las condiciones de `if` y `while` deben ser booleanas o numéricas
5. **Inicialización**: Advierte sobre variables potencialmente no inicializadas

## 📊 Salida del Compilador

El compilador genera:

1. **Lista de tokens** (Fase Léxica)
2. **Árbol Sintáctico Abstracto** (Fase Sintáctica)
3. **Tabla de Símbolos** (Fase Semántica)
4. **Reporte de errores y advertencias**

## ❌ Manejo de Errores

### Errores Léxicos
- Caracteres no reconocidos
- Tokens mal formados

### Errores Sintácticos
- Estructuras gramaticales incorrectas
- Tokens faltantes o inesperados
- **Recuperación de errores**: El parser intenta continuar después de un error

### Errores Semánticos
- Variables no declaradas
- Redeclaración de variables
- Tipos incompatibles
- Operaciones inválidas

## 🧪 Casos de Prueba

### Programa Correcto
```c
int x = 10;
float y = 3.14;

if (x > 5) {
    int z;
    z = x + 5;
    print(z);
}

while (x < 20) {
    x = x + 1;
}

print(x, y);
```
**Resultado**: ✅ Compilación exitosa

### Error: Variable No Declarada
```c
int x;
x = 10;
y = 5;  // ERROR: 'y' no declarada
```
**Resultado**: ❌ Error semántico en línea 3

### Error: Tipos Incompatibles
```c
int numero;
string texto;
numero = texto;  // ERROR: tipos incompatibles
```
**Resultado**: ❌ Error semántico

### Error: Redeclaración
```c
int x;
float x;  // ERROR: 'x' ya fue declarada
```
**Resultado**: ❌ Error semántico

## 🎓 Características Técnicas

- **Tipo de Parser**: Recursivo Descendente LL(1)
- **Tabla de Símbolos**: Con soporte para ámbitos anidados
- **Inferencia de Tipos**: Automática para expresiones
- **Recuperación de Errores**: En análisis sintáctico
- **AST**: Representación estructurada del programa

## 📌 Limitaciones

1. **No permite encadenar comparaciones**: `a < b < c` es inválido. Usar `a < b && b < c`
2. **String solo para declaración**: Aún no se implementa concatenación ni literales string
3. **No hay funciones**: Solo programa principal
4. **No hay arrays**: Solo variables escalares

## 👥 Autores

[Tu nombre y equipo]

## 📄 Licencia

Proyecto académico - [Tu Universidad]