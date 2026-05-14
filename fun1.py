

def validate_password(password):
    """Validate password strength"""
    score = 0
    
    # Length check
    if len(password) >= 8:
        score += 1
    elif len(password) >= 6:
        score += 0.5
    
    # Complexity checks
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*" for c in password)
    
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1
    
    # Determine strength
    if score >= 4:
        strength = "Strong"
    elif score >= 2.5:
        strength = "Medium"
    else:
        strength = "Weak"
    
    return strength, score
 
# Test password validation
passwords = ["123", "password", "Password123", "MyP@ssw0rd!", "Python2023"]
 
for pwd in passwords:
    strength, score = validate_password(pwd)
    print(f"Password: {'*' * len(pwd)} - Strength: {strength} (Score: {score:.1f})")
