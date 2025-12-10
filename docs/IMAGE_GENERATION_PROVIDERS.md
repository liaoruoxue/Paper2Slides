# Image Generation Providers

Paper2Slides supports multiple image generation providers for flexibility and cost optimization.

## Available Providers

### 1. OpenRouter (Default)
- **Description**: Uses OpenRouter as a proxy to access various models including Gemini
- **Advantages**:
  - Simple unified API
  - Pay-as-you-go pricing
  - Access to multiple models
- **Setup**: Requires OpenRouter API key

### 2. Google GenAI (Direct)
- **Description**: Directly uses Google's Generative AI API for Gemini models
- **Advantages**:
  - Direct connection to Google's API
  - Potentially lower latency
  - Native Google API features
- **Setup**: Requires Google API key and `google-generativeai` package

---

## Configuration

### Environment Variables

Edit your `.env` file (copy from `.env.example`):

#### Using OpenRouter (Default)

```bash
# Provider selection
IMAGE_GEN_PROVIDER="openrouter"

# OpenRouter credentials
IMAGE_GEN_API_KEY="your-openrouter-api-key"
IMAGE_GEN_BASE_URL="https://openrouter.ai/api/v1"  # Optional
IMAGE_GEN_MODEL="google/gemini-3-pro-image-preview"  # Optional
```

#### Using Google GenAI Directly

```bash
# Provider selection
IMAGE_GEN_PROVIDER="google"

# Google API credentials
GOOGLE_API_KEY="your-google-api-key"
IMAGE_GEN_MODEL="gemini-3-pro-image-preview"  # Optional

# Install the required package:
# pip install google-generativeai
```

---

## Installation

### For OpenRouter
No additional packages needed (uses `openai` package which is already installed).

### For Google GenAI
Install the Google GenAI SDK:

```bash
pip install google-generativeai
```

Or uncomment the line in `requirements.txt`:
```txt
# google-generativeai>=0.3.0
```

---

## Usage Examples

### CLI Usage

The provider is automatically selected based on your `.env` configuration:

```bash
# Will use the provider specified in IMAGE_GEN_PROVIDER
python -m paper2slides \
  --input paper.pdf \
  --style doraemon \
  --length medium
```

### Programmatic Usage

#### Using Environment Configuration (Recommended)

```python
from paper2slides.generator import ImageGenerator
from paper2slides.generator.content_planner import ContentPlanner

# Automatically creates provider from environment
generator = ImageGenerator()

# Generate images
images = generator.generate(plan, gen_input)
```

#### Explicitly Specifying Provider

```python
from paper2slides.generator import ImageGenerator
from paper2slides.generator.providers import (
    ProviderFactory,
    OpenRouterProvider,
    GoogleGenAIProvider
)

# Option 1: Use factory with provider name
provider = ProviderFactory.create(
    "openrouter",
    api_key="your-key",
    model="google/gemini-3-pro-image-preview"
)

# Option 2: Create provider directly
provider = GoogleGenAIProvider(
    api_key="your-google-key",
    model="gemini-3-pro-image-preview"
)

# Use with generator
generator = ImageGenerator(provider=provider)
images = generator.generate(plan, gen_input)
```

---

## API Keys Setup

### Getting OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Getting Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new API key or use an existing one
5. Copy the key to your `.env` file

---

## Troubleshooting

### "No API key found" Error

**Problem**:
```
ValueError: OpenRouter API key is required. Set IMAGE_GEN_API_KEY environment variable.
```

**Solution**:
- Make sure `.env` file exists in the `paper2slides/` directory
- Check that the appropriate API key variable is set:
  - `IMAGE_GEN_API_KEY` for OpenRouter
  - `GOOGLE_API_KEY` for Google GenAI

### "Unknown provider" Error

**Problem**:
```
ValueError: Unknown provider: xyz
```

**Solution**:
- Check `IMAGE_GEN_PROVIDER` in `.env`
- Valid values: `"openrouter"`, `"google"`, or `"genai"`

### "google-generativeai not installed" Error

**Problem**:
```
ImportError: google-generativeai package is required for GoogleGenAIProvider
```

**Solution**:
```bash
pip install google-generativeai
```

### Rate Limiting

Both providers have rate limits:

**OpenRouter**:
- Varies by model and payment plan
- Check [OpenRouter limits](https://openrouter.ai/docs#limits)

**Google GenAI**:
- Free tier: 60 requests per minute
- Paid tier: Higher limits
- Check [Google AI limits](https://ai.google.dev/pricing)

**Mitigation**:
- The generator includes automatic retry logic with exponential backoff
- For large batches, use `--parallel 1` to reduce concurrent requests
- Consider upgrading your plan if hitting limits frequently

---

## Cost Comparison

### OpenRouter Pricing (as of 2024)
- Gemini 3 Pro Image Preview: ~$X per 1K tokens (check current rates)
- Pay-as-you-go, no monthly fees

### Google GenAI Pricing
- Free tier: Limited requests per day
- Paid tier: Competitive pricing for high volume
- Check [Google AI pricing](https://ai.google.dev/pricing) for current rates

**Recommendation**:
- **OpenRouter**: Better for getting started, flexible usage
- **Google GenAI**: Better for high-volume production usage with direct Google integration

---

## Adding New Providers

To add a new provider (e.g., OpenAI DALL-E, Midjourney API):

1. **Create Provider Class**:

```python
# paper2slides/generator/providers.py

class MyCustomProvider(ImageGenerationProvider):
    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        # Initialize your client...

    def get_default_model(self) -> str:
        return "my-model-name"

    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        # Your implementation...
        pass
```

2. **Register in Factory**:

```python
# In ProviderFactory class
PROVIDERS = {
    "openrouter": OpenRouterProvider,
    "google": GoogleGenAIProvider,
    "mycustom": MyCustomProvider,  # Add here
}
```

3. **Update Environment Configuration**:

```bash
# .env
IMAGE_GEN_PROVIDER="mycustom"
MY_CUSTOM_API_KEY="..."
```

---

## Advanced Configuration

### Custom Model Parameters

Some providers support additional parameters:

```python
from paper2slides.generator.providers import GoogleGenAIProvider

provider = GoogleGenAIProvider(
    api_key="your-key",
    model="gemini-3-pro-image-preview"
)

# You can extend the provider class to customize generation config
# See providers.py for implementation details
```

### Multiple Providers in Same Project

```python
# Use different providers for different tasks
openrouter_gen = ImageGenerator(
    provider=ProviderFactory.create("openrouter", api_key="...")
)

google_gen = ImageGenerator(
    provider=ProviderFactory.create("google", api_key="...")
)

# Generate slides with OpenRouter
slides_images = openrouter_gen.generate(slides_plan, gen_input)

# Generate poster with Google GenAI
poster_images = google_gen.generate(poster_plan, gen_input)
```

---

## FAQ

### Q: Which provider should I use?

**A**:
- **Getting started**: Use OpenRouter (simpler setup, no extra packages)
- **Production with high volume**: Consider Google GenAI (potentially lower cost and latency)
- **Experimenting**: OpenRouter gives you access to multiple models easily

### Q: Can I use both providers in the same project?

**A**: Yes! You can programmatically create different `ImageGenerator` instances with different providers.

### Q: What if I want to use a different model?

**A**: Set `IMAGE_GEN_MODEL` in your `.env` file. For OpenRouter, use their model naming (e.g., `google/gemini-3-pro-image-preview`). For Google GenAI, use Google's model names (e.g., `gemini-3-pro-image-preview`).

### Q: Is my API key secure?

**A**:
- Never commit `.env` files to git (already in `.gitignore`)
- Use environment variables in production
- Rotate keys regularly
- Consider using secret management services for production deployments

---

## Support

For issues related to:
- **OpenRouter**: Check [OpenRouter Docs](https://openrouter.ai/docs)
- **Google GenAI**: Check [Google AI Studio Docs](https://ai.google.dev/docs)
- **Paper2Slides**: Open an issue on GitHub

---

**Last Updated**: 2024-12-10
