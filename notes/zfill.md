## zfill EXPLANATION

- zfill() → pads a string with zeros from the LEFT until it reaches a specific length
- zfill() works on strings only, not numbers

→ so we need to convert the number to a string first
------
### *** Convert number to string
str(i) → converts a number to a string

**=> ex:**
```python
i = 5
str(i)  # "5"
```
-------
### *** Using zfill
- now we can use zfill(4) to make the length = 4

**=> ex:**
```python
"5".zfill(4)    # "0005"
"23".zfill(4)   # "0023"
"456".zfill(4)  # "0456"
"9999".zfill(4) # "9999"
```
----------
### *** Combining everything
```python
[str(i).zfill(4) for i in range(10000)]
```
**? Meaning:**
- range(10000) → numbers from 0 to 9999
- convert each number to string
- apply zfill(4)
- store results in a list
--------
**!! Important:**
ensures fixed-length format → 0001 instead of 1
commonly used in brute force