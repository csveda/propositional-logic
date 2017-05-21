"""Describe the possible operations."""


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
        pass


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
