class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def consume(self, expected_type=None, expected_value=None):
        if expected_type and self.current_token[0] != expected_type:
            raise Exception(
                f"Error sintáctico: Se esperaba tipo '{expected_type}', pero se obtuvo '{self.current_token[0]}'."
            )
        if expected_value and self.current_token[1] != expected_value:
            raise Exception(
                f"Error sintáctico: Se esperaba valor '{expected_value}', pero se obtuvo '{self.current_token[1]}'."
            )
        self.current_token_index += 1
        self.current_token = (
            self.tokens[self.current_token_index]
            if self.current_token_index < len(self.tokens)
            else ('EOF', None)
        )

    def parse_program(self):
        self.consume('KEYWORD', 'inicio')
        self.consume('SYMBOL', '{')
        block = self.parse_block()
        self.consume('SYMBOL', '}')
        self.consume('KEYWORD', 'fin')
        return ProgramNode(block)

    def parse_block(self):
        statements = []
        while self.current_token[0] != 'SYMBOL' or self.current_token[1] != '}':
            statements.append(self.parse_statement())
        return BlockNode(statements)

    def parse_statement(self):
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
        raise Exception(f"Error sintáctico: Instrucción no válida '{self.current_token[1]}'.")

    def parse_declaration(self):
        self.consume('KEYWORD', 'var')
        identifier = self.current_token[1]
        self.consume('IDENTIFIER')
        self.consume('OPERATOR', '=')
        expression = self.parse_expression()
        self.consume('SYMBOL', ';')
        return DeclarationNode(identifier, expression)

    def parse_print(self):
        self.consume('KEYWORD', 'imprimir')
        self.consume('SYMBOL', '(')
        expression = self.parse_expression()
        self.consume('SYMBOL', ')')
        self.consume('SYMBOL', ';')
        return PrintNode(expression)

    def parse_if(self):
        self.consume('KEYWORD', 'if')
        self.consume('SYMBOL', '(')
        condition = self.parse_expression()
        self.consume('SYMBOL', ')')
        self.consume('SYMBOL', '{')
        true_block = self.parse_block()
        self.consume('SYMBOL', '}')

        false_block = None
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
            self.consume('KEYWORD', 'else')
            self.consume('SYMBOL', '{')
            false_block = self.parse_block()
            self.consume('SYMBOL', '}')

        return IfNode(condition, true_block, false_block)

    def parse_for(self):
        self.consume('KEYWORD', 'for')
        self.consume('SYMBOL', '(')
        initialization = self.parse_declaration()
        condition = self.parse_expression()
        self.consume('SYMBOL', ';')
        update = self.parse_expression()
        self.consume('SYMBOL', ')')
        self.consume('SYMBOL', '{')
        body = self.parse_block()
        self.consume('SYMBOL', '}')
        return ForNode(initialization, condition, update, body)


    def parse_while(self):
        self.consume('KEYWORD', 'while')
        self.consume('SYMBOL', '(')
        condition = self.parse_expression()
        self.consume('SYMBOL', ')')
        self.consume('SYMBOL', '{')
        body = self.parse_block()
        self.consume('SYMBOL', '}')
        return WhileNode(condition, body)

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ['+', '-']:
            operator = self.current_token[1]
            self.consume('OPERATOR')
            right = self.parse_term()
            left = BinaryOpNode(operator, left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ['*', '/']:
            operator = self.current_token[1]
            self.consume('OPERATOR')
            right = self.parse_factor()
            left = BinaryOpNode(operator, left, right)
        return left

    def parse_factor(self):
        token = self.current_token
        if token[0] == 'NUMBER':
            self.consume('NUMBER')
            return NumberNode(token[1])
        elif token[0] == 'IDENTIFIER':
            self.consume('IDENTIFIER')
            return IdentifierNode(token[1])
        elif token[0] == 'SYMBOL' and token[1] == '(':
            self.consume('SYMBOL', '(')
            expression = self.parse_expression()
            self.consume('SYMBOL', ')')
            return expression
        raise Exception(f"Error sintáctico: Factor no válido '{token[1]}'.")

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
