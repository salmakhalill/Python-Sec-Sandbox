## >>> STRING LIBRARY <<<

- Python has built-in module called `string`  
- used to generate characters  

```python
import string
uppercase letters A-Z
string.ascii_uppercase
lowercase letters a-z
string.ascii_lowercase
examples:
string.ascii_uppercase  # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
string.ascii_lowercase  # "abcdefghijklmnopqrstuvwxyz"
NOTE:
useful for brute force attacks with letters
example:
for c in string.ascii_lowercase:
    print(c)
IMPORTANT:
can combine with loops to generate passwords
example: aa, ab, ac ... zz