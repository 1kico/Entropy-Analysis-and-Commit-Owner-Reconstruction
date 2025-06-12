# CS206 Assignment - Entropy Analysis & Commit Owner Identification

## Overview

This project is divided into two parts:

1. **Entropy Analysis** — Measure and analyze the entropy of n-grams (n = 0 to 10) from cleaned Albanian.
2. **Commit Owner Identification** — Given a long "weld" string and an employee list, determine the sequence of employee IDs that most likely generated the string.

---

## Part 1: Entropy Analysis

### Folder Structure

```
Part1/
├── data/                # Folder with .txt files to analyze
├── entropy_analysis.py  # Main Python script
```

### How It Works

- Cleans text (removes digits, punctuation, keeps ë and ç)
- Generates n-grams (n = 0 to 10)
- Calculates entropy:
  - `n = 0`: uniform entropy
  - `n = 1`: standard Shannon entropy
  - `n ≥ 2`: conditional entropy based on context
- Displays:
  - Entropy value
  - Total and unique n-grams
  - Most/least frequent n-grams

### Usage

```bash
python entropy_analysis.py
```

Ensure `.txt` files are inside `Part1/data/`

### Time Complexity

- `n = 0 or 1`: O(N)
- `n ≥ 2`: O(N + V log V)
  - N = length of cleaned text
  - V = number of unique n-grams

---

## Part 2: Commit Owner Identification

### Folder Structure

```
Part2/
├── employees.txt        # Employee list: id,surname,name
├── commit_owners.py     # Main Python script
```

### How It Works

- Reads employee ID list
- Takes a weld string (e.g., `123456910`)
- Recursively finds all ways to split the string into valid IDs
- Returns the decomposition with **most commits** (max IDs)

### Usage

```bash
python commit_owners.py employees.txt 123456910
```

### Time Complexity

- Uses recursive DFS with backtracking
- Worst-case exponential, but works fast for short welds

---

## Documentation

- See `Kristi Shehaj, Frenki Selmani - Entropy Analysis and Commit Owner Reconstruction.pdf` for full report
- Includes formulas, implementation breakdown, examples, and complexity

---

## Requirements

- Python 3.6+
- No external libraries required (uses only built-in modules)

---

## Example Output

```bash
# Part 1
[2-gram Analysis]
Entropy: 3.4321 bits
Total n-grams: 1,042,200
Unique n-grams: 734
```


```
# Part 2
Employees file: employees.txt
Weld string: 123456910

Longest Commit sequence:
12: Smith, John
34: Wong, Alice
56: Lee, Michael
910: Kara, Fatma
```

---
