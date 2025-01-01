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

class SemanticError(Exception):
    """Clase personalizada para errores semánticos."""
    def __init__(self, message, line, column):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"Línea {self.line}, Columna {self.column}: {self.message}"


class SemanticAnalyzer:
    def __init__(self):
        # Pila de tablas de símbolos para manejar ámbitos
        self.symbol_table_stack = [{}]

    def current_symbol_table(self):
        """Obtiene la tabla de símbolos del ámbito actual."""
        return self.symbol_table_stack[-1]

    def push_scope(self):
        """Crea un nuevo ámbito."""
        self.symbol_table_stack.append({})

    def pop_scope(self):
        """Elimina el ámbito actual."""
        self.symbol_table_stack.pop()

    def analyze(self, ast):
        try:
            self._analyze(ast)
        except SemanticError as e:
            return str(e)  # Devuelve el error como texto
        return "Análisis semántico completado sin errores."

    def _analyze(self, ast):
        if isinstance(ast, ProgramNode):
            self._analyze(ast.block)
        elif isinstance(ast, BlockNode):
            self.push_scope()
            for statement in ast.statements:
                self._analyze(statement)
            self.pop_scope()
        elif isinstance(ast, DeclarationNode):
            self._analyze_declaration(ast)
        elif isinstance(ast, PrintNode):
            self._analyze_expression(ast.expression)
        elif isinstance(ast, IfNode):
            self._analyze_if(ast)
        elif isinstance(ast, ForNode):
            self._analyze_for(ast)
        elif isinstance(ast, WhileNode):
            self._analyze_while(ast)
        elif isinstance(ast, BinaryOpNode):
            self._analyze_binary_op(ast)
        elif isinstance(ast, IdentifierNode):
            self._analyze_identifier(ast)
        elif isinstance(ast, NumberNode):
            pass  # Los números siempre son válidos
        else:
            raise SemanticError(f"Nodo no reconocido: '{type(ast).__name__}'.", 0, 0)

    def _analyze_declaration(self, node):
        current_table = self.current_symbol_table()
        if node.identifier in current_table:
            raise SemanticError(
                f"La variable '{node.identifier}' ya está declarada en este ámbito.",
                0, 0
            )
        value_type = self._evaluate_expression(node.expression)
        current_table[node.identifier] = value_type

    def _analyze_if(self, node):
        condition_type = self._evaluate_expression(node.condition)
        if condition_type != 'number':
            raise SemanticError(
                "La condición del 'if' debe ser un número (0 para falso, diferente de 0 para verdadero).",
                0, 0
            )
        self._analyze(node.true_block)
        if node.false_block:
            self._analyze(node.false_block)

    def _analyze_for(self, node):
        self._analyze(node.initialization)
        condition_type = self._evaluate_expression(node.condition)
        if condition_type != 'number':
            raise SemanticError("La condición del 'for' debe ser un número.", 0, 0)
        self._evaluate_expression(node.update)
        self._analyze(node.body)

    def _analyze_while(self, node):
        condition_type = self._evaluate_expression(node.condition)
        if condition_type != 'number':
            raise SemanticError("La condición del 'while' debe ser un número.", 0, 0)
        self._analyze(node.body)

    def _analyze_binary_op(self, node):
        left_type = self._evaluate_expression(node.left)
        right_type = self._evaluate_expression(node.right)
        if left_type != right_type:
            raise SemanticError("Los operandos de una operación deben ser del mismo tipo.", 0, 0)
        return left_type

    def _analyze_identifier(self, node):
        current_table = self.current_symbol_table()
        if node.name not in current_table:
            raise SemanticError(
                f"La variable '{node.name}' no está declarada.",
                0, 0
            )
        return current_table[node.name]

    def _evaluate_expression(self, node):
        if isinstance(node, NumberNode):
            return 'number'
        elif isinstance(node, IdentifierNode):
            return self._analyze_identifier(node)
        elif isinstance(node, BinaryOpNode):
            return self._analyze_binary_op(node)
        else:
            raise SemanticError(f"Expresión no válida: '{type(node).__name__}'.", 0, 0)
