import re
from passlib.context import CryptContext

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a password against a hash.
    
    Args:
        plain_password: Plain text password
        hashed: Hashed password
        
    Returns:
        bool: True if password matches hash
    """
    try:
        return pwd_context.verify(plain_password, hashed)
    except Exception:
        return False


def is_password_strong(password: str) -> bool:
    """Check if password meets strength requirements.
    
    Args:
        password: Plain text password
        
    Returns:
        bool: True if password is strong enough
    """
    if len(password) < 8:
        return False
    # Require upper, lower and digit for a basic check
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True


def is_username_email_unique(username: str, email: str, existing_users) -> bool:
    """Check if username and email are unique.
    
    Args:
        username: Username to check
        email: Email to check
        existing_users: List of existing users
        
    Returns:
        bool: True if username and email are unique
    """
    for u in existing_users:
        if u["username"] == username or u["email"] == email:
            return False
    return True
