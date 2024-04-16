from typing import Optional

import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel


class UrlPreviewResponse(BaseModel):
    """
    The structured response containing metadata extracted from the URL for preview purposes.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    url: str


async def generate_url_preview(url: str) -> UrlPreviewResponse:
    """
    Generates a preview for a given URL by extracting and presenting its metadata.

    Args:
    url (str): The URL to generate a preview for.

    Returns:
    UrlPreviewResponse: The structured response containing metadata extracted from the URL for preview purposes.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title_tag = soup.find("title")
            title = title_tag.text.strip() if title_tag else None
            description_tag = soup.find("meta", attrs={"name": "description"})
            description = (
                description_tag["content"].strip()
                if description_tag and "content" in description_tag.attrs
                else None
            )  # TODO(autogpt): Cannot access member "strip" for type "list[str]"
            #     Member "strip" is unknown. reportAttributeAccessIssue
            image_tag = soup.find("meta", attrs={"property": "og:image"})
            image = (
                image_tag["content"].strip()
                if image_tag and "content" in image_tag.attrs
                else None
            )  # TODO(autogpt): Cannot access member "strip" for type "list[str]"
            #     Member "strip" is unknown. reportAttributeAccessIssue
            return UrlPreviewResponse(
                title=title, description=description, image=image, url=url
            )
        else:
            return UrlPreviewResponse(url=url)
