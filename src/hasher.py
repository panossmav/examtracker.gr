import hashlib as hl

def hash_password(password):
    return hl.sha256(password.encode()).hexdigest()