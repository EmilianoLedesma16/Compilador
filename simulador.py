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

class RuntimeError(Exception):
    """Clase personalizada para errores en tiempo de ejecución."""
    def __init__(self, message, line=0, column=0):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        if self.line > 0 and self.column > 0:
            return f"Línea {self.line}, Columna {self.column}: {self.message}"
        return self.message


class Simulator:
    def __init__(self, semantic_analyzer):
        self.semantic_analyzer = semantic_analyzer
        self.symbol_table = {}
        self.output = []  # Acumula la salida para mostrarla en la GUI

    def run(self, ast):
        try:
            self._run(ast)
            return "\n".join(self.output)  # Devuelve la salida acumulada
        except RuntimeError as e:
            return str(e)  # Devuelve el error como texto

    def _run(self, ast):
        if isinstance(ast, ProgramNode):
            self._run(ast.block)
        elif isinstance(ast, BlockNode):
            for statement in ast.statements:
                self._run(statement)
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
            raise RuntimeError(f"Error en ejecución: Nodo no reconocido '{type(ast).__name__}'.")

    def run_declaration(self, node):
        value = self.evaluate_expression(node.expression)
        self.symbol_table[node.identifier] = value

    def run_print(self, node):
        value = self.evaluate_expression(node.expression)
        self.output.append(str(value))  # Captura la salida en lugar de imprimir

    def run_if(self, node):
        condition = self.evaluate_expression(node.condition)
        if condition != 0:
            self._run(node.true_block)
        elif node.false_block:
            self._run(node.false_block)

    def run_for(self, node):
        self.run_declaration(node.initialization)
        while self.evaluate_expression(node.condition) != 0:
            self._run(node.body)
            self.evaluate_expression(node.update)

    def run_while(self, node):
        while self.evaluate_expression(node.condition) != 0:
            self._run(node.body)

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
                raise RuntimeError("División por cero.")
            return left // right  # División entera
        else:
            raise RuntimeError(f"Operador no reconocido '{node.operator}'.")

    def run_identifier(self, node):
        if node.name not in self.symbol_table:
            raise RuntimeError(f"La variable '{node.name}' no está definida.")
        return self.symbol_table[node.name]

    def evaluate_expression(self, node):
        return self._run(node)
