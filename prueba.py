from lexico import Lexer
from sintactico import Parser
from semantico import SemanticAnalyzer

# Programa de prueba
code = """
inicio {
    var x = 10;
    var y = 20;
    var z = x + y;
    imprimir z;
} fin
"""

# Paso 1: Análisis léxico
lexer = Lexer(code)
tokens = lexer.tokenize()

print("Tokens generados:")
for token in tokens:
    print(token)

# Paso 2: Análisis sintáctico
parser = Parser(tokens)
try:
    ast = parser.parse()
    print("\nAST generado:")
    print(ast)

    # Paso 3: Análisis semántico
    try:
        analyzer = SemanticAnalyzer(ast)
        analyzer.analyze()
    except Exception as e:
        print("\nError durante el análisis semántico:")
        print(e)
except Exception as e:
    print("\nError durante el análisis sintáctico:")
    print(e)
