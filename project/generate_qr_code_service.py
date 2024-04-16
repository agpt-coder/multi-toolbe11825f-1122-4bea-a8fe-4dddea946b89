import base64
from io import BytesIO

import qrcode
from pydantic import BaseModel


class GenerateQRCodeResponse(BaseModel):
    """
    This model wraps the response from the QR code generation endpoint, providing the generated QR code in a specified format.
    """

    qr_code_data: str
    format: str


def generate_qr_code(
    content: str, size: int, color: str, background_color: str, border: int
) -> GenerateQRCodeResponse:
    """
    Generates a custom QR Code based on user specifications

    Args:
    content (str): The content to be encoded in the QR Code. This could be a URL, text, or any other valid data.
    size (int): The size of the QR code in pixels. Specifies the length of one side of the QR code as it is square in shape.
    color (str): The color of the QR code. This is in a standard web format (e.g., '#000000' for black).
    background_color (str): The background color of the QR code. Defaults to white if not specified.
    border (int): The size of the border around the QR code in pixels.

    Returns:
    GenerateQRCodeResponse: This model wraps the response from the QR code generation endpoint, providing the generated QR code in a specified format.
    """
    qr_code_image = qrcode.make(content, box_size=size // 40, border=border)
    if color != "#000000" or background_color != "#FFFFFF":
        qr_code_image = qr_code_image.convert("RGBA")
        data = qr_code_image.getdata()
        newData = []
        for item in data:
            if item[0] == 0:
                newData.append(
                    (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16), 255)
                )
            else:
                newData.append(
                    (
                        int(background_color[1:3], 16),
                        int(background_color[3:5], 16),
                        int(background_color[5:7], 16),
                        255,
                    )
                )
        qr_code_image.putdata(newData)
    buffered = BytesIO()
    qr_code_image.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()
    return GenerateQRCodeResponse(qr_code_data=qr_code_base64, format="base64")
