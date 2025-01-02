class Simulator:
    def __init__(self, semantic_analyzer):
        """
        Inicializa el simulador con los resultados del análisis semántico.
        :param semantic_analyzer: El analizador semántico con la tabla de símbolos.
        """
        self.semantic_analyzer = semantic_analyzer
        self.variables = {}  # Almacenará los valores de las variables

    def run(self, ast):
        """
        Ejecuta el programa a partir del AST generado.
        :param ast: El árbol de sintaxis abstracta generado por el analizador sintáctico.
        :return: La salida simulada del programa.
        """
        try:
            output = self.execute_block(ast)
            return output
        except Exception as e:
            return f"Error en la simulación: {str(e)}"

    def execute_block(self, block):
        """
        Ejecuta un bloque de instrucciones.
        :param block: El bloque de instrucciones en forma de AST.
        :return: La salida generada por el bloque.
        """
        output = ""
        for statement in block:
            if statement["type"] == "declaration":
                self.execute_declaration(statement)
            elif statement["type"] == "assignment":
                self.execute_assignment(statement)
            elif statement["type"] == "print":
                output += self.execute_print(statement) + "\n"
        return output

    def execute_declaration(self, statement):
        """
        Ejecuta una declaración de variable.
        :param statement: La instrucción de declaración.
        """
        var_name = statement["identifier"]
        value = self.evaluate_expression(statement["expression"])
        if var_name in self.variables:
            raise Exception(f"La variable '{var_name}' ya ha sido declarada.")
        self.variables[var_name] = value

    def execute_assignment(self, statement):
        """
        Ejecuta una asignación de variable.
        :param statement: La instrucción de asignación.
        """
        var_name = statement["identifier"]
        value = self.evaluate_expression(statement["expression"])
        if var_name not in self.variables:
            raise Exception(f"La variable '{var_name}' no ha sido declarada.")
        self.variables[var_name] = value

    def execute_print(self, statement):
        """
        Ejecuta una instrucción de impresión.
        :param statement: La instrucción de impresión.
        :return: El valor que se imprimirá.
        """
        return str(self.evaluate_expression(statement["expression"]))

    def evaluate_expression(self, expression):
        """
        Evalúa una expresión aritmética.
        :param expression: La expresión en forma de AST.
        :return: El valor de la expresión.
        """
        if expression["type"] == "number":
            return expression["value"]
        elif expression["type"] == "identifier":
            var_name = expression["value"]
            if var_name not in self.variables:
                raise Exception(f"La variable '{var_name}' no ha sido declarada.")
            return self.variables[var_name]
        elif expression["type"] == "binary_operation":
            left = self.evaluate_expression(expression["left"])
            right = self.evaluate_expression(expression["right"])
            operator = expression["operator"]

            if operator == "+":
                return left + right
            elif operator == "-":
                return left - right
            elif operator == "*":
                return left * right
            elif operator == "/":
                if right == 0:
                    raise Exception("Error: División entre cero.")
                return left / right
            else:
                raise Exception(f"Operador desconocido: {operator}")
        else:
            raise Exception(f"Tipo de expresión desconocido: {expression['type']}")
