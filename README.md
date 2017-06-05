
## Functionalities

This program perform 4 operations in formulas of the Propositional Language:

* S = Verify the semantic status of a formula;
  * Arguments: a formula.
* EQ = Verify if two formulas are semantically equivalent;
  * Arguments: two formulas, comma separated.
* C = Verify if a set of formulas is consistent;
  * Arguments: a set of formulas, inside brackets, comma separated.
* CL = Verifiy if the formula is logical consequence of a set of formulas.
  * Arguments: a set of formulas and a formula, comma separated

It accepts a file as input where each line of the file is a list (described by brackets ('[', ']')),
containing the operation to be performed and its arguments.

### Operators and symbols

The propositional symbols must be a lower case letter followed or not by an integer index.
Examples: p, q, r1, q2, p10, ...

The accepted operators are:
* Negation: -
* Conjunction: &
* Disjunction: |
* Implication: ->
* Bi-implication: <->

## Requirements

This programs was written in Python 3, so it needs it to run. Another versions may not work properly.

## Usage

Just call the parser.py script passing the input file as first argument and the output file as second argument.

`$ python3 parser.py input.txt output.txt`

If no output file is given, then will be created a _results.txt_.


### Example of input file

This would be an example of the content of an input file:

    [S, p123 -> (q20 & r | -r1)]
    [C, [p|s, s<->-q, p->q]]
    [EQ, p -> q, -p | q]
    [CL, [-r -> (p|q), r&-q], r->q]