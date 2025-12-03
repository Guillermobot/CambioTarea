
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple

class TokenType(Enum):
    # Palabras reservadas
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    PRINT = "print"
    
    # Identificadores y literales
    ID = "id"
    NUM = "num"
    
    # Operadores lógicos
    OR = "||"
    AND = "&&"
    NOT = "!"
    
    # Operadores relacionales
    EQ = "=="
    NEQ = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    
    # Operadores aritméticos
    PLUS = "+"
    MINUS = "-"
    MULT = "*"
    DIV = "/"
    MOD = "%"
    
    # Asignación
    ASSIGN = "="
    
    # Delimitadores
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    SEMICOLON = ";"
    COMMA = ","
    
    # Especiales
    EOF = "$"
    ERROR = "ERROR"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Construir tabla de transiciones
        self.transitions = self._build_transitions()
        
        # Estados finales y sus tokens correspondientes
        self.final_states = {
            # Palabras reservadas
            "q_int": TokenType.INT,
            "q_if": TokenType.IF,
            "q_float": TokenType.FLOAT,
            "q_string": TokenType.STRING,
            "q_else": TokenType.ELSE,
            "q_while": TokenType.WHILE,
            "q_print": TokenType.PRINT,
            
            # Operadores
            "q_or": TokenType.OR,
            "q_and": TokenType.AND,
            "q_not": TokenType.NOT,
            "q_eq": TokenType.EQ,
            "q_neq": TokenType.NEQ,
            "q_lt": TokenType.LT,
            "q_lte": TokenType.LTE,
            "q_gt": TokenType.GT,
            "q_gte": TokenType.GTE,
            "q_plus": TokenType.PLUS,
            "q_minus": TokenType.MINUS,
            "q_mult": TokenType.MULT,
            "q_div": TokenType.DIV,
            "q_mod": TokenType.MOD,
            "q_assign": TokenType.ASSIGN,
            
            # Delimitadores
            "q_lparen": TokenType.LPAREN,
            "q_rparen": TokenType.RPAREN,
            "q_lbrace": TokenType.LBRACE,
            "q_rbrace": TokenType.RBRACE,
            "q_semicolon": TokenType.SEMICOLON,
            "q_comma": TokenType.COMMA,
            
            # Números e identificadores
            "q_num": TokenType.NUM,
            "q_num_decimal": TokenType.NUM,
            "q_id": TokenType.ID,
        }
        
        # Palabras reservadas
        self.keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'string': TokenType.STRING,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'print': TokenType.PRINT,
        }
    
    def _build_transitions(self) -> Dict[Tuple[str, str], str]:
        """Construye la tabla de transiciones del AFD"""
        trans = {}
        
        # ========================================
        # PALABRAS RESERVADAS
        # ========================================
        
        # INT: i->n->t
        trans[("q0", 'i')] = "q_i"
        trans[("q_i", 'n')] = "q_in"
        trans[("q_in", 't')] = "q_int"
        
        # IF: i->f
        trans[("q_i", 'f')] = "q_if"
        
        # FLOAT: f->l->o->a->t
        trans[("q0", 'f')] = "q_f"
        trans[("q_f", 'l')] = "q_fl"
        trans[("q_fl", 'o')] = "q_flo"
        trans[("q_flo", 'a')] = "q_floa"
        trans[("q_floa", 't')] = "q_float"
        
        # STRING: s->t->r->i->n->g
        trans[("q0", 's')] = "q_s"
        trans[("q_s", 't')] = "q_st"
        trans[("q_st", 'r')] = "q_str"
        trans[("q_str", 'i')] = "q_stri"
        trans[("q_stri", 'n')] = "q_strin"
        trans[("q_strin", 'g')] = "q_string"
        
        # ELSE: e->l->s->e
        trans[("q0", 'e')] = "q_e"
        trans[("q_e", 'l')] = "q_el"
        trans[("q_el", 's')] = "q_els"
        trans[("q_els", 'e')] = "q_else"
        
        # WHILE: w->h->i->l->e
        trans[("q0", 'w')] = "q_w"
        trans[("q_w", 'h')] = "q_wh"
        trans[("q_wh", 'i')] = "q_whi"
        trans[("q_whi", 'l')] = "q_whil"
        trans[("q_whil", 'e')] = "q_while"
        
        # PRINT: p->r->i->n->t
        trans[("q0", 'p')] = "q_p"
        trans[("q_p", 'r')] = "q_pr"
        trans[("q_pr", 'i')] = "q_pri"
        trans[("q_pri", 'n')] = "q_prin"
        trans[("q_prin", 't')] = "q_print"
        
        # ========================================
        # OPERADORES DE DOS CARACTERES
        # ========================================
        
        # || (OR)
        trans[("q0", '|')] = "q_pipe"
        trans[("q_pipe", '|')] = "q_or"
        
        # && (AND)
        trans[("q0", '&')] = "q_amp"
        trans[("q_amp", '&')] = "q_and"
        
        # == (EQ)
        trans[("q0", '=')] = "q_assign"
        trans[("q_assign", '=')] = "q_eq"
        
        # != (NEQ)
        trans[("q0", '!')] = "q_not"
        trans[("q_not", '=')] = "q_neq"
        
        # < y <= (LT, LTE)
        trans[("q0", '<')] = "q_lt"
        trans[("q_lt", '=')] = "q_lte"
        
        # > y >= (GT, GTE)
        trans[("q0", '>')] = "q_gt"
        trans[("q_gt", '=')] = "q_gte"
        
        # ========================================
        # OPERADORES DE UN CARACTER
        # ========================================
        
        trans[("q0", '+')] = "q_plus"
        trans[("q0", '-')] = "q_minus"
        trans[("q0", '*')] = "q_mult"
        trans[("q0", '/')] = "q_div"
        trans[("q0", '%')] = "q_mod"
        
        # ========================================
        # DELIMITADORES
        # ========================================
        
        trans[("q0", '(')] = "q_lparen"
        trans[("q0", ')')] = "q_rparen"
        trans[("q0", '{')] = "q_lbrace"
        trans[("q0", '}')] = "q_rbrace"
        trans[("q0", ';')] = "q_semicolon"
        trans[("q0", ',')] = "q_comma"
        
        # ========================================
        # NÚMEROS
        # ========================================
        
        # Dígitos iniciales
        for d in "0123456789":
            trans[("q0", d)] = "q_num"
            trans[("q_num", d)] = "q_num"
        
        # Punto decimal
        trans[("q_num", '.')] = "q_num_dot"
        for d in "0123456789":
            trans[("q_num_dot", d)] = "q_num_decimal"
            trans[("q_num_decimal", d)] = "q_num_decimal"
        
        # ========================================
        # IDENTIFICADORES
        # ========================================
        
        # Permitir que palabras reservadas continúen como IDs
        # Ejemplo: "integer" debe ser ID, no INT
        for state in ["q_int", "q_if", "q_float", "q_string", "q_else", "q_while", "q_print"]:
            for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
                trans[(state, c)] = "q_id"
        
        # ID desde q0 con cualquier letra o _
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
            if (("q0", c) not in trans):  # Si no es inicio de palabra reservada
                trans[("q0", c)] = "q_id"
        
        # Continuación de ID
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
            trans[("q_id", c)] = "q_id"
        
        return trans
    
    def current_char(self) -> Optional[str]:
        """Retorna el caracter actual"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def advance(self):
        """Avanza una posición"""
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        """Salta espacios en blanco"""
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def skip_comment(self) -> bool:
        """Salta comentarios // y /* */"""
        if self.current_char() == '/' and self.pos + 1 < len(self.source):
            next_char = self.source[self.pos + 1]
            
            # Comentario de línea //
            if next_char == '/':
                while self.current_char() and self.current_char() != '\n':
                    self.advance()
                if self.current_char() == '\n':
                    self.advance()
                return True
            
            # Comentario de bloque /* */
            elif next_char == '*':
                self.advance()  # /
                self.advance()  # *
                while self.current_char():
                    if self.current_char() == '*' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '/':
                        self.advance()  # *
                        self.advance()  # /
                        return True
                    self.advance()
                return True
        
        return False
    
    def get_next_token(self) -> Optional[Token]:
        """Obtiene el siguiente token usando la tabla de transiciones"""
        # Saltar whitespace y comentarios
        while self.current_char() and (self.current_char().isspace() or self.skip_comment()):
            if self.current_char() and self.current_char().isspace():
                self.skip_whitespace()
        
        if not self.current_char():
            return Token(TokenType.EOF, '$', self.line, self.column)
        
        # Guardar posición inicial
        start_line = self.line
        start_col = self.column
        lexeme = ""
        state = "q0"
        last_final_state = None
        last_final_pos = self.pos
        last_final_lexeme = ""
        
        # Simular el AFD
        while self.current_char():
            c = self.current_char()
            key = (state, c)
            
            if key in self.transitions:
                state = self.transitions[key]
                lexeme += c
                self.advance()
                
                # Si es un estado final, guardarlo
                if state in self.final_states:
                    last_final_state = state
                    last_final_pos = self.pos
                    last_final_lexeme = lexeme
            else:
                # No hay transición, intentar cerrar token
                break
        
        # Si encontramos un estado final, crear el token
        if last_final_state:
            # Retroceder a la última posición válida
            while self.pos > last_final_pos:
                self.pos -= 1
                if self.pos < len(self.source) and self.source[self.pos] == '\n':
                    self.line -= 1
                self.column -= 1
            
            token_type = self.final_states[last_final_state]
            
            # Verificar si es palabra reservada o identificador
            if token_type == TokenType.ID and last_final_lexeme in self.keywords:
                token_type = self.keywords[last_final_lexeme]
            
            return Token(token_type, last_final_lexeme, start_line, start_col)
        
        # Si no se encontró transición válida, es un error
        if lexeme:
            return Token(TokenType.ERROR, lexeme, start_line, start_col)
        else:
            # Consumir el caracter inválido
            error_char = self.current_char()
            self.advance()
            return Token(TokenType.ERROR, error_char, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Tokeniza todo el código fuente"""
        self.tokens = []
        
        while True:
            token = self.get_next_token()
            self.tokens.append(token)
            
            if token.type == TokenType.EOF:
                break
        
        return self.tokens
    
    def print_tokens(self):
        """Imprime los tokens de forma legible"""
        print("\n=== ANÁLISIS LÉXICO COMPLETADO ===")
        print(f"Total de tokens: {len(self.tokens)}\n")
        
        # Agrupar por tipo
        by_type = {}
        for token in self.tokens:
            type_name = token.type.name
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(token.value)
        
        for type_name in sorted(by_type.keys()):
            print(f"{type_name}:")
            for value in by_type[type_name]:
                print(f"  - {value}")
            print()
        
        print("=== SECUENCIA DE TOKENS ===")
        for token in self.tokens:
            print(f"{token.value:10} {token.type.name:15} [{token.line}:{token.column}]")

# ============================================
# EJEMPLO DE USO
# ============================================

if __name__ == "__main__":
    codigo = """
    int x;
    float total;
    x = 5 + 3;
    
    if (x < 10) {
        print(x);
    } else {
        x = x + 1;
    }
    
    while (x < 20) {
        x = x + 2;
    }
    """
    
    print("CÓDIGO FUENTE:")
    print("=" * 60)
    print(codigo)
    print("=" * 60)
    
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    lexer.print_tokens()
    
    print("\n=== ERRORES LÉXICOS ===")
    errores = [t for t in tokens if t.type == TokenType.ERROR]
    if errores:
        for error in errores:
            print(f"Error en línea {error.line}, columna {error.column}: caracter no reconocido '{error.value}'")
    else:
        print("No se encontraron errores léxicos")