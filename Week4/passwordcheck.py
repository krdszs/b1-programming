passwords = [ 
"Pass123",
"SecurePassword1",
"weak",
"MyP@ssw0rd",
"NOLOWER123"]

compliant = 0
non_compliant = 0

min_length = 8

for password in passwords:
    problems = []

    if len(password) < min_length:
        problems.append("Too short")
    
    has_upper = False
    has_lower = False
    has_digit = False

    for char in password:
        if "A" < char < "Z":
            has_upper = True
        if "a" < char < "z":
            has_lower = True
        if "0" < char < "9":
            has_digit = True
    
    if not has_upper:
        problems.append("No uppercase letters")
    if not has_lower:
        problems.append("No lowercase letters")
    if not has_digit:
        problems.append("No digits")

    if len(problems) == 0:
        compliant += 1
        print(f"PASS: {password} - Meets all requirements")
    else:
        non_compliant += 1
        text = ", ".join(problems)
        print(f"FAIL: {password} - {text}")

print(f"Summary: {compliant} compliant, {non_compliant} non-compliant")
