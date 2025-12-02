"""
Parser Recursivo Descendente LL(1)
Implementa la gramática definida para el lenguaje
"""

from lexer_simple import Token, TokenType, Lexer
from typing import List, Optional
from dataclasses import dataclass, field

# ============================================
# NODOS DEL ÁRBOL SINTÁCTICO ABSTRACTO (AST)
# ============================================

@dataclass
class ASTNode:
    """Clase base para nodos del AST"""
    line: int = 0
    column: int = 0

@dataclass
class Program(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class DeclStmt(ASTNode):
    type_name: str  # 'int', 'float', 'string'
    var_name: str
    init_value: Optional[ASTNode] = None

@dataclass
class AssignStmt(ASTNode):
    var_name: str
    value: ASTNode

@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    then_stmt: ASTNode
    else_stmt: Optional[ASTNode] = None

@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode
    body: ASTNode

@dataclass
class PrintStmt(ASTNode):
    arguments: List[ASTNode] = field(default_factory=list)

@dataclass
class Block(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class BinaryOp(ASTNode):
    operator: str
    left: ASTNode
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class Literal(ASTNode):
    value: str

# ============================================
# PARSER
# ============================================

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.errors: List[str] = []
    
    def current_token(self) -> Token:
        """Retorna el token actual"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek_token(self, offset=1) -> Token:
        """Mira el siguiente token sin consumir"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def consume(self, expected_type: TokenType) -> Optional[Token]:
        """Consume un token del tipo esperado"""
        token = self.current_token()
        
        if token.type == expected_type:
            self.pos += 1
            return token
        else:
            self.error(f"Se esperaba {expected_type.name}, se encontró {token.type.name} ('{token.value}')")
            return None
    
    def match(self, *token_types: TokenType) -> bool:
        """Verifica si el token actual es de alguno de los tipos dados"""
        return self.current_token().type in token_types
    
    def error(self, message: str):
        """Registra un error sintáctico"""
        token = self.current_token()
        error_msg = f"Error sintáctico en línea {token.line}, columna {token.column}: {message}"
        self.errors.append(error_msg)
        print(error_msg)
    
    def synchronize(self):
        """Recuperación de errores: avanza hasta encontrar un punto de sincronización"""
        sync_tokens = {TokenType.SEMICOLON, TokenType.RBRACE, TokenType.INT, 
                       TokenType.FLOAT, TokenType.STRING, TokenType.IF, 
                       TokenType.WHILE, TokenType.PRINT, TokenType.EOF}
        
        while not self.match(*sync_tokens):
            self.pos += 1
        
        if self.match(TokenType.SEMICOLON):
            self.pos += 1
    
    # ============================================
    # REGLAS DE LA GRAMÁTICA
    # ============================================
    
    def parse(self) -> Optional[Program]:
        """Punto de entrada: Program → StmtList"""
        try:
            statements = self.parse_stmt_list()
            
            if not self.match(TokenType.EOF):
                self.error("Se esperaba fin de archivo")
            
            if self.errors:
                print(f"\n❌ Se encontraron {len(self.errors)} errores sintácticos")
                return None
            
            print("✅ Análisis sintáctico completado sin errores")
            return Program(statements=statements)
        
        except Exception as e:
            self.error(f"Error inesperado: {str(e)}")
            return None
    
    def parse_stmt_list(self) -> List[ASTNode]:
        """StmtList → Stmt StmtList | ε"""
        statements = []
        
        # FIRST(Stmt) = {int, float, string, id, if, while, print, '{'}
        while self.match(TokenType.INT, TokenType.FLOAT, TokenType.STRING,
                         TokenType.ID, TokenType.IF, TokenType.WHILE,
                         TokenType.PRINT, TokenType.LBRACE):
            stmt = self.parse_stmt()
            if stmt:
                statements.append(stmt)
            else:
                # Error recovery
                self.synchronize()
        
        return statements
    
    def parse_stmt(self) -> Optional[ASTNode]:
        """
        Stmt → Decl ';' | Assign ';' | IfStmt | WhileStmt | PrintStmt ';' | Block
        """
        token = self.current_token()
        
        # Decl → Type id DeclInit
        if self.match(TokenType.INT, TokenType.FLOAT, TokenType.STRING):
            return self.parse_decl()
        
        # Assign → id '=' Expr
        elif self.match(TokenType.ID):
            return self.parse_assign()
        
        # IfStmt
        elif self.match(TokenType.IF):
            return self.parse_if_stmt()
        
        # WhileStmt
        elif self.match(TokenType.WHILE):
            return self.parse_while_stmt()
        
        # PrintStmt
        elif self.match(TokenType.PRINT):
            return self.parse_print_stmt()
        
        # Block
        elif self.match(TokenType.LBRACE):
            return self.parse_block()
        
        else:
            self.error(f"Inicio de sentencia inválido: {token.value}")
            return None
    
    def parse_decl(self) -> Optional[DeclStmt]:
        """Decl → Type id DeclInit ';'"""
        type_token = self.current_token()
        type_name = type_token.value
        self.pos += 1  # Consumir tipo
        
        id_token = self.consume(TokenType.ID)
        if not id_token:
            return None
        
        var_name = id_token.value
        init_value = None
        
        # DeclInit → '=' Expr | ε
        if self.match(TokenType.ASSIGN):
            self.pos += 1  # Consumir '='
            init_value = self.parse_expr()
        
        self.consume(TokenType.SEMICOLON)
        
        return DeclStmt(type_name=type_name, var_name=var_name, 
                       init_value=init_value, line=type_token.line, 
                       column=type_token.column)
    
    def parse_assign(self) -> Optional[AssignStmt]:
        """Assign → id '=' Expr ';'"""
        id_token = self.current_token()
        var_name = id_token.value
        self.pos += 1  # Consumir id
        
        self.consume(TokenType.ASSIGN)
        value = self.parse_expr()
        self.consume(TokenType.SEMICOLON)
        
        return AssignStmt(var_name=var_name, value=value, 
                         line=id_token.line, column=id_token.column)
    
    def parse_if_stmt(self) -> Optional[IfStmt]:
        """IfStmt → if '(' Expr ')' Stmt ElseOpt"""
        if_token = self.current_token()
        self.pos += 1  # Consumir 'if'
        
        self.consume(TokenType.LPAREN)
        condition = self.parse_expr()
        self.consume(TokenType.RPAREN)
        
        then_stmt = self.parse_stmt()
        
        # ElseOpt → else Stmt | ε
        else_stmt = None
        if self.match(TokenType.ELSE):
            self.pos += 1  # Consumir 'else'
            else_stmt = self.parse_stmt()
        
        return IfStmt(condition=condition, then_stmt=then_stmt, 
                     else_stmt=else_stmt, line=if_token.line, 
                     column=if_token.column)
    
    def parse_while_stmt(self) -> Optional[WhileStmt]:
        """WhileStmt → while '(' Expr ')' Stmt"""
        while_token = self.current_token()
        self.pos += 1  # Consumir 'while'
        
        self.consume(TokenType.LPAREN)
        condition = self.parse_expr()
        self.consume(TokenType.RPAREN)
        
        body = self.parse_stmt()
        
        return WhileStmt(condition=condition, body=body, 
                        line=while_token.line, column=while_token.column)
    
    def parse_print_stmt(self) -> Optional[PrintStmt]:
        """PrintStmt → print '(' ArgListOpt ')' ';'"""
        print_token = self.current_token()
        self.pos += 1  # Consumir 'print'
        
        self.consume(TokenType.LPAREN)
        
        # ArgListOpt → ArgList | ε
        arguments = []
        if not self.match(TokenType.RPAREN):  # Si no es ')', hay argumentos
            arguments = self.parse_arg_list()
        
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.SEMICOLON)
        
        return PrintStmt(arguments=arguments, line=print_token.line, 
                        column=print_token.column)
    
    def parse_arg_list(self) -> List[ASTNode]:
        """ArgList → Expr ArgList'"""
        args = [self.parse_expr()]
        
        # ArgList' → ',' Expr ArgList' | ε
        while self.match(TokenType.COMMA):
            self.pos += 1  # Consumir ','
            args.append(self.parse_expr())
        
        return args
    
    def parse_block(self) -> Optional[Block]:
        """Block → '{' StmtList '}'"""
        lbrace_token = self.current_token()
        self.pos += 1  # Consumir '{'
        
        statements = self.parse_stmt_list()
        
        self.consume(TokenType.RBRACE)
        
        return Block(statements=statements, line=lbrace_token.line, 
                    column=lbrace_token.column)
    
    # ============================================
    # EXPRESIONES
    # ============================================
    
    def parse_expr(self) -> Optional[ASTNode]:
        """Expr → OrExpr"""
        return self.parse_or_expr()
    
    def parse_or_expr(self) -> Optional[ASTNode]:
        """OrExpr → AndExpr OrTail"""
        left = self.parse_and_expr()
        return self.parse_or_tail(left)
    
    def parse_or_tail(self, left: ASTNode) -> ASTNode:
        """OrTail → '||' AndExpr OrTail | ε"""
        while self.match(TokenType.OR):
            op_token = self.current_token()
            self.pos += 1  # Consumir '||'
            right = self.parse_and_expr()
            left = BinaryOp(operator='||', left=left, right=right, 
                           line=op_token.line, column=op_token.column)
        return left
    
    def parse_and_expr(self) -> Optional[ASTNode]:
        """AndExpr → RelExpr AndTail"""
        left = self.parse_rel_expr()
        return self.parse_and_tail(left)
    
    def parse_and_tail(self, left: ASTNode) -> ASTNode:
        """AndTail → '&&' RelExpr AndTail | ε"""
        while self.match(TokenType.AND):
            op_token = self.current_token()
            self.pos += 1  # Consumir '&&'
            right = self.parse_rel_expr()
            left = BinaryOp(operator='&&', left=left, right=right, 
                           line=op_token.line, column=op_token.column)
        return left
    
    def parse_rel_expr(self) -> Optional[ASTNode]:
        """RelExpr → AddExpr RelTail"""
        left = self.parse_add_expr()
        return self.parse_rel_tail(left)
    
    def parse_rel_tail(self, left: ASTNode) -> ASTNode:
        """RelTail → RelOp AddExpr | ε"""
        if self.match(TokenType.EQ, TokenType.NEQ, TokenType.LT, 
                     TokenType.LTE, TokenType.GT, TokenType.GTE):
            op_token = self.current_token()
            self.pos += 1  # Consumir operador relacional
            right = self.parse_add_expr()
            return BinaryOp(operator=op_token.value, left=left, right=right, 
                           line=op_token.line, column=op_token.column)
        return left
    
    def parse_add_expr(self) -> Optional[ASTNode]:
        """AddExpr → MulExpr AddTail"""
        left = self.parse_mul_expr()
        return self.parse_add_tail(left)
    
    def parse_add_tail(self, left: ASTNode) -> ASTNode:
        """AddTail → ('+' | '-') MulExpr AddTail | ε"""
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token()
            self.pos += 1  # Consumir operador
            right = self.parse_mul_expr()
            left = BinaryOp(operator=op_token.value, left=left, right=right, 
                           line=op_token.line, column=op_token.column)
        return left
    
    def parse_mul_expr(self) -> Optional[ASTNode]:
        """MulExpr → Unary MulTail"""
        left = self.parse_unary()
        return self.parse_mul_tail(left)
    
    def parse_mul_tail(self, left: ASTNode) -> ASTNode:
        """MulTail → ('*' | '/' | '%') Unary MulTail | ε"""
        while self.match(TokenType.MULT, TokenType.DIV, TokenType.MOD):
            op_token = self.current_token()
            self.pos += 1  # Consumir operador
            right = self.parse_unary()
            left = BinaryOp(operator=op_token.value, left=left, right=right, 
                           line=op_token.line, column=op_token.column)
        return left
    
    def parse_unary(self) -> Optional[ASTNode]:
        """Unary → '!' Unary | '-' Unary | Primary"""
        if self.match(TokenType.NOT, TokenType.MINUS):
            op_token = self.current_token()
            self.pos += 1  # Consumir operador unario
            operand = self.parse_unary()
            return UnaryOp(operator=op_token.value, operand=operand, 
                          line=op_token.line, column=op_token.column)
        
        return self.parse_primary()
    
    def parse_primary(self) -> Optional[ASTNode]:
        """Primary → id | NUM | '(' Expr ')'"""
        token = self.current_token()
        
        if self.match(TokenType.ID):
            self.pos += 1
            return Identifier(name=token.value, line=token.line, 
                            column=token.column)
        
        elif self.match(TokenType.NUM):
            self.pos += 1
            return Literal(value=token.value, line=token.line, 
                          column=token.column)
        
        elif self.match(TokenType.LPAREN):
            self.pos += 1  # Consumir '('
            expr = self.parse_expr()
            self.consume(TokenType.RPAREN)
            return expr
        
        else:
            self.error(f"Se esperaba identificador, número o '(', se encontró {token.value}")
            return None


# ============================================
# EJEMPLO DE USO
# ============================================

if __name__ == "__main__":
    # Código de prueba
    codigo = """
    int x;
    float y;
    x = 5 + 3 * 2;
    y = 3.14;
    
    if (x < 10) {
        print(x);
    } else {
        x = x + 1;
    }
    
    while (x < 20) {
        x = x + 1;
        print(x, y);
    }
    """
    
    print("=" * 60)
    print("CÓDIGO FUENTE:")
    print("=" * 60)
    print(codigo)
    print()
    
    # Fase 1: Análisis Léxico
    print("=" * 60)
    print("FASE 1: ANÁLISIS LÉXICO")
    print("=" * 60)
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    lexer.print_tokens()
    
    # Fase 2: Análisis Sintáctico
    print("\n" + "=" * 60)
    print("FASE 2: ANÁLISIS SINTÁCTICO")
    print("=" * 60)
    parser = Parser(tokens)
    ast = parser.parse()
    
    if ast:
        print(f"\n✅ AST generado con éxito")
        print(f"Número de sentencias en el programa: {len(ast.statements)}")
    else:
        print(f"\n❌ No se pudo generar el AST debido a errores")