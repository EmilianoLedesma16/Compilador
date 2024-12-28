from sintactico import (
    ProgramNode,
    BlockNode,
    DeclarationNode,
    PrintNode,
    IfNode,
    ForNode,
    WhileNode,
    BinaryOpNode,
    IdentifierNode,
    NumberNode
)


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, ast):
        if isinstance(ast, ProgramNode):
            self.analyze(ast.block)
        elif isinstance(ast, BlockNode):
            for statement in ast.statements:
                self.analyze(statement)
        elif isinstance(ast, DeclarationNode):
            self.analyze_declaration(ast)
        elif isinstance(ast, PrintNode):
            self.analyze_expression(ast.expression)
        elif isinstance(ast, IfNode):
            self.analyze_if(ast)
        elif isinstance(ast, ForNode):
            self.analyze_for(ast)
        elif isinstance(ast, WhileNode):
            self.analyze_while(ast)
        elif isinstance(ast, BinaryOpNode):
            self.analyze_binary_op(ast)
        elif isinstance(ast, IdentifierNode):
            self.analyze_identifier(ast)
        elif isinstance(ast, NumberNode):
            pass  # Los números son siempre válidos
        else:
            raise Exception(f"Error semántico: Nodo no reconocido '{type(ast).__name__}'.")

    def analyze_declaration(self, node):
        if node.identifier in self.symbol_table:
            raise Exception(f"Error semántico: La variable '{node.identifier}' ya está declarada.")
        value_type = self.evaluate_expression(node.expression)
        self.symbol_table[node.identifier] = value_type

    def analyze_if(self, node):
        condition_type = self.evaluate_expression(node.condition)
        if condition_type != 'number':
            raise Exception("Error semántico: La condición del 'if' debe ser un número (0 para falso, diferente de 0 para verdadero).")
        self.analyze(node.true_block)
        if node.false_block:
            self.analyze(node.false_block)

    def analyze_for(self, node):
        self.analyze(node.initialization)
        condition_type = self.evaluate_expression(node.condition)
        if condition_type != 'number':
            raise Exception("Error semántico: La condición del 'for' debe ser un número.")
        self.evaluate_expression(node.update)
        self.analyze(node.body)

    def analyze_while(self, node):
        condition_type = self.evaluate_expression(node.condition)
        if condition_type != 'number':
            raise Exception("Error semántico: La condición del 'while' debe ser un número.")
        self.analyze(node.body)

    def analyze_binary_op(self, node):
        left_type = self.evaluate_expression(node.left)
        right_type = self.evaluate_expression(node.right)
        if left_type != right_type:
            raise Exception("Error semántico: Los operandos de una operación deben ser del mismo tipo.")
        return left_type

    def analyze_identifier(self, node):
        if node.name not in self.symbol_table:
            raise Exception(f"Error semántico: La variable '{node.name}' no está declarada.")
        return self.symbol_table[node.name]

    def evaluate_expression(self, node):
        if isinstance(node, NumberNode):
            return 'number'
        elif isinstance(node, IdentifierNode):
            return self.analyze_identifier(node)
        elif isinstance(node, BinaryOpNode):
            return self.analyze_binary_op(node)
        else:
            raise Exception(f"Error semántico: Expresión no válida '{type(node).__name__}'.")

# Este archivo verifica que el AST generado sea semánticamente válido y utiliza una tabla de símbolos para rastrear variables.
