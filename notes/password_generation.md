## PASSWORD COMBINATION LOGIC 

- step 1: choose characters  
- step 2: choose password length  
- step 3: generate combinations  
- step 4: convert tuple → string  

---

### *** CHARACTER SET 

```python
import string

string.ascii_lowercase
string.ascii_uppercase
string.digits
```
---------

### *** 1. BUILD CHARACTER SET 

```python
#                 a-z          +     0-9
chars = string.ascii_lowercase + string.digits
```

### *** 2. PASSWORD LENGTH 

```python
length = 2
```

**meaning:**
- password = 2 characters

### *** 3. GENERATE PASSWORDS 

```python
import itertools

for p in itertools.product(chars, repeat=length):
    password = ''.join(p)
    print(password)
```
--------------

### *** NUMBER OF COMBINATIONS 

*=> formula:*
- total = (len(chars)) ^ length

> ex:

> chars = 3
> length = 2

> total = 3^2 = 9
------------------

### *** REAL-WORLD NOTE 
- increasing length increases combinations exponentially

**=> ex:** 
> 26 letters, length = 4
> 26^4 = 456,976 attempts

**!! IMPORTANT:**
- brute force becomes very slow with large length