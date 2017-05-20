"""Parse the input file and delegate the treatment."""

from os import path
import re
import sys

from handler import OperationHandler


# The filename should be the first argument
input_file = sys.argv[1]
# The result filename should be the second argument
result_file = sys.argv[2] if 2 in sys.argv else 'results.txt'

if not path.isfile(input_file):
    raise Exception('File not found.')

# Load each line of the file to a list
with open(input_file) as file:
    entries = [entry.strip() for entry in file if entry is not '\n']

# Regexp to match only the accepted characters
pattern = re.compile(r'^\[([a-z0-9SEQCL, &\-\|><\(\)]*)\]$')

lines_with_error = []
results = []
for entry in entries:
    matches = pattern.match(entry)
    if matches:
        line = matches.groups()[0]
        # Removing all whitespaces
        line = "".join(line.split())
        result = OperationHandler.handle(line)
        results.append(result)
    else:
        lines_with_error.append(entry)

# Save the results in the results.txt file
with open(result_file, 'w') as results_file:
    for result in results:
        if result is not None:
            results_file.write(result)

if lines_with_error:
    print('Lines with error (not parsed):')
    for line in lines_with_error:
        print(line)
