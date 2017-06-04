"""Describe the possible operations."""

from lp.interpreter import TruthTable


class Operation:
    """Base class for operations."""

    def perform(self, *args):
        """Perform the operation."""
        raise NotImplementedError

    def parse(self, line):
        """
        Generic parser for operations.

        A line generally comes like that:

            OPERATION, formula1, formula2, ...

        So it returns the comma separated values without the operation as list.
        """
        args = line.split(',')
        return args[1:]


class SemanticStatus(Operation):
    """Verify the semantic status of a formula."""

    SYMBOL = 'S'

    def perform(self, formula):
        """Check a formula semantic status."""
        truth_table = TruthTable(formula)
        formula = truth_table.formula
        valuations = truth_table.get_formula_valuations(formula)

        formula_values = []
        for line, valuation in valuations.items():
            formula_values.append(valuation[1])

        status = self.check_status(formula_values)

        return '[' + status + ', ' + truth_table.str_representation() + ']'

    def check_status(self, formula_values):
        """Get the formulas semantic status based on its valuations."""
        tautology = True in formula_values and False not in formula_values
        contradiction = False in formula_values and True not in formula_values

        if tautology:
            status = "TAUTOLOGIA"
        elif contradiction:
            status = "CONTRADICAO"
        else:
            status = "CONTINGENCIA"

        return status

class SemanticEquivalence(Operation):
    """Verify if two formulas are semantic equivalent."""

    SYMBOL = 'EQ'

    def perform(self, formula1, formula2):
        """Check if the two formulas are equivalent."""
        pass


class Consistency(Operation):
    """Verify if a set of formulas is consistent."""

    SYMBOL = 'C'

    def perform(self, formulas):
        """Check if the set of formulas is consistent."""
        pass

    def parse(self, line):
        """Parse a bracketed, comma separated formulas into a list."""
        # Remove the operation symbol from the line
        line = line.replace(self.SYMBOL, '')
        # Remove the whitespaces and the first character (that will be a comma)
        line = "".join(line.split())[1:]
        # Remove the brackets of the string
        line = line.replace('[', '').replace(']', '')
        # Split the line on comma to get all formulas of the set as list
        args = line.split(',')
        return [args]


class LogicConsequence(Operation):
    """Verify if a formula is logic consequence of a set of formulas."""

    SYMBOL = 'CL'

    def perform(self, formulas_set, formula):
        """Check if the formula is logic consequence of the formulas_set."""
        pass
