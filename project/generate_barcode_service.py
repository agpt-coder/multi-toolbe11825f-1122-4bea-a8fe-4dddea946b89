from tempfile import NamedTemporaryFile
from typing import Optional

import barcode
from barcode.writer import ImageWriter
from pydantic import BaseModel


class GenerateBarcodeResponse(BaseModel):
    """
    The response containing the generated barcode data.
    """

    barcode_image_url: str
    format: str
    content: str


def generate_barcode(
    format: str,
    content: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    color: Optional[str] = None,
    background_color: Optional[str] = None,
    text: Optional[str] = None,
) -> GenerateBarcodeResponse:
    """
    Generates a barcode in a specified format with customization options.

    Args:
    format (str): The barcode format, e.g., QR, UPC, EAN, etc.
    content (str): The content to be encoded in the barcode.
    width (Optional[int]): Width of the barcode, in pixels.
    height (Optional[int]): Height of the barcode, in pixels.
    color (Optional[str]): Hex code for the barcode color. Defaults to black if not specified.
    background_color (Optional[str]): Hex code for the barcode background color. Defaults to white if not specified.
    text (Optional[str]): Optional text to include with the barcode.

    Returns:
    GenerateBarcodeResponse: The response containing the generated barcode data.
    """
    if format.upper() not in barcode.PROVIDED_BARCODES:
        raise ValueError(f"Unsupported barcode format: {format}.")
    barcode_class = barcode.get_barcode_class(format)
    writer_options = {
        "module_width": 0.2 if not width else width / 102.0,
        "module_height": 15.0 if not height else height,
        "foreground": color or "black",
        "background": background_color or "white",
        "text": text,
        "write_text": bool(text),
        "quiet_zone": 1.0,
    }
    writer = ImageWriter()
    with NamedTemporaryFile(delete=False, suffix=".png") as f:
        barcode_instance = barcode_class(content, writer=writer)
        barcode_instance.write(f, options=writer_options)
        image_url = f"{f.name}"
    response = GenerateBarcodeResponse(
        barcode_image_url=image_url, format=format, content=content
    )
    return response
