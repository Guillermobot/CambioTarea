# Casos de Prueba del Compilador

## Descripción
Este archivo contiene casos de prueba para validar el compilador.
Los casos están organizados por categorías y cubren diferentes aspectos de la gramática.

---

## ✅ Casos VÁLIDOS (deben compilar exitosamente)

### Caso 1: Declaraciones Básicas
**Descripción**: Declaraciones simples de variables sin inicialización
**Código**:
```c
int x;
float y;
string nombre;
```

---

### Caso 2: Declaraciones con Inicialización
**Descripción**: Declaraciones con valores iniciales
**Código**:
```c
int x = 10;
float pi = 3.14;
int resultado = 0;
```

---

### Caso 3: Asignaciones
**Descripción**: Asignaciones después de declaración
**Código**:
```c
int x;
x = 5;
int y;
y = x + 10;
```

---

### Caso 4: Expresiones Aritméticas
**Descripción**: Operaciones aritméticas básicas
**Código**:
```c
int a = 5;
int b = 10;
int suma = a + b;
int resta = b - a;
int mult = a * b;
int div = b / a;
int mod = b % a;
```

---

### Caso 5: Expresiones con Paréntesis
**Descripción**: Precedencia con paréntesis
**Código**:
```c
int resultado;
resultado = (5 + 3) * 2;
int otro = 10 / (2 + 3);
```

---

### Caso 6: If Simple
**Descripción**: Condicional if sin else
**Código**:
```c
int x = 10;
if (x > 5) {
    x = x + 1;
}
```

---

### Caso 7: If-Else
**Descripción**: Condicional if-else completo
**Código**:
```c
int edad = 18;
if (edad >= 18) {
    print(edad);
} else {
    edad = 0;
}
```

---

### Caso 8: While Loop
**Descripción**: Bucle while básico
**Código**:
```c
int contador = 0;
while (contador < 5) {
    print(contador);
    contador = contador + 1;
}
```

---

### Caso 9: Operadores Relacionales
**Descripción**: Todos los operadores de comparación
**Código**:
```c
int a = 5;
int b = 10;
if (a < b) {
    print(a);
}
if (a <= b) {
    print(a);
}
if (b > a) {
    print(b);
}
if (b >= a) {
    print(b);
}
if (a == 5) {
    print(a);
}
if (a != b) {
    print(a);
}
```

---

### Caso 10: Operadores Lógicos
**Descripción**: AND, OR, NOT
**Código**:
```c
int x = 5;
int y = 10;
if (x > 0 && y > 0) {
    print(x);
}
if (x < 0 || y > 0) {
    print(y);
}
if (!(x < 0)) {
    print(x);
}
```

---

### Caso 11: Operador Unario Negación
**Descripción**: Negación aritmética
**Código**:
```c
int x = 5;
int y;
y = -x;
int z = -10;
```

---

### Caso 12: Print con Múltiples Argumentos
**Descripción**: Print con varios valores separados por comas
**Código**:
```c
int x = 5;
int y = 10;
float z = 3.14;
print(x, y, z);
```

---

### Caso 13: Bloques Anidados
**Descripción**: Ámbitos anidados
**Código**:
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

---

### Caso 14: If-Else Anidado
**Descripción**: Condicionales anidados
**Código**:
```c
int x = 10;
if (x > 5) {
    if (x > 8) {
        print(x);
    } else {
        x = x - 1;
    }
}
```

---

### Caso 15: Expresiones Complejas
**Descripción**: Expresiones con múltiples operadores y precedencia
**Código**:
```c
int a = 5;
int b = 10;
int c = 2;
int resultado;
resultado = (a + b) * c - a / 2 + b % 3;
```

---

### Caso 16: Programa Completo
**Descripción**: Programa que usa todas las características
**Código**:
```c
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

{
    int local = 100;
    print(local, x, y);
}
```

---

## ❌ Casos INVÁLIDOS (deben detectar errores)

### Error 1: Variable No Declarada
**Descripción**: Uso de variable antes de declararla
**Error Esperado**: Error semántico - variable no declarada
**Código**:
```c
int x;
x = 10;
y = 5;
```

---

### Error 2: Redeclaración de Variable
**Descripción**: Declarar la misma variable dos veces en el mismo ámbito
**Error Esperado**: Error semántico - redeclaración
**Código**:
```c
int x;
int x;
```

---

### Error 3: Tipos Incompatibles en Asignación
**Descripción**: Asignar string a int
**Error Esperado**: Error semántico - tipos incompatibles
**Código**:
```c
int numero;
string texto;
numero = texto;
```

---

### Error 4: Falta Punto y Coma
**Descripción**: Error sintáctico - falta ;
**Error Esperado**: Error sintáctico
**Código**:
```c
int x
x = 5;
```

---

### Error 5: Falta Paréntesis en If
**Descripción**: Error sintáctico - condición sin paréntesis
**Error Esperado**: Error sintáctico
**Código**:
```c
int x = 5;
if x > 5 {
    print(x);
}
```

---

### Error 6: Falta Llave de Cierre
**Descripción**: Error sintáctico - bloque sin cerrar
**Error Esperado**: Error sintáctico
**Código**:
```c
int x = 5;
{
    int y = 10;
```

---

### Error 7: Operador Inválido
**Descripción**: Error léxico - caracter no reconocido
**Error Esperado**: Error léxico
**Código**:
```c
int x = 5;
int y = x @ 10;
```

---

### Error 8: Expresión Incompleta
**Descripción**: Error sintáctico - operador sin operando derecho
**Error Esperado**: Error sintáctico
**Código**:
```c
int x;
x = 5 + ;
```

---

### Error 9: Falta Expresión en While
**Descripción**: Error sintáctico - while sin condición
**Error Esperado**: Error sintáctico
**Código**:
```c
int x = 0;
while () {
    x = x + 1;
}
```

---

### Error 10: Print sin Cerrar Paréntesis
**Descripción**: Error sintáctico - print incompleto
**Error Esperado**: Error sintáctico
**Código**:
```c
int x = 5;
print(x;
```

---

## 📊 Resumen de Casos de Prueba

**Total de casos**: 26
- ✅ Casos válidos: 16
- ❌ Casos inválidos: 10

**Cobertura de la gramática**:
- Declaraciones (Type, DeclInit)
- Asignaciones (Assign)
- Sentencias de control (IfStmt, WhileStmt, PrintStmt)
- Bloques (Block)
- Expresiones (OrExpr, AndExpr, RelExpr, AddExpr, MulExpr, Unary)
- Operadores relacionales y lógicos
- Precedencia de operadores
- Ámbitos anidados
