import base64
from io import BytesIO
from typing import Optional

from PIL import Image
from pydantic import BaseModel


class ResizeImageResponse(BaseModel):
    """
    The response containing the resized image data or a link to the processed image.
    """

    resized_image_data: Optional[str] = None
    resized_image_url: Optional[str] = None


def resize_image(
    image_data: str, width: int, height: int, format: Optional[str]
) -> ResizeImageResponse:
    """
    Resizes an image according to specified dimensions and optimization settings.

    Args:
        image_data (str): The raw image data to be resized, provided as a base64 encoded string.
        width (int): The target width of the image in pixels.
        height (int): The target height of the image in pixels.
        format (Optional[str]): The desired image format (e.g., 'jpeg', 'png') for the output. Defaults to the input format if not specified.

    Returns:
        ResizeImageResponse: The response containing the resized image data or a link to the processed image.

    Example:
        # Assuming 'some_base64_encoded_image' is a base64 encoded string of an image.
        resize_image_response = resize_image(some_base64_encoded_image, 100, 100, 'jpeg')
        print(resize_image_response.resized_image_data)  # This shows the resized image data as a base64 string.
    """
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    resized_image = image.resize((width, height))
    image_format = format if format else image.format
    buffer = BytesIO()
    resized_image.save(buffer, format=image_format)
    resized_image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return ResizeImageResponse(resized_image_data=resized_image_data)
