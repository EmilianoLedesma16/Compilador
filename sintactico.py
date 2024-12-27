class ASTNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"{self.node_type}({self.value}, {self.children})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def match(self, token_type, value=None):
        if self.current < len(self.tokens):
            token = self.tokens[self.current]
            if token[0] == token_type and (value is None or token[1] == value):
                self.current += 1
                return token
        return None

    def parse_program(self):
        node = ASTNode("Program")

        if not self.match("KEYWORD", "inicio"):
            raise Exception("Se esperaba 'inicio'")

        node.add_child(self.parse_block())

        if not self.match("KEYWORD", "fin"):
            raise Exception("Se esperaba 'fin'")

        return node

    def parse_block(self):
        if not self.match("SYMBOL", "{"):
            raise Exception("Se esperaba '{'")

        block_node = ASTNode("Block")

        while not self.match("SYMBOL", "}"):
            block_node.add_child(self.parse_statement())

        return block_node

    def parse_statement(self):
        token = self.tokens[self.current]

        if token[0] == "KEYWORD" and token[1] == "var":
            return self.parse_declaration()
        elif token[0] == "KEYWORD" and token[1] == "imprimir":
            return self.parse_print()
        else:
            raise Exception(f"Instrucción no válida: {token}")

    def parse_declaration(self):
        self.match("KEYWORD", "var")

        identifier = self.match("IDENTIFIER")
        if not identifier:
            raise Exception("Se esperaba un identificador")

        if not self.match("OPERATOR", "="):
            raise Exception("Se esperaba '='")

        expression = self.parse_expression()

        if not self.match("SYMBOL", ";"):
            raise Exception("Se esperaba ';'")

        node = ASTNode("Declaration", identifier[1])
        node.add_child(expression)
        return node

    def parse_print(self):
        self.match("KEYWORD", "imprimir")

        if not self.match("SYMBOL", "("):
            raise Exception("Se esperaba '('")

        expression = self.parse_expression()

        if not self.match("SYMBOL", ")"):
            raise Exception("Se esperaba ')'")

        if not self.match("SYMBOL", ";"):
            raise Exception("Se esperaba ';'")

        node = ASTNode("Print")
        node.add_child(expression)
        return node

    def parse_expression(self):
        token = self.tokens[self.current]

        if token[0] == "NUMBER":
            self.current += 1
            return ASTNode("Number", token[1])
        elif token[0] == "IDENTIFIER":
            self.current += 1
            return ASTNode("Identifier", token[1])
        else:
            raise Exception(f"Expresión no válida: {token}")

# Prueba del parser
if __name__ == "__main__":
    tokens = [
        ("KEYWORD", "inicio"),
        ("SYMBOL", "{"),
        ("KEYWORD", "var"), ("IDENTIFIER", "x"), ("OPERATOR", "="), ("NUMBER", "10"), ("SYMBOL", ";"),
        ("KEYWORD", "imprimir"), ("SYMBOL", "("), ("IDENTIFIER", "x"), ("SYMBOL", ")"), ("SYMBOL", ";"),
        ("SYMBOL", "}"),
        ("KEYWORD", "fin")
    ]

    parser = Parser(tokens)
    ast = parser.parse_program()
    print(ast)
