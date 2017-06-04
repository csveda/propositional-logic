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
            if PropositionalSymbol.check(token_str):
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
                if Implication.check(token_str):
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
            if BiImplication.check(token_str):
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


class Formula:
    """Describe some formula properties and operations."""

    def __init__(self, formula):
        """."""
        self.formula = formula

    def get_subformulas(self):
        """Separate the propositional symbols of the subformulas list."""
        subformulas = []
        propositional_symbols = []
        for formula in self._get_subformulas():
            if formula.is_a(PropositionalSymbol):
                propositional_symbols.append(formula)
            else:
                subformulas.append(formula)
        return subformulas, propositional_symbols

    def _get_subformulas(self):
        """Get the formula subformulas without repetion."""
        subformulas = self.formula.subformulas()
        treated_subformulas = {}
        for formula in subformulas:
            formula_repr = formula.str_representation()
            if formula_repr not in treated_subformulas:
                treated_subformulas[formula_repr] = formula
        return list(treated_subformulas.values())


class TruthTable:
    """Represent a truth table of a formula."""

    def __init__(self, expression):
        """."""
        self.formula = Interpreter.parse_expression(expression)
        self.formula_handler = Formula(self.formula)
        self.build()

    def build(self):
        """Build the truth table for the given formula."""
        subformulas, prop_symbols = self.formula_handler.get_subformulas()
        subformulas = self.order_lexicographically(subformulas)
        prop_symbols = self.order_lexicographically(prop_symbols)
        self.prop_symbols = prop_symbols
        self.subformulas = subformulas

        m = len(subformulas)
        n = len(prop_symbols)
        lines_quantity = 2**n

        # First line is the subformulas
        lines = [[formula for formula in (prop_symbols + subformulas)]]

        # Initialize all lines with n + m columns
        for j in range(0, lines_quantity):
            lines.append([[] for k in range(0, n + m)])

        # Fill the propositional symbols with all possible values
        i = n
        while i > 0:
            value = True
            count = 0
            for line_index in range(1, lines_quantity + 1):
                if count == 2**(n - i):
                    value = not value
                    count = 0
                line = lines[line_index]
                line[i - 1] = value
                count += 1
            i -= 1

        # Calculate the subformulas values
        i = n + 1
        while i <= (m + n):
            for line_index in range(1, lines_quantity + 1):
                line = lines[line_index]
                current_formula = lines[0][i - 1]
                line[i - 1] = current_formula.evaluate(
                    self.get_symbols_value_for_line(line_index, lines=lines)
                )
            i += 1

        self.lines = lines

    def order_lexicographically(self, formulas):
        """Order a set of formulas lexicographically."""
        # TO-DO
        return formulas

    def get_symbols_value_for_line(self, line_index, lines=False):
        """
        Get the value of propositional symbols for a given line.

        Return dict like: {'p': True, 'q': False}
        """
        if not lines:
            lines = self.lines

        propositional_symbols = {
            i: symbol
            for i, symbol in enumerate(self.prop_symbols)
        }
        return {
            propositional_symbols[i].str_representation(): lines[line_index][i]
            for i, symbol in enumerate(self.prop_symbols)
        }

    def get_formula_models(self, formula):
        """
        Get the formula models.

        The models of a formula is all valuations that are true.
        """
        models = {}
        valuations = self.get_formula_valuations(formula)
        for line_index, valuation in valuations.items():
            if valuation[1] is True:
                models[line_index] = valuation
        return models

    def get_formula_valuations(self, formula):
        """Get the valuations of a given formula by querying truth table."""
        formula_column = self.get_formula_index(formula)
        valuations = {}
        for line_index, line in enumerate(self.lines):
            # Skip first line, because it is the formulas
            if line_index is 0:
                continue
            symbols_values = self.get_symbols_value_for_line(line_index)
            valuations[line_index] = (symbols_values, line[formula_column])
        return valuations

    def get_formula_index(self, formula):
        """Get the formula column index on the truth table."""
        all_formulas = self.lines[0]
        formula_column = None
        for index, subformula in enumerate(all_formulas):
            if subformula.str_representation() == formula.str_representation():
                formula_column = index

        if formula_column is None:
            self.print_table()
            raise Exception(
                'Formula "%s" not present in truth table.'
                % (formula.str_representation())
            )

        return formula_column

    def print_table(self):
        """Visually representation of the truth table."""
        for line in self.lines:
            for column in line:
                print(column, end='\t')
            print()
