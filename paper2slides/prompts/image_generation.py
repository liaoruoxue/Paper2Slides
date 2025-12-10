"""
Prompts and style configurations for image generation
"""
from typing import Dict

# Prompt template for processing custom style
STYLE_PROCESS_PROMPT = """User wants this style for presentation slides: {user_style}

IMPORTANT RULES:
1. Default to MORANDI COLOR PALETTE (soft, muted, low-saturation colors with gray undertones) and LIGHT background unless user specifies otherwise.
2. Keep it CLEAN and SIMPLE - NO flashy/gaudy elements. Every visual element must be MEANINGFUL.
3. LIMITED COLOR PALETTE (3-4 colors max).

Output JSON:
{{
    "style_name": "Style name with brief description (e.g., Cyberpunk sci-fi style with high-tech aesthetic)",
    "color_tone": "Color tone description - prefer Morandi palette with light background (e.g., light cream background with muted sage green and dusty rose accents)",
    "special_elements": "Any special visual elements like characters, mascots, motifs - must be MEANINGFUL, not random decoration",
    "decorations": "Background/border effects - keep SIMPLE and CLEAN (or empty string)",
    "valid": true,
    "error": null
}}

Examples:
- "cyberpunk": {{"style_name": "Cyberpunk sci-fi style with high-tech aesthetic", "color_tone": "dark background with neon cyan and magenta accents", "special_elements": "", "decorations": "subtle grid pattern, neon glow on borders", "valid": true, "error": null}}
- "Studio Ghibli": {{"style_name": "Studio Ghibli anime style with whimsical aesthetic", "color_tone": "light cream background with soft Morandi watercolor tones - muted sage, dusty pink, soft gray-blue", "special_elements": "Totoro or soot sprites can appear as friendly guides - must relate to content", "decorations": "soft clouds or nature elements as borders", "valid": true, "error": null}}
- "minimalist": {{"style_name": "Clean minimalist style", "color_tone": "light warm gray background with Morandi palette - charcoal text, muted gold accent", "special_elements": "", "decorations": "", "valid": true, "error": null}}

If inappropriate, set valid=false with error."""

# Format prefixes
FORMAT_POSTER = "Wide landscape poster layout (16:9 aspect ratio). Just ONE poster. Keep information density moderate, leave whitespace for readability."
FORMAT_POSTER_A0 = """PORTRAIT A0 academic conference poster (aspect ratio approximately 2:3 vertical, like 841mm width x 1189mm height).
Generate ONE complete vertical poster image. The poster should be TALLER than it is wide.
This is a professional academic conference poster with structured layout."""
FORMAT_SLIDE = "Wide landscape slide layout (16:9 aspect ratio)."

# Style hints for poster (landscape 16:9)
POSTER_STYLE_HINTS: Dict[str, str] = {
    "academic": "Academic conference poster style with LIGHT CLEAN background. English text only. Use PROFESSIONAL, CLEAR tones with good contrast and academic fonts. Use 3-column layout showing story progression. Preserve details from the content. Title section at the top can have a colored background bar to make it stand out. FIGURES: Preserve original scientific figures - maintain their accuracy, style, and integrity. Include institution logo if present.",
    "doraemon": "Classic Doraemon anime style, bright and friendly. English text only. Use WARM, ELEGANT, MUTED tones. Use ROUNDED sans-serif fonts for ALL text (NO artistic/fancy/decorative fonts). Large readable text. Use 3-column layout showing story progression. Each column can have scene-appropriate background (e.g., cloudy for problem, clearing for method, sunny for result). Keep it simple, not too fancy. Doraemon character as guide only (1-2 small figures), not the main focus.",
}

# Style hints for A0 portrait poster
POSTER_A0_STYLE_HINTS: Dict[str, str] = {
    "academic": """Professional academic conference poster style for A0 PORTRAIT format.

LAYOUT STRUCTURE (Top to Bottom):
┌─────────────────────────────────┐
│      TITLE BAR (colored)        │  ← Title, authors, affiliations, logos
├─────────────────────────────────┤
│                                 │
│  ┌─────────┐ ┌─────────┐       │
│  │  LEFT   │ │ CENTER  │       │  ← 2-3 column layout for content
│  │ COLUMN  │ │ COLUMN  │       │
│  │         │ │         │       │
│  │ Intro/  │ │ Method  │       │
│  │ Problem │ │ Details │       │
│  └─────────┘ └─────────┘       │
│                                 │
│  ┌─────────────────────┐       │
│  │   RESULTS SECTION   │       │  ← Wide section for tables/figures
│  │   (tables, charts)  │       │
│  └─────────────────────┘       │
│                                 │
│  ┌─────────────────────┐       │
│  │    CONCLUSIONS      │       │  ← Bottom section
│  └─────────────────────┘       │
└─────────────────────────────────┘

STYLE REQUIREMENTS:
- Background: Clean white or very light gray (#f8f9fa)
- Title bar: Navy blue (#1e3a8a) or institution color with white text
- Section headers: Bold, clear hierarchy
- Typography: Professional sans-serif (like Roboto, Arial, Helvetica)
  * Title: 72-96pt bold
  * Section headers: 48-60pt bold
  * Body text: 28-36pt regular
- Colors: LIMITED PALETTE (3-4 colors max) - navy blue primary, light blue accent, white/gray background
- Figures: REDRAW to match poster style, maintain scientific accuracy
- Tables: Clean borders, highlight key data
- Include QR code or contact info at bottom if space permits
- Leave adequate whitespace for readability
- English text only""",

    "doraemon": """Doraemon-themed academic poster style for A0 PORTRAIT format.

LAYOUT STRUCTURE (Top to Bottom):
┌─────────────────────────────────┐
│      TITLE SECTION              │  ← Title with Doraemon decorative frame
│   (sky blue banner/frame)       │
├─────────────────────────────────┤
│                                 │
│  Story-based layout:            │
│  ┌─────────────────────┐       │
│  │  THE PROBLEM        │       │  ← Nobita struggling (visual metaphor)
│  │  (cloudy scene)     │       │
│  └─────────────────────┘       │
│                                 │
│  ┌─────────────────────┐       │
│  │  THE SOLUTION       │       │  ← Doraemon presents gadget/method
│  │  (brightening)      │       │
│  └─────────────────────┘       │
│                                 │
│  ┌─────────────────────┐       │
│  │  THE RESULTS        │       │  ← Happy outcome with data
│  │  (sunny scene)      │       │
│  └─────────────────────┘       │
│                                 │
│  [Conclusions with characters]  │
└─────────────────────────────────┘

STYLE REQUIREMENTS:
- Background: Soft sky blue gradient or warm cream
- Colors: SOPHISTICATED Doraemon palette - NOT childish
  * Primary: Sky blue (#7EC8E3), white
  * Accent: Coral red, warm yellow
  * MUTED, ELEGANT tones throughout
- Typography: ROUNDED sans-serif for ALL text
  * Title: 72-96pt bold
  * Body: 28-36pt regular
- Character usage: MEANINGFUL integration
  * Doraemon as guide/presenter
  * Characters should relate to content themes
  * NOT random decoration
- Figures: Redraw in matching anime style
- Tables: Simple, clean, with soft borders
- English text only""",
}

# A0 poster layout templates by density
POSTER_A0_LAYOUTS: Dict[str, str] = {
    "sparse": """A0 Poster Layout (SPARSE density):
- Title section: Paper title, authors, affiliations (top 15%)
- 2 main columns:
  * Left: Background/Problem (brief)
  * Right: Method overview (key points only)
- Results: 1-2 key figures or tables with main findings
- Conclusion: 3-4 bullet points
- Keep generous whitespace, large fonts, minimal text""",

    "medium": """A0 Poster Layout (MEDIUM density):
- Title section: Full title, all authors, affiliations, logos (top 12%)
- 3 main content columns:
  * Left: Introduction, Background, Problem statement
  * Center: Method with architecture figure
  * Right: Key results with main table
- Wide results section: Additional figures, comparison charts
- Conclusion: Main contributions (5-6 points)
- Contact/QR code at bottom""",

    "dense": """A0 Poster Layout (DENSE density):
- Title section: Complete header with all details (top 10%)
- 3 content columns with subsections:
  * Left: Full introduction, related work summary, problem formulation
  * Center: Complete method with multiple figures, algorithm details
  * Right: Comprehensive results, ablation studies
- Wide results section: Multiple tables, all key figures
- Analysis section: Discussion of findings
- Conclusion: All contributions, future work
- References, acknowledgments, contact info at bottom""",
}

# Style hints for slides
SLIDE_STYLE_HINTS: Dict[str, str] = {
    "academic": "Professional STANDARD ACADEMIC style. English text only. Use ROUNDED sans-serif fonts for ALL text. Use MORANDI COLOR PALETTE (soft, muted, low-saturation colors) with LIGHT background. Clean simple lines. IMPORTANT: Figures and tables are CRUCIAL - REDRAW them to match the visual style, make them BLEND seamlessly with the background and color scheme. Visualize data with CHARTS (bar, line, pie, radar) - REDRAW charts to match the style, make them LARGE and meaningful. Layout should be SPACIOUS and ELEGANT - avoid crowding, leave breathing room. Overall feel: minimal, scholarly, professional, sophisticated.",
    "doraemon": "Classic Doraemon anime style, bright and friendly. Doraemon anime style with SOPHISTICATED, REFINED color palette (NOT childish bright colors). English text only. PRESERVE EVERY DETAIL from the content. Use ROUNDED sans-serif fonts for ALL text (NO artistic/fancy/decorative fonts). Bullet point headings should be BOLD. LIMITED COLOR PALETTE (3-4 colors max): Use WARM, ELEGANT, MUTED tones - mature and tasteful, consistent throughout all slides. IF the slide has figures/tables: focus on them as the main visual content, enlarge when helpful. IF NO figures/tables: add illustrations or icons for each paragraph to fill the page. Tables should have PLAIN borders (NO patterns/decorations on borders). Highlight key numbers with colors. Characters should appear MEANINGFULLY (not random decoration) - they should react to or interact with the content, with appropriate poses/actions and sizes.",
}

# Slide layout rules by style and section type
SLIDE_LAYOUTS_ACADEMIC: Dict[str, str] = {
    "opening": """Opening Slide Layout:
- Title: Large font at TOP CENTER
- Authors/Affiliations: Small font at BOTTOM
- Main Visual: ONE element on CENTER
- Background: LIGHT color (white or very light gray)""",
    
    "content": """Content Slide Layout:
- Title: At TOP LEFT of slide
- Content: Moderate font size, SPACIOUS layout
- Figures/tables should BLEND with background color and style - polished and refined
- Visualize data with CHARTS (bar, line, pie, radar) - make them LARGE and meaningful
- All charts/figures should use UNIFIED style (same accent color, same line weights)
- IF figures/tables present: Feature them LARGE as main visual content
- Add LARGE simple-line icons for each paragraph
- Background: LIGHT color, SAME as previous slide
- Overall feel: minimal, scholarly, professional""",
    
    "ending": """Ending Slide Layout:
- Title/Heading: At TOP CENTER of slide
- Main Content: Key takeaways in CENTER
- Background: LIGHT color, SAME as previous slide""",
}

SLIDE_LAYOUTS_DORAEMON: Dict[str, str] = {
    "opening": """Opening Slide Layout (Sophisticated Anime Style, Classic Doraemon Style):
- Title: Large simple sans-serif font at TOP CENTER (NO artistic/decorative fonts)
- Authors/Affiliations: Small font at BOTTOM center
- Main Visual: Doraemon character in CENTER, can be within a scene/setting that hints at the topic
- Background: Can use a SCENE illustration as border/frame (e.g., doorway, window, landscape) instead of plain border
- Color: SOPHISTICATED, WARM, MUTED tones (NOT childish bright colors)
- Overall feel: Mature, elegant, refined""",
    
    "content": """Content Slide Layout (Sophisticated Anime Style, Classic Doraemon Style):
- Title: Simple sans-serif font at TOP LEFT of slide (NO artistic/decorative fonts)
- Optional: TOP HALF can feature a WIDE scene illustration that reflects the content's mood/theme
- Content Area: Inside a THIN, PLAIN, SOFT-COLORED rounded border/frame (NO patterns/decorations on border)
- Background: CLEAN, WARM tones (keep it simple and uncluttered)
- Color: SOPHISTICATED, WARM, MUTED tones - consistent throughout all slides (NOT childish bright colors)
- IF figures/tables present: Feature them prominently as main visual content
- IF NO figures/tables: Add illustrations or icons for each paragraph to fill space
- Characters: Should appear MEANINGFULLY with context-appropriate actions/poses (not random decoration), size can vary based on importance
- PRESERVE EVERY DETAIL from the content provided
- Fill the slide with rich visual content, avoid empty space""",
    
    "ending": """Ending Slide Layout (Sophisticated Anime Style, Classic Doraemon Style):
- Title/Heading: Simple sans-serif font at TOP CENTER of slide (NO artistic/decorative fonts)
- Main Content: Key takeaways or closing message in CENTER
- Background: FULL-SCREEN illustration featuring ALL main characters (Doraemon, Nobita, friends) as the background, covering the entire slide
- Characters should have meaningful poses reflecting the journey's conclusion
- Color: SOPHISTICATED, WARM, MUTED tones (NOT childish bright colors)
- Overall feel: Mature, elegant, refined""",
}

# Default layout for custom styles
SLIDE_LAYOUTS_DEFAULT: Dict[str, str] = {
    "opening": """Opening Slide Layout:
- Title: Large bold font at TOP CENTER
- Authors/Affiliations: Small font at BOTTOM
- Main Visual: ONE central element (icon, illustration, or abstract shape)
- Background: Solid color or subtle gradient matching style theme""",
    
    "content": """Content Slide Layout:
- Title: At TOP LEFT of slide
- Content: Well-organized with moderate font size, good spacing
- IF figures/tables present: Feature them prominently as main visual content
- IF NO figures/tables: Add icons or illustrations for each paragraph to fill space
- Layout: Can be vertical (top-to-bottom) OR horizontal (columns)""",
    
    "ending": """Ending Slide Layout:
- Title/Heading: At TOP CENTER of slide
- Main Content: Key takeaways or closing message in CENTER""",
}

# Common rules for slides (appended to custom style_hints)
SLIDE_COMMON_STYLE_RULES = """IF the slide has figures/tables: focus on them as the main visual content, polish them to fit the style. IF NO figures/tables: add icons or illustrations for each paragraph to fill the page. Tables should have PLAIN borders (NO patterns/decorations). Fill the page well, avoid empty space."""

# Common rules for posters (appended to custom style_hints)
POSTER_COMMON_STYLE_RULES = """IF the poster has figures/tables: focus on them as the main visual content, polish them to fit the style."""

# General hints
VISUALIZATION_HINTS = """Visualization:
- Use diagrams and icons to represent concepts
- Visualize data/numbers as charts
- Use bullet points, highlight key metrics
- Keep background CLEAN and simple"""

CONSISTENCY_HINT = "IMPORTANT: Maintain consistent colors and style with the reference slide."

SLIDE_FIGURE_HINT = "For reference figures: REDRAW them to match the visual style and color scheme. Preserve the original structure and key information, but make them BLEND seamlessly with the slide design."

POSTER_FIGURE_HINT = "For reference figures: REDRAW them to match the visual style and color scheme. Preserve the original structure and key information, but make them BLEND seamlessly with the poster design."


# Language hint for image generation
def get_language_hint(language: str) -> str:
    """Get language hint for image generation prompts."""
    if language.lower() == "en":
        return "TEXT LANGUAGE: English text only."

    lang_hints = {
        "zh": "TEXT LANGUAGE: Use Simplified Chinese (简体中文) for ALL text. Technical terms can include English in parentheses.",
        "zh-tw": "TEXT LANGUAGE: Use Traditional Chinese (繁體中文) for ALL text. Technical terms can include English in parentheses.",
        "ja": "TEXT LANGUAGE: Use Japanese (日本語) for ALL text. Technical terms can use katakana or include English.",
        "ko": "TEXT LANGUAGE: Use Korean (한국어) for ALL text. Technical terms can include English in parentheses.",
        "es": "TEXT LANGUAGE: Use Spanish (Español) for ALL text.",
        "fr": "TEXT LANGUAGE: Use French (Français) for ALL text.",
        "de": "TEXT LANGUAGE: Use German (Deutsch) for ALL text.",
        "ru": "TEXT LANGUAGE: Use Russian (Русский) for ALL text.",
        "pt": "TEXT LANGUAGE: Use Portuguese (Português) for ALL text.",
        "it": "TEXT LANGUAGE: Use Italian (Italiano) for ALL text.",
        "ar": "TEXT LANGUAGE: Use Arabic (العربية) for ALL text. Right-to-left layout where appropriate.",
    }
    return lang_hints.get(language.lower(), f"TEXT LANGUAGE: Use {language} for ALL text.")