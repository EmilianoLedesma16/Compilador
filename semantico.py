class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, value=None):
        if name in self.symbols:
            raise Exception(f"Variable '{name}' ya declarada.")
        self.symbols[name] = value

    def assign(self, name, value):
        if name not in self.symbols:
            raise Exception(f"Variable '{name}' no declarada.")
        self.symbols[name] = value

    def lookup(self, name):
        if name not in self.symbols:
            raise Exception(f"Variable '{name}' no declarada.")
        return self.symbols[name]

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, node):
        method_name = f"analyze_{node.node_type}"
        method = getattr(self, method_name, self.no_analyze_method)
        return method(node)

    def no_analyze_method(self, node):
        raise Exception(f"No se puede analizar el nodo: {node.node_type}")

    def analyze_Program(self, node):
        for child in node.children:
            self.analyze(child)

    def analyze_Block(self, node):
        for child in node.children:
            self.analyze(child)

    def analyze_Declaration(self, node):
        var_name = node.value
        expr_value = self.analyze(node.children[0])  # Analizar la expresión asignada
        self.symbol_table.declare(var_name, expr_value)

    def analyze_Print(self, node):
        expr_value = self.analyze(node.children[0])  # Analizar la expresión a imprimir
        return expr_value

    def analyze_Number(self, node):
        return int(node.value)

    def analyze_Identifier(self, node):
        return self.symbol_table.lookup(node.value)

# Prueba del Analizador Semántico
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

    # Análisis semántico
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    print("Tabla de símbolos:", analyzer.symbol_table.symbols)
