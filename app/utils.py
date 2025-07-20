import random
import string
import qrcode
from qrcode.image.pil import PilImage
import base64
from io import BytesIO
from typing import Final
import logging

logger = logging.getLogger(__name__)

SHORT_CODE_CHARS: Final[str] = string.ascii_letters + string.digits


def generate_short_code(length: int = 6) -> str:
    """
    Generates a random alphanumeric short code of a specified length.

    Args:
        length (int): The desired length of the short code. Defaults to 6.

    Returns:
        str: A randomly generated short code.
    """
    if length <= 0:
        logger.error(f"Invalid short code length requested: {length}")
        raise ValueError("Short code length must be a positive integer.")
    return ''.join(random.choices(SHORT_CODE_CHARS, k=length))


def generate_qr_code_base64(data: str) -> str:
    """
    Generates a QR code for the given data and returns it as a base64 encoded string.

    Args:
        data (str): The string data to encode in the QR code (e.g., the short URL).

    Returns:
        str: A base64 encoded string of the QR code image (PNG format).
    """
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(image_factory=PilImage)

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        logger.info(f"QR code generated for data: {data[:50]}...")
        return img_str
    except Exception as e:
        logger.error(f"Failed to generate QR code for data '{data[:50]}...': {e}")
        raise
