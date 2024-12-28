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

class Simulator:
    def __init__(self, semantic_analyzer):
        self.semantic_analyzer = semantic_analyzer
        self.symbol_table = {}

    def run(self, ast):
        if isinstance(ast, ProgramNode):
            self.run(ast.block)
        elif isinstance(ast, BlockNode):
            for statement in ast.statements:
                self.run(statement)
        elif isinstance(ast, DeclarationNode):
            self.run_declaration(ast)
        elif isinstance(ast, PrintNode):
            self.run_print(ast)
        elif isinstance(ast, IfNode):
            self.run_if(ast)
        elif isinstance(ast, ForNode):
            self.run_for(ast)
        elif isinstance(ast, WhileNode):
            self.run_while(ast)
        elif isinstance(ast, BinaryOpNode):
            return self.run_binary_op(ast)
        elif isinstance(ast, IdentifierNode):
            return self.run_identifier(ast)
        elif isinstance(ast, NumberNode):
            return int(ast.value)  # Convertir el valor a entero para simplificar
        else:
            raise Exception(f"Error en ejecución: Nodo no reconocido '{type(ast).__name__}'.")

    def run_declaration(self, node):
        value = self.evaluate_expression(node.expression)
        self.symbol_table[node.identifier] = value

    def run_print(self, node):
        value = self.evaluate_expression(node.expression)
        print(value)

    def run_if(self, node):
        condition = self.evaluate_expression(node.condition)
        if condition != 0:
            self.run(node.true_block)
        elif node.false_block:
            self.run(node.false_block)

    def run_for(self, node):
        self.run(node.initialization)
        while self.evaluate_expression(node.condition) != 0:
            self.run(node.body)
            self.evaluate_expression(node.update)

    def run_while(self, node):
        while self.evaluate_expression(node.condition) != 0:
            self.run(node.body)

    def run_binary_op(self, node):
        left = self.evaluate_expression(node.left)
        right = self.evaluate_expression(node.right)

        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise Exception("Error en ejecución: División por cero.")
            return left // right  # División entera
        else:
            raise Exception(f"Error en ejecución: Operador no reconocido '{node.operator}'.")

    def run_identifier(self, node):
        if node.name not in self.symbol_table:
            raise Exception(f"Error en ejecución: La variable '{node.name}' no está definida.")
        return self.symbol_table[node.name]

    def evaluate_expression(self, node):
        return self.run(node)

# Este archivo utiliza el AST validado para simular la ejecución del programa.
