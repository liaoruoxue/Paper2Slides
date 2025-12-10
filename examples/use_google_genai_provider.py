"""
Example: Using Google GenAI Provider for Image Generation

This example demonstrates how to use the Google GenAI provider directly
instead of OpenRouter.

Prerequisites:
    1. pip install google-generativeai
    2. Set GOOGLE_API_KEY environment variable
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from paper2slides.generator import ImageGenerator
from paper2slides.generator.providers import GoogleGenAIProvider, ProviderFactory


def example_1_using_environment():
    """Example 1: Use provider from environment configuration."""
    print("\n" + "="*60)
    print("Example 1: Using Environment Configuration")
    print("="*60)

    # Make sure IMAGE_GEN_PROVIDER is set to "google" in .env
    # And GOOGLE_API_KEY is set

    # This will automatically use Google GenAI if configured
    generator = ImageGenerator()
    print(f"✓ Generator created with provider: {type(generator.provider).__name__}")
    print(f"✓ Using model: {generator.model}")

    # Now use generator normally...
    # generator.generate(plan, gen_input)


def example_2_explicit_provider():
    """Example 2: Explicitly create Google GenAI provider."""
    print("\n" + "="*60)
    print("Example 2: Explicit Provider Creation")
    print("="*60)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not set. Please set it in environment.")
        return

    # Create provider directly
    provider = GoogleGenAIProvider(
        api_key=api_key,
        model="gemini-3-pro-image-preview"
    )
    print(f"✓ Created provider: {type(provider).__name__}")

    # Use with generator
    generator = ImageGenerator(provider=provider)
    print(f"✓ Generator initialized with custom provider")

    # Now use generator normally...
    # generator.generate(plan, gen_input)


def example_3_using_factory():
    """Example 3: Use factory to create provider."""
    print("\n" + "="*60)
    print("Example 3: Using Provider Factory")
    print("="*60)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not set. Please set it in environment.")
        return

    # Use factory
    provider = ProviderFactory.create(
        "google",
        api_key=api_key,
        model="gemini-3-pro-image-preview"
    )
    print(f"✓ Factory created provider: {type(provider).__name__}")

    generator = ImageGenerator(provider=provider)
    print(f"✓ Generator ready")


def example_4_compare_providers():
    """Example 4: Compare different providers."""
    print("\n" + "="*60)
    print("Example 4: Comparing Providers")
    print("="*60)

    # Check which providers are available
    openrouter_key = os.getenv("IMAGE_GEN_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")

    print(f"OpenRouter available: {'✓' if openrouter_key else '✗'}")
    print(f"Google GenAI available: {'✓' if google_key else '✗'}")

    if openrouter_key and google_key:
        # Create both providers
        openrouter_gen = ImageGenerator(
            provider=ProviderFactory.create(
                "openrouter",
                api_key=openrouter_key,
                model="google/gemini-3-pro-image-preview"
            )
        )

        google_gen = ImageGenerator(
            provider=ProviderFactory.create(
                "google",
                api_key=google_key,
                model="gemini-3-pro-image-preview"
            )
        )

        print("\n✓ Both generators ready for comparison")
        print("\nYou can now use them to generate images and compare:")
        print("  - Quality")
        print("  - Latency")
        print("  - Cost")
        print("  - Features")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Google GenAI Provider Examples")
    print("="*60)

    # Check if google-generativeai is installed
    try:
        import google.generativeai
        print("✓ google-generativeai package installed")
    except ImportError:
        print("❌ google-generativeai package not installed")
        print("\nTo use Google GenAI provider, install it:")
        print("  pip install google-generativeai")
        return 1

    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n⚠️  GOOGLE_API_KEY not set in environment")
        print("\nTo use Google GenAI provider:")
        print("1. Get API key from: https://makersuite.google.com/app/apikey")
        print("2. Set in .env file: GOOGLE_API_KEY=your-key")
        print("3. Set provider: IMAGE_GEN_PROVIDER=google")
        return 1

    # Run examples
    example_1_using_environment()
    example_2_explicit_provider()
    example_3_using_factory()
    example_4_compare_providers()

    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
