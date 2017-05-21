"""Delegates the operation to the respective class."""

import operations


class OperationHandler:
    """Facade to handle an operation."""

    OPERATIONS = {
        operations.SemanticStatus.SYMBOL: operations.SemanticStatus,
        operations.SemanticEquivalence.SYMBOL: operations.SemanticEquivalence,
        operations.Consistency.SYMBOL: operations.Consistency,
        operations.LogicConsequence.SYMBOL: operations.LogicConsequence,
    }

    @classmethod
    def handle(cls, line):
        """
        Handle the given line by parsing the operation in first param.

        Args:
            line (str):
                A comma separated string containing the
                operation and its params

        Examples:

            >>> line = 'S,p123->(q20&r|-r1)'
            >>> OperationHandler.handle(line)
            Will call the 'S' entry in OperationHandler.OPERATIONS dict
        """
        # Split the line to get the operation (first argument)
        requested_operation = line.split(',')[0]
        if requested_operation in cls.OPERATIONS:
            # Call the respective operation with the given params
            operation = cls.OPERATIONS[requested_operation]()
            args = operation.parse(line)
            return operation.perform(*args)
        else:
            raise Exception('Invalid operation "%s"' % operation)
