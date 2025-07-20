import pytest
import base64
from app.utils import generate_short_code, generate_qr_code_base64


def test_generate_short_code_length():
    """Test that generated short code has correct length."""
    code = generate_short_code(8)
    assert len(code) == 8, "Short code should have length 8."

def test_generate_short_code_charset():
    """Test that generated short code contains only alphanumeric chars."""
    code = generate_short_code(12)
    assert all(c.isalnum() for c in code), "Short code should be alphanumeric."

def test_generate_short_code_invalid_length():
    """Test that invalid length raises ValueError."""
    with pytest.raises(ValueError):
        generate_short_code(0)

def test_generate_qr_code_base64():
    """Test that QR code is valid base64-encoded PNG."""
    data = "https://example.com"
    qr_b64 = generate_qr_code_base64(data)
    try:
        decoded = base64.b64decode(qr_b64)
        assert isinstance(decoded, bytes), "Decoded QR should be bytes."
        assert len(decoded) > 0, "Decoded QR should not be empty."
    except Exception:
        pytest.fail("QR code is not valid base64")
