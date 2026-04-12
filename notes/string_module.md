## STRING LIBRARY 

- Python has built-in module called string
- provides useful constants for character sets

```python
import string

# -- uppercase letters A-Z
string.ascii_uppercase    # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# -- lowercase letters a-z
string.ascii_lowercase    # "abcdefghijklmnopqrstuvwxyz"
``` 
-------
**=> ex:** iterate over lowercase letters

```python
for c in string.ascii_lowercase:
    print(c)
```
> => Output:


> a

> b

> c

> d

> ...

> z

------
**!! IMPORTANT:**
- useful for working with character generation
- often combined with loops in password / pattern generation

- can be used to build combinations like:
> aa, ab, ac ... zz

- this is just a basic way → there are more powerful tools for generating combinations (like *itertools*)