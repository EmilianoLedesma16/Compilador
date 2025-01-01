class ParserError(Exception):
    """Clase personalizada para errores sintácticos."""
    def __init__(self, message, line, column):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"Línea {self.line}, Columna {self.column}: {self.message}"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def consume(self, expected_type=None, expected_value=None):
        while self.current_token[0] == 'NEWLINE':  # Ignorar saltos de línea
            print(f"Ignorando NEWLINE. Token actual: {self.current_token}")
            self.advance()
        print(f"Validando token: {self.current_token}")
        if expected_type and self.current_token[0] != expected_type:
            self.raise_error(
                f"Se esperaba tipo '{expected_type}', pero se obtuvo '{self.current_token[0]}'. "
                f"Token actual: {self.current_token}"
            )
        if expected_value and self.current_token[1] != expected_value:
            self.raise_error(
                f"Se esperaba valor '{expected_value}', pero se obtuvo '{self.current_token[1]}'. "
                f"Token actual: {self.current_token}"
            )
        print(f"Consumido: {self.current_token}")
        self.advance()

    def advance(self):
        """Avanza al siguiente token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = ('EOF', None)
        print(f"Avanzando al siguiente token: {self.current_token}")

    def raise_error(self, message):
        """Genera un error sintáctico con contexto."""
        line, column = self.current_token[2], self.current_token[3]
        raise ParserError(message, line, column)

    def parse_program(self):
        try:
            print("Iniciando análisis del programa.")
            self.consume('KEYWORD', 'inicio')
            self.consume('SYMBOL', '{')
            block = self.parse_block()
            self.consume('SYMBOL', '}')
            self.consume('KEYWORD', 'fin')
            print("Análisis del programa completado.")
            return ProgramNode(block)
        except ParserError as e:
            print(f"Error detectado durante el análisis: {e}")
            return str(e)  # Devuelve el error como texto para la GUI

    def parse_block(self):
        print("Iniciando análisis de bloque.")
        statements = []
        while self.current_token[0] != 'SYMBOL' or self.current_token[1] != '}':
            if self.current_token[0] == 'NEWLINE':
                self.consume()
                continue
            statements.append(self.parse_statement())
        if not statements:
            self.raise_error("Bloque vacío no permitido.")
        print("Análisis de bloque completado.")
        return BlockNode(statements)

    def parse_statement(self):
        print(f"Statement - Token actual: {self.current_token}")
        if self.current_token[0] == 'KEYWORD':
            if self.current_token[1] == 'var':
                return self.parse_declaration()
            elif self.current_token[1] == 'imprimir':
                return self.parse_print()
            elif self.current_token[1] == 'if':
                return self.parse_if()
            elif self.current_token[1] == 'for':
                return self.parse_for()
            elif self.current_token[1] == 'while':
                return self.parse_while()
        elif self.current_token[0] == 'IDENTIFIER':  # Reconoce expresiones
            return self.parse_expression_statement()
        self.raise_error(f"Instrucción no válida: '{self.current_token[1]}'.")

    def parse_declaration(self):
        print(f"Declaración - Token actual: {self.current_token}")
        self.consume('KEYWORD', 'var')  # Consumir 'var'
        
        # Validar identificador
        print(f"Esperando IDENTIFIER, token actual: {self.current_token}")
        if self.current_token[0] != 'IDENTIFIER':
            self.raise_error("Se esperaba un identificador después de 'var'.")
        identifier = self.current_token[1]
        print(f"Identificador reconocido: {identifier}")
        self.consume('IDENTIFIER')  # Consumir identificador

        # Consumir operador '='
        print(f"Esperando '=', token actual: {self.current_token}")
        self.consume('OPERATOR', '=')  # Consumir '='
        print(f"Operador '=' consumido. Token actual: {self.current_token}")

        # Validar expresión
        expression = self.parse_expression()
        print(f"Expresión parseada. Token actual: {self.current_token}")

        # Consumir punto y coma ';'
        print(f"Esperando ';', token actual: {self.current_token}")
        self.consume('SYMBOL', ';')  # Consumir ';'

        print(f"Declaración completada para {identifier}")
        return DeclarationNode(identifier, expression)

    def parse_print(self):
        print(f"Iniciando análisis de imprimir. Token actual: {self.current_token}")
        self.consume('KEYWORD', 'imprimir')
        self.consume('SYMBOL', '(')
        expression = self.parse_expression()
        self.consume('SYMBOL', ')')
        self.consume('SYMBOL', ';')
        print("Análisis de imprimir completado.")
        return PrintNode(expression)

    def parse_expression(self):
        print(f"Expresión - Token actual: {self.current_token}")
        left = self.parse_term()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ['+', '-']:
            operator = self.current_token[1]
            print(f"Operador encontrado: {operator}")
            self.consume('OPERATOR')
            right = self.parse_term()
            left = BinaryOpNode(operator, left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ['*', '/']:
            operator = self.current_token[1]
            print(f"Operador encontrado: {operator}")
            self.consume('OPERATOR')
            right = self.parse_factor()
            left = BinaryOpNode(operator, left, right)
        return left

    def parse_factor(self):
        token = self.current_token
        print(f"Factor - Token actual: {token}")
        if token[0] == 'NUMBER':
            self.consume('NUMBER')
            return NumberNode(token[1])
        elif token[0] == 'IDENTIFIER':
            self.consume('IDENTIFIER')
            return IdentifierNode(token[1])
        elif token[0] == 'SYMBOL' and token[1] == '(':
            self.consume('SYMBOL', '(')
            expr = self.parse_expression()
            self.consume('SYMBOL', ')')
            return expr
        self.raise_error(f"Factor inesperado: '{token[1]}'.")

    def parse_expression_statement(self):
        print(f"Iniciando análisis de expresión como statement. Token actual: {self.current_token}")
        expression = self.parse_expression()
        self.consume('SYMBOL', ';')  # Verifica que termine con un punto y coma
        print("Análisis de expresión como statement completado.")
        return ExpressionStatementNode(expression)


# Definición de nodos del AST
class ProgramNode:
    def __init__(self, block):
        self.block = block

class BlockNode:
    def __init__(self, statements):
        self.statements = statements

class DeclarationNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class PrintNode:
    def __init__(self, expression):
        self.expression = expression

class IfNode:
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

class ForNode:
    def __init__(self, initialization, condition, update, body):
        self.initialization = initialization
        self.condition = condition
        self.update = update
        self.body = body

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class BinaryOpNode:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class IdentifierNode:
    def __init__(self, name):
        self.name = name

class NumberNode:
    def __init__(self, value):
        self.value = value

class ExpressionStatementNode:
    def __init__(self, expression):
        self.expression = expression
