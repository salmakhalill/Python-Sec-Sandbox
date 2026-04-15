## Regex (Regular Expressions)
- regex → used to search inside text using patterns (not fixed words)
- think of it as: smart search instead of exact search

### *** Basic usage:

```python
import re

re.search("word", text)
```

**? Meaning:**
- searches for any text containing "word"
- NOT required to be the whole string
***Examples**
*✓ matches:*
- hello word here
- word is found
- this is a word test

*✘ does NOT match:*
- hello world   # different word

**# NOTE:**
- search = looks for substring (part of text)
- NOT exact match for whole string

**!! Important:**
- to match whole word only:
```python
r"\bword\b"
```
- \b = word boundary
------------
### *** Using patterns:
```python
re.search(r"sql.*error", text, re.IGNORECASE)
```
**? Meaning:**
- sql → must appear first
- .* → any characters (0 or more)
- error → must appear after
> sql ... error

***Examples**
*✓ matches:*
- SQL syntax error
- sql server internal error
- sql blah blah error

*✘ does NOT match:*
- SQL query executed
- sql connection success

**# NOTE:**
- regex does NOT guess
- YOU define what should match

> if pattern does not include "error" → it will NOT detect it
- always design patterns based on what you want to catch
------------
### *** in vs re.search:

| method      | behavior                        |
|-------------|---------------------------------|
| `in`        | simple substring check          |
| `re.search` | pattern matching (smart search) |

```python
"error" in content   # simple
re.search("error", content)   # regex
```

**# NOTE:**
- in is built-in Python
- NOT related to re
---------
### *** re.IGNORECASE:
```python
re.search(pattern, text, re.IGNORECASE)
```
**? Meaning:**
- ignores uppercase/lowercase

***Ex:**
```python
re.search("sql", "SQL ERROR")                 # ✘ no match
re.search("sql", "SQL ERROR", re.IGNORECASE)  # ✓ match
```
**!! Important:**
- makes search case-insensitive
--------------
### *** lower() vs IGNORECASE:

```python
content = response.text.lower()
error.lower() in content
```
- same idea as IGNORECASE

**# NOTE:**
- .lower() → convert text first
- IGNORECASE → handled by regex