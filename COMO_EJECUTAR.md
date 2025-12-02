# Manual de Ejecución - Casos de Prueba del Compilador

## 🐍 Requisito: Python

Para ejecutar el compilador necesitas tener Python instalado en tu sistema.

### Verificar si Python está instalado
Abre una terminal PowerShell y ejecuta:
```powershell
python --version
# o
python3 --version
# o  
py --version
```

Si no está instalado, descárgalo de: https://www.python.org/downloads/

---

## 📝 Estructura de Archivos Creados

```
Compiladores/
├── main_compiler.py          # Programa principal (✅ corregido)
├── lexer_simple.py           # Analizador léxico
├── parser_rd.py              # Analizador sintáctico
├── semantic_analyzer.py      # Analizador semántico (✅ corregido)
├── gramatica.md              # Gramática completa del lenguaje
├── casos_de_prueba.md        # Documentación de 26 casos de prueba
├── readme_compiler.md        # README original
└── ejemplos/                 # Archivos de prueba
    ├── programa_completo.txt
    ├── error_variable_no_declarada.txt
    └── operadores_logicos.txt
```

---

## 🔧 Cambios Realizados

### ✅ Corrección de Imports
Se arreglaron los errores de importación en:
- `main_compiler.py`: Cambió `from parser import Parser` → `from parser_rd import Parser`
- `semantic_analyzer.py`: Cambió `from parser import *` → `from parser_rd import *`

---

## 🚀 Cómo Ejecutar los Casos de Prueba

### Opción 1: Ejecutar un archivo específico
```powershell
python main_compiler.py ejemplos/programa_completo.txt
```

### Opción 2: Modo interactivo
```powershell
python main_compiler.py -i
```
Luego escribe tu código y presiona Enter dos veces.

### Opción 3: Ejecutar todos los tests predefinidos
```powershell
python main_compiler.py --test
```

### Opción 4: Ver ayuda
```powershell
python main_compiler.py --help
```

---

## 📊 Casos de Prueba Creados

### Archivos de Ejemplo (en carpeta `ejemplos/`)

1. **programa_completo.txt** ✅
   - Programa válido que usa todas las características
   - Declaraciones, condicionales, bucles, bloques anidados, print

2. **operadores_logicos.txt** ✅
   - Prueba operadores lógicos (&&, ||)
   - Operadores relacionales (<, >, etc.)

3. **error_variable_no_declarada.txt** ❌
   - Caso de error intencional
   - Debe detectar: "Error semántico: variable 'y' no declarada"

---

## 📋 Todos los Casos en casos_de_prueba.md

El archivo `casos_de_prueba.md` contiene **26 casos de prueba** organizados:

### ✅ Casos Válidos (16)
1. Declaraciones básicas
2. Declaraciones con inicialización
3. Asignaciones
4. Expresiones aritméticas
5. Expresiones con paréntesis
6. If simple
7. If-else
8. While loop
9. Operadores relacionales
10. Operadores lógicos
11. Operador unario negación
12. Print con múltiples argumentos
13. Bloques anidados
14. If-else anidado
15. Expresiones complejas
16. Programa completo

### ❌ Casos Inválidos (10)
1. Variable no declarada
2. Redeclaración de variable
3. Tipos incompatibles
4. Falta punto y coma
5. Falta paréntesis en if
6. Falta llave de cierre
7. Operador inválido
8. Expresión incompleta
9. Falta expresión en while
10. Print sin cerrar paréntesis

---

## 🧪 Ejecución Manual de Casos

Para probar un caso específico del documento, crea un archivo `.txt` con el código y ejecútalo:

```powershell
# Crear archivo de prueba
echo 'int x = 10;
float y = 3.14;
print(x, y);' > test.txt

# Ejecutar
python main_compiler.py test.txt
```

---

## 📈 Salida Esperada del Compilador

Cuando ejecutes un programa válido, verás:

```
================================================================================
COMPILADOR - ejemplos/programa_completo.txt
================================================================================

📄 CÓDIGO FUENTE:
--------------------------------------------------------------------------------
[tu código aquí]
--------------------------------------------------------------------------------

================================================================================
📝 FASE 1: ANÁLISIS LÉXICO
================================================================================
✅ Análisis léxico exitoso: X tokens generados

================================================================================
🔍 FASE 2: ANÁLISIS SINTÁCTICO
================================================================================
✅ Análisis sintáctico exitoso
Número de sentencias: X

================================================================================
🧠 FASE 3: ANÁLISIS SEMÁNTICO
================================================================================
✅ Análisis semántico exitoso

================================================================================
✅ COMPILACIÓN EXITOSA
================================================================================
[estadísticas]
```

---

## ⚠️ Problemas Conocidos

1. **Python no instalado**: 
   - Instala Python desde python.org
   - Asegúrate de agregar Python al PATH durante la instalación

2. **Módulo no encontrado**:
   - Verifica que todos los archivos estén en la misma carpeta
   - Los archivos deben llamarse exactamente como se especifica

---

## 🎯 Próximos Pasos

1. **Instalar Python** si aún no lo tienes
2. **Ejecutar los tests predefinidos**: `python main_compiler.py --test`
3. **Probar tus propios programas**: Crea archivos `.txt` con código
4. **Verificar errores**: Prueba los casos de error intencionalmente

---

## 📞 Soporte

Si encuentras algún problema:
1. Verifica que Python esté instalado correctamente
2. Revisa que todos los archivos estén en la carpeta correcta
3. Verifica que los nombres de archivos sean exactos (case-sensitive)
