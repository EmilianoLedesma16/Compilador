import re

# Definición de patrones para tokens del lenguaje
TOKEN_REGEX = [
    (r'\b(inicio|fin|var|imprimir|if|else|for|while|do|leer)\b', 'KEYWORD'),  # Palabras clave
    (r'\b\d+\b', 'NUMBER'),  # Números enteros
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),  # Identificadores
    (r'[+\-*/=<>!]+', 'OPERATOR'),  # Operadores
    (r'[{}();]', 'SYMBOL'),  # Símbolos especiales
    (r'".*?"', 'STRING'),  # Cadenas
    (r'\s+', None),  # Ignorar espacios y tabulaciones
]

class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []

    def tokenize(self):
        """Convierte el texto fuente en una lista de tokens."""
        while self.text:
            match = None
            for regex, token_type in TOKEN_REGEX:
                match = re.match(regex, self.text)
                if match:
                    if token_type:  # Si no es un token ignorado
                        self.tokens.append((token_type, match.group(0)))
                    self.text = self.text[match.end():]  # Avanzar en el texto
                    break
            if not match:
                raise Exception(f"Token no reconocido: {self.text[:10]}")
        return self.tokens

# Prueba rápida del analizador léxico
if __name__ == "__main__":
    code = """
    inicio {
        var x = 10;
        imprimir(x);
        if (x > 5) {
            imprimir("Mayor que 5");
        }
    } fin
    """

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
