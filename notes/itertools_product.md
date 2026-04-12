## PROBLEM BEFORE ITERTOOLS 

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


**# NOTE:**
- this works for length = 2
- but if length = 3 → we need 3 loops


**!! IMPORTANT:**
- more length = more nested loops = messy code

--------------------------------

### *** SOLUTION: ITERTOOLS.PRODUCT
- instead of writing loops inside loops
- Python gives us a ready function: product()

```python
import itertools
```
**? syntax:**
- itertools.product(iterable, repeat=n)
- iterable → characters
- repeat → number of loops (password length)

**=> ex:**  
```python
for p in itertools.product("ab", repeat=2):
    print(p)
```

> output:
> ('a','a'), ('a','b'), ('b','a'), ('b','b')


**# NOTE:**
- product() automatically does nested loops

--------------------------------

### *** WHAT IS "p" 
- in each loop:
```python
p = ('a','b') → it's a tuple, not a string
```

--------------------------------

### *** PROBLEM: NEED STRING 
- we want: "ab"
- but we have: ('a','b')
- **solution → join()**