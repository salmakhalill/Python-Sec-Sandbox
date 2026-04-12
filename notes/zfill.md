## zfill EXPLANATION 

- str(i) → converts number to string 

**=> ex:**  
```python
i = 5
str(i)  # "5"
```
**=> examples:**
```Python
"5".zfill(4)    # "0005"
"23".zfill(4)   # "0023"
"456".zfill(4)  # "0456"
"9999".zfill(4) # "9999"
```

**# NOTE:**
- zfill only adds zeros if length < required
- if already 4 digits → no change
- range(10000) → generates numbers from 0 to 9999


**# Combining everything:**
```Python
[str(i).zfill(4) for i in range(10000)]
```

**? Meaning:**
- loop through numbers from 0 → 9999
- convert each number to string
- make it 4 digits using zfill
- store all values in a list

**!! IMPORTANT:**
- used in brute force to generate fixed-length passwords
- ensures format like: 0001 instead of 1