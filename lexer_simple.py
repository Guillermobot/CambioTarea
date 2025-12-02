"""
Lexer simplificado para el lenguaje definido en la gramática
Compatible con: int, float, string, if, else, while, print
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

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
        
        # Operadores de dos caracteres
        self.two_char_ops = {
            '||': TokenType.OR,
            '&&': TokenType.AND,
            '==': TokenType.EQ,
            '!=': TokenType.NEQ,
            '<=': TokenType.LTE,
            '>=': TokenType.GTE,
        }
        
        # Operadores de un caracter
        self.one_char_ops = {
            '!': TokenType.NOT,
            '<': TokenType.LT,
            '>': TokenType.GT,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULT,
            '/': TokenType.DIV,
            '%': TokenType.MOD,
            '=': TokenType.ASSIGN,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
        }
    
    def current_char(self) -> Optional[str]:
        """Retorna el caracter actual o None si llegó al final"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset=1) -> Optional[str]:
        """Mira el siguiente caracter sin avanzar"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
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
    
    def skip_comment(self):
        """Salta comentarios // y /* */"""
        if self.current_char() == '/' and self.peek_char() == '/':
            # Comentario de línea
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            self.advance()  # Saltar el \n
            return True
        
        if self.current_char() == '/' and self.peek_char() == '*':
            # Comentario de bloque
            self.advance()  # /
            self.advance()  # *
            while self.current_char():
                if self.current_char() == '*' and self.peek_char() == '/':
                    self.advance()  # *
                    self.advance()  # /
                    return True
                self.advance()
            return True
        
        return False
    
    def read_number(self) -> Token:
        """Lee un número (entero o decimal)"""
        start_line = self.line
        start_col = self.column
        num_str = ""
        
        # Parte entera
        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()
        
        # Parte decimal
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            num_str += self.current_char()
            self.advance()
            while self.current_char() and self.current_char().isdigit():
                num_str += self.current_char()
                self.advance()
        
        return Token(TokenType.NUM, num_str, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Lee un identificador o palabra reservada"""
        start_line = self.line
        start_col = self.column
        id_str = ""
        
        # Primer caracter: letra o _
        if self.current_char() and (self.current_char().isalpha() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        # Siguientes: letra, dígito o _
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        # Verificar si es palabra reservada
        token_type = self.keywords.get(id_str, TokenType.ID)
        return Token(token_type, id_str, start_line, start_col)
    
    def read_operator(self) -> Token:
        """Lee operadores de uno o dos caracteres"""
        start_line = self.line
        start_col = self.column
        
        # Intentar operador de dos caracteres
        two_char = self.current_char() + (self.peek_char() or '')
        if two_char in self.two_char_ops:
            token_type = self.two_char_ops[two_char]
            self.advance()
            self.advance()
            return Token(token_type, two_char, start_line, start_col)
        
        # Operador de un caracter
        one_char = self.current_char()
        if one_char in self.one_char_ops:
            token_type = self.one_char_ops[one_char]
            self.advance()
            return Token(token_type, one_char, start_line, start_col)
        
        # Error: caracter no reconocido
        self.advance()
        return Token(TokenType.ERROR, one_char, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Analiza el código fuente y genera la lista de tokens"""
        self.tokens = []
        
        while self.current_char():
            # Saltar espacios y comentarios
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            if self.skip_comment():
                continue
            
            # Números
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identificadores y palabras reservadas
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operadores y delimitadores
            self.tokens.append(self.read_operator())
        
        # Agregar token EOF
        self.tokens.append(Token(TokenType.EOF, '$', self.line, self.column))
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


# Ejemplo de uso
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
    """
    
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