# Parser Kombinators

a small and terrible parser combinator library for python.

## Examples

### JSON

The file `json_example.py` contains a fully working parser for a subset of json.

This subset supports afaik everything that json supports except:

* `null`
* booleans

### Math

The script `math.py` is a math expression parser, which compiles the expression to bytecode. This bytecode can be executed with the `stack_vm.c` program. It only supports multiplication and addition.

This script is very sensitive about whitespaces; it doesn't like them.
