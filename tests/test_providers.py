"""
Test image generation providers.

Run with:
    python tests/test_providers.py
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from paper2slides.generator.providers import (
    ProviderFactory,
    OpenRouterProvider,
    GoogleGenAIProvider,
    ImageGenerationRequest,
)


def test_openrouter_provider():
    """Test OpenRouter provider."""
    print("\n" + "="*60)
    print("Testing OpenRouter Provider")
    print("="*60)

    api_key = os.getenv("IMAGE_GEN_API_KEY")
    if not api_key:
        print("⚠️  IMAGE_GEN_API_KEY not set. Skipping OpenRouter test.")
        return False

    try:
        # Create provider
        provider = OpenRouterProvider(
            api_key=api_key,
            model="google/gemini-3-pro-image-preview"
        )
        print(f"✓ Provider initialized: {type(provider).__name__}")
        print(f"✓ Default model: {provider.get_default_model()}")

        # Create a simple test request
        request = ImageGenerationRequest(
            prompt="""
Create a simple test slide with the following:
- Title: "Hello World"
- Background: white
- Text: black
- A simple geometric shape (circle or square) in the center
Output a 16:9 horizontal slide image.
""",
            reference_images=[],
            model=None  # Use default
        )

        print("⏳ Generating test image...")
        response = provider.generate_image(request)

        print(f"✓ Image generated successfully")
        print(f"  - Size: {len(response.image_data)} bytes")
        print(f"  - MIME type: {response.mime_type}")

        # Save test image
        output_path = Path(__file__).parent / "output_openrouter_test.png"
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.image_data)
        print(f"✓ Test image saved: {output_path}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_google_provider():
    """Test Google GenAI provider."""
    print("\n" + "="*60)
    print("Testing Google GenAI Provider")
    print("="*60)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not set. Skipping Google GenAI test.")
        return False

    try:
        # Check if package is installed
        try:
            import google.generativeai as genai
            print("✓ google-generativeai package installed")
        except ImportError:
            print("❌ google-generativeai package not installed")
            print("   Install with: pip install google-generativeai")
            return False

        # Create provider
        provider = GoogleGenAIProvider(
            api_key=api_key,
            model="gemini-3-pro-image-preview"
        )
        print(f"✓ Provider initialized: {type(provider).__name__}")
        print(f"✓ Default model: {provider.get_default_model()}")

        # Create a simple test request
        request = ImageGenerationRequest(
            prompt="""
Create a simple test slide with the following:
- Title: "Hello World"
- Background: white
- Text: black
- A simple geometric shape (circle or square) in the center
Output a 16:9 horizontal slide image.
""",
            reference_images=[],
            model=None  # Use default
        )

        print("⏳ Generating test image...")
        response = provider.generate_image(request)

        print(f"✓ Image generated successfully")
        print(f"  - Size: {len(response.image_data)} bytes")
        print(f"  - MIME type: {response.mime_type}")

        # Save test image
        output_path = Path(__file__).parent / "output_google_test.png"
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.image_data)
        print(f"✓ Test image saved: {output_path}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_factory():
    """Test provider factory."""
    print("\n" + "="*60)
    print("Testing Provider Factory")
    print("="*60)

    # Test factory with environment variables
    provider_name = os.getenv("IMAGE_GEN_PROVIDER", "openrouter")
    print(f"Environment provider: {provider_name}")

    try:
        provider = ProviderFactory.from_env()
        print(f"✓ Factory created provider: {type(provider).__name__}")
        print(f"✓ Default model: {provider.get_default_model()}")
        return True
    except Exception as e:
        print(f"❌ Factory error: {e}")
        return False


def main():
    """Run all provider tests."""
    print("\n" + "="*60)
    print("Image Generation Provider Tests")
    print("="*60)

    results = []

    # Test factory
    results.append(("Factory", test_factory()))

    # Test OpenRouter
    results.append(("OpenRouter", test_openrouter_provider()))

    # Test Google GenAI
    results.append(("Google GenAI", test_google_provider()))

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    for name, success in results:
        status = "✓ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")

    all_passed = all(success for _, success in results if success is not False)
    skipped = sum(1 for _, success in results if success is False)

    print(f"\nTotal: {len(results)} tests")
    print(f"Passed: {sum(1 for _, s in results if s is True)}")
    print(f"Failed: {sum(1 for _, s in results if s is False and s is not None)}")
    print(f"Skipped: {sum(1 for _, s in results if s is False and s is None)}")

    return 0 if all_passed or skipped > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
