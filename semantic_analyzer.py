"""
Analizador Semántico
Realiza validaciones semánticas y construye la tabla de símbolos

Validaciones implementadas:
1. Declaración antes de uso de variables
2. Tipos compatibles en operaciones
3. No redeclaración de variables en el mismo ámbito
"""

from parser_rd import *
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field

# ============================================
# TABLA DE SÍMBOLOS
# ============================================

@dataclass
class Symbol:
    """Representa un símbolo en la tabla"""
    name: str
    type: str  # 'int', 'float', 'string', 'bool'
    line: int
    column: int
    initialized: bool = False

class SymbolTable:
    """Tabla de símbolos con soporte para ámbitos anidados"""
    
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]  # Stack de ámbitos
        self.current_scope = 0
    
    def enter_scope(self):
        """Entra a un nuevo ámbito (bloque)"""
        self.scopes.append({})
        self.current_scope += 1
    
    def exit_scope(self):
        """Sale del ámbito actual"""
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1
    
    def declare(self, name: str, symbol_type: str, line: int, column: int, initialized: bool = False) -> bool:
        """
        Declara una variable en el ámbito actual
        Retorna True si fue exitoso, False si ya existe
        """
        current = self.scopes[self.current_scope]
        
        if name in current:
            return False  # Ya existe en este ámbito
        
        current[name] = Symbol(name, symbol_type, line, column, initialized)
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Busca una variable en todos los ámbitos (del más interno al más externo)"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def update_initialized(self, name: str):
        """Marca una variable como inicializada"""
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name].initialized = True
                return
    
    def get_all_symbols(self) -> List[Symbol]:
        """Retorna todos los símbolos de todos los ámbitos"""
        all_symbols = []
        for scope in self.scopes:
            all_symbols.extend(scope.values())
        return all_symbols
    
    def print_table(self):
        """Imprime la tabla de símbolos"""
        print("\n" + "=" * 80)
        print("TABLA DE SÍMBOLOS")
        print("=" * 80)
        print(f"{'Variable':<15} {'Tipo':<10} {'Inicializada':<15} {'Ubicación':<20}")
        print("-" * 80)
        
        for i, scope in enumerate(self.scopes):
            if scope:
                print(f"\n--- Ámbito {i} ---")
                for symbol in scope.values():
                    init_str = "Sí" if symbol.initialized else "No"
                    loc = f"[{symbol.line}:{symbol.column}]"
                    print(f"{symbol.name:<15} {symbol.type:<10} {init_str:<15} {loc:<20}")
        print()

# ============================================
# ANALIZADOR SEMÁNTICO
# ============================================

class SemanticAnalyzer:
    """Analizador semántico con validaciones"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def error(self, message: str, line: int, column: int):
        """Registra un error semántico"""
        error_msg = f"Error semántico [{line}:{column}]: {message}"
        self.errors.append(error_msg)
        print(f"❌ {error_msg}")
    
    def warning(self, message: str, line: int, column: int):
        """Registra una advertencia"""
        warn_msg = f"Advertencia [{line}:{column}]: {message}"
        self.warnings.append(warn_msg)
        print(f"⚠️  {warn_msg}")
    
    def analyze(self, ast: Program) -> bool:
        """
        Punto de entrada del análisis semántico
        Retorna True si no hubo errores
        """
        print("\n" + "=" * 80)
        print("FASE 3: ANÁLISIS SEMÁNTICO")
        print("=" * 80)
        
        self.visit_program(ast)
        
        # Mostrar tabla de símbolos
        self.symbol_table.print_table()
        
        # Resumen
        print("=" * 80)
        print("RESUMEN DEL ANÁLISIS SEMÁNTICO")
        print("=" * 80)
        print(f"Errores encontrados: {len(self.errors)}")
        print(f"Advertencias: {len(self.warnings)}")
        
        if self.errors:
            print("\n❌ El análisis semántico falló")
            return False
        else:
            print("\n✅ Análisis semántico completado sin errores")
            return True
    
    # ============================================
    # VISITADORES DEL AST
    # ============================================
    
    def visit_program(self, node: Program):
        """Visita el nodo Program"""
        for stmt in node.statements:
            self.visit_stmt(stmt)
    
    def visit_stmt(self, node: ASTNode):
        """Despacha al visitador apropiado según el tipo de sentencia"""
        if isinstance(node, DeclStmt):
            self.visit_decl(node)
        elif isinstance(node, AssignStmt):
            self.visit_assign(node)
        elif isinstance(node, IfStmt):
            self.visit_if(node)
        elif isinstance(node, WhileStmt):
            self.visit_while(node)
        elif isinstance(node, PrintStmt):
            self.visit_print(node)
        elif isinstance(node, Block):
            self.visit_block(node)
    
    def visit_decl(self, node: DeclStmt):
        """
        Validación 1: No redeclaración en el mismo ámbito
        """
        # Intentar declarar la variable
        success = self.symbol_table.declare(
            node.var_name, 
            node.type_name, 
            node.line, 
            node.column,
            initialized=(node.init_value is not None)
        )
        
        if not success:
            self.error(
                f"La variable '{node.var_name}' ya fue declarada en este ámbito",
                node.line, node.column
            )
        
        # Si tiene valor inicial, verificar compatibilidad de tipos
        if node.init_value:
            expr_type = self.get_expr_type(node.init_value)
            if not self.are_types_compatible(node.type_name, expr_type):
                self.error(
                    f"Tipo incompatible en inicialización: se esperaba '{node.type_name}', se encontró '{expr_type}'",
                    node.line, node.column
                )
    
    def visit_assign(self, node: AssignStmt):
        """
        Validación 2: La variable debe estar declarada antes de usarse
        Validación 3: Los tipos deben ser compatibles
        """
        # Verificar que la variable existe
        symbol = self.symbol_table.lookup(node.var_name)
        
        if not symbol:
            self.error(
                f"La variable '{node.var_name}' no ha sido declarada",
                node.line, node.column
            )
            return
        
        # Marcar como inicializada
        self.symbol_table.update_initialized(node.var_name)
        
        # Verificar compatibilidad de tipos
        expr_type = self.get_expr_type(node.value)
        if not self.are_types_compatible(symbol.type, expr_type):
            self.error(
                f"Tipo incompatible en asignación: se esperaba '{symbol.type}', se encontró '{expr_type}'",
                node.line, node.column
            )
    
    def visit_if(self, node: IfStmt):
        """
        Validación 4: La condición debe ser de tipo booleano (o numérico)
        """
        cond_type = self.get_expr_type(node.condition)
        
        # La condición debe ser booleana o numérica
        if cond_type not in ['bool', 'int', 'float', 'unknown']:
            self.error(
                f"La condición del 'if' debe ser de tipo booleano o numérico, se encontró '{cond_type}'",
                node.line, node.column
            )
        
        # Visitar ramas
        self.visit_stmt(node.then_stmt)
        if node.else_stmt:
            self.visit_stmt(node.else_stmt)
    
    def visit_while(self, node: WhileStmt):
        """
        Validación 5: La condición debe ser de tipo booleano (o numérico)
        """
        cond_type = self.get_expr_type(node.condition)
        
        if cond_type not in ['bool', 'int', 'float', 'unknown']:
            self.error(
                f"La condición del 'while' debe ser de tipo booleano o numérico, se encontró '{cond_type}'",
                node.line, node.column
            )
        
        # Visitar cuerpo
        self.visit_stmt(node.body)
    
    def visit_print(self, node: PrintStmt):
        """Visita la sentencia print y verifica los argumentos"""
        for arg in node.arguments:
            # Verificar que las variables usadas estén declaradas
            self.get_expr_type(arg)
    
    def visit_block(self, node: Block):
        """Visita un bloque y crea un nuevo ámbito"""
        self.symbol_table.enter_scope()
        
        for stmt in node.statements:
            self.visit_stmt(stmt)
        
        self.symbol_table.exit_scope()
    
    # ============================================
    # INFERENCIA Y VALIDACIÓN DE TIPOS
    # ============================================
    
    def get_expr_type(self, node: ASTNode) -> str:
        """Infiere el tipo de una expresión"""
        if isinstance(node, Literal):
            # Detectar si es entero o decimal
            if '.' in node.value:
                return 'float'
            else:
                return 'int'
        
        elif isinstance(node, Identifier):
            # Buscar el tipo en la tabla de símbolos
            symbol = self.symbol_table.lookup(node.name)
            
            if not symbol:
                self.error(
                    f"La variable '{node.name}' no ha sido declarada",
                    node.line, node.column
                )
                return 'unknown'
            
            if not symbol.initialized:
                self.warning(
                    f"La variable '{node.name}' podría no estar inicializada",
                    node.line, node.column
                )
            
            return symbol.type
        
        elif isinstance(node, BinaryOp):
            return self.get_binary_op_type(node)
        
        elif isinstance(node, UnaryOp):
            return self.get_unary_op_type(node)
        
        return 'unknown'
    
    def get_binary_op_type(self, node: BinaryOp) -> str:
        """Determina el tipo resultado de una operación binaria"""
        left_type = self.get_expr_type(node.left)
        right_type = self.get_expr_type(node.right)
        
        # Operadores lógicos: retornan bool
        if node.operator in ['||', '&&']:
            return 'bool'
        
        # Operadores relacionales: retornan bool
        if node.operator in ['==', '!=', '<', '<=', '>', '>=']:
            # Verificar que los operandos sean comparables
            if left_type in ['int', 'float'] and right_type in ['int', 'float']:
                return 'bool'
            elif left_type == right_type:
                return 'bool'
            else:
                self.error(
                    f"Tipos incompatibles en comparación: '{left_type}' y '{right_type}'",
                    node.line, node.column
                )
                return 'bool'
        
        # Operadores aritméticos
        if node.operator in ['+', '-', '*', '/', '%']:
            # Si uno es float, el resultado es float
            if left_type == 'float' or right_type == 'float':
                return 'float'
            elif left_type == 'int' and right_type == 'int':
                return 'int'
            else:
                self.error(
                    f"Tipos incompatibles en operación aritmética: '{left_type}' {node.operator} '{right_type}'",
                    node.line, node.column
                )
                return 'unknown'
        
        return 'unknown'
    
    def get_unary_op_type(self, node: UnaryOp) -> str:
        """Determina el tipo resultado de una operación unaria"""
        operand_type = self.get_expr_type(node.operand)
        
        if node.operator == '!':
            # NOT lógico retorna bool
            return 'bool'
        
        elif node.operator == '-':
            # Negación numérica preserva el tipo
            if operand_type in ['int', 'float']:
                return operand_type
            else:
                self.error(
                    f"El operador '-' requiere un operando numérico, se encontró '{operand_type}'",
                    node.line, node.column
                )
                return 'unknown'
        
        return 'unknown'
    
    def are_types_compatible(self, target_type: str, source_type: str) -> bool:
        """Verifica si dos tipos son compatibles para asignación"""
        if target_type == source_type:
            return True
        
        # Conversión implícita: int -> float
        if target_type == 'float' and source_type == 'int':
            return True
        
        # Unknown puede ser compatible (errores ya reportados)
        if source_type == 'unknown':
            return True
        
        return False


# ============================================
# PROGRAMA PRINCIPAL INTEGRADO
# ============================================

def compile_program(source_code: str):
    """Compila un programa completo: léxico + sintáctico + semántico"""
    print("=" * 80)
    print("COMPILADOR - ANÁLISIS COMPLETO")
    print("=" * 80)
    print("\nCÓDIGO FUENTE:")
    print("-" * 80)
    print(source_code)
    print("-" * 80)
    
    # FASE 1: Análisis Léxico
    print("\n" + "=" * 80)
    print("FASE 1: ANÁLISIS LÉXICO")
    print("=" * 80)
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    # Verificar errores léxicos
    lex_errors = [t for t in tokens if t.type == TokenType.ERROR]
    if lex_errors:
        print(f"\n❌ Se encontraron {len(lex_errors)} errores léxicos:")
        for error in lex_errors:
            print(f"  [{error.line}:{error.column}] Caracter no reconocido: '{error.value}'")
        return False
    
    print(f"✅ {len(tokens)-1} tokens generados correctamente")  # -1 por EOF
    
    # FASE 2: Análisis Sintáctico
    print("\n" + "=" * 80)
    print("FASE 2: ANÁLISIS SINTÁCTICO")
    print("=" * 80)
    parser = Parser(tokens)
    ast = parser.parse()
    
    if not ast:
        return False
    
    # FASE 3: Análisis Semántico
    semantic = SemanticAnalyzer()
    success = semantic.analyze(ast)
    
    return success


# ============================================
# CASOS DE PRUEBA
# ============================================

if __name__ == "__main__":
    # PRUEBA 1: Programa correcto
    print("\n" + "#" * 80)
    print("PRUEBA 1: PROGRAMA CORRECTO")
    print("#" * 80)
    
    codigo_correcto = """
    int x;
    float y;
    x = 10;
    y = 3.14;
    
    if (x > 5) {
        int z;
        z = x + 5;
        print(z);
    }
    
    while (x < 20) {
        x = x + 1;
    }
    
    print(x, y);
    """
    
    compile_program(codigo_correcto)
    
    # PRUEBA 2: Variable no declarada
    print("\n\n" + "#" * 80)
    print("PRUEBA 2: ERROR - VARIABLE NO DECLARADA")
    print("#" * 80)
    
    codigo_error1 = """
    int x;
    x = 10;
    y = 5;
    """
    
    compile_program(codigo_error1)
    
    # PRUEBA 3: Tipos incompatibles
    print("\n\n" + "#" * 80)
    print("PRUEBA 3: ERROR - TIPOS INCOMPATIBLES")
    print("#" * 80)
    
    codigo_error2 = """
    int x;
    string nombre;
    x = 10;
    x = nombre;
    """
    
    compile_program(codigo_error2)
    
    # PRUEBA 4: Redeclaración
    print("\n\n" + "#" * 80)
    print("PRUEBA 4: ERROR - REDECLARACIÓN")
    print("#" * 80)
    
    codigo_error3 = """
    int x;
    float x;
    """
    
    compile_program(codigo_error3)