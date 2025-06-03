"""Authentication module for JWT token creation and password verification."""

import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext


class AuthConfig:
    """Configuration class for authentication settings."""
    
    # Use environment variable for production, fallback for development
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_change_in_production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    DEFAULT_EXPIRE_MINUTES = 15


class PasswordManager:
    """Handles password hashing and verification."""
    
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        
        Args:
            plain_password: The plain text password to verify
            hashed_password: The hashed password to compare against
            
        Returns:
            bool: True if passwords match, False otherwise
        """
        try:
            return self._pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False
    
    def hash_password(self, password: str) -> str:
        """
        Hash a plain text password.
        
        Args:
            password: The plain text password to hash
            
        Returns:
            str: The hashed password
        """
        return self._pwd_context.hash(password)


class TokenManager:
    """Handles JWT token creation and validation."""
    
    def __init__(self, config: Optional[AuthConfig] = None):
        self._config = config or AuthConfig()
    
    def create_access_token(
        self, 
        data: Dict[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: The payload to encode in the token
            expires_delta: Optional custom expiration time delta
            
        Returns:
            str: The encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self._config.DEFAULT_EXPIRE_MINUTES
            )
        
        to_encode.update({"exp": expire})
        
        return jwt.encode(
            to_encode, 
            self._config.SECRET_KEY, 
            algorithm=self._config.ALGORITHM
        )
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate a JWT token.
        
        Args:
            token: The JWT token to decode
            
        Returns:
            Dict[str, Any]: The decoded token payload
            
        Raises:
            JWTError: If the token is invalid or expired
        """
        return jwt.decode(
            token, 
            self._config.SECRET_KEY, 
            algorithms=[self._config.ALGORITHM]
        )


# Create singleton instances
password_manager = PasswordManager()
token_manager = TokenManager()

# Convenience functions for backward compatibility
verify_password = password_manager.verify_password
create_access_token = token_manager.create_access_token


# Example usage:
if __name__ == "__main__":
    # Password handling
    plain_password = "mysecretpassword"
    hashed = password_manager.hash_password(plain_password)
    print(f"Password verified: {password_manager.verify_password(plain_password, hashed)}")
    
    # Token handling
    user_data = {"sub": "user@example.com", "role": "user"}
    token = token_manager.create_access_token(user_data)
    print(f"Token created: {token[:20]}...")
    
    try:
        decoded = token_manager.decode_token(token)
        print(f"Token decoded: {decoded}")
    except JWTError as e:
        print(f"Token error: {e}")