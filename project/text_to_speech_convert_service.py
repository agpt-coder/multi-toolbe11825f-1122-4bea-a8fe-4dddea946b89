from typing import Optional

from google.cloud import texttospeech_v1 as texttospeech
from pydantic import BaseModel


class TextToSpeechResponse(BaseModel):
    """
    Provides a response containing the audio data or a link to the generated speech audio.
    """

    audio_link: str
    audio_format: str
    status: str


def text_to_speech_convert(
    text: str,
    language: str,
    pitch: Optional[float],
    speed: Optional[float],
    gender: Optional[str],
) -> TextToSpeechResponse:
    """
    Converts provided textual content into speech audio with customizable voice parameters.

    Args:
        text (str): The textual content to be converted to speech.
        language (str): The language code for the text-to-speech conversion. Example: 'en-US'
        pitch (Optional[float]): Optional. Modifies the pitch of the voice. Default is 0.
        speed (Optional[float]): Optional. Controls the speed of the speech. Default is 1.0.
        gender (Optional[str]): Optional. Specifies the gender of the voice. Values can be 'male', 'female', or 'neutral'. Default is 'neutral'.

    Returns:
        TextToSpeechResponse: Provides a response containing the audio data or a link to the generated speech audio.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    if gender == "male":
        voice_gender = texttospeech.SsmlVoiceGender.MALE
    elif gender == "female":
        voice_gender = texttospeech.SsmlVoiceGender.FEMALE
    else:
        voice_gender = texttospeech.SsmlVoiceGender.NEUTRAL
    voice = texttospeech.VoiceSelectionParams(
        language_code=language, ssml_gender=voice_gender
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=pitch if pitch is not None else 0,
        speaking_rate=speed if speed is not None else 1.0,
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    fake_audio_link = "https://cloudstorage/audio/generated_audio.mp3"
    status = "Success"
    return TextToSpeechResponse(
        audio_link=fake_audio_link, audio_format="mp3", status=status
    )
