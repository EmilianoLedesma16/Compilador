class SemanticAnalyzer:
    def __init__(self, ast):
        if ast is None or not isinstance(ast, list):
            raise ValueError("Error: El AST proporcionado no es válido.")
        self.ast = ast
        self.symbol_table = {}  # Tabla de símbolos para almacenar variables y valores

    def analyze(self):
        """Inicia el análisis semántico recorriendo el AST."""
        print("\nIniciando análisis semántico...")
        for node in self.ast:
            print(f"\nProcesando nodo principal: {node}")  # Log de nivel alto
            self.process_node(node)
        print("\nAnálisis semántico completado sin errores.")

    def process_node(self, node):
        """Procesa un nodo del AST de forma recursiva."""
        print(f"Entrando a process_node con nodo: {node}")
        if isinstance(node, dict):  # Nodo con hijos
            for key, children in node.items():
                print(f"Clave actual: {key}, Hijos: {children}")
                if key == 'Program':  # Nodo raíz
                    self.process_node(children)
                elif key == 'Block':  # Nodo de bloque
                    for statement in children:
                        self.process_node(statement)
                elif key == 'Statement':  # Nodo de statement
                    for statement_type in children:
                        self.process_node(statement_type)
                elif key == 'Declaration':  # Declaración de variable
                    self.handle_variable_declaration(children)
                elif key == 'Print':  # Sentencia de impresión
                    self.handle_print_statement(children)
                elif key == 'Expression':  # Nodo de expresión
                    return self.evaluate_expression(children)
                else:
                    print(f"Nodo no reconocido: {key}. Procesando recursivamente...")
                    self.process_node(children)

        elif isinstance(node, list):  # Lista de nodos
            for child in node:
                print(f"Procesando lista de nodos: {child}")
                self.process_node(child)
        else:
            print(f"Tipo de nodo inesperado: {node}")

    def handle_variable_declaration(self, children):
        """Maneja la declaración de variables."""
        print(f"Manejando declaración de variable: {children}")
        identifier = None
        value = None

        for token in children:
            print(f"Token en declaración: {token}")
            if isinstance(token, tuple) and token[0] == 'IDENTIFIER':
                identifier = token[1]
            elif isinstance(token, dict) and 'Expression' in token:
                value = self.evaluate_expression(token['Expression'])

        if identifier is None:
            raise Exception("Error semántico: Falta identificador en declaración.")
        if value is None:
            raise Exception(f"Error semántico: Falta valor para la variable '{identifier}'.")

        self.symbol_table[identifier] = value
        print(f"Variable declarada: {identifier} = {value}")

    def handle_print_statement(self, children):
        """Maneja las sentencias de impresión."""
        print(f"Manejando sentencia de impresión: {children}")
        for token in children:
            if isinstance(token, tuple) and token[0] == 'IDENTIFIER':
                identifier = token[1]
                if identifier not in self.symbol_table:
                    raise Exception(f"Error semántico: La variable '{identifier}' no está declarada.")
                print(f"Imprimiendo: {identifier} = {self.symbol_table[identifier]}")

    def evaluate_expression(self, expression):
        """Evalúa una expresión para obtener su valor."""
        print(f"Evaluando expresión: {expression}")
        if not isinstance(expression, list):
            raise Exception("Error semántico: Expresión no válida.")

        value_stack = []  # Pila para valores numéricos
        operator_stack = []  # Pila para operadores

        for token in expression:
            print(f"Token en expresión: {token}")
            if isinstance(token, tuple):
                if token[0] == 'NUMBER':
                    value_stack.append(int(token[1]))
                elif token[0] == 'IDENTIFIER':
                    if token[1] not in self.symbol_table:
                        raise Exception(f"Error semántico: La variable '{token[1]}' no está declarada.")
                    value_stack.append(self.symbol_table[token[1]])
                elif token[0] == 'OPERATOR':
                    operator_stack.append(token[1])
            elif isinstance(token, dict):
                for key, value in token.items():
                    if key == 'Expression':
                        value_stack.append(self.evaluate_expression(value))
            elif isinstance(token, list):  # Manejo de sub-listas
                value_stack.append(self.evaluate_expression(token))
            else:
                raise Exception(f"Error semántico: Nodo inesperado en expresión: {token}")

        print(f"Pila de valores antes de procesar operadores: {value_stack}")
        print(f"Pila de operadores: {operator_stack}")
        while operator_stack:
            if len(value_stack) < 2:
                raise Exception("Error semántico: Expresión incompleta.")
            right = value_stack.pop()
            left = value_stack.pop()
            operator = operator_stack.pop()
            result = self.apply_operator(left, operator, right)
            value_stack.append(result)
            print(f"Resultado parcial: {result}")

        if len(value_stack) != 1:
            raise Exception("Error semántico: Expresión no válida.")
        return value_stack.pop()

    def apply_operator(self, left, operator, right):
        """Aplica un operador a dos valores."""
        print(f"Aplicando operador: {left} {operator} {right}")
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise Exception("Error semántico: División por cero.")
            return left // right
        else:
            raise Exception(f"Error semántico: Operador desconocido '{operator}'.")
