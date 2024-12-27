class Interpreter:
    def __init__(self):
        self.symbol_table = {}  # Tabla de símbolos local para el intérprete

    def interpret(self, node):
        method_name = f"visit_{node.node_type}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No se puede interpretar el nodo: {node.node_type}")

    def visit_Program(self, node):
        for child in node.children:
            self.interpret(child)

    def visit_Block(self, node):
        for child in node.children:
            self.interpret(child)

    def visit_Declaration(self, node):
        var_name = node.value
        expr_value = self.interpret(node.children[0])  # Obtener el valor de la expresión
        self.symbol_table[var_name] = expr_value

    def visit_Print(self, node):
        expr_value = self.interpret(node.children[0])  # Obtener el valor a imprimir
        print(expr_value)

    def visit_Number(self, node):
        return int(node.value)

    def visit_Identifier(self, node):
        var_name = node.value
        if var_name not in self.symbol_table:
            raise Exception(f"Variable no definida: {var_name}")
        return self.symbol_table[var_name]

# Prueba del Intérprete
if __name__ == "__main__":
    from sintactico import ASTNode  # Importar la clase ASTNode del parser

    # Simulación de un AST generado por el parser
    ast = ASTNode("Program")
    block = ASTNode("Block")
    ast.add_child(block)

    # Declaración: var x = 10;
    declaration = ASTNode("Declaration", "x")
    declaration.add_child(ASTNode("Number", "10"))
    block.add_child(declaration)

    # Impresión: imprimir(x);
    print_stmt = ASTNode("Print")
    print_stmt.add_child(ASTNode("Identifier", "x"))
    block.add_child(print_stmt)

    # Ejecutar el intérprete
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("Estado final de la tabla de símbolos:", interpreter.symbol_table)
