"""
Image Generation Providers

Support multiple image generation backends (OpenRouter, Google GenAI, etc.)
"""
import os
import base64
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class ImageGenerationRequest:
    """Request for image generation."""
    prompt: str
    reference_images: List[Dict]  # List of {figure_id, caption, base64, mime_type}
    model: str = None


@dataclass
class ImageGenerationResponse:
    """Response from image generation."""
    image_data: bytes
    mime_type: str


class ImageGenerationProvider(ABC):
    """Abstract base class for image generation providers."""

    @abstractmethod
    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate an image from prompt and reference images."""
        pass

    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model name for this provider."""
        pass


class OpenRouterProvider(ImageGenerationProvider):
    """OpenRouter provider for Gemini image generation."""

    def __init__(
        self,
        api_key: str = None,
        base_url: str = "https://openrouter.ai/api/v1",
        model: str = "google/gemini-3-pro-image-preview"
    ):
        self.api_key = api_key or os.getenv("IMAGE_GEN_API_KEY", "")
        self.base_url = base_url
        self.default_model = model

        if not self.api_key:
            raise ValueError("OpenRouter API key is required. Set IMAGE_GEN_API_KEY environment variable.")

        # Use OpenAI client with OpenRouter endpoint
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        logger.info(f"Initialized OpenRouter provider with model: {model}")

    def get_default_model(self) -> str:
        return self.default_model

    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate image using OpenRouter API."""
        model = request.model or self.default_model

        # Build message content
        content = [{"type": "text", "text": request.prompt}]

        # Add reference images with labels
        for img in request.reference_images:
            if img.get("base64") and img.get("mime_type"):
                fig_id = img.get("figure_id", "Figure")
                caption = img.get("caption", "")
                label = f"[{fig_id}]: {caption}" if caption else f"[{fig_id}]"
                content.append({"type": "text", "text": label})
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{img['mime_type']};base64,{img['base64']}"}
                })

        logger.debug(f"Calling OpenRouter API with model: {model}")

        # Call API
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": content}],
            extra_body={"modalities": ["image", "text"]}
        )

        # Extract image from response
        if not response or not hasattr(response, 'choices') or not response.choices:
            raise RuntimeError(f"Invalid API response: {response}")

        message = response.choices[0].message
        if not hasattr(message, 'images') or not message.images:
            raise RuntimeError("No images in API response")

        image_url = message.images[0]['image_url']['url']
        if not image_url.startswith('data:'):
            raise RuntimeError(f"Unexpected image URL format: {image_url[:50]}")

        # Parse data URL
        header, base64_data = image_url.split(',', 1)
        mime_type = header.split(':')[1].split(';')[0]
        image_data = base64.b64decode(base64_data)

        logger.info(f"Image generated successfully via OpenRouter ({len(image_data)} bytes)")
        return ImageGenerationResponse(image_data=image_data, mime_type=mime_type)


class GoogleGenAIProvider(ImageGenerationProvider):
    """Google GenAI provider for Gemini image generation."""

    def __init__(
        self,
        api_key: str = None,
        model: str = "gemini-3-pro-image-preview"
    ):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        self.default_model = model

        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")

        try:
            from google import genai
            from google.genai import types
            self.genai = genai
            self.types = types

            # Create client
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Initialized Google GenAI provider with model: {model}")
        except ImportError:
            raise ImportError(
                "google-generativeai package is required for GoogleGenAIProvider. "
                "Install it with: pip install google-generativeai"
            )

    def get_default_model(self) -> str:
        return self.default_model

    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate image using Google GenAI API."""
        model_name = request.model or self.default_model

        # Build content list
        content_parts = []

        # Add prompt text first
        content_parts.append(request.prompt)

        # Add reference images if any
        for img in request.reference_images:
            if img.get("base64") and img.get("mime_type"):
                # Add label before image
                fig_id = img.get("figure_id", "Figure")
                caption = img.get("caption", "")
                label = f"[{fig_id}]: {caption}" if caption else f"[{fig_id}]"
                content_parts.append(label)

                # Decode base64 to bytes
                image_bytes = base64.b64decode(img['base64'])

                # Create PIL Image from bytes
                from PIL import Image
                import io
                pil_image = Image.open(io.BytesIO(image_bytes))
                content_parts.append(pil_image)

        logger.debug(f"Calling Google GenAI API with model: {model_name}")

        # Configure generation with image output (following official example)
        config = self.types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],  # Request both text and image
            image_config=self.types.ImageConfig(    # Note: ImageConfig not ImageGenerationConfig
                aspect_ratio="16:9",  # For slides
                image_size="4K"       # High quality: "1K", "2K", "4K"
            )
        )

        # Generate content using the new API
        response = self.client.models.generate_content(
            model=model_name,
            contents=content_parts,
            config=config
        )

        # Extract image from response.parts (following official example)
        image_data = None
        mime_type = "image/png"

        for part in response.parts:
            # Check if this part has text
            if part.text is not None:
                logger.debug(f"Response text: {part.text[:100]}...")

            # Check if this part has an image
            try:
                image = part.as_image()
                if image:
                    # Save to a temporary file path first (following official example pattern)
                    import tempfile
                    import os
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        tmp_path = tmp.name

                    # Save using the pattern from official example
                    image.save(tmp_path)

                    # Read the file content
                    with open(tmp_path, 'rb') as f:
                        image_data = f.read()

                    # Clean up
                    os.unlink(tmp_path)

                    mime_type = "image/png"
                    break
            except Exception as e:
                logger.warning(f"Failed to extract image from part: {e}")
                continue

        if not image_data:
            raise RuntimeError("No image data in API response")

        logger.info(f"Image generated successfully via Google GenAI ({len(image_data)} bytes)")
        return ImageGenerationResponse(image_data=image_data, mime_type=mime_type)


class ProviderFactory:
    """Factory for creating image generation providers."""

    PROVIDERS = {
        "openrouter": OpenRouterProvider,
        "google": GoogleGenAIProvider,
        "genai": GoogleGenAIProvider,  # Alias
    }

    @classmethod
    def create(cls, provider_name: str, **kwargs) -> ImageGenerationProvider:
        """
        Create an image generation provider.

        Args:
            provider_name: Provider name ("openrouter", "google", "genai")
            **kwargs: Provider-specific configuration

        Returns:
            ImageGenerationProvider instance

        Raises:
            ValueError: If provider name is unknown
        """
        provider_name = provider_name.lower()

        if provider_name not in cls.PROVIDERS:
            available = ", ".join(cls.PROVIDERS.keys())
            raise ValueError(
                f"Unknown provider: {provider_name}. "
                f"Available providers: {available}"
            )

        provider_class = cls.PROVIDERS[provider_name]
        return provider_class(**kwargs)

    @classmethod
    def from_env(cls) -> ImageGenerationProvider:
        """
        Create provider from environment variables.

        Environment variables:
            IMAGE_GEN_PROVIDER: Provider name (default: "openrouter")
            IMAGE_GEN_API_KEY: API key for OpenRouter
            IMAGE_GEN_BASE_URL: Base URL for OpenRouter (optional)
            IMAGE_GEN_MODEL: Model name (optional)
            GOOGLE_API_KEY: API key for Google GenAI

        Returns:
            ImageGenerationProvider instance
        """
        provider_name = os.getenv("IMAGE_GEN_PROVIDER", "openrouter").lower()

        if provider_name == "openrouter":
            return cls.create(
                provider_name,
                api_key=os.getenv("IMAGE_GEN_API_KEY"),
                base_url=os.getenv("IMAGE_GEN_BASE_URL", "https://openrouter.ai/api/v1"),
                model=os.getenv("IMAGE_GEN_MODEL", "google/gemini-3-pro-image-preview")
            )
        elif provider_name in ["google", "genai"]:
            return cls.create(
                provider_name,
                api_key=os.getenv("GOOGLE_API_KEY"),
                model=os.getenv("IMAGE_GEN_MODEL", "gemini-3-pro-image-preview")
            )
        else:
            raise ValueError(f"Unsupported provider in environment: {provider_name}")
