class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t[0] != 'NEWLINE']  # Filtrar NEWLINE
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.stack = ['$']  # Pila inicializada con el símbolo de fin de entrada

        # Tabla LL(1)
        self.table = {
            'Program': {'inicio': ['inicio', '{', 'Block', '}', 'fin']},
            'Block': {
                'var': ['Statement', 'Block'],
                'IDENTIFIER': ['Statement', 'Block'],
                'imprimir': ['Statement', 'Block'],
                '}': ['ε']  # epsilon para finalizar el bloque
            },
            'Statement': {
                'var': ['Declaration'],
                'IDENTIFIER': ['Assignment'],
                'imprimir': ['Print']
            },
            'Declaration': {'var': ['var', 'IDENTIFIER', '=', 'Expression', ';']},
            'Assignment': {'IDENTIFIER': ['IDENTIFIER', '=', 'Expression', ';']},
            'Print': {'imprimir': ['imprimir', 'Expression', ';']},
            'Expression': {
                'IDENTIFIER': ['Term', "Expression'"],
                'NUMBER': ['Term', "Expression'"],
                '(': ['Term', "Expression'"]
            },
            "Expression'": {
                '+': ['+', 'Term', "Expression'"],
                '-': ['-', 'Term', "Expression'"],
                ';': ['ε'],  # epsilon para finalizar la expresión
                ')': ['ε'],
                '}': ['ε'],
                '$': ['ε']  # Final del archivo
            },
            'Term': {
                'IDENTIFIER': ['Factor', "Term'"],
                'NUMBER': ['Factor', "Term'"],
                '(': ['Factor', "Term'"]
            },
            "Term'": {
                '*': ['*', 'Factor', "Term'"],
                '/': ['/', 'Factor', "Term'"],
                '+': ['ε'],
                '-': ['ε'],
                ';': ['ε'],  # epsilon para finalizar el término
                ')': ['ε'],
                '}': ['ε'],
                '$': ['ε']  # Final del archivo
            },
            'Factor': {
                'NUMBER': ['NUMBER'],
                'IDENTIFIER': ['IDENTIFIER'],
                '(': ['(', 'Expression', ')']
            }
        }

        self.ast = []

    def advance(self):
        """Avanza al siguiente token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = ('$', None)

    def raise_error(self, message):
        """Lanza un error sintáctico con contexto claro."""
        line, column = self.current_token[2], self.current_token[3]
        raise Exception(f"{message} en línea {line}, columna {column}. Token encontrado: {self.current_token}")

    def parse(self):
        """Inicia el análisis sintáctico y genera el AST."""
        self.stack.append('Program')
        current_node = {'Program': []}
        self.ast = [current_node]
        parent_stack = [current_node['Program']]  # Rastreo de nodos padres

        while self.stack:
            top = self.stack.pop()
            print(f"Pila: {self.stack}, Top: {top}, Token actual: {self.current_token}")

            if top == 'ε':
                # Ignorar nodos vacíos
                continue

            if top in self.table:
                production = self.table[top].get(self.current_token[0]) or self.table[top].get(self.current_token[1])
                if production is None:
                    self.raise_error(f"Error: No hay producción para {top} con token {self.current_token}")
                print(f"Producción seleccionada para {top}: {production}")
                self.stack.extend(reversed(production))

                # Agregar un nodo solo si tiene hijos relevantes
                new_node = {top: []}
                parent_stack[-1].append(new_node)
                parent_stack.append(new_node[top])

            elif top == self.current_token[0] or top == self.current_token[1]:
                # Agregar token al nodo actual
                print(f"Coincidencia encontrada: {top}")
                parent_stack[-1].append(self.current_token)
                self.advance()

            else:
                self.raise_error(f"Error: Se esperaba {top}")

            # Si el nodo actual ya no tiene hijos pendientes, volver al nodo padre
            while parent_stack and isinstance(parent_stack[-1], list) and not self.stack:
                parent_stack.pop()

        if self.current_token[0] != '$':
            raise Exception("Error: Entrada no completamente consumida.")

        print("Análisis sintáctico completado sin errores.")
        return self.ast
