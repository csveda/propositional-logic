"""Provide means to interpret formulas."""

from lp.syntax import PropositionalSymbol, PontuationSymbol
from lp.syntax import Negation, Conjunction, Disjunction
from lp.syntax import Implication, BiImplication
from lp.syntax import OpeningParenthesis, ClosingParenthesis
from lp.syntax import UnaryOperator, BinaryOperator, Operator


class Scanner:
    """."""

    class Char:
        """Represents a read character."""

        def __init__(self, char):
            """Instantiate a char object."""
            self.value = char

        def is_a(self, token_type):
            """Check if the stored char is a token_type."""
            return token_type.accepts_initial_char(self.value)

    instance = None

    def __init__(self, expression):
        """Create a new scanner instance with the given expression."""
        self.expression = expression
        self.current_index = 0

    def get_current_char(self):
        """Return the char in the current index."""
        return self.expression[self.current_index]

    def check_current_index(self):
        """Check the current index."""
        if self.current_index > len(self.expression) - 1:
            self.current_index = len(self.expression) - 1

    def read_next_token(self):
        """Return the next token in the expression and tokenize it."""
        token = None
        current_char = Scanner.Char(self.get_current_char())

        if current_char.is_a(PropositionalSymbol):
            token = self.get_propositional_symbol(current_char)

        elif current_char.is_a(OpeningParenthesis):
            token = OpeningParenthesis(current_char.value)
            self.current_index += 1

        elif current_char.is_a(ClosingParenthesis):
            token = ClosingParenthesis(current_char.value)
            self.current_index += 1

        elif current_char.is_a(Implication):
            token = self.get_implication(current_char)

        elif current_char.is_a(Conjunction):
            token = Conjunction(current_char.value)
            self.current_index += 1

        elif current_char.is_a(Disjunction):
            token = Disjunction(current_char.value)
            self.current_index += 1

        elif current_char.is_a(BiImplication):
            token = self.get_bi_implication(current_char)

        else:
            raise Exception('Invalid syntax on char "%s"' % current_char.value)

        if token is None:
            raise Exception('Invalid syntax "%s"' % self.get_current_char())

        return token

    def get_propositional_symbol(self, char):
        """Read the expression until it is not a valid propositional_symbol."""
        token = None
        token_str = char.value
        self.current_index += 1

        for i in range(self.current_index, len(self.expression) + 1):
            if PropositionalSymbol.evaluate(token_str):
                if self.there_are_tokens():
                    token_str += self.expression[i]
                    self.current_index += 1
                else:
                    token = PropositionalSymbol(token_str)
            else:
                token = PropositionalSymbol(token_str[:-1])
                self.current_index -= 1
                break
        return token

    def get_implication(self, char):
        """Read the implication symbol in the expression."""
        try:
            token_str = char.value
            self.current_index += 1
            if self.there_are_tokens():
                token_str += self.get_current_char()
                self.current_index += 1
                token = None
                if Implication.evaluate(token_str):
                    token = Implication(token_str)
                else:
                    token = Negation('-')
                    self.current_index -= 1
            else:
                token = Negation('-')

        except IndexError:
            token = None
        return token

    def get_bi_implication(self, char):
        """Read the bi-implication symbol in the expression."""
        try:
            token_str = char.value
            self.current_index += 1
            token_str += self.get_current_char()
            self.current_index += 1
            token_str += self.get_current_char()
            self.current_index += 1
            token = None
            if BiImplication.evaluate(token_str):
                token = BiImplication(token_str)
        except IndexError:
            token = None
        return token

    def there_are_tokens(self):
        """Check if there are tokens to read."""
        return self.current_index < len(self.expression)


class Interpreter:
    """Ability to interpret a formula."""

    @classmethod
    def parse_expression(cls, expression):
        """
        Turn an expression to the Reverse Polish Notation (RPN).

        This method is an implementatin of the
        Djikstra's Shunting-yard algorithm.
        """
        scanner = Scanner(expression)

        output_queue = []
        operator_stack = []
        while scanner.there_are_tokens():
            token = scanner.read_next_token()

            if token.is_a(PropositionalSymbol):
                output_queue.append(token)

            elif token.is_a(Operator):
                o1 = token
                o2 = operator_stack[-1] if operator_stack \
                    and operator_stack[-1].is_a(Operator) else False
                while(
                    o2 and ((
                        (o1.associativity is Operator.Associativity.LEFT) and
                        (o1.precendence <= o2.precendence)
                    ) or (
                        (o1.associativity is Operator.Associativity.RIGHT) and
                        (o1.precendence < o2.precendence)
                    ))
                ):
                    output_queue.append(operator_stack.pop())
                    o2 = operator_stack[-1] if operator_stack \
                        and operator_stack[-1].is_a(Operator) else False

                operator_stack.append(o1)

            elif token.is_a(OpeningParenthesis):
                operator_stack.append(token)

            elif token.is_a(ClosingParenthesis):
                while(operator_stack and
                      not operator_stack[-1].is_a(OpeningParenthesis)):
                    output_queue.append(operator_stack.pop())

                if not operator_stack:
                    raise Exception('Parenthesis mismatched.')

                popped = operator_stack.pop()
                assert popped.is_a(OpeningParenthesis)

            else:
                raise Exception('Token mismatched.')

        while(operator_stack):
            if operator_stack[-1].is_a(PontuationSymbol):
                raise Exception('Parenthesis mismatched.')
            output_queue.append(operator_stack.pop())

        return cls.create_formula(output_queue)

    @classmethod
    def create_formula(cls, rpn_tokens):
        """Create a formula based on the expression RPN notation."""
        # Reverse the token list to use it like a stack
        rpn_tokens.reverse()
        formula_stack = []
        while rpn_tokens:
            token = rpn_tokens.pop()
            if token.is_a(PropositionalSymbol):
                formula_stack.append(token)
            elif token.is_a(UnaryOperator):
                arg = formula_stack.pop()
                token.set_arg(arg)
                formula_stack.append(token)
            elif token.is_a(BinaryOperator):
                arg2 = formula_stack.pop()
                arg1 = formula_stack.pop()
                token.set_args(arg1, arg2)
                formula_stack.append(token)
            else:
                raise Exception('Invalid RPN expression.')

        # The formula_stack must contain only the result formula
        assert len(formula_stack) is 1

        return formula_stack.pop()
