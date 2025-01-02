class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = {}  # Tabla de símbolos para almacenar variables y valores

    def analyze(self):
        print("\nIniciando análisis semántico...")
        for token in self.tokens:
            if token[0] == 'KEYWORD' and token[1] == 'var':
                self.handle_variable_declaration(token)
            elif token[0] == 'IDENTIFIER':
                self.handle_variable_usage(token)
        print("\nAnálisis semántico completado sin errores.")

    def handle_variable_declaration(self, token):
        index = self.tokens.index(token)
        if index + 3 >= len(self.tokens):
            raise Exception("Error semántico: Declaración de variable incompleta.")

        identifier_token = self.tokens[index + 1]
        equals_token = self.tokens[index + 2]
        value_token = self.tokens[index + 3]

        if identifier_token[0] != 'IDENTIFIER':
            raise Exception(f"Error semántico: Se esperaba un identificador después de 'var'. Token encontrado: {identifier_token}")

        if equals_token[0] != 'OPERATOR' or equals_token[1] != '=':
            raise Exception(f"Error semántico: Se esperaba un '=' después del identificador. Token encontrado: {equals_token}")

        if value_token[0] not in ['NUMBER', 'IDENTIFIER']:
            raise Exception(f"Error semántico: Valor inválido asignado a la variable. Token encontrado: {value_token}")

        # Registrar la variable en la tabla de símbolos
        self.symbol_table[identifier_token[1]] = value_token[1]
        print(f"Variable declarada: {identifier_token[1]} = {value_token[1]}")

    def handle_variable_usage(self, token):
        if token[1] not in self.symbol_table:
            raise Exception(f"Error semántico: La variable '{token[1]}' no está declarada.")
        print(f"Uso de variable válido: {token[1]} = {self.symbol_table[token[1]]}")

# Ejemplo de uso (probado con el sintáctico):
if __name__ == "__main__":
    tokens = [
        ('KEYWORD', 'var', 1, 0),
        ('IDENTIFIER', 'x', 1, 4),
        ('OPERATOR', '=', 1, 6),
        ('NUMBER', '10', 1, 8),
        ('SYMBOL', ';', 1, 10),
        ('IDENTIFIER', 'x', 2, 0),
    ]

    analyzer = SemanticAnalyzer(tokens)
    analyzer.analyze()
