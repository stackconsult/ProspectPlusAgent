"""Tests for core functionality."""

import pytest
from prospectplusagent.core.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token
)


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_token_creation_and_verification():
    """Test JWT token creation and verification."""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    
    payload = verify_token(token)
    assert payload["sub"] == "testuser"


def test_invalid_token():
    """Test that invalid tokens raise exceptions."""
    with pytest.raises(Exception):
        verify_token("invalid.token.here")
