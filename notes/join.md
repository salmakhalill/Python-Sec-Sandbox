## JOIN EXPLAINED 

- join() merges elements into one string  

### *** syntax:
```python
"separator".join(iterable)
```
- separator = what goes between elements

**=> ex:**  
```python
''.join(['a','b'])        # "ab"
'-'.join(['1','2','3'])   # "1-2-3"
```


**# NOTE:**
- '' = no separator (just glue them together)

------------------

### *** JOIN WITH PRODUCT

```python
import itertools

for p in itertools.product("ab", repeat=2):
    print(''.join(p))
```
> output:
> aa, ab, ba, bb