import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        keywords = {"inicio", "fin", "var", "imprimir", "leer", "if", "else", "for", "while", "do"}
        token_specification = [
            ("NUMBER",   r'\b\d+\b'),                     # Números
            ("IDENTIFIER", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'), # Identificadores
            ("OPERATOR", r'[+\-*/=<>!]'),                  # Operadores
            ("SYMBOL",   r'[{}();]'),                       # Símbolos
            ("STRING",   r'".*?"'),                       # Cadenas
            ("SKIP",     r'[ \t]+'),                       # Espacios y tabulaciones
            ("NEWLINE",  r'\n'),                           # Nueva línea
            ("MISMATCH", r'.')                              # Caracteres no válidos
        ]
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        line_number = 1
        line_start = 0

        for mo in re.finditer(token_regex, self.source_code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == "NEWLINE":
                line_number += 1
                line_start = mo.end()
            elif kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise RuntimeError(f"Error léxico: '{value}' inesperado en línea {line_number}, columna {column}.")
            elif kind == "IDENTIFIER" and value in keywords:
                kind = "KEYWORD"
            self.tokens.append((kind, value, line_number, column))
        return self.tokens

# Este archivo ahora espera que el usuario proporcione dinámicamente el código fuente para analizar.
