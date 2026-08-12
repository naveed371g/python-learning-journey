"""
==============================================================
 PYTHON REGEX QUICK REFERENCE + RUNNABLE EXAMPLES
==============================================================
 Run this file:   python regex_guide.py
 It prints each example with its result so you can learn by seeing.

 Tip: always write patterns as raw strings  ->  r"..."
==============================================================

 CORE FUNCTIONS
   re.search(pattern, text)     find first match anywhere
   re.match(pattern, text)      match only at the START of text
   re.findall(pattern, text)    return ALL matches as a list
   re.sub(pattern, repl, text)  replace matches
   re.split(pattern, text)      split on a pattern

 BUILDING BLOCKS
   .     any character (except newline)
   \d    a digit 0-9            \D  not a digit
   \w    word char (a-z 0-9 _)  \W  not a word char
   \s    whitespace             \S  not whitespace

 QUANTIFIERS (how many)
   *     0 or more
   +     1 or more
   ?     0 or 1 (optional)
   {3}   exactly 3
   {2,4} between 2 and 4

 ANCHORS & SETS
   ^        start of string
   $        end of string
   [abc]    any one of a, b, c
   [a-z]    any lowercase letter
   [^0-9]   any char that is NOT a digit
   \b       word boundary
   a|b      a OR b
   ( )      capture group
"""

import re


def show(label, value):
    print(f"{label:<45} -> {value}")


print("=" * 60)
print("PYTHON REGEX EXAMPLES")
print("=" * 60)

text = "This is test for 10"

# 1. Find all numbers
show('re.findall(r"\\d+", text)', re.findall(r"\d+", text))

# 2. Find all words
show('re.findall(r"\\w+", text)', re.findall(r"\w+", text))

# 3. search returns a match object (or None)
m = re.search(r"\d+", text)
show('re.search(r"\\d+", text).group()', m.group() if m else None)

# 4. match only checks the START of the string
show('re.match(r"This", text)', bool(re.match(r"This", text)))
show('re.match(r"test", text)', bool(re.match(r"test", text)))

# 5. Validate a simple email
show('valid email "hi@site.com"',
     bool(re.match(r"^\w+@\w+\.\w+$", "hi@site.com")))

# 6. Extract date groups
d = re.search(r"(\d{4})-(\d{2})-(\d{2})", "date: 2026-07-08")
show('date whole match  group(0)', d.group(0))
show('date year         group(1)', d.group(1))
show('date month        group(2)', d.group(2))

# 7. Replace: collapse extra whitespace
show('re.sub collapse spaces',
     re.sub(r"\s+", " ", "too    many     spaces"))

# 8. Split on multiple delimiters
show('re.split on , ; and spaces',
     re.split(r"[,;\s]+", "a, b; c   d"))

# 9. Case-insensitive search
show('case-insensitive find "test"',
     re.findall(r"test", "TEST test TeSt", re.IGNORECASE))

print("=" * 60)
print("Edit the patterns above and re-run to experiment!")
print("=" * 60)
