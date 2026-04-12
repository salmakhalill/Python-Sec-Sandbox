## Problem before itertools

- suppose we want to generate all passwords of length 2  
- using characters: "ab"  

### *** manual way (nested loops):
```python
for a in "ab":
    for b in "ab":
        print(a + b)
```

> output:
> aa, ab, ba, bb


**# Problem:**
- this works for small lengths (e.g. 2)
- longer lengths → more nested loops → messy and unscalable code

--------------------------------

### *** Solution: itertools.product
- Python provides a built-in function to replace nested loops: `product()`
- it automatically simulates nested loops internally
- same result, but scalable and cleaner

```python
import itertools
```
**? syntax:**
- itertools.product(iterable, repeat=n)
- iterable → characters set
- repeat → number of loops (password length)

**=> ex:**  
```python
for p in itertools.product("ab", repeat=2):
    print(p)
```

> output:
> ('a','a'), ('a','b'), ('b','a'), ('b','b')

--------------------------------

### *** What is "p"?
- in each loop:
```python
p = ('a','b') → it's a tuple, not a string
```

**# Problem:** need string
- we want: "ab"
- but we have: ('a','b')

**# solution → join()**
- convert tuple → string
