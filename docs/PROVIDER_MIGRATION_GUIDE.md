# Provider System Migration Guide

## What Changed?

Paper2Slides now supports multiple image generation providers through a flexible provider system. This allows you to choose between:
- **OpenRouter** (default): Proxy service for various AI models
- **Google GenAI**: Direct access to Google's Generative AI API

## Why This Change?

1. **Flexibility**: Choose the provider that best fits your needs
2. **Cost Optimization**: Different providers have different pricing models
3. **Performance**: Direct API access may offer better latency
4. **Future-Proof**: Easy to add more providers (OpenAI DALL-E, Midjourney, etc.)

---

## For Existing Users

### No Changes Required! 🎉

If you're already using Paper2Slides with OpenRouter, **nothing changes**:
- Your existing `.env` configuration still works
- Default provider is still OpenRouter
- All existing code continues to work

### Optional: Migrate to Google GenAI

If you want to use Google GenAI directly:

1. **Install the package**:
   ```bash
   pip install google-generativeai
   ```

2. **Update `.env`**:
   ```bash
   # Change provider
   IMAGE_GEN_PROVIDER="google"

   # Add Google API key
   GOOGLE_API_KEY="your-google-api-key"

   # Optional: specify model
   IMAGE_GEN_MODEL="gemini-3-pro-image-preview"
   ```

3. **That's it!** Your CLI and API usage remain unchanged.

---

## For New Users

### Quick Start with OpenRouter

1. Get API key from [OpenRouter](https://openrouter.ai/)

2. Create `.env` file:
   ```bash
   cp paper2slides/.env.example paper2slides/.env
   ```

3. Edit `.env`:
   ```bash
   IMAGE_GEN_PROVIDER="openrouter"
   IMAGE_GEN_API_KEY="your-openrouter-key"
   ```

4. Run:
   ```bash
   python -m paper2slides --input paper.pdf --style doraemon
   ```

### Quick Start with Google GenAI

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Install package:
   ```bash
   pip install google-generativeai
   ```

3. Edit `.env`:
   ```bash
   IMAGE_GEN_PROVIDER="google"
   GOOGLE_API_KEY="your-google-key"
   ```

4. Run:
   ```bash
   python -m paper2slides --input paper.pdf --style doraemon
   ```

---

## API Changes

### Before (Still Works!)

```python
from paper2slides.generator import ImageGenerator

# Old way - still works, uses environment config
generator = ImageGenerator()
images = generator.generate(plan, gen_input)
```

### After (New Options)

```python
from paper2slides.generator import ImageGenerator
from paper2slides.generator.providers import (
    ProviderFactory,
    GoogleGenAIProvider
)

# Option 1: Use environment config (recommended)
generator = ImageGenerator()

# Option 2: Explicitly create provider
provider = ProviderFactory.create("google", api_key="...")
generator = ImageGenerator(provider=provider)

# Option 3: Direct provider instance
provider = GoogleGenAIProvider(api_key="...")
generator = ImageGenerator(provider=provider)
```

---

## Environment Variable Reference

### Old Configuration (Deprecated but Still Works)
```bash
IMAGE_GEN_API_KEY="openrouter-key"
IMAGE_GEN_BASE_URL="https://openrouter.ai/api/v1"
```

### New Configuration (Recommended)

#### For OpenRouter:
```bash
IMAGE_GEN_PROVIDER="openrouter"
IMAGE_GEN_API_KEY="openrouter-key"
IMAGE_GEN_BASE_URL="https://openrouter.ai/api/v1"  # Optional
IMAGE_GEN_MODEL="google/gemini-3-pro-image-preview"  # Optional
```

#### For Google GenAI:
```bash
IMAGE_GEN_PROVIDER="google"
GOOGLE_API_KEY="google-key"
IMAGE_GEN_MODEL="gemini-3-pro-image-preview"  # Optional
```

---

## Backward Compatibility

✅ **All existing code continues to work**
- Old `ImageGenerator()` initialization still works
- Environment variables are backward compatible
- No breaking changes to public APIs

---

## Testing

Test your provider setup:

```bash
# Run provider tests
python tests/test_providers.py

# Run example script
python examples/use_google_genai_provider.py
```

---

## Troubleshooting

### "google-generativeai not installed"
```bash
pip install google-generativeai
```

### "No API key found"
Make sure the correct key is set:
- OpenRouter: `IMAGE_GEN_API_KEY`
- Google GenAI: `GOOGLE_API_KEY`

### "Unknown provider"
Check `IMAGE_GEN_PROVIDER` value:
- Valid: `"openrouter"`, `"google"`, `"genai"`
- Default: `"openrouter"` (if not set)

---

## Documentation

- **Provider Documentation**: See `docs/IMAGE_GENERATION_PROVIDERS.md`
- **Code Examples**: See `examples/use_google_genai_provider.py`
- **Test Suite**: See `tests/test_providers.py`

---

## Questions?

1. Check the [Provider Documentation](./IMAGE_GENERATION_PROVIDERS.md)
2. Run the test suite: `python tests/test_providers.py`
3. Open an issue on GitHub

---

## Summary

| Feature | Before | After |
|---------|--------|-------|
| Default Provider | OpenRouter | OpenRouter (no change) |
| Supported Providers | OpenRouter only | OpenRouter + Google GenAI |
| Configuration | `.env` | `.env` (backward compatible) |
| API Compatibility | N/A | ✅ 100% backward compatible |
| New Dependencies | None required | `google-generativeai` (optional) |

**Bottom Line**: Existing users don't need to change anything. New users have more flexibility!
