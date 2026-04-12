# Python Sec Sandbox

A personal repository for building and experimenting with custom security tools using Python.

This repo is based on hands-on practice from the *Custom Tooling using Python* room, focusing on understanding the logic behind building tools rather than just using them.

---

## Structure


.
├── 01_bruteforce_tools/
├── 02_vulnerability_scanners/
├── 03_exploit_development/
├── 04_task_automation/
└── notes/


---

## 01 - Brute Force Tools

Basic scripts to understand how brute-force attacks work and how to generate password combinations.

Includes:
- Numeric brute force (0000–9999)
- Alphanumeric brute force
- Pattern-based brute force (e.g. 3 digits + 1 uppercase letter)

Focus:
- Password generation logic
- Using `itertools.product`
- Handling HTTP requests with `requests`

---

## 02 - Vulnerability Scanners

Simple scripts to discover potential weaknesses in web applications.

Planned:
- Directory/path discovery
- Basic response analysis (status codes, content)

---

## 03 - Exploit Development

Basic exploit scripts to understand how vulnerabilities are abused.

Planned:
- Simple SQL injection automation
- Request-based exploit scripts

---

## 04 - Task Automation

Scripts to automate repetitive tasks during testing.

Planned:
- Batch requests
- Log parsing
- File handling

---

## Notes

The `notes/` directory contains explanations and breakdowns of concepts used in the scripts, such as:
- `zfill()`
- `itertools.product`
- `join()`
- password pattern logic

---

## Disclaimer

This repository is for educational purposes only.  
All scripts are tested in controlled environments (e.g. labs like TryHackMe).