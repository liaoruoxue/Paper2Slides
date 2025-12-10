"""
Generator module

Generates poster images or slides from RAG summary content.
"""
from .config import (
    OutputType,
    PosterFormat,
    PosterDensity,
    SlidesLength,
    StyleType,
    SLIDES_PAGE_RANGES,
    POSTER_A0_DIMENSIONS,
    GenerationConfig,
    GenerationInput,
)
from .content_planner import (
    TableRef,
    FigureRef,
    Section,
    ContentPlan,
    ContentPlanner,
)


__all__ = [
    # Config
    "OutputType",
    "PosterFormat",
    "PosterDensity",
    "SlidesLength",
    "StyleType",
    "SLIDES_PAGE_RANGES",
    "POSTER_A0_DIMENSIONS",
    "GenerationConfig",
    "GenerationInput",
    # Content Planner
    "TableRef",
    "FigureRef",
    "Section",
    "ContentPlan",
    "ContentPlanner",
]
