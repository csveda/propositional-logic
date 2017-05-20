"""Describe the possible operations."""


class Operation:
    """Base class for operations."""

    @classmethod
    def perform(cls, *args):
        """Perform the operation."""
        raise NotImplementedError


class SemanticStatus(Operation):
    """Verify the semantic status of a formula."""

    SYMBOL = 'S'

    @classmethod
    def perform(cls, formula):
        """Check a formula semantic status."""
        print(formula)


class SemanticEquivalence(Operation):
    """Verify if two formulas are semantic equivalent."""

    SYMBOL = 'EQ'

    @classmethod
    def perform(cls, formula1, formula2):
        """Check if the two formulas are equivalent."""
        print('EQ')
        print(formula1)
        print(formula2)


class Consistency(Operation):
    """Verify if a set of formulas is consistent."""

    SYMBOL = 'C'

    @classmethod
    def perform(cls, formulas):
        """Check if the set of formulas is consistent."""
        pass


class LogicConsequence(Operation):
    """Verify if a formula is logic consequence of a set of formulas."""

    SYMBOL = 'CL'

    @classmethod
    def perform(cls, formulas_set, formula):
        """Check if the formula is logic consequence of the formulas_set."""
        pass
