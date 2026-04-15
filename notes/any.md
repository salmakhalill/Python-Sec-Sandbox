## any() Explained
- any() → returns True if at least ONE element is True
*** syntax
any(condition for item in list)
*** example
```python
words = ["cat", "dog", "bird"]

any("o" in w for w in words)
```
**? Meaning:**
- check each word
- if ANY contains "o" → return True

*** equivalent normal loop
```python
for w in words:
    if "o" in w:
        return True
return False
```
**# NOTE:**
- stops at first True → faster

**!! Important:**
- any() = OR logic
- all() = AND logic
--------------------------------------------
## Generator Expression (Short for loop)
- used to write loops in one line
*** normal loop
```python
result = []
for x in data:
    result.append(f(x))
```
*** short version
```python
result = [f(x) for x in data]
```
*** with condition
```python
[x for x in data if condition]
```
*** inside any()
```python
any(re.search(p, content) for p in patterns)
```
**? Meaning:**
- loop over patterns
- apply search
- return True if any match

**!! Important:**
- same logic as loop
- just shorter syntax

ⶆ Understanding this line
```python
any(re.search(p, content, re.IGNORECASE) for p in patterns)
```
**? Step by step:**
- for each pattern p
- search in content
- if ONE match → True

≡ same as:
```python
for p in patterns:
    if re.search(p, content, re.IGNORECASE):
        return True
return False
```
