import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.add_watermark_to_pdf_service
import project.check_password_strength_service
import project.convert_feed_to_json_service
import project.convert_timezone_service
import project.generate_barcode_service
import project.generate_qr_code_service
import project.generate_url_preview_service
import project.get_exchange_rate_service
import project.get_ip_geolocation_service
import project.resize_image_service
import project.text_to_speech_convert_service
import project.validate_email_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="multi tool",
    lifespan=lifespan,
    description="The Multi-Purpose API Toolkit provides a robust and cohesive collection of APIs designed to facilitate a wide array of common yet pivotal tasks for developers. This toolkit consolidates diverse functionalities into a singular endpoint, simplifying the process of integrating multiple third-party services. Key offerings include:\n\n1. **QR Code Generator**: Allows for the creation of custom QR codes to streamline the process of information sharing.\n2. **Currency Exchange Rate**: Enables access to real-time exchange rates across a variety of currencies, aiding in financial transactions and analyses.\n3. **IP Geolocation**: Offers detailed geolocation data based on IP addresses, which can be pivotal for content localization and user analytics.\n4. **Image Resizing**: Provides on-the-fly resizing and optimization of images, crucial for improving web performance and user experience.\n5. **Password Strength Checker**: Assesses the strength of passwords, offering suggestions for improvements to bolster security.\n6. **Text-to-Speech**: Converts text into natural-sounding audio, enhancing accessibility and user engagement.\n7. **Barcode Generator**: Generates high-quality barcodes in various formats, supporting a range of inventory and retail applications.\n8. **Email Validation**: Validates email addresses to improve deliverability and reduce bounce rates, essential for marketing and outreach efforts.\n9. **Time Zone Conversion**: Facilitates the conversion of timestamps between different time zones, critical for global applications and communications.\n10. **URL Preview**: Extracts metadata and generates previews for web links, aiding in content curation and social sharing.\n11. **PDF Watermarking**: Allows the addition of customizable watermarks to PDF documents, useful for copyright protection and branding.\n12. **RSS Feed to JSON**: Converts RSS feeds into structured JSON format, simplifying the integration of live updates and news into applications.\n\nThis toolkit's design emphasizes simplicity and ease of use, offering developers a versatile set of tools to enhance project capabilities without the complexity of managing multiple API integrations. Through a single endpoint, the toolkit streamlines development workflows and fosters efficiency across various domains, from web development to software engineering.",
)


@app.get(
    "/geolocation/{ip}",
    response_model=project.get_ip_geolocation_service.GeoLocationResponse,
)
async def api_get_get_ip_geolocation(
    ip: str,
) -> project.get_ip_geolocation_service.GeoLocationResponse | Response:
    """
    Retrieves geolocation data for a given IP address.
    """
    try:
        res = await project.get_ip_geolocation_service.get_ip_geolocation(ip)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/image/resize", response_model=project.resize_image_service.ResizeImageResponse
)
async def api_post_resize_image(
    image_data: str, width: int, height: int, format: Optional[str]
) -> project.resize_image_service.ResizeImageResponse | Response:
    """
    Resizes an image according to specified dimensions and optimization settings.
    """
    try:
        res = project.resize_image_service.resize_image(
            image_data, width, height, format
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/text-to-speech/convert",
    response_model=project.text_to_speech_convert_service.TextToSpeechResponse,
)
async def api_post_text_to_speech_convert(
    text: str,
    language: str,
    pitch: Optional[float],
    speed: Optional[float],
    gender: Optional[str],
) -> project.text_to_speech_convert_service.TextToSpeechResponse | Response:
    """
    Converts provided textual content into speech audio with customizable voice parameters.
    """
    try:
        res = project.text_to_speech_convert_service.text_to_speech_convert(
            text, language, pitch, speed, gender
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/barcode/generate",
    response_model=project.generate_barcode_service.GenerateBarcodeResponse,
)
async def api_post_generate_barcode(
    height: Optional[int],
    format: str,
    content: str,
    width: Optional[int],
    color: Optional[str],
    background_color: Optional[str],
    text: Optional[str],
) -> project.generate_barcode_service.GenerateBarcodeResponse | Response:
    """
    Generates a barcode in a specified format with customization options.
    """
    try:
        res = project.generate_barcode_service.generate_barcode(
            height, format, content, width, color, background_color, text
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/currency/rate",
    response_model=project.get_exchange_rate_service.GetExchangeRateResponse,
)
async def api_get_get_exchange_rate(
    base_currency: str, target_currency: str, date: Optional[str]
) -> project.get_exchange_rate_service.GetExchangeRateResponse | Response:
    """
    Retrieves the latest exchange rates for specified currency pairs.
    """
    try:
        res = await project.get_exchange_rate_service.get_exchange_rate(
            base_currency, target_currency, date
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feed/convert",
    response_model=project.convert_feed_to_json_service.FeedConversionResponse,
)
async def api_post_convert_feed_to_json(
    feed_url: str,
) -> project.convert_feed_to_json_service.FeedConversionResponse | Response:
    """
    Converts an RSS or Atom feed into a structured JSON format.
    """
    try:
        res = project.convert_feed_to_json_service.convert_feed_to_json(feed_url)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/pdf/watermark",
    response_model=project.add_watermark_to_pdf_service.AddWatermarkResponse,
)
async def api_post_add_watermark_to_pdf(
    pdf_document: str,
    watermark_text: str,
    text_style: project.add_watermark_to_pdf_service.TextStyle,
    opacity: float,
    position: str,
) -> project.add_watermark_to_pdf_service.AddWatermarkResponse | Response:
    """
    Adds a customizable watermark to a PDF document.
    """
    try:
        res = project.add_watermark_to_pdf_service.add_watermark_to_pdf(
            pdf_document, watermark_text, text_style, opacity, position
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/qr/generate",
    response_model=project.generate_qr_code_service.GenerateQRCodeResponse,
)
async def api_post_generate_qr_code(
    content: str, size: int, color: str, background_color: str, border: int
) -> project.generate_qr_code_service.GenerateQRCodeResponse | Response:
    """
    Generates a custom QR Code based on user specifications
    """
    try:
        res = project.generate_qr_code_service.generate_qr_code(
            content, size, color, background_color, border
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/url/preview",
    response_model=project.generate_url_preview_service.UrlPreviewResponse,
)
async def api_post_generate_url_preview(
    url: str,
) -> project.generate_url_preview_service.UrlPreviewResponse | Response:
    """
    Generates a preview for a given URL by extracting and presenting its metadata.
    """
    try:
        res = await project.generate_url_preview_service.generate_url_preview(url)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/security/password/strength",
    response_model=project.check_password_strength_service.CheckPasswordStrengthResponse,
)
async def api_post_check_password_strength(
    password: str,
) -> project.check_password_strength_service.CheckPasswordStrengthResponse | Response:
    """
    Assesses the strength of a given password and provides suggestions for improvement.
    """
    try:
        res = project.check_password_strength_service.check_password_strength(password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/timezone/convert",
    response_model=project.convert_timezone_service.TimezoneConvertResponse,
)
async def api_post_convert_timezone(
    timestamp: str, source_timezone: str, target_timezone: str
) -> project.convert_timezone_service.TimezoneConvertResponse | Response:
    """
    Converts a timestamp from one time zone to another, adjusting for daylight saving time as necessary.
    """
    try:
        res = project.convert_timezone_service.convert_timezone(
            timestamp, source_timezone, target_timezone
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/security/email/validate",
    response_model=project.validate_email_service.ValidateEmailResponse,
)
async def api_post_validate_email(
    email: str,
) -> project.validate_email_service.ValidateEmailResponse | Response:
    """
    Validates an email address for proper format and potential deliverability issues.
    """
    try:
        res = project.validate_email_service.validate_email(email)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
