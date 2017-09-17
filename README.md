# Polynomials
Compares two polynomials using math parsing.

## How to execute

In Windows PowerShell or Command Prompt:
```
python __main.py__ [-h] [-e epsilon | -d n | -m] [-s] [-f file] [first] [second]
```

In bash:
```
python3 __main.py__ [first] [second]
```

To get help:

```
python __main.py__ --help
```

## Tests

Tests can be only executed manually.
For instance, in command prompt you can type this:

```
cd tests && for %a in (*.py) do (python %a) && cd ..
```