"""
LLM prompts for content planning (slides and posters)
"""
from typing import Dict

# Language instruction template - injected at the start of prompts
LANGUAGE_INSTRUCTION = """## Output Language
ALL text content in your response must be written in **{language_name}**.
This includes: titles, section content, descriptions, and any other text.
{special_instruction}
"""

# Special instructions for specific languages
LANGUAGE_SPECIAL_INSTRUCTIONS: Dict[str, str] = {
    "zh": "Use Simplified Chinese characters. Technical terms can keep English in parentheses if needed, e.g., '卷积神经网络 (CNN)'.",
    "zh-tw": "Use Traditional Chinese characters. Technical terms can keep English in parentheses if needed.",
    "ja": "Use Japanese (日本語). Technical terms can keep English in katakana or parentheses if needed.",
    "ko": "Use Korean (한국어). Technical terms can keep English in parentheses if needed.",
    "en": "",  # No special instruction for English
}

def get_language_instruction(language: str) -> str:
    """Get language instruction for prompts."""
    if language.lower() == "en":
        return ""  # No instruction needed for English (default)

    lang_names = {
        "en": "English",
        "zh": "Chinese (Simplified Chinese / 简体中文)",
        "zh-tw": "Chinese (Traditional Chinese / 繁體中文)",
        "ja": "Japanese (日本語)",
        "ko": "Korean (한국어)",
        "es": "Spanish (Español)",
        "fr": "French (Français)",
        "de": "German (Deutsch)",
        "ru": "Russian (Русский)",
        "pt": "Portuguese (Português)",
        "it": "Italian (Italiano)",
        "ar": "Arabic (العربية)",
    }
    language_name = lang_names.get(language.lower(), language)
    special_instruction = LANGUAGE_SPECIAL_INSTRUCTIONS.get(language.lower(), "")

    return LANGUAGE_INSTRUCTION.format(
        language_name=language_name,
        special_instruction=special_instruction
    )


# =============================================================================
# Stage 1: Content Analysis Prompt
# =============================================================================
# This prompt analyzes what content elements actually exist in the document
# WITHOUT forcing it into predefined categories

CONTENT_ANALYSIS_PROMPT = """Analyze the following document summary and identify what content elements are ACTUALLY PRESENT.

## Document Summary
{summary}

## Your Task
Identify which of the following content elements are genuinely present in this document. For each element, only mark it as present if there is SUBSTANTIAL content for it (not just a brief mention).

## Output Format (JSON)
```json
{{
  "title": "[Exact title of the document]",
  "authors": "[Authors if mentioned, otherwise empty string]",
  "content_elements": {{
    "problem_or_motivation": {{
      "present": true/false,
      "description": "[Brief description of what problem/motivation is discussed, or empty if not present]"
    }},
    "background_or_related_work": {{
      "present": true/false,
      "description": "[Brief description of background/related work covered, or empty if not present]"
    }},
    "proposed_approach": {{
      "present": true/false,
      "description": "[Brief description of what approach/method/framework is proposed, or empty if not present]"
    }},
    "technical_details": {{
      "present": true/false,
      "description": "[Brief description of technical details like algorithms, formulas, architecture, or empty if not present]"
    }},
    "experiments_or_evaluation": {{
      "present": true/false,
      "description": "[Brief description of experiments/evaluation performed, or empty if not present]"
    }},
    "quantitative_results": {{
      "present": true/false,
      "description": "[Brief description of numerical results/metrics, or empty if not present]"
    }},
    "qualitative_analysis": {{
      "present": true/false,
      "description": "[Brief description of qualitative findings/observations, or empty if not present]"
    }},
    "discussion_or_insights": {{
      "present": true/false,
      "description": "[Brief description of discussion/insights, or empty if not present]"
    }},
    "conclusions_or_contributions": {{
      "present": true/false,
      "description": "[Brief description of main conclusions/contributions, or empty if not present]"
    }},
    "limitations_or_future_work": {{
      "present": true/false,
      "description": "[Brief description if mentioned, or empty if not present]"
    }}
  }},
  "key_figures": "[List figure IDs that are most important, e.g., 'Figure 1, Figure 3']",
  "key_tables": "[List table IDs that are most important, e.g., 'Table 1, Table 2']",
  "main_topic_summary": "[One sentence describing what this document is primarily about]"
}}
```

## CRITICAL RULES
1. Only mark an element as "present": true if there is SUBSTANTIAL content for it
2. Do NOT assume content exists - only report what is explicitly in the summary
3. If something is only briefly mentioned without details, mark it as NOT present
4. Be conservative - when in doubt, mark as NOT present
"""


# =============================================================================
# Stage 2: Adaptive Content Planning Prompts
# =============================================================================
# These prompts generate sections based on what content actually exists

ADAPTIVE_SLIDES_PLANNING_PROMPT = """Create slides based on the ACTUAL content available in this document.

## Document Summary
{summary}
{assets_section}

## Content Analysis
The following content elements are available in this document:
{content_analysis}

## Your Task
Create {min_pages}-{max_pages} slides using ONLY the content that actually exists.

## CRITICAL RULES
1. **ONLY use content that exists** - Do NOT invent or hallucinate content
2. **Skip missing sections** - If "experiments" is not present, do NOT create an experiments slide
3. **Adapt structure to content** - The slide structure should match what's actually in the document
4. **Preserve details** - Include specific numbers, formulas, and technical details from the source
5. **Match figures/tables** - Only reference figures/tables that exist in the assets section

## Output Fields
- **id**: Slide identifier (e.g., "slide_01")
- **title**: A concise, specific title for this slide
- **content**: Detailed text for this slide. Requirements:
  - Copy and adapt text from the source - do NOT summarize into vague statements
  - Preserve specific numbers, percentages, metrics
  - Include key formulas in LaTeX if present in source
  - Each slide should have substantial content (150+ words except title slide)
- **tables**: Tables to show (only if they exist in assets)
  - table_id: e.g., "Table 1"
  - extract: Partial table HTML with ACTUAL data values
  - focus: What to emphasize
- **figures**: Figures to show (only if they exist in assets)
  - figure_id: e.g., "Figure 1"
  - focus: What to highlight

## Suggested Slide Structure (adapt based on available content)
1. **Title slide**: Document title, authors
2. **Content slides**: Create slides for each PRESENT content element
   - Only create slides for elements marked as present in the content analysis
   - Combine related elements if appropriate
   - Split large elements into multiple slides if needed
3. **Summary slide**: Key takeaways (only from content that exists)

## Output Format (JSON)
```json
{{
  "slides": [
    {{
      "id": "slide_01",
      "title": "[Document Title]",
      "content": "[Authors and affiliations if available]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "slide_02",
      "title": "[Specific topic from content]",
      "content": "[Detailed content extracted from source...]",
      "tables": [],
      "figures": [{{"figure_id": "Figure X", "focus": "..."}}]
    }}
  ]
}}
```
"""


ADAPTIVE_POSTER_PLANNING_PROMPT = """Create poster sections based on the ACTUAL content available in this document.

## Document Summary
{summary}
{assets_section}

## Content Analysis
The following content elements are available in this document:
{content_analysis}

## Content Density
{density_guidelines}

## Your Task
Create poster sections using ONLY the content that actually exists.

## CRITICAL RULES
1. **ONLY use content that exists** - Do NOT invent or hallucinate content
2. **Skip missing sections** - If "experiments" is not present, do NOT create a results section
3. **Adapt structure to content** - The poster structure should match what's actually in the document
4. **Preserve details** - Include specific numbers, formulas, and technical details from the source
5. **Match figures/tables** - Only reference figures/tables that exist in the assets section

## Output Fields
- **id**: Section identifier (e.g., "header", "main_content", "findings")
- **title**: A concise, specific title for this section
- **content**: Detailed text for this section. Requirements:
  - Copy and adapt text from the source - do NOT summarize into vague statements
  - Preserve specific numbers, percentages, metrics
  - Include key formulas in LaTeX if present in source
  - Adjust detail level based on density setting
- **tables**: Tables to show (only if they exist in assets)
- **figures**: Figures to show (only if they exist in assets)

## Suggested Section Structure (adapt based on available content)
1. **Header**: Title, authors (always present)
2. **Content sections**: Create sections for PRESENT content elements only
   - Group related elements logically
   - Do NOT create empty or hallucinated sections
3. **Key findings/Summary**: Main takeaways (only from content that exists)

## Output Format (JSON)
```json
{{
  "sections": [
    {{
      "id": "header",
      "title": "[Document Title]",
      "content": "[Authors if available]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "main_content",
      "title": "[Specific topic]",
      "content": "[Detailed content from source...]",
      "tables": [{{"table_id": "Table X", "extract": "...", "focus": "..."}}],
      "figures": [{{"figure_id": "Figure X", "focus": "..."}}]
    }}
  ]
}}
```
"""


ADAPTIVE_POSTER_A0_PLANNING_PROMPT = """Create A0 portrait poster sections based on the ACTUAL content available.

## Document Summary
{summary}
{assets_section}

## Content Analysis
The following content elements are available in this document:
{content_analysis}

## Content Density and Layout
{density_guidelines}

{layout_guidelines}

## Your Task
Create A0 poster sections (841mm x 1189mm, vertical layout) using ONLY content that actually exists.

## CRITICAL RULES
1. **ONLY use content that exists** - Do NOT invent or hallucinate content
2. **Skip missing sections** - If an element is not present, do NOT create a section for it
3. **Adapt structure to content** - Create sections that match the actual document content
4. **Preserve details** - Include specific numbers, formulas, and technical details
5. **Match figures/tables** - Only reference assets that actually exist

## Output Fields
- **id**: Section identifier
- **title**: Specific title for this section
- **content**: Detailed text (adjust based on density setting)
  - Copy from source, preserve specific numbers and formulas
  - Do NOT make up content that isn't in the source
- **tables**: Tables with actual data values (only if they exist)
- **figures**: Figures (only if they exist)

## Section Structure (create ONLY sections for present content)
- **header**: Always include - title and authors
- **Additional sections**: Create based on what content actually exists
  - Name sections appropriately for their content
  - Do NOT use generic names for non-existent content
  - Combine or split sections as appropriate for the content

## Output Format (JSON)
```json
{{
  "sections": [
    {{
      "id": "header",
      "title": "[Document Title]",
      "content": "[Authors and affiliations]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "[appropriate_id]",
      "title": "[Specific title matching content]",
      "content": "[Actual content from source...]",
      "tables": [],
      "figures": []
    }}
  ]
}}
```

## IMPORTANT
- The number of sections should match how much content is actually available
- Do NOT force a fixed number of sections
- Quality over quantity - fewer detailed sections is better than many empty/hallucinated ones
"""

# Paper slides planning prompt
PAPER_SLIDES_PLANNING_PROMPT = """Organize the document into {min_pages}-{max_pages} slides by distributing the content below.

## Document Summary
{summary}
{assets_section}
## Output Fields
- **id**: Slide identifier
- **title**: A concise title suitable for this slide, such as paper title, method name, or topic name
- **content**: The main text for this slide. This is the MOST IMPORTANT field. Requirements:
  - **DETAILED METHOD DESCRIPTION**: For method slides, describe each step/component in detail. If there are multiple steps, explain each one (what it does, how it works, what's the input/output). Don't compress into one vague sentence.
  - **PRESERVE KEY FORMULAS**: If the source has formulas, include 1-2 relevant ones in LaTeX (\\( ... \\) or \\[ ... \\]) with variable meanings.
  - **PRESERVE SPECIFIC NUMBERS**: Key percentages, metrics, dataset sizes, and comparison values.
  - **SUBSTANTIAL CONTENT**: Each slide should contain enough detail to fully explain its topic.
  - **COPY FROM SOURCE**: Extract and adapt text from the summary. Do not over-simplify into vague one-liners.
  - Only use information provided above. Do not invent details.
- **tables**: Tables you want to show on this slide
  - table_id: e.g., "Table 1", "Doc Table 1"
  - extract: (optional) Partial table in HTML format. INCLUDE ACTUAL DATA VALUES from the original table, not placeholders
  - focus: (optional) What aspect to emphasize
- **figures**: Figures you want to show on this slide
  - figure_id: e.g., "Figure 1", "Doc Figure 1"
  - focus: (optional) What to highlight
- Note: A slide can have both tables and figures together if they complement each other.

## Content Guidelines

Distribute content across {min_pages}-{max_pages} slides covering these areas:

1. **Title/Cover**: Paper title or method name, all author names, affiliations

2. **Background/Problem**:
   - The research problem with full context
   - Specific limitations of existing approaches (list each one)
   - Why these limitations matter

3. **Method/Approach** (can span multiple slides):
   - Framework overview with component names and their roles
   - If the method has multiple stages, dedicate content to each stage
   - Include 1-2 key formulas with variable explanations
   - Technical details: algorithms, parameters, implementation specifics
   - Match figures showing architecture or pipeline

4. **Results/Experiments** (can span multiple slides):
   - Dataset details: name, size, splits, categories with EXACT numbers
   - Main evaluation metrics and what they measure
   - Performance numbers with EXACT values and comparisons
   - Ablation findings with specific impact numbers
   - Match tables showing results

5. **Conclusion**:
   - Each main contribution listed explicitly
   - Key findings with specific numbers

## Output Format (JSON)
```json
{{
  "slides": [
    {{
      "id": "slide_01",
      "title": "[Paper/Method name]",
      "content": "[All authors with affiliations]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "slide_02",
      "title": "[Method/Framework name]",
      "content": "[Detailed description: The framework consists of X components. Component A does... Component B handles... The process flow is...]",
      "tables": [],
      "figures": [{{"figure_id": "Figure X", "focus": "[architecture/pipeline]"}}]
    }},
    {{
      "id": "slide_03",
      "title": "[Results/Evaluation]",
      "content": "[Full results: Evaluated on Dataset (size, categories). Metrics include X, Y, Z. Main results show... Compared to baselines...]",
      "tables": [{{"table_id": "Table X", "extract": "<table><tr><th>Method</th><th>Metric</th></tr><tr><td>Ours</td><td>XX.X</td></tr><tr><td>Baseline</td><td>XX.X</td></tr></table>", "focus": "[comparison]"}}],
      "figures": []
    }}
  ]
}}
```

## CRITICAL REQUIREMENTS
1. **MATHEMATICAL FORMULAS**: If the source contains formulas, include at least 1-2 key/representative formulas in Method slides using LaTeX notation. In JSON, escape backslashes as \\\\ (e.g., \\\\( \\\\mathcal{{X}} \\\\)).
2. **MINIMUM CONTENT LENGTH**: Each slide content should be at least 150-200 words (except title). Avoid overly brief summaries.
3. **SPECIFIC NUMBERS**: Use precise values from source.
4. **TABLE DATA**: Extract tables with actual numerical values from the original.
"""

# Paper poster density guidelines
PAPER_POSTER_DENSITY_GUIDELINES: Dict[str, str] = {
    "sparse": """Current density level is **sparse**. Content should be concise but still informative.
Keep: main research problem, method name and core idea, best performance numbers, key contribution.
Present tables using extract (partial table) showing only the most important rows with ACTUAL values.
Write clear sentences that capture the essential point of each section.
Still include key mathematical formulas if they are central to the method.""",

    "medium": """Current density level is **medium**. Content should cover main points with supporting details.
Keep: research problem with context, method components and how they work, main results with comparisons, contributions.
**INCLUDE mathematical formulas** that define the method with notation explanations.
Include relevant tables with key columns/rows and ACTUAL data values.
Write complete explanations that give readers a solid understanding.""",

    "dense": """Current density level is **dense**. Content should be comprehensive with full technical details.
Keep: complete problem context and limitations, all method components with technical descriptions, full experimental results including ablations, all contributions and findings.
**INCLUDE key mathematical formulas** with notation explanations.
Include complete tables or detailed extracts showing relevant data with actual values.
Write thorough explanations covering methodology, implementation details, and analysis.
Copy specific numbers, percentages, and metrics directly from the source.""",
}

# Paper poster planning prompt (landscape 16:9)
PAPER_POSTER_PLANNING_PROMPT = """Organize the document into poster sections by distributing the content below.

## Document Summary
{summary}
{assets_section}
## Content Density
{density_guidelines}

## Output Fields
- **id**: Section identifier
- **title**: A concise title for this section, such as paper title, method name, or topic
- **content**: The main text for this section. This is the MOST IMPORTANT field. Requirements:
  - **DETAILED METHOD DESCRIPTION**: For method section, describe each step/component in detail. If there are multiple steps, explain each one separately.
  - **PRESERVE KEY FORMULAS**: If the source has formulas, include 1-2 relevant ones in LaTeX (\\( ... \\)) with variable meanings.
  - **PRESERVE SPECIFIC NUMBERS**: Key percentages, metrics, dataset sizes, comparison values.
  - **SUBSTANTIAL CONTENT**: Each section should contain enough detail to fully explain its topic.
  - **COPY FROM SOURCE**: Extract and adapt text from summary. Do not over-simplify into vague summaries.
  - Adjust detail level based on density above. Only use information provided. Do not invent details.
- **tables**: Tables to show in this section
  - table_id: e.g., "Table 1", "Doc Table 1"
  - extract: (optional) Partial table in HTML format. INCLUDE ACTUAL DATA VALUES from the original table, not placeholders
  - focus: (optional) What aspect to emphasize
- **figures**: Figures to show in this section
  - figure_id: e.g., "Figure 1", "Doc Figure 1"
  - focus: (optional) What to highlight
- Note: A section can have both tables and figures together if they complement each other.

## Section Guidelines

1. **Title/Header**: Paper title or method name, all authors, affiliations

2. **Background/Motivation**: Research problem with context, specific limitations of existing methods

3. **Method** (core section):
   - Framework overview with component names and their roles
   - If the method has multiple stages, dedicate content to each stage
   - Include 1-2 key formulas with variable explanations
   - Technical details: algorithms, parameters, implementation specifics
   - Pair with figures

4. **Results**:
   - Dataset details with EXACT numbers (size, splits, categories)
   - Main metrics and what they measure
   - Performance numbers with EXACT values from tables
   - Key comparisons and ablation findings

5. **Conclusion**: Main contributions listed explicitly

## Output Format (JSON)
```json
{{
  "sections": [
    {{
      "id": "poster_title",
      "title": "[Paper/Method name]",
      "content": "[All authors with affiliations]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "poster_method",
      "title": "[Method/Framework name]",
      "content": "[Detailed description: The framework consists of X components. Component A does... Component B handles... The process flow is...]",
      "tables": [],
      "figures": [{{"figure_id": "Figure X", "focus": "[architecture]"}}]
    }},
    {{
      "id": "poster_results",
      "title": "[Results/Evaluation]",
      "content": "[Full results: Evaluated on Dataset (size, categories). Metrics include X, Y, Z. Main results show... Compared to baselines...]",
      "tables": [{{"table_id": "Table X", "extract": "<table><tr><th>Method</th><th>Metric</th></tr><tr><td>Ours</td><td>XX.X</td></tr><tr><td>Baseline</td><td>XX.X</td></tr></table>", "focus": "[comparison]"}}],
      "figures": []
    }}
  ]
}}
```

## CRITICAL REQUIREMENTS
1. **MATHEMATICAL FORMULAS**: If the source contains formulas, include at least 1-2 key/representative formulas in Method section using LaTeX. In JSON, escape backslashes as \\\\ (e.g., \\\\( \\\\mathcal{{X}} \\\\)).
2. **MINIMUM CONTENT LENGTH**: Each section content should be at least 100-150 words (except title). Avoid overly brief summaries.
3. **SPECIFIC NUMBERS**: Use precise values from source.
4. **TABLE DATA**: Extract tables with actual numerical values from the original.
"""

# A0 Portrait Poster Planning Prompt (for academic papers)
PAPER_POSTER_A0_PLANNING_PROMPT = """Organize the document into sections for a PORTRAIT A0 academic poster (841mm x 1189mm, vertical layout).

## Document Summary
{summary}
{assets_section}
## Content Density and Layout
{density_guidelines}

{layout_guidelines}

## Output Fields
- **id**: Section identifier (e.g., "header", "introduction", "method", "results", "conclusion")
- **title**: Section title for the poster
- **content**: The main text for this section. Requirements:
  - **DETAILED DESCRIPTIONS**: Explain each concept/step thoroughly
  - **PRESERVE KEY FORMULAS**: Include 1-2 key formulas in LaTeX with notation explanations
  - **PRESERVE SPECIFIC NUMBERS**: All key metrics, dataset sizes, performance values
  - **SUBSTANTIAL CONTENT**: Enough detail to stand alone on a poster section
  - **COPY FROM SOURCE**: Extract and adapt text, do not over-simplify
  - Adjust detail level based on density. Only use information provided.
- **tables**: Tables to show in this section
  - table_id: Reference ID
  - extract: Partial table HTML with ACTUAL values
  - focus: What to emphasize
- **figures**: Figures to show in this section
  - figure_id: Reference ID
  - focus: What to highlight

## Required Sections for A0 Poster

Create sections in this order (top to bottom of poster):

1. **header**: Paper title, ALL authors with affiliations, institution logos if mentioned
   - This becomes the title bar at the top of the poster

2. **introduction**: Background, problem statement, motivation
   - Why this research matters
   - What problem are we solving
   - Limitations of existing approaches

3. **method**: Proposed approach/framework
   - Overview of the method
   - Key components and their roles
   - Algorithm steps or process flow
   - Include 1-2 key formulas
   - Pair with architecture/pipeline figures

4. **results**: Experimental evaluation
   - Datasets with EXACT numbers
   - Metrics used
   - Main results with EXACT values
   - Key comparisons (include table extracts)
   - Ablation highlights if present

5. **conclusion**: Main contributions and takeaways
   - List each contribution explicitly
   - Key findings with numbers
   - Future directions if mentioned

## Output Format (JSON)
```json
{{
  "sections": [
    {{
      "id": "header",
      "title": "[Paper Title]",
      "content": "[All authors with affiliations, e.g., John Doe (MIT), Jane Smith (Stanford)]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "introduction",
      "title": "Introduction & Motivation",
      "content": "[Research problem with context. Current approaches have these limitations: 1) ... 2) ... This motivates our work to...]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "method",
      "title": "[Method Name]",
      "content": "[Our framework consists of X main components: 1) Component A handles... 2) Component B processes... The key formula is \\\\( formula \\\\) where variables represent...]",
      "tables": [],
      "figures": [{{"figure_id": "Figure X", "focus": "architecture overview"}}]
    }},
    {{
      "id": "results",
      "title": "Experiments & Results",
      "content": "[Evaluated on Dataset (N samples, K categories). Main metrics: Metric1, Metric2. Our method achieves XX.X% on Metric1, outperforming baseline by Y.Y%...]",
      "tables": [{{"table_id": "Table X", "extract": "<table>...</table>", "focus": "main comparison"}}],
      "figures": [{{"figure_id": "Figure Y", "focus": "qualitative results"}}]
    }},
    {{
      "id": "conclusion",
      "title": "Conclusions",
      "content": "[Main contributions: 1) We propose... 2) We demonstrate... Key findings include...]",
      "tables": [],
      "figures": []
    }}
  ]
}}
```

## CRITICAL REQUIREMENTS
1. **EXACTLY 5 SECTIONS**: header, introduction, method, results, conclusion (in this order)
2. **MATHEMATICAL FORMULAS**: Include key formulas in Method section using LaTeX
3. **MINIMUM CONTENT**: header ~50 words, other sections 100-200 words each
4. **SPECIFIC NUMBERS**: Use exact values from source
5. **TABLE DATA**: Extract tables with actual numerical values
"""

# A0 Poster layout guidelines by density (used with PAPER_POSTER_A0_PLANNING_PROMPT)
PAPER_POSTER_A0_LAYOUT_GUIDELINES: Dict[str, str] = {
    "sparse": """LAYOUT FOR SPARSE DENSITY:
- Header: Title, authors, affiliations only (no abstract)
- Introduction: 2-3 sentences on problem and motivation
- Method: Core idea in 3-4 sentences, 1 key figure
- Results: Best performance numbers, 1 main table extract
- Conclusion: 3 bullet points
Total target: ~400-500 words of content""",

    "medium": """LAYOUT FOR MEDIUM DENSITY:
- Header: Title, authors, affiliations, brief abstract (1-2 sentences)
- Introduction: Full problem context, 3-4 limitations of prior work
- Method: All components explained, key formula, 1-2 figures
- Results: Dataset details, main results table, key comparisons
- Conclusion: 4-5 contributions/findings
Total target: ~700-900 words of content""",

    "dense": """LAYOUT FOR DENSE DENSITY:
- Header: Complete title, all authors with affiliations, full abstract
- Introduction: Comprehensive background, all limitations, motivation
- Method: Full technical description, multiple figures, algorithm details, formulas with explanations
- Results: Complete experimental setup, all datasets, full results with ablations, multiple tables
- Conclusion: All contributions, detailed findings, future work
Total target: ~1000-1300 words of content""",
}

# General document prompts (no fixed academic structure)
GENERAL_SLIDES_PLANNING_PROMPT = """Organize the document into {min_pages}-{max_pages} slides by distributing the content below.

## Document Content
{summary}
{assets_section}
## Output Fields
- **id**: Slide identifier
- **title**: A concise title for this slide, such as document title or topic name
- **content**: The main text for this slide. This is the MOST IMPORTANT field. Requirements:
  - **DETAILED DESCRIPTIONS**: If there are multiple points/steps, describe each one. Don't compress into vague summaries.
  - **PRESERVE KEY FORMULAS**: If present, include relevant mathematical or technical formulas.
  - **PRESERVE SPECIFIC NUMBERS**: Key percentages, statistics, dates, quantities, and comparison values.
  - **SUBSTANTIAL CONTENT**: Each slide should contain enough detail to fully explain its topic.
  - **COPY FROM SOURCE**: Extract and adapt text from the content. Do not over-simplify into vague one-liners.
  - Only use information provided above. Do not invent details.
- **tables**: Tables you want to show on this slide
  - table_id: e.g., "Table 1", "Doc Table 1"
  - extract: (optional) Partial table in HTML format. INCLUDE ACTUAL DATA VALUES from the original table, not placeholders
  - focus: (optional) What aspect to emphasize
- **figures**: Figures you want to show on this slide
  - figure_id: e.g., "Figure 1", "Doc Figure 1"
  - focus: (optional) What to highlight
- Note: A slide can have both tables and figures together if they complement each other.

## Content Guidelines

Distribute content across {min_pages}-{max_pages} slides. Identify the document's own structure and follow it:

1. **Title/Cover**: Document title, authors/source if available

2. **Main Content** (can span multiple slides):
   - Organize into logical slides based on the document's natural structure
   - Each slide should focus on one topic with full details
   - If the content has multiple stages/steps, dedicate content to each
   - Include specific numbers, data points, and examples
   - Match relevant tables/figures with their explanations

3. **Summary/Conclusion**: Key takeaways with specific numbers if applicable

## Output Format (JSON)
```json
{{
  "slides": [
    {{
      "id": "slide_01",
      "title": "[Document title]",
      "content": "[Authors/source if available]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "slide_02",
      "title": "[Topic name]",
      "content": "[Detailed description: This section covers X, Y, Z. The key aspects include... Specific data shows...]",
      "tables": [],
      "figures": [{{"figure_id": "Figure X", "focus": "[what to highlight]"}}]
    }},
    {{
      "id": "slide_03",
      "title": "[Key Data/Statistics]",
      "content": "[Full details with specific numbers, statistics, and comparisons...]",
      "tables": [{{"table_id": "Table X", "extract": "<table><tr><th>Item</th><th>Value</th></tr><tr><td>A</td><td>XX.X</td></tr></table>", "focus": "[key point]"}}],
      "figures": []
    }}
  ]
}}
```

## CRITICAL REQUIREMENTS
1. **FORMULAS**: If present, include any formulas or technical expressions exactly as they appear.
2. **MINIMUM CONTENT LENGTH**: Each slide content should be at least 150-200 words (except title). Avoid overly brief summaries.
3. **SPECIFIC NUMBERS**: Use precise values from source.
4. **TABLE DATA**: Extract tables with actual numerical values from the original.
"""

# General poster density guidelines
GENERAL_POSTER_DENSITY_GUIDELINES: Dict[str, str] = {
    "sparse": """Current density level is **sparse**. Content should be concise but still informative.
Keep: main topic, core message, key points, important takeaways.
For narrative content: key plot points, main characters, central theme.
For data content: most important numbers and comparisons with ACTUAL values.
Present tables using extract (partial table) showing only the most important rows with REAL data.
Write clear sentences that capture the essential point of each section.
Still include key formulas if they are central to the content.""",
    
    "medium": """Current density level is **medium**. Content should cover main points with supporting details.
Keep: topic with context, key concepts explained, supporting examples, main conclusions.
For narrative content: plot development, character relationships, cause and effect.
For data content: key statistics with context and comparisons using EXACT numbers.
**INCLUDE formulas/equations** that are important with explanations.
Include relevant tables with key columns/rows and ACTUAL data values.
Write complete explanations that give readers a solid understanding.""",
    
    "dense": """Current density level is **dense**. Content should be comprehensive with full details.
Keep: complete context and background, all key concepts with full explanations, detailed examples and analysis.
For narrative content: full plot with subplots, all character details, complete cause-effect chains.
For data content: key statistics with EXACT values, detailed breakdowns, thorough comparisons.
**INCLUDE key formulas/equations** with explanations.
Include complete tables or detailed extracts showing relevant data with actual values.
Write thorough explanations covering all important aspects.
Copy specific numbers and technical details directly from the source.""",
}

# General poster planning prompt
GENERAL_POSTER_PLANNING_PROMPT = """Organize the document into poster sections by distributing the content below.

## Document Content
{summary}
{assets_section}
## Content Density
{density_guidelines}

## Output Fields
- **id**: Section identifier
- **title**: A concise title for this section, such as document title or topic name
- **content**: The main text for this section. This is the MOST IMPORTANT field. Requirements:
  - **DETAILED DESCRIPTIONS**: If there are multiple points/steps, describe each one. Don't compress into vague summaries.
  - **PRESERVE KEY FORMULAS**: If present, include relevant mathematical or technical formulas.
  - **PRESERVE SPECIFIC NUMBERS**: Key percentages, statistics, dates, quantities, and comparison values.
  - **SUBSTANTIAL CONTENT**: Each section should contain enough detail to fully explain its topic.
  - **COPY FROM SOURCE**: Extract and adapt text from the content. Do not over-simplify into vague summaries.
  - Adjust detail level based on density above. Only use information provided. Do not invent details.
- **tables**: Tables to show in this section
  - table_id: e.g., "Table 1", "Doc Table 1"
  - extract: (optional) Partial table in HTML format. INCLUDE ACTUAL DATA VALUES from the original table, not placeholders
  - focus: (optional) What aspect to emphasize
- **figures**: Figures to show in this section
  - figure_id: e.g., "Figure 1", "Doc Figure 1"
  - focus: (optional) What to highlight
- Note: A section can have both tables and figures together if they complement each other.

## Section Guidelines

Organize content into logical sections based on the document's natural structure:

1. **Title/Header**: Document title, authors/source if available

2. **Main Content**: Key topics with full details, if there are multiple stages/steps dedicate content to each

3. **Key Data**: Important numbers, statistics, or data from tables with EXACT values

4. **Summary**: Main takeaways listed with specific numbers

## Output Format (JSON)
```json
{{
  "sections": [
    {{
      "id": "poster_title",
      "title": "[Document title]",
      "content": "[Authors/source if available]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "poster_content",
      "title": "[Topic name]",
      "content": "[Detailed description: This topic covers X, Y, Z. The key aspects include... Specific data shows...]",
      "tables": [],
      "figures": [{{"figure_id": "Figure X", "focus": "[key concept]"}}]
    }},
    {{
      "id": "poster_data",
      "title": "[Key Data/Statistics]",
      "content": "[Important data with specific numbers and comparisons...]",
      "tables": [{{"table_id": "Table X", "extract": "<table><tr><th>Item</th><th>Value</th></tr><tr><td>A</td><td>XX.X</td></tr></table>"}}],
      "figures": []
    }}
  ]
}}
```

## CRITICAL REQUIREMENTS
1. **FORMULAS**: If present, include any formulas or technical expressions exactly as they appear.
2. **MINIMUM CONTENT LENGTH**: Each section content should be at least 100-150 words (except title). Avoid overly brief summaries.
3. **SPECIFIC NUMBERS**: Use precise values from source.
4. **TABLE DATA**: Extract tables with actual numerical values from the original.
"""

# A0 Portrait Poster Planning Prompt (for general documents)
GENERAL_POSTER_A0_PLANNING_PROMPT = """Organize the document into sections for a PORTRAIT A0 poster (841mm x 1189mm, vertical layout).

## Document Content
{summary}
{assets_section}
## Content Density and Layout
{density_guidelines}

{layout_guidelines}

## Output Fields
- **id**: Section identifier (e.g., "header", "overview", "details", "data", "summary")
- **title**: Section title for the poster
- **content**: The main text for this section. Requirements:
  - **DETAILED DESCRIPTIONS**: Explain each concept/point thoroughly
  - **PRESERVE KEY FORMULAS**: Include relevant formulas if present
  - **PRESERVE SPECIFIC NUMBERS**: All key statistics, values, percentages
  - **SUBSTANTIAL CONTENT**: Enough detail to stand alone on a poster section
  - **COPY FROM SOURCE**: Extract and adapt text, do not over-simplify
  - Adjust detail level based on density. Only use information provided.
- **tables**: Tables to show in this section
  - table_id: Reference ID
  - extract: Partial table HTML with ACTUAL values
  - focus: What to emphasize
- **figures**: Figures to show in this section
  - figure_id: Reference ID
  - focus: What to highlight

## Required Sections for A0 Poster

Create sections in this order (top to bottom of poster):

1. **header**: Document title, source/authors if available
   - This becomes the title bar at the top of the poster

2. **overview**: Introduction and context
   - What is this document about
   - Key background information
   - Main purpose or thesis

3. **details**: Main content
   - Core concepts explained
   - Key points with supporting details
   - Include relevant figures

4. **data**: Key statistics and numbers
   - Important data points
   - Comparisons and analysis
   - Include table extracts if available

5. **summary**: Main takeaways
   - Key conclusions
   - Important findings listed

## Output Format (JSON)
```json
{{
  "sections": [
    {{
      "id": "header",
      "title": "[Document Title]",
      "content": "[Source/authors if available]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "overview",
      "title": "Overview",
      "content": "[Introduction and context. This document covers... The main focus is...]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "details",
      "title": "[Main Topic]",
      "content": "[Detailed explanation of main content. Key concepts include... The process involves...]",
      "tables": [],
      "figures": [{{"figure_id": "Figure X", "focus": "key illustration"}}]
    }},
    {{
      "id": "data",
      "title": "Key Data",
      "content": "[Important statistics and numbers. The data shows... Comparisons indicate...]",
      "tables": [{{"table_id": "Table X", "extract": "<table>...</table>", "focus": "main data"}}],
      "figures": []
    }},
    {{
      "id": "summary",
      "title": "Key Takeaways",
      "content": "[Main conclusions: 1) ... 2) ... Important findings include...]",
      "tables": [],
      "figures": []
    }}
  ]
}}
```

## CRITICAL REQUIREMENTS
1. **EXACTLY 5 SECTIONS**: header, overview, details, data, summary (in this order)
2. **FORMULAS**: Include formulas if present in the source
3. **MINIMUM CONTENT**: header ~30 words, other sections 80-150 words each
4. **SPECIFIC NUMBERS**: Use exact values from source
5. **TABLE DATA**: Extract tables with actual numerical values
"""

# A0 Poster layout guidelines for general documents
GENERAL_POSTER_A0_LAYOUT_GUIDELINES: Dict[str, str] = {
    "sparse": """LAYOUT FOR SPARSE DENSITY:
- Header: Title, source only
- Overview: 2-3 sentences on main topic
- Details: Core concepts in 3-4 sentences, 1 key figure if available
- Data: Most important statistics or numbers
- Summary: 3 bullet points
Total target: ~350-450 words of content""",

    "medium": """LAYOUT FOR MEDIUM DENSITY:
- Header: Title, source, brief description
- Overview: Full context, background information
- Details: All key concepts explained, 1-2 figures
- Data: Main statistics with context and comparisons
- Summary: 4-5 key takeaways
Total target: ~600-800 words of content""",

    "dense": """LAYOUT FOR DENSE DENSITY:
- Header: Complete title, all source information
- Overview: Comprehensive introduction, full background
- Details: Thorough explanation of all concepts, multiple figures
- Data: All important statistics, detailed comparisons, multiple tables
- Summary: All conclusions, detailed findings
Total target: ~900-1100 words of content""",
}
