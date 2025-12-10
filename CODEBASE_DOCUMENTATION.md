# Paper2Slides 代码库完整说明文档

## 📚 目录
- [第一层：快速入门](#第一层快速入门)
- [第二层：深入理解](#第二层深入理解)
- [第三层：高级开发](#第三层高级开发)

---

# 第一层：快速入门

## 🎯 项目简介

**Paper2Slides** 是一个将学术论文自动转换为专业演示幻灯片和海报的 AI 系统。

### 核心功能
- 📄 **输入**：PDF/DOCX/PPTX/MD 文档
- 🎨 **输出**：精美的幻灯片（PNG序列 + PDF）或海报
- 🤖 **技术**：RAG + GPT-4o + Gemini 图像生成

### 快速使用

```bash
# 1. 安装依赖
pip install -e .

# 2. 配置 API 密钥
cp paper2slides/.env.example paper2slides/.env
# 编辑 .env 填入 API 密钥（支持 OpenRouter 或 Google GenAI）

# 3. 生成幻灯片
python -m paper2slides --input paper.pdf --style doraemon --length medium
```

### 图像生成提供商配置

系统支持两种图像生成提供商，可通过环境变量切换：

#### OpenRouter（默认）
```bash
# .env
IMAGE_GEN_PROVIDER="openrouter"
IMAGE_GEN_API_KEY="your-openrouter-api-key"
IMAGE_GEN_MODEL="google/gemini-3-pro-image-preview"
```

#### Google GenAI（直连）
```bash
# .env
IMAGE_GEN_PROVIDER="google"
GOOGLE_API_KEY="your-google-api-key"
IMAGE_GEN_MODEL="gemini-3-pro-image-preview"

# 需要安装额外依赖
pip install google-generativeai
```

### 两种使用模式

#### CLI 模式（命令行）
```bash
python -m paper2slides \
  --input paper.pdf \           # 输入文件
  --output slides \             # slides 或 poster
  --poster-format portrait_a0 \ # 海报格式：landscape (16:9) 或 portrait_a0 (A0竖向)
  --style academic \            # 风格：academic, doraemon, 或自定义
  --length medium \             # 幻灯片长度：short, medium, long
  --density medium \            # 海报密度：sparse, medium, dense
  --fast \                      # 快速模式（跳过 RAG）
  --parallel 2                  # 并行生成数量
```

#### 海报格式说明
- `landscape`：16:9 横向海报（默认）
- `portrait_a0`：A0 竖向学术海报（841mm x 1189mm）

```bash
# 生成 A0 竖向学术海报
python -m paper2slides --input paper.pdf --output poster --poster-format portrait_a0 --style academic

# 生成 A0 竖向 Doraemon 风格海报
python -m paper2slides --input paper.pdf --output poster --poster-format portrait_a0 --style doraemon --density dense
```

#### Web 模式（图形界面）
```bash
# 启动服务
bash scripts/start.sh

# 访问 http://localhost:5173
# 拖拽上传文件 → 选择配置 → 生成 → 预览下载
```

---

## 📁 项目结构（简化版）

```
Paper2Slides/
├── paper2slides/          # 核心 Python 库
│   ├── main.py           # CLI 入口
│   ├── core/             # 流水线编排
│   ├── raganything/      # RAG 引擎
│   ├── summary/          # 内容提取
│   ├── generator/        # 图像生成
│   │   ├── config.py     # 配置类（OutputType, PosterFormat, StyleType等）
│   │   ├── providers.py  # 图像生成提供商（OpenRouter/GoogleGenAI）
│   │   ├── image_generator.py  # 图像生成主逻辑
│   │   └── content_planner.py  # 内容规划
│   └── prompts/          # LLM 提示词
│
├── api/                  # Web API (FastAPI)
├── frontend/             # React 前端
├── scripts/              # 启动脚本
└── outputs/              # 生成结果
```

---

## 🔄 工作流程（四阶段）

```
┌─────────────┐
│  输入文档   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│ 阶段1: RAG (文档解析与索引)     │
│ - Fast模式: 直接用GPT-4o分析    │
│ - Normal模式: 构建RAG索引       │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ 阶段2: Summary (内容提取)       │
│ - 提取论文元数据                │
│ - 提取各章节内容                │
│ - 提取表格和图片                │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ 阶段3: Plan (内容规划)          │
│ - 确定页数和布局                │
│ - 分配内容到各页                │
│ - 匹配图表到对应页面            │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ 阶段4: Generate (图像生成)      │
│ - 幻灯片：前2页顺序+后续并行    │
│ - 海报：单张生成（支持横/竖向） │
│ - 合成为PDF                     │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────┐
│  输出结果   │ slides.pdf/poster.png + PDF
└─────────────┘
```

---

## 🎨 可用风格

### 内置风格
1. **academic** - 学术专业风格（深蓝色 + 白色背景）
2. **doraemon** - 哆啦A梦友好风格（天蓝色 + 卡通元素）

### 海报格式
| 格式 | 尺寸 | 适用场景 |
|------|------|----------|
| `landscape` | 16:9 横向 | 快速概览、在线分享 |
| `portrait_a0` | 841mm x 1189mm 竖向 | 学术会议、海报展示 |

### 自定义风格
```bash
# 直接用自然语言描述
python -m paper2slides \
  --input paper.pdf \
  --style "赛博朋克科幻风格，霓虹色调，深色背景"
```

---

## 🚀 输出示例

### 输出目录结构
```
outputs/
└── my_paper/                          # 项目名
    └── paper/                         # 内容类型
        └── normal/                    # 模式 (fast/normal)
            ├── checkpoint_rag.json    # 断点文件（fast 模式无）
            ├── checkpoint_summary.json
            │
            ├── slides_doraemon_medium/       # 幻灯片配置
            │   └── 20231210_143052/          # 时间戳
            │       ├── slide_01.png
            │       ├── slide_02.png
            │       └── slides.pdf
            │
            ├── poster_academic_medium/       # 横向海报 (16:9)
            │   └── 20231210_144022/
            │       └── poster.png
            │
            └── poster_a0_academic_dense/     # A0 竖向海报 (841x1189mm)
                └── 20231210_145533/
                    └── poster.png
```

### 断点续传
系统自动保存每个阶段的检查点，如果中断可以继续：
```bash
# 自动从中断处继续
python -m paper2slides --input paper.pdf --style academic

# 或手动指定从某阶段开始
python -m paper2slides --input paper.pdf --from-stage plan
```

---

## 💡 常见使用场景

### 场景1：学术论文 → 会议演讲幻灯片
```bash
python -m paper2slides \
  --input research_paper.pdf \
  --output slides \
  --style academic \
  --length long            # 15-18页，详细讲解
```

### 场景2：论文 → 16:9 横向海报
```bash
python -m paper2slides \
  --input paper.pdf \
  --output poster \
  --poster-format landscape \  # 默认，可省略
  --density medium \           # sparse/medium/dense
  --style doraemon \
  --fast                       # 快速生成
```

### 场景3：论文 → A0 竖向学术海报
```bash
python -m paper2slides \
  --input paper.pdf \
  --output poster \
  --poster-format portrait_a0 \  # A0 竖向 (841mm x 1189mm)
  --density medium \
  --style academic
```

### 场景4：技术文档 → 教学幻灯片
```bash
python -m paper2slides \
  --input tutorial.md \
  --content general \      # 通用文档模式
  --style "简洁现代风格，蓝绿色调" \
  --length medium
```

---

# 第二层：深入理解

## 🏗️ 架构设计

### 核心设计理念

Paper2Slides 采用 **管道式架构**，将复杂任务分解为四个独立阶段，每个阶段都有：
- 📌 **清晰的输入输出**
- 💾 **检查点保存**
- 🔄 **可重启能力**
- ⚡ **并发优化**

---

## 🔍 四阶段详解

### 阶段 1: RAG Stage - 文档解析与索引

**文件位置**: `paper2slides/core/stages/rag_stage.py`

#### 两种工作模式

##### Fast Mode（快速模式）
```python
# 跳过 RAG 索引，直接用 GPT-4o 多模态分析
def run_fast_mode(markdown_paths):
    # 1. 读取 Markdown 文本
    # 2. 提取图片并转换为 base64
    # 3. 构建多模态输入（文本 + 图片）
    content_parts = [
        {"type": "text", "text": markdown_content},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img1}"}},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img2}"}},
        ...
    ]

    # 4. 调用 GPT-4o
    response = await openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content_parts}]
    )
```

**适用场景**：
- ✅ 短文档（< 20页）
- ✅ 快速预览
- ✅ 单文件
- ❌ 不适合超长文档（Token 限制）

##### Normal Mode（标准模式）
```python
# 完整 RAG 流程
def run_normal_mode(input_path):
    # 1. 文档解析（使用 MinerU）
    parsed_files = batch_parser.process_batch([input_path])
    # 输出: Markdown + 提取的图片

    # 2. 构建 RAG 索引（使用 LightRAG）
    rag_client = RAGClient(...)
    await rag_client.index(markdown_path)
    # 创建: 向量索引 + 知识图谱

    # 3. 批量查询（按类别分组）
    rag_results = await rag_client.batch_query_by_category({
        "paper_info": ["论文标题", "作者", "机构"],
        "motivation": ["研究问题", "现有方法局限"],
        "solution": ["提出方法", "核心模块", "算法步骤"],
        "results": ["实验数据", "性能指标", "对比结果"],
        ...
    })
```

**适用场景**：
- ✅ 长文档（> 20页）
- ✅ 多文件
- ✅ 需要精确检索
- ✅ 成本敏感（RAG 比直接用 GPT-4o 便宜）

#### 输出格式

**checkpoint_rag.json**:
```json
{
  "rag_results": {
    "paper_info": [
      "论文标题: Deep Learning for NLP\n作者: John Doe\n机构: MIT"
    ],
    "motivation": [
      "现有方法在长文本处理上存在效率问题..."
    ],
    "solution": [
      "我们提出了一个基于 Transformer 的新架构..."
    ],
    "results": [
      "在 GLUE 基准上达到了 92.3% 的准确率..."
    ],
    "figures": [...],
    "tables": [...],
    ...
  },
  "markdown_paths": ["/path/to/paper.md"],
  "mode": "normal",
  "timestamp": "2023-12-10T14:30:52"
}
```

---

### 阶段 2: Summary Stage - 内容提取与结构化

**文件位置**: `paper2slides/core/stages/summary_stage.py`

#### 核心任务
1. 从 RAG 结果中提取结构化内容
2. 清理和格式化文本
3. 提取表格和图片元信息

#### 工作流程

```python
async def run_summary_stage(base_dir, config):
    # 1. 加载 RAG 结果
    rag_checkpoint = load_json(base_dir / "checkpoint_rag.json")
    rag_results = rag_checkpoint["rag_results"]

    # 2. 选择提取器
    if content_type == "paper":
        content = await extract_paper(
            rag_results=rag_results,
            llm_client=OpenAI(),
            parallel=True,         # 并行提取各部分
            max_concurrency=5      # 最多 5 个并发
        )
    else:
        content = await extract_general(rag_results)

    # 3. 提取表格和图片
    origin = extract_tables_and_figures(markdown_paths)

    # 4. 保存结果
    save_json("checkpoint_summary.json", {
        "content": content.__dict__,
        "origin": origin.to_dict()
    })
```

#### 数据模型

**PaperContent** (`summary/models.py:40`):
```python
@dataclass
class PaperContent:
    paper_info: str       # 标题、作者、机构、摘要
    motivation: str       # 研究背景、问题、重要性
    solution: str         # 方法描述、架构、算法
    results: str          # 实验设置、数据集、结果
    contributions: str    # 主要贡献、创新点
```

**OriginalElements** (`summary/models.py:76`):
```python
@dataclass
class OriginalElements:
    tables: List[TableInfo]     # 表格列表
    figures: List[FigureInfo]   # 图片列表
    base_path: str              # 基础路径

    def to_dict(self):
        return {
            "tables": [t.__dict__ for t in self.tables],
            "figures": [f.__dict__ for f in self.figures],
            "base_path": self.base_path
        }
```

#### 并行提取策略

```python
# summary/paper.py:30
async def extract_paper(rag_results, llm_client, parallel=True, max_concurrency=5):
    """并行提取论文各部分内容"""

    if parallel:
        # 创建提取任务
        tasks = []
        for section in ["paper_info", "motivation", "solution", "results", "contributions"]:
            task = extract_section(
                section=section,
                rag_results=rag_results[section],
                llm_client=llm_client
            )
            tasks.append(task)

        # 并发执行（使用 Semaphore 控制并发数）
        results = await asyncio.gather(*tasks)
    else:
        # 顺序执行
        results = []
        for section in sections:
            result = await extract_section(...)
            results.append(result)

    return PaperContent(*results)
```

#### 表格提取示例

```python
# summary/extractors/table_extractor.py:15
def extract_tables(markdown_content):
    """从 Markdown 提取 HTML 表格"""
    tables = []

    # 1. 查找表格模式（Table X: Caption）
    pattern = r'(Table\s+\d+:?\s+[^\n]+)\n\s*<table'

    for match in re.finditer(pattern, markdown_content):
        caption = match.group(1)
        table_id = extract_table_id(caption)  # "Table 1"

        # 2. 提取 HTML 表格内容
        html_start = match.end()
        html_end = find_table_end(markdown_content, html_start)
        html_content = markdown_content[html_start:html_end]

        # 3. 清理表格（移除不必要的 HTML 属性）
        cleaned_html = clean_table_html(html_content)

        tables.append(TableInfo(
            table_id=table_id,
            caption=caption,
            html_content=cleaned_html
        ))

    return tables
```

---

### 阶段 3: Plan Stage - 内容规划

**文件位置**: `paper2slides/core/stages/plan_stage.py`

#### 核心职责
- 决定幻灯片页数（根据 length 参数）或海报内容量（根据 density 参数）
- 分配内容到各页/各区块
- 为每页/区块匹配合适的图表
- 支持两种海报格式：横向 16:9 和 A0 竖向

#### 内容规划器

**文件位置**: `paper2slides/generator/content_planner.py:20`

```python
class ContentPlanner:
    def __init__(self, llm_client, style_type="academic"):
        self.llm_client = llm_client
        self.style_type = style_type

    def plan(self, gen_input: GenerationInput) -> ContentPlan:
        """生成内容布局方案（幻灯片或海报）"""

        if gen_input.config.output_type == OutputType.POSTER:
            return self._plan_poster(gen_input, ...)  # 海报规划
        else:
            return self._plan_slides(gen_input, ...)  # 幻灯片规划

    def _plan_poster(self, gen_input, summary, tables_md, figure_images):
        """海报内容规划（支持横向和 A0 竖向）"""
        density = gen_input.config.poster_density.value
        is_a0 = gen_input.config.poster_format == PosterFormat.PORTRAIT_A0

        # 根据格式选择对应的提示词模板
        if is_a0:
            template = PAPER_POSTER_A0_PLANNING_PROMPT
            layout_guidelines = PAPER_POSTER_A0_LAYOUT_GUIDELINES[density]
        else:
            template = PAPER_POSTER_PLANNING_PROMPT
            layout_guidelines = None

        # ... 调用 LLM 进行规划

    def _plan_slides(self, gen_input, ...):
        """幻灯片内容规划"""
        # 1. 确定页数范围
        page_config = self._get_page_config(gen_input)
        # short: 5-8页, medium: 10-13页, long: 15-18页

        # 2. 加载图片为 base64（用于多模态分析）
        figure_images = self._load_figure_images(gen_input.origin.figures)

        # 3. 构建提示词
        prompt = PAPER_SLIDES_PLANNING_PROMPT.format(
            min_pages=page_config["min"],
            max_pages=page_config["max"],
            summary=self._format_summary(gen_input.content),
            tables_md=self._format_tables(gen_input.origin.tables)
        )

        # 4. 调用 GPT-4o（多模态输入）
        response = self._call_multimodal_llm(
            prompt=prompt,
            images=figure_images  # 让 LLM 看到所有图片
        )

        # 5. 解析 JSON 响应
        plan_data = json.loads(response)
        sections = self._parse_sections(plan_data["slides"])

        return ContentPlan(sections=sections)
```

#### 提示词结构

**文件位置**: `paper2slides/prompts/content_planning.py:10`

```python
PAPER_SLIDES_PLANNING_PROMPT = """
你是一个专业的演示设计师。将以下学术论文组织为 {min_pages}-{max_pages} 页幻灯片。

## 输入信息
- 论文摘要和各部分内容
- 可用的表格（HTML格式）
- 可用的图片（你可以看到图片内容）

## 输出要求

### 1. 内容分配
- 标题页（1页）：论文标题、作者、机构
- 背景/动机（1-2页）：研究问题、现有方法局限、重要性
- 方法/解决方案（3-5页）：
  * 方法概览（架构图）
  * 关键模块详细说明
  * 核心算法/公式
  * 实现细节
- 实验/结果（2-4页）：
  * 数据集和评价指标
  * 主要结果（对比表格）
  * 消融实验
  * 可视化结果
- 结论（1页）：贡献总结、未来工作

### 2. 内容质量要求
对于每一页的 `content` 字段：
- **详细程度**：每页至少 150-200 词
- **保留细节**：
  * 具体数字（准确率 92.3%，不要说"超过90%"）
  * 关键公式（LaTeX 格式）
  * 技术术语（保持原文）
  * 步骤说明（算法的每个步骤）
- **不要过度简化**：从源文本提取和改编，不要只写高层概述

### 3. 图表匹配
为每页匹配合适的图表：

**tables**（表格列表）：
- `table_id`: "Table 1"（引用原始表格ID）
- `extract`: 部分表格 HTML（只包含关键行，不要全部）
- `focus`: 在这一页重点关注的方面（如"与baseline对比"）

**figures**（图片列表）：
- `figure_id`: "Figure 1"（引用原始图片ID）
- `focus`: 图片中重点突出的内容（如"注意力机制模块"）

### 4. 输出格式（JSON）
{{
  "slides": [
    {{
      "id": "slide_01",
      "title": "[论文标题]",
      "content": "[作者列表及机构，完整格式]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "slide_02",
      "title": "背景与动机",
      "content": "[详细描述研究问题的背景、现有方法的局限性、为什么这个问题重要。至少150词，包含具体例子和数据。]",
      "tables": [],
      "figures": [
        {{
          "figure_id": "Figure 1",
          "focus": "现有方法的架构图，突出其局限性"
        }}
      ]
    }},
    {{
      "id": "slide_03",
      "title": "提出方法：整体架构",
      "content": "[详细描述方法的整体架构。包含：1）主要组件及其作用，2）组件间的连接关系，3）数据流向。至少200词。]",
      "tables": [],
      "figures": [
        {{
          "figure_id": "Figure 2",
          "focus": "整体架构图，标注每个模块"
        }}
      ]
    }},
    ...
  ]
}}

## 当前文档信息

### 论文内容
{summary}

### 可用表格
{tables_md}

### 可用图片
[已作为图片附件提供，你可以看到每个图片的内容]

现在请生成幻灯片规划方案（JSON格式）：
"""
```

#### 页数配置

```python
# generator/content_planner.py:80
PAGE_CONFIGS = {
    "slides": {
        "short": {"min": 5, "max": 8},
        "medium": {"min": 10, "max": 13},
        "long": {"min": 15, "max": 18}
    },
    "poster": {
        "sparse": {"pages": 1},    # 海报固定 1 页
        "medium": {"pages": 1},
        "dense": {"pages": 1}
    }
}

# A0 竖向海报密度配置（字数指南）
PAPER_POSTER_A0_LAYOUT_GUIDELINES = {
    "sparse": "~400-500 words, minimal content, focus on key points",
    "medium": "~700-900 words, balanced coverage",
    "dense": "~1000-1300 words, comprehensive content",
}
```

#### 输出格式

**checkpoint_plan.json**:
```json
{
  "sections": [
    {
      "section_id": "slide_01",
      "title": "Deep Learning for Natural Language Processing",
      "content": "Authors: John Doe (MIT), Jane Smith (Stanford)\n\nThis work addresses...",
      "tables": [],
      "figures": []
    },
    {
      "section_id": "slide_02",
      "title": "Background and Motivation",
      "content": "Natural language processing has seen remarkable progress...\n\nKey challenges:\n1. Long-range dependencies...\n2. Computational efficiency...",
      "tables": [],
      "figures": [
        {
          "figure_id": "Figure 1",
          "caption": "Comparison of existing architectures",
          "focus": "Limitations of RNN-based models",
          "image_path": "/path/to/figure_1.png",
          "mime_type": "image/png"
        }
      ]
    },
    {
      "section_id": "slide_03",
      "title": "Proposed Method: Architecture Overview",
      "content": "Our method consists of three main components:\n\n1. Multi-Head Attention Module\n   - Computes attention weights: α = softmax(QK^T / √d_k)\n   - Enables parallel processing...\n\n2. Feed-Forward Network\n   - Two-layer MLP with ReLU activation...",
      "tables": [],
      "figures": [
        {
          "figure_id": "Figure 2",
          "caption": "Overall architecture",
          "focus": "Multi-head attention mechanism",
          "image_path": "/path/to/figure_2.png",
          "mime_type": "image/png"
        }
      ]
    },
    {
      "section_id": "slide_04",
      "title": "Experimental Results",
      "content": "We evaluate on three benchmark datasets:\n- GLUE: 92.3% average score\n- SQuAD 2.0: 88.7% F1 score\n- CoNLL 2003: 94.1% F1 score\n\nOur method outperforms...",
      "tables": [
        {
          "table_id": "Table 1",
          "caption": "Performance comparison on GLUE benchmark",
          "extract": "<table><tr><th>Model</th><th>GLUE</th></tr><tr><td>BERT</td><td>88.5</td></tr><tr><td>Ours</td><td>92.3</td></tr></table>",
          "focus": "Comparison with BERT baseline"
        }
      ],
      "figures": []
    }
  ],
  "timestamp": "2023-12-10T14:35:22"
}
```

---

### 阶段 4: Generate Stage - 图像生成

**文件位置**: `paper2slides/core/stages/generate_stage.py`

#### 图像生成提供商系统

系统支持多种图像生成提供商，通过抽象工厂模式实现灵活切换：

**文件位置**: `paper2slides/generator/providers.py`

```python
# 抽象基类
class ImageGenerationProvider(ABC):
    """图像生成提供商抽象基类"""

    @abstractmethod
    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """生成图像"""
        pass

    @abstractmethod
    def get_default_model(self) -> str:
        """获取默认模型名"""
        pass


# OpenRouter 提供商（默认）
class OpenRouterProvider(ImageGenerationProvider):
    """通过 OpenRouter 调用 Gemini"""

    def __init__(
        self,
        api_key: str = None,
        base_url: str = "https://openrouter.ai/api/v1",
        model: str = "google/gemini-3-pro-image-preview"
    ):
        self.api_key = api_key or os.getenv("IMAGE_GEN_API_KEY")
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)

    def generate_image(self, request):
        # 使用 OpenAI 兼容 API
        response = self.client.chat.completions.create(
            model=request.model or self.default_model,
            messages=[{"role": "user", "content": content}],
            extra_body={"modalities": ["image", "text"]}
        )
        # 从 response.choices[0].message.images 提取图像
        ...


# Google GenAI 提供商（直连）
class GoogleGenAIProvider(ImageGenerationProvider):
    """直接调用 Google GenAI API"""

    def __init__(
        self,
        api_key: str = None,
        model: str = "gemini-3-pro-image-preview"
    ):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        from google import genai
        from google.genai import types
        self.client = genai.Client(api_key=self.api_key)
        self.types = types

    def generate_image(self, request):
        # 使用 Google GenAI 原生 API
        config = self.types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
            image_config=self.types.ImageConfig(
                aspect_ratio="16:9",
                image_size="4K"
            )
        )
        response = self.client.models.generate_content(
            model=request.model or self.default_model,
            contents=content_parts,
            config=config
        )
        # 从 response.parts 提取图像
        for part in response.parts:
            image = part.as_image()
            if image:
                image.save(tmp_path)
                ...


# 提供商工厂
class ProviderFactory:
    """图像生成提供商工厂"""

    PROVIDERS = {
        "openrouter": OpenRouterProvider,
        "google": GoogleGenAIProvider,
        "genai": GoogleGenAIProvider,  # 别名
    }

    @classmethod
    def from_env(cls) -> ImageGenerationProvider:
        """从环境变量创建提供商"""
        provider_name = os.getenv("IMAGE_GEN_PROVIDER", "openrouter")

        if provider_name == "openrouter":
            return OpenRouterProvider(
                api_key=os.getenv("IMAGE_GEN_API_KEY"),
                model=os.getenv("IMAGE_GEN_MODEL", "google/gemini-3-pro-image-preview")
            )
        elif provider_name in ["google", "genai"]:
            return GoogleGenAIProvider(
                api_key=os.getenv("GOOGLE_API_KEY"),
                model=os.getenv("IMAGE_GEN_MODEL", "gemini-3-pro-image-preview")
            )
```

#### 环境变量配置

```bash
# .env 文件配置示例

# 选项 1: 使用 OpenRouter（默认）
IMAGE_GEN_PROVIDER="openrouter"
IMAGE_GEN_API_KEY="your-openrouter-api-key"
IMAGE_GEN_MODEL="google/gemini-3-pro-image-preview"

# 选项 2: 使用 Google GenAI 直连
IMAGE_GEN_PROVIDER="google"
GOOGLE_API_KEY="your-google-api-key"
IMAGE_GEN_MODEL="gemini-3-pro-image-preview"
```

#### 核心策略：混合并行生成

```python
# generator/image_generator.py:120
def _generate_slides(self, plan, gen_input, max_workers):
    """
    生成策略：
    1. 前 2 页顺序生成（建立风格基调）
    2. 第 2 页作为风格参考
    3. 后续页面并行生成（所有页面都参考第 2 页）
    """

    images = []
    style_ref_image = None
    total = len(plan.sections)

    # === 阶段 1: 顺序生成前 2 页 ===
    for i in range(min(2, total)):
        section = plan.sections[i]

        # 构建提示词
        prompt = self._build_prompt(section, gen_input)

        # 准备图片（如果有）
        section_images = self._prepare_section_images(section)

        # 生成（第1页无参考，第2页参考第1页）
        if i == 0:
            image = self._call_model(prompt, section_images)
        else:
            # 第2页生成时，参考第1页
            ref_images = [style_ref_image] if style_ref_image else []
            image = self._call_model(prompt, ref_images + section_images)

        images.append(image)

        # 保存第 2 页作为风格参考
        if i == 1:
            style_ref_image = {
                "figure_id": "Reference Slide",
                "caption": "STRICTLY MAINTAIN this exact style: " +
                           "same background color, accent colors, " +
                           "font style, layout structure, visual elements.",
                "base64": base64.b64encode(image).decode(),
                "mime_type": "image/png"
            }

    # === 阶段 2: 并行生成剩余页面 ===
    if total > 2:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            def generate_single(idx):
                section = plan.sections[idx]
                prompt = self._build_prompt(section, gen_input)
                section_images = self._prepare_section_images(section)

                # 所有页面都参考第 2 页的风格
                all_images = [style_ref_image] + section_images

                return self._call_model(prompt, all_images)

            # 提交所有任务
            futures = [
                executor.submit(generate_single, i)
                for i in range(2, total)
            ]

            # 收集结果
            for future in futures:
                image = future.result()
                images.append(image)

    return images
```

#### 提示词构建

```python
# generator/image_generator.py:250
def _build_prompt(self, section, gen_input):
    """构建图像生成提示词"""

    # 1. 获取风格提示
    style_hint = self._get_style_hint()

    # 2. 构建内容描述
    content_desc = f"""
## 幻灯片内容
标题: {section.title}

主要内容:
{section.content}
"""

    # 3. 表格处理指令
    if section.tables:
        table_instructions = """
## 表格要求
- 将提供的 HTML 表格准确转换为视觉表格
- 保持所有数据完整性（数字、单位、小数点）
- 使用清晰的边框和对齐
- 重点突出：{focus}
"""
        table_html = "\n\n".join([
            f"表格 {t.table_id}:\n{t.extract}"
            for t in section.tables
        ])
        content_desc += table_instructions + table_html

    # 4. 图片处理指令
    if section.figures:
        figure_instructions = """
## 图片要求
- 参考提供的原始图片
- 重绘为与幻灯片风格一致的版本
- 保持图片的核心信息和结构
- 重点突出：{focus}
"""
        content_desc += figure_instructions

    # 5. 组合完整提示词
    full_prompt = f"""
{style_hint}

{content_desc}

## 整体要求
- 创建一张完整的演示幻灯片（16:9 横向）
- 高分辨率、专业质量
- 布局清晰，层次分明
- 确保文本可读性（字体大小适中）
- 保持视觉一致性

直接输出幻灯片图像。
"""

    return full_prompt
```

#### 风格系统

**内置风格** (`prompts/image_generation.py:10`):

```python
SLIDE_STYLE_HINTS = {
    "academic": """
Professional academic presentation style.

Visual Design:
- Background: Clean white or very light gray (#f8f9fa)
- Accent Color: Navy blue (#1e3a8a) for headers and key elements
- Typography:
  * Headers: Bold sans-serif (Roboto/Inter), 48-60pt
  * Body: Regular sans-serif, 24-32pt
  * Code/Math: Monospace font
- Layout: Clear hierarchy with ample whitespace
- Decorations: Minimal geometric shapes (thin lines, subtle corners)

Content Presentation:
- Use bullet points for lists
- Tables with subtle borders
- Equations in clear LaTeX rendering
- Charts with professional color scheme
""",

    "doraemon": """
Friendly, approachable style featuring Doraemon character.

Visual Design:
- Background: Soft light blue gradient or white with blue accents
- Primary Colors: Sky blue (#0ea5e9), white, red accents
- Typography:
  * Headers: Rounded sans-serif, playful but readable
  * Body: Clean sans-serif, 24-30pt
- Decorations: Rounded corners, soft shadows
- Character Integration:
  * Doraemon appears as a guide/mascot
  * Appropriate poses for slide content
  * Don't obstruct main content

Content Presentation:
- Colorful but organized
- Use icons and visual metaphors
- Maintain professional content despite playful style
"""
}
```

**自定义风格处理** (`generator/image_generator.py:300`):

```python
def process_custom_style(llm_client, custom_style_description):
    """将用户自然语言描述转换为结构化风格参数"""

    prompt = f"""
分析以下幻灯片风格描述，提取关键设计元素：

用户描述：
{custom_style_description}

请输出 JSON 格式的结构化风格参数：
{{
  "style_name": "风格名称（简短）",
  "background": "背景描述（颜色、渐变等）",
  "color_palette": "主要颜色（至少3个，含16进制代码）",
  "typography": "字体风格描述",
  "decorations": "装饰元素描述",
  "special_elements": "特殊视觉元素（如果有）",
  "layout_hints": "布局建议",
  "valid": true/false
}}

如果描述不清晰或不适合幻灯片，设置 valid: false 并说明原因。
"""

    response = llm_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    style_params = json.loads(response.choices[0].message.content)

    if not style_params.get("valid", False):
        raise ValueError(f"Invalid style: {style_params.get('reason', 'Unknown')}")

    return style_params
```

#### API 调用（通过提供商抽象）

```python
# generator/image_generator.py
class ImageGenerator:
    """使用提供商抽象进行图像生成"""

    def __init__(self, provider: ImageGenerationProvider = None, model: str = None):
        # 从环境变量自动创建提供商
        self.provider = provider or ProviderFactory.from_env()
        self.model = model or self.provider.get_default_model()

    def _call_model(self, prompt: str, reference_images: List[dict]) -> tuple:
        """调用图像生成模型（带重试）"""

        # 1. 创建请求
        request = ImageGenerationRequest(
            prompt=prompt,
            reference_images=reference_images,
            model=self.model
        )

        # 2. 重试逻辑
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # 3. 调用提供商（自动路由到 OpenRouter 或 Google GenAI）
                response = self.provider.generate_image(request)
                return response.image_data, response.mime_type

            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise
```

#### OpenRouter 调用流程

```python
# OpenRouterProvider.generate_image()
def generate_image(self, request):
    # 1. 构建消息内容（多模态）
    content = [{"type": "text", "text": request.prompt}]

    # 2. 添加参考图片
    for img in request.reference_images:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{img['mime_type']};base64,{img['base64']}"}
        })

    # 3. 调用 OpenRouter API（OpenAI 兼容格式）
    response = self.client.chat.completions.create(
        model=request.model or self.default_model,
        messages=[{"role": "user", "content": content}],
        extra_body={"modalities": ["image", "text"]}
    )

    # 4. 提取图像
    image_url = response.choices[0].message.images[0]['image_url']['url']
    # data:image/png;base64,... 格式
    header, base64_data = image_url.split(',', 1)
    mime_type = header.split(':')[1].split(';')[0]
    image_data = base64.b64decode(base64_data)

    return ImageGenerationResponse(image_data=image_data, mime_type=mime_type)
```

#### Google GenAI 调用流程

```python
# GoogleGenAIProvider.generate_image()
def generate_image(self, request):
    # 1. 构建内容列表
    content_parts = [request.prompt]

    # 2. 添加参考图片（PIL Image 格式）
    for img in request.reference_images:
        image_bytes = base64.b64decode(img['base64'])
        pil_image = Image.open(io.BytesIO(image_bytes))
        content_parts.append(pil_image)

    # 3. 配置图像生成参数
    config = self.types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=self.types.ImageConfig(
            aspect_ratio="16:9",
            image_size="4K"
        )
    )

    # 4. 调用 Google GenAI API
    response = self.client.models.generate_content(
        model=request.model or self.default_model,
        contents=content_parts,
        config=config
    )

    # 5. 从 response.parts 提取图像
    for part in response.parts:
        image = part.as_image()
        if image:
            # 保存到临时文件
            image.save(tmp_path)
            with open(tmp_path, 'rb') as f:
                image_data = f.read()
            return ImageGenerationResponse(image_data=image_data, mime_type="image/png")
```

---

## 🧩 核心模块深入

### RAG 引擎 (RAG-Anything)

**文件位置**: `paper2slides/raganything/`

#### 架构概览

```
RAG-Anything = LightRAG + 多模态处理器
```

**组件**：
1. **文档解析器** - 将各种格式转为 Markdown
2. **多模态处理器** - 处理文本、图片、表格
3. **向量化引擎** - 构建检索索引
4. **查询引擎** - 支持多种检索模式

#### 批量解析器

**文件位置**: `raganything/batch_parser.py:20`

```python
class BatchParser:
    """批量文档解析器（基于 MinerU）"""

    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.supported_formats = [".pdf", ".docx", ".pptx", ".md"]

    def process_batch(self, file_paths: List[str]) -> ParseResult:
        """
        批量解析文档

        工作流程：
        1. 验证文件格式
        2. 调用 MinerU CLI 进行解析
        3. 收集解析结果（Markdown + 图片）
        4. 返回成功/失败列表
        """

        # 1. 过滤有效文件
        valid_files = [
            f for f in file_paths
            if Path(f).suffix.lower() in self.supported_formats
        ]

        # 2. 调用 MinerU
        command = [
            "magic-pdf",
            "-p", ",".join(valid_files),
            "-o", str(self.output_dir),
            "-m", "auto"  # 自动模式（OCR + 布局分析）
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=600  # 10分钟超时
        )

        # 3. 解析输出
        if result.returncode == 0:
            # 检查生成的 Markdown 文件
            markdown_files = list(self.output_dir.glob("**/*.md"))

            return ParseResult(
                successful_files=markdown_files,
                failed_files=[],
                output_dir=self.output_dir
            )
        else:
            return ParseResult(
                successful_files=[],
                failed_files=valid_files,
                error=result.stderr
            )
```

#### RAG 客户端

**文件位置**: `rag/client.py:30`

```python
class RAGClient:
    """RAG 客户端（封装 LightRAG）"""

    def __init__(self, working_dir, llm_config):
        self.working_dir = Path(working_dir)
        self.llm_config = llm_config
        self.rag = None  # LightRAG 实例

    @classmethod
    def from_storage(cls, storage_dir):
        """从已有存储目录加载"""
        # 检查存储文件是否存在
        required_files = [
            "kv_store_full_docs.json",
            "kv_store_text_chunks.json",
            "graph_chunk_entity_relation.graphml"
        ]

        for file in required_files:
            if not (storage_dir / file).exists():
                raise FileNotFoundError(f"Missing: {file}")

        # 初始化 LightRAG
        rag = LightRAG(working_dir=str(storage_dir), ...)

        client = cls(storage_dir, llm_config)
        client.rag = rag
        return client

    async def index(self, file_path: str):
        """
        索引文档

        流程：
        1. 读取 Markdown 文本
        2. 分块（Chunking）
        3. 向量化（Embedding）
        4. 构建知识图谱（Entity + Relations）
        5. 存储到磁盘
        """

        # 1. 读取内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 2. 索引（LightRAG 内部处理）
        await self.rag.ainsert(content)

        logger.info(f"Indexed: {file_path}")

    async def query(self, question: str, mode: str = "mix") -> str:
        """
        查询

        mode 选项：
        - local: 局部检索（基于向量相似度）
        - global: 全局检索（基于图谱）
        - hybrid: 混合检索（向量 + 图谱）
        - mix: 自适应混合（推荐）
        """

        answer = await self.rag.aquery(question, param=QueryParam(mode=mode))
        return answer

    async def batch_query_by_category(
        self,
        queries_by_category: Dict[str, List[str]],
        max_concurrency: int = 8
    ) -> Dict[str, List[str]]:
        """
        按类别批量查询（并发控制）

        示例输入：
        {
            "paper_info": ["论文标题", "作者", "机构"],
            "motivation": ["研究问题", "现有方法局限"],
            ...
        }

        输出：
        {
            "paper_info": ["标题: ...", "作者: ...", "机构: ..."],
            "motivation": ["问题: ...", "局限: ..."],
            ...
        }
        """

        results = {}

        for category, questions in queries_by_category.items():
            # 使用 Semaphore 控制并发数
            semaphore = asyncio.Semaphore(max_concurrency)

            async def query_one(q):
                async with semaphore:
                    return await self.query(q)

            # 并发查询
            answers = await asyncio.gather(*[
                query_one(q) for q in questions
            ])

            results[category] = answers

        return results
```

#### 预定义查询模板

**文件位置**: `rag/query.py:10`

```python
RAG_PAPER_QUERIES = {
    "paper_info": [
        "论文的完整标题是什么？",
        "谁是这篇论文的作者？列出所有作者姓名。",
        "作者来自哪些机构或大学？",
        "论文的摘要或概述是什么？"
    ],

    "motivation": [
        "这篇论文要解决什么研究问题或挑战？",
        "现有方法有哪些局限性或不足？",
        "为什么这个研究问题很重要？有什么应用价值？",
        "论文在引言中提到了哪些相关工作？"
    ],

    "solution": [
        "论文提出了什么新方法或技术？",
        "方法的整体架构或框架是什么？描述主要组件。",
        "有哪些关键的算法步骤或流程？",
        "方法中使用了哪些核心公式或数学模型？",
        "有哪些技术细节或实现要点？"
    ],

    "results": [
        "论文在哪些数据集上进行了实验？",
        "使用了哪些评价指标？",
        "主要的实验结果是什么？包括具体数字和对比。",
        "与baseline方法相比，性能提升了多少？",
        "进行了哪些消融实验？验证了什么？"
    ],

    "figures": [
        "图1展示了什么内容？详细描述。",
        "有哪些架构图或流程图？它们显示了什么？",
        "有哪些可视化结果图？它们展示了什么趋势或模式？"
    ],

    "tables": [
        "表1包含什么数据？列出关键数值。",
        "有哪些性能对比表？比较了哪些方法？",
        "有哪些消融实验表？验证了哪些组件的作用？"
    ],

    "contributions": [
        "论文的主要贡献是什么？",
        "相比已有工作，论文的创新点在哪里？",
        "论文的局限性是什么？未来工作方向？"
    ]
}
```

---

### Web API 服务

**文件位置**: `api/server.py`

#### 服务器架构

```python
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Paper2Slides API")

# CORS 配置（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 静态文件服务
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
app.mount("/uploads", StaticFiles(directory="sources/uploads"), name="uploads")

# 全局状态
app.state.results = {}            # {session_id: result}
app.state.session_manager = SessionManager()
```

#### 会话管理器

```python
class SessionManager:
    """
    全局会话管理器（单例模式）

    限制：同时只能运行一个生成任务
    """

    def __init__(self):
        self.running_session = None
        self.cancelled_sessions = set()
        self.lock = asyncio.Lock()

    async def start_session(self, session_id: str) -> bool:
        """尝试启动会话"""
        async with self.lock:
            if self.running_session is not None:
                logger.warning(f"Session {session_id} blocked: {self.running_session} is running")
                return False

            self.running_session = session_id
            logger.info(f"Session {session_id} started")
            return True

    async def end_session(self, session_id: str):
        """结束会话"""
        async with self.lock:
            if self.running_session == session_id:
                self.running_session = None
                logger.info(f"Session {session_id} ended")

    async def cancel_session(self, session_id: str):
        """取消会话"""
        self.cancelled_sessions.add(session_id)
        logger.info(f"Session {session_id} marked for cancellation")

    def is_cancelled(self, session_id: str) -> bool:
        """检查会话是否已取消"""
        return session_id in self.cancelled_sessions

    def is_running(self) -> bool:
        """是否有任务正在运行"""
        return self.running_session is not None
```

#### 核心端点实现

##### 1. 上传和启动

```python
@app.post("/api/chat")
async def chat(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    content: str = Form("paper"),
    output_type: str = Form("slides"),
    style: str = Form("academic"),
    slides_length: str = Form("medium"),
    poster_density: str = Form("medium"),
    poster_format: str = Form("landscape"),  # landscape 或 portrait_a0
    fast_mode: bool = Form(False),
    session_id: Optional[str] = Form(None)
):
    """
    处理用户请求

    工作流程：
    1. 检查是否有任务正在运行（互斥锁）
    2. 创建会话 ID
    3. 保存上传的文件
    4. 后台启动流水线
    5. 立即返回 session_id
    """

    # 1. 检查任务运行状态
    if session_manager.is_running():
        raise HTTPException(
            status_code=429,
            detail="Another task is running. Please wait."
        )

    # 2. 创建会话
    if not session_id:
        session_id = str(uuid.uuid4())

    # 3. 保存文件
    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    file_paths = []
    for file in files:
        file_path = session_dir / file.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(str(file_path))

    # 4. 构建配置
    config = {
        "content_type": content,
        "output_type": output_type,
        "style": style,
        "slides_length": slides_length,
        "poster_density": poster_density,
        "poster_format": poster_format,  # 海报格式：landscape 或 portrait_a0
        "fast_mode": fast_mode
    }

    # 5. 后台启动流水线
    background_tasks.add_task(
        run_pipeline_background,
        session_id,
        file_paths,
        config
    )

    # 6. 返回
    return {
        "session_id": session_id,
        "uploaded_files": [f.filename for f in files],
        "message": "Generation started"
    }
```

##### 2. 后台任务

```python
async def run_pipeline_background(
    session_id: str,
    input_files: List[str],
    config: dict
):
    """后台运行流水线"""

    try:
        # 1. 获取会话锁
        success = await session_manager.start_session(session_id)
        if not success:
            logger.error(f"Failed to start session {session_id}")
            return

        # 2. 运行流水线
        logger.info(f"Starting pipeline for session {session_id}")

        result = await generate_slides_with_pipeline(
            input_path=input_files[0] if len(input_files) == 1 else input_files,
            config=config,
            session_id=session_id,
            session_manager=session_manager
        )

        # 3. 保存结果到内存缓存
        app.state.results[session_id] = {
            "status": "completed",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"Pipeline completed for session {session_id}")

    except Exception as e:
        # 检查是否是用户取消
        if session_manager.is_cancelled(session_id):
            app.state.results[session_id] = {
                "status": "cancelled",
                "error": "Task cancelled by user"
            }
        else:
            # 其他错误
            logger.error(f"Pipeline failed for session {session_id}: {e}")
            app.state.results[session_id] = {
                "status": "failed",
                "error": str(e)
            }

    finally:
        # 4. 释放会话锁
        await session_manager.end_session(session_id)


async def generate_slides_with_pipeline(
    input_path,
    config,
    session_id,
    session_manager
):
    """实际执行流水线"""

    # 1. 确定路径
    project_name = get_project_name(input_path)
    base_dir = get_base_dir("outputs", project_name, config["content_type"])
    config_dir = get_config_dir(base_dir, config)

    # 2. 检测起始阶段（断点续传）
    from_stage = detect_start_stage(base_dir, config_dir, config)

    # 3. 运行流水线
    await run_pipeline(
        base_dir=base_dir,
        config_dir=config_dir,
        config=config,
        from_stage=from_stage,
        session_id=session_id,
        session_manager=session_manager
    )

    # 4. 收集输出文件
    output_dir = find_latest_output_dir(config_dir)
    slides = []

    for png_file in sorted(output_dir.glob("slide_*.png")):
        slides.append({
            "title": f"Slide {png_file.stem.split('_')[1]}",
            "image_url": f"/outputs/{png_file.relative_to('outputs')}"
        })

    pdf_path = output_dir / "slides.pdf"
    pdf_url = f"/outputs/{pdf_path.relative_to('outputs')}" if pdf_path.exists() else None

    return {
        "slides": slides,
        "pdf_url": pdf_url
    }
```

##### 3. 状态查询

```python
@app.get("/api/status/{session_id}")
async def get_status(session_id: str):
    """
    查询任务状态

    返回：
    - status: running, completed, failed, cancelled
    - stages: 各阶段状态
    - progress: 进度信息
    """

    # 1. 从磁盘读取状态文件
    state_file = find_state_file(session_id)

    if not state_file:
        # 检查内存缓存
        if session_id in app.state.results:
            return app.state.results[session_id]

        raise HTTPException(status_code=404, detail="Session not found")

    # 2. 解析状态
    with open(state_file, 'r') as f:
        state = json.load(f)

    # 3. 判断整体状态
    stages = state.get("stages", {})

    if all(s == "completed" for s in stages.values()):
        overall_status = "completed"
    elif any(s == "failed" for s in stages.values()):
        overall_status = "failed"
    elif any(s == "running" for s in stages.values()):
        overall_status = "running"
    else:
        overall_status = "pending"

    return {
        "status": overall_status,
        "stages": stages,
        "timestamp": state.get("timestamp")
    }
```

##### 4. 结果获取

```python
@app.get("/api/result/{session_id}")
async def get_result(session_id: str):
    """获取生成结果"""

    # 1. 检查缓存
    if session_id not in app.state.results:
        raise HTTPException(status_code=404, detail="Result not found")

    cached = app.state.results[session_id]

    # 2. 检查状态
    if cached["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Task is {cached['status']}"
        )

    # 3. 返回结果
    return cached["result"]
```

##### 5. 取消任务

```python
@app.post("/api/cancel/{session_id}")
async def cancel_task(session_id: str):
    """取消任务"""

    # 标记为取消（流水线会定期检查）
    await session_manager.cancel_session(session_id)

    return {"message": f"Cancellation requested for session {session_id}"}
```

---

### 前端界面

**文件位置**: `frontend/src/`

#### 主应用组件

**App.jsx**:
```jsx
import { useState, useEffect } from 'react'
import ChatWindow from './components/ChatWindow'
import ConfigPanel from './components/ConfigPanel'
import FileUpload from './components/FileUpload'

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [status, setStatus] = useState('idle')  // idle, uploading, processing, completed
  const [config, setConfig] = useState({
    content: 'paper',
    outputType: 'slides',
    style: 'academic',
    length: 'medium',
    fastMode: false
  })

  // 上传文件
  const handleFileUpload = async (files) => {
    setStatus('uploading')

    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    formData.append('content', config.content)
    formData.append('output_type', config.outputType)
    formData.append('style', config.style)
    formData.append('slides_length', config.length)
    formData.append('fast_mode', config.fastMode)

    try {
      const response = await fetch('http://localhost:8001/api/chat', {
        method: 'POST',
        body: formData
      })

      const data = await response.json()
      setSessionId(data.session_id)
      setStatus('processing')

      // 开始轮询状态
      startPolling(data.session_id)

    } catch (error) {
      console.error('Upload failed:', error)
      setStatus('error')
    }
  }

  // 轮询状态
  const startPolling = (sid) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`http://localhost:8001/api/status/${sid}`)
        const data = await response.json()

        if (data.status === 'completed') {
          clearInterval(interval)
          setStatus('completed')
          loadResults(sid)
        } else if (data.status === 'failed') {
          clearInterval(interval)
          setStatus('error')
        }

      } catch (error) {
        console.error('Polling error:', error)
      }
    }, 2000)  // 每 2 秒轮询一次
  }

  // 加载结果
  const loadResults = async (sid) => {
    try {
      const response = await fetch(`http://localhost:8001/api/result/${sid}`)
      const data = await response.json()

      // 显示结果...

    } catch (error) {
      console.error('Load results error:', error)
    }
  }

  return (
    <div className="app">
      <ConfigPanel config={config} onChange={setConfig} />
      <FileUpload onUpload={handleFileUpload} />
      <ChatWindow sessionId={sessionId} status={status} />
    </div>
  )
}
```

---

## 🛠️ 工具和辅助模块

### 路径工具

**文件位置**: `paper2slides/core/paths.py`

```python
def get_project_name(input_path):
    """从输入路径提取项目名"""
    if isinstance(input_path, list):
        input_path = input_path[0]

    return Path(input_path).stem  # 不含扩展名的文件名


def get_base_dir(output_dir, project_name, content_type):
    """获取基础输出目录"""
    # outputs/{project_name}/{content_type}/{mode}/
    return Path(output_dir) / project_name / content_type


def get_config_name(config):
    """生成配置目录名"""
    output_type = config["output_type"]
    style = config.get("style", "academic")

    if output_type == "poster":
        param = config.get("poster_density", "medium")
        # A0 竖向海报使用 poster_a0 前缀
        poster_format = config.get("poster_format", "landscape")
        if poster_format == "portrait_a0":
            return f"poster_a0_{style}_{param}"  # poster_a0_academic_medium
        return f"poster_{style}_{param}"  # poster_academic_medium
    else:
        param = config.get("slides_length", "medium")
        return f"{output_type}_{style}_{param}"  # slides_doraemon_medium


def get_config_dir(base_dir, config):
    """获取配置特定目录"""
    mode = "fast" if config.get("fast_mode") else "normal"
    config_name = get_config_name(config)

    # outputs/{project}/{content}/{mode}/{config}/
    return base_dir / mode / config_name


def get_timestamped_output_dir(config_dir):
    """获取时间戳输出目录"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return config_dir / timestamp
```

### 状态管理

**文件位置**: `paper2slides/core/state.py`

```python
def create_initial_state():
    """创建初始状态"""
    return {
        "stages": {
            "rag": "pending",
            "summary": "pending",
            "plan": "pending",
            "generate": "pending"
        },
        "timestamp": datetime.now().isoformat(),
        "version": "1.0"
    }


def save_state(config_dir, state):
    """保存状态到磁盘"""
    state_file = config_dir / "state.json"
    config_dir.mkdir(parents=True, exist_ok=True)

    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)


def load_state(config_dir):
    """从磁盘加载状态"""
    state_file = config_dir / "state.json"

    if not state_file.exists():
        return create_initial_state()

    with open(state_file, 'r') as f:
        return json.load(f)


def detect_start_stage(base_dir, config_dir, config):
    """智能检测起始阶段"""
    mode = "fast" if config.get("fast_mode") else "normal"
    mode_dir = base_dir / mode

    # 检查各阶段检查点
    checkpoints = {
        "rag": mode_dir / "checkpoint_rag.json",
        "summary": mode_dir / "checkpoint_summary.json",
        "plan": config_dir / "checkpoint_plan.json"
    }

    # 从后往前检查
    if checkpoints["plan"].exists():
        return "generate"  # 只需重新生成

    if checkpoints["summary"].exists():
        return "plan"  # 从规划开始

    if checkpoints["rag"].exists():
        return "summary"  # 从提取开始

    return "rag"  # 从头开始
```

---

## 📊 数据流示意

```
┌──────────────┐
│   PDF 文件   │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────┐
│ MinerU 解析                         │
│ - 提取文本                          │
│ - 提取图片                          │
│ - 识别表格                          │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Markdown + Images                   │
│ paper.md                            │
│ images/                             │
│   ├─ figure_1.png                   │
│   └─ figure_2.png                   │
└──────┬──────────────────────────────┘
       │
       ├──────────► Fast Mode
       │            (直接用 GPT-4o)
       │
       └──────────► Normal Mode
                    │
                    ▼
           ┌─────────────────────┐
           │ LightRAG 索引       │
           │ - 文本向量化        │
           │ - 知识图谱构建      │
           └──────┬──────────────┘
                  │
                  ▼
           ┌─────────────────────┐
           │ 批量查询            │
           │ {category: answers} │
           └──────┬──────────────┘
                  │
       ┌──────────┴──────────┐
       │                     │
       ▼                     ▼
┌─────────────┐      ┌─────────────┐
│ RAG 结果    │      │ Markdown    │
│ checkpoint_ │      │ 原文        │
│ rag.json    │      │             │
└──────┬──────┘      └──────┬──────┘
       │                     │
       └──────────┬──────────┘
                  │
                  ▼
           ┌─────────────────────┐
           │ 内容提取            │
           │ - 提取各部分        │
           │ - 提取表格/图片     │
           └──────┬──────────────┘
                  │
                  ▼
           ┌─────────────────────┐
           │ 结构化内容          │
           │ checkpoint_         │
           │ summary.json        │
           │ - PaperContent      │
           │ - OriginalElements  │
           └──────┬──────────────┘
                  │
                  ▼
           ┌─────────────────────┐
           │ 内容规划            │
           │ (GPT-4o 多模态)     │
           │ - 确定页数          │
           │ - 分配内容          │
           │ - 匹配图表          │
           └──────┬──────────────┘
                  │
                  ▼
           ┌─────────────────────┐
           │ 内容方案            │
           │ checkpoint_         │
           │ plan.json           │
           │ - sections[]        │
           └──────┬──────────────┘
                  │
                  ▼
           ┌─────────────────────┐
           │ 图像生成            │
           │ (Gemini 3 Pro)      │
           │ - 前2页顺序         │
           │ - 后续并行          │
           └──────┬──────────────┘
                  │
                  ▼
           ┌─────────────────────┐
           │ 最终输出            │
           │ slide_01.png        │
           │ slide_02.png        │
           │ ...                 │
           │ slides.pdf          │
           └─────────────────────┘
```

---

# 第三层：高级开发

## 🚀 扩展和定制

### 1. 海报格式系统（已实现）

系统已支持两种海报格式：**横向 16:9** 和 **A0 竖向学术海报**。

#### 配置定义

```python
# generator/config.py

class PosterFormat(str, Enum):
    """海报格式选项"""
    LANDSCAPE = "landscape"     # 16:9 横向（默认）
    PORTRAIT_A0 = "portrait_a0" # A0 竖向 (841mm x 1189mm)

# A0 海报尺寸常量
POSTER_A0_DIMENSIONS = {
    "width_mm": 841,
    "height_mm": 1189,
    "aspect_ratio": "9:13",  # 近似竖向比例
    "dpi": 300,
}

@dataclass
class GenerationConfig:
    output_type: OutputType = OutputType.POSTER
    poster_density: PosterDensity = PosterDensity.MEDIUM
    poster_format: PosterFormat = PosterFormat.LANDSCAPE  # 新增
    slides_length: SlidesLength = SlidesLength.MEDIUM
    style: StyleType = StyleType.ACADEMIC
    custom_style: Optional[str] = None

    def is_portrait_poster(self) -> bool:
        """检查是否为 A0 竖向海报"""
        return (self.output_type == OutputType.POSTER and
                self.poster_format == PosterFormat.PORTRAIT_A0)
```

#### A0 海报提示词模板

```python
# prompts/image_generation.py

FORMAT_POSTER_A0 = """PORTRAIT A0 academic conference poster (aspect ratio approximately 2:3 vertical, like 841mm width x 1189mm height).
Generate ONE complete vertical poster image. The poster should be TALLER than it is wide.
This is a professional academic conference poster with structured layout."""

POSTER_A0_STYLE_HINTS = {
    "academic": """Professional academic conference poster style for A0 PORTRAIT format.

LAYOUT STRUCTURE (Top to Bottom):
┌─────────────────────────────────┐
│      TITLE BAR (colored)        │  ← Title, authors, affiliations, logos
├─────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐       │
│  │  LEFT   │ │ CENTER  │       │  ← 2-3 column layout for content
│  │ COLUMN  │ │ COLUMN  │       │
│  └─────────┘ └─────────┘       │
│  ┌─────────────────────┐       │
│  │   RESULTS SECTION   │       │  ← Wide section for tables/figures
│  └─────────────────────┘       │
│  ┌─────────────────────┐       │
│  │    CONCLUSIONS      │       │  ← Bottom section
│  └─────────────────────┘       │
└─────────────────────────────────┘

STYLE REQUIREMENTS:
- Background: Clean white or very light gray
- Title bar: Navy blue with white text
- Typography: Professional sans-serif
- Colors: LIMITED PALETTE (3-4 colors max)
- English text only""",

    "doraemon": """Doraemon-themed academic poster style for A0 PORTRAIT format.
Story-based layout with problem → solution → results flow.
SOPHISTICATED Doraemon palette - NOT childish colors.""",
}

# 按密度的布局模板
POSTER_A0_LAYOUTS = {
    "sparse": "Title + 2 columns + 1-2 figures + 3-4 bullet conclusion",
    "medium": "Title + 3 columns + full results section + 5-6 contributions",
    "dense": "Complete header + 3 detailed columns + multiple tables + full analysis",
}
```

#### 内容规划提示词

```python
# prompts/content_planning.py

PAPER_POSTER_A0_PLANNING_PROMPT = """Organize the document into sections for a PORTRAIT A0 academic poster (841mm x 1189mm, vertical layout).

## Required Sections for A0 Poster (in order):
1. **header**: Paper title, ALL authors with affiliations
2. **introduction**: Background, problem statement, motivation
3. **method**: Proposed approach with key components and formulas
4. **results**: Experimental evaluation with tables and figures
5. **conclusion**: Main contributions and takeaways

## Output Format (JSON)
{
  "sections": [
    {"id": "header", "title": "[Paper Title]", "content": "[Authors]", ...},
    {"id": "introduction", "title": "Introduction & Motivation", ...},
    {"id": "method", "title": "[Method Name]", ...},
    {"id": "results", "title": "Experiments & Results", ...},
    {"id": "conclusion", "title": "Conclusions", ...}
  ]
}
"""

# 密度对应的布局指南
PAPER_POSTER_A0_LAYOUT_GUIDELINES = {
    "sparse": "~400-500 words, minimal content",
    "medium": "~700-900 words, balanced content",
    "dense": "~1000-1300 words, comprehensive content",
}
```

#### ContentPlanner 更新

```python
# generator/content_planner.py

def _plan_poster(self, gen_input, summary, tables_md, figure_images):
    """Plan poster sections (landscape or portrait A0)."""
    density = gen_input.config.poster_density.value
    is_a0 = gen_input.config.poster_format == PosterFormat.PORTRAIT_A0

    if gen_input.is_paper():
        density_guidelines = PAPER_POSTER_DENSITY_GUIDELINES[density]
        if is_a0:
            template = PAPER_POSTER_A0_PLANNING_PROMPT
            layout_guidelines = PAPER_POSTER_A0_LAYOUT_GUIDELINES[density]
        else:
            template = PAPER_POSTER_PLANNING_PROMPT
            layout_guidelines = None
    # ... 类似处理 general content

    prompt = template.format(
        density_guidelines=density_guidelines,
        layout_guidelines=layout_guidelines,
        summary=summary,
        assets_section=assets_section,
    )

    result = self._call_multimodal_llm(prompt, figure_images)
    return self._parse_sections(result, is_slides=False)
```

#### ImageGenerator 更新

```python
# generator/image_generator.py

def _generate_poster(self, style_name, processed_style, sections_md, images,
                     poster_format=PosterFormat.LANDSCAPE, density="medium"):
    """Generate 1 poster image (landscape 16:9 or portrait A0)."""
    is_a0 = poster_format == PosterFormat.PORTRAIT_A0

    if is_a0:
        prompt = self._build_poster_a0_prompt(
            style_name=style_name,
            processed_style=processed_style,
            sections_md=sections_md,
            density=density,
        )
    else:
        prompt = self._build_poster_prompt(
            format_prefix=FORMAT_POSTER,
            style_name=style_name,
            processed_style=processed_style,
            sections_md=sections_md,
        )

    image_data, mime_type = self._call_model(prompt, images)
    return [GeneratedImage(section_id="poster", image_data=image_data, mime_type=mime_type)]

def _build_poster_a0_prompt(self, style_name, processed_style, sections_md, density):
    """Build prompt for A0 portrait poster."""
    parts = [FORMAT_POSTER_A0]

    # 使用 A0 专用样式提示
    style_hints = POSTER_A0_STYLE_HINTS.get(style_name, POSTER_A0_STYLE_HINTS["academic"])
    parts.append(style_hints)

    # 添加密度对应的布局指南
    layout_guide = POSTER_A0_LAYOUTS.get(density, POSTER_A0_LAYOUTS["medium"])
    parts.append(layout_guide)

    parts.append(VISUALIZATION_HINTS)
    parts.append(POSTER_FIGURE_HINT)
    parts.append(f"---\nContent:\n{sections_md}")

    return "\n\n".join(parts)
```

#### 使用示例

```bash
# 生成 A0 竖向学术海报
python -m paper2slides --input paper.pdf --output poster --poster-format portrait_a0 --style academic --density medium

# 生成 A0 竖向 Doraemon 风格海报
python -m paper2slides --input paper.pdf --output poster --poster-format portrait_a0 --style doraemon --density dense

# 生成默认横向海报（向后兼容）
python -m paper2slides --input paper.pdf --output poster --style academic
```

#### 输出目录结构

系统根据海报格式生成不同的目录名：

```
outputs/
├── paper_name/
│   └── paper/
│       └── normal/
│           ├── poster_academic_medium/          # 横向海报
│           │   └── 20241210_143022/
│           │       └── poster.png
│           └── poster_a0_academic_medium/       # A0 竖向海报
│               └── 20241210_144533/
│                   └── poster.png
```

---

### 2. 自定义 RAG 查询策略

**目标**：针对特定学科（如计算机视觉论文）优化查询

#### 创建专用查询模板

```python
# rag/query.py
RAG_CV_PAPER_QUERIES = {
    "paper_info": [
        "论文的完整标题是什么？",
        "作者及机构信息？",
        "发表在哪个会议或期刊？"
    ],

    "motivation": [
        "要解决计算机视觉中的什么问题？",
        "现有 CV 方法的局限性？",
        "在哪些具体场景或数据集上存在挑战？"
    ],

    "architecture": [
        "提出了什么网络架构？",
        "架构包含哪些模块（Backbone, Neck, Head）？",
        "使用了哪些注意力机制或特征融合方法？",
        "模型的输入输出是什么？"
    ],

    "training": [
        "使用了哪些损失函数？",
        "训练策略是什么（学习率、优化器、数据增强）？",
        "预训练模型或权重初始化方式？"
    ],

    "datasets": [
        "在哪些数据集上评估（COCO, ImageNet, ADE20K等）？",
        "数据集的规模和特点？",
        "数据预处理或后处理步骤？"
    ],

    "results": [
        "主要评价指标（mAP, IoU, Accuracy等）及数值？",
        "与 SOTA 方法的对比结果？",
        "消融实验验证了哪些设计选择？",
        "推理速度和模型大小？"
    ],

    "visualizations": [
        "有哪些可视化结果（检测框、分割掩码、注意力图）？",
        "定性分析展示了什么？"
    ]
}
```

#### 注册查询策略

```python
# rag/client.py
class RAGClient:
    QUERY_STRATEGIES = {
        "paper_general": RAG_PAPER_QUERIES,
        "paper_cv": RAG_CV_PAPER_QUERIES,
        "paper_nlp": RAG_NLP_PAPER_QUERIES,  # 可扩展
        "general_doc": RAG_GENERAL_QUERIES
    }

    def __init__(self, ..., query_strategy="paper_general"):
        self.query_strategy = query_strategy
        self.queries = self.QUERY_STRATEGIES[query_strategy]

    async def query_all_categories(self):
        """使用当前策略查询所有类别"""
        return await self.batch_query_by_category(self.queries)
```

#### 自动检测学科

```python
# summary/paper.py
def detect_paper_domain(rag_results):
    """自动检测论文领域"""

    keywords_map = {
        "cv": ["image", "vision", "detection", "segmentation", "CNN", "ResNet"],
        "nlp": ["language", "text", "BERT", "transformer", "embedding"],
        "ml": ["learning", "optimization", "gradient", "model"],
        "rl": ["reinforcement", "agent", "policy", "reward"]
    }

    # 从 paper_info 和 motivation 提取关键词
    text = " ".join(rag_results.get("paper_info", []) +
                    rag_results.get("motivation", []))
    text_lower = text.lower()

    # 计算匹配分数
    scores = {}
    for domain, keywords in keywords_map.items():
        scores[domain] = sum(1 for kw in keywords if kw.lower() in text_lower)

    # 返回最高分的领域
    best_domain = max(scores, key=scores.get)

    if scores[best_domain] >= 3:  # 至少 3 个关键词匹配
        return best_domain
    else:
        return "general"
```

---

### 3. 优化图像生成质量

#### 策略 1：迭代改进

```python
# generator/image_generator.py
class ImageGenerator:
    def generate_with_refinement(self, section, gen_input, max_iterations=2):
        """迭代改进生成质量"""

        # 第一次生成
        image_v1 = self._generate_single(section, gen_input)

        if max_iterations == 1:
            return image_v1

        # 提取文本进行验证
        extracted_text = self._extract_text_from_image(image_v1)
        expected_text = self._extract_key_terms(section.content)

        # 检查关键信息是否完整
        missing = self._find_missing_elements(extracted_text, expected_text)

        if not missing:
            return image_v1  # 已经完美

        # 第二次生成（带反馈）
        refinement_prompt = f"""
前一版本缺失或不清晰的内容：
{missing}

请生成改进版本，确保包含所有关键信息。
"""

        image_v2 = self._generate_single(
            section,
            gen_input,
            additional_prompt=refinement_prompt,
            reference_image=image_v1  # 作为参考
        )

        return image_v2

    def _extract_text_from_image(self, image_bytes):
        """使用 OCR 提取图片中的文本"""
        # 使用 GPT-4o vision 或 Tesseract OCR
        pass

    def _find_missing_elements(self, extracted, expected):
        """检查缺失的关键元素"""
        missing = []

        for key_term in expected:
            if key_term not in extracted:
                missing.append(key_term)

        return missing
```

#### 策略 2：风格迁移

```python
class StyleTransferGenerator(ImageGenerator):
    """基于参考图片的风格迁移生成器"""

    def __init__(self, ..., style_reference_image):
        super().__init__(...)
        self.style_reference = self._load_style_reference(style_reference_image)

    def _build_prompt(self, section, gen_input):
        base_prompt = super()._build_prompt(section, gen_input)

        # 添加风格迁移指令
        style_prompt = f"""
参考图片展示了目标风格。请严格遵循参考图片的：
- 配色方案（精确的颜色代码）
- 字体风格和大小
- 布局结构和边距
- 装饰元素的位置和形状
- 整体视觉风格

同时用新内容替换参考图片中的文字和数据。
"""

        return base_prompt + "\n\n" + style_prompt

    def _generate_single(self, section, gen_input):
        prompt = self._build_prompt(section, gen_input)
        images = [self.style_reference] + self._prepare_section_images(section)

        return self._call_model(prompt, images)
```

#### 策略 3：分辨率提升

```python
def upscale_image(image_bytes, target_width=3840, target_height=2160):
    """提升图像分辨率（4K）"""

    from PIL import Image
    import io

    # 1. 加载图片
    img = Image.open(io.BytesIO(image_bytes))

    # 2. 使用高质量重采样
    upscaled = img.resize(
        (target_width, target_height),
        resample=Image.LANCZOS  # 高质量插值
    )

    # 3. 或使用 AI 超分辨率模型（Real-ESRGAN）
    # upscaled = ai_upscale(img, scale=2)

    # 4. 保存
    output = io.BytesIO()
    upscaled.save(output, format='PNG', quality=95)

    return output.getvalue()


# 集成到生成流程
class ImageGenerator:
    def generate_slides(self, plan, gen_input):
        # 生成原始图片
        images = self._generate_all(plan, gen_input)

        # 提升分辨率
        if gen_input.config.get("high_resolution", False):
            images = [upscale_image(img) for img in images]

        return images
```

---

### 4. 性能优化

#### 优化 1：缓存机制

```python
# core/cache.py
import hashlib
import pickle

class ResultCache:
    """结果缓存（避免重复生成）"""

    def __init__(self, cache_dir=".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_key(self, data):
        """生成缓存键（基于内容哈希）"""
        serialized = pickle.dumps(data)
        hash_value = hashlib.sha256(serialized).hexdigest()
        return hash_value[:16]

    def get(self, key):
        """获取缓存"""
        cache_file = self.cache_dir / f"{key}.pkl"

        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        return None

    def set(self, key, value):
        """设置缓存"""
        cache_file = self.cache_dir / f"{key}.pkl"

        with open(cache_file, 'wb') as f:
            pickle.dump(value, f)


# 在 RAG 阶段使用
cache = ResultCache()

async def run_rag_stage_with_cache(base_dir, config):
    # 生成缓存键
    cache_key = cache.get_cache_key({
        "input_files": config["input_path"],
        "mode": config.get("fast_mode", False),
        "queries": RAG_PAPER_QUERIES
    })

    # 检查缓存
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info("Using cached RAG results")
        return cached_result

    # 执行 RAG
    result = await run_rag_stage(base_dir, config)

    # 保存缓存
    cache.set(cache_key, result)

    return result
```

#### 优化 2：批量处理

```python
# api/server.py
class BatchProcessor:
    """批量处理多个任务"""

    def __init__(self, max_batch_size=5, max_wait_time=10):
        self.max_batch_size = max_batch_size
        self.max_wait_time = max_wait_time
        self.pending_tasks = []
        self.lock = asyncio.Lock()

    async def add_task(self, session_id, files, config):
        """添加任务到批次"""
        async with self.lock:
            self.pending_tasks.append({
                "session_id": session_id,
                "files": files,
                "config": config,
                "added_at": time.time()
            })

            # 检查是否达到批次大小或等待时间
            if len(self.pending_tasks) >= self.max_batch_size:
                await self._process_batch()
            else:
                # 启动定时器
                asyncio.create_task(self._wait_and_process())

    async def _wait_and_process(self):
        """等待并处理批次"""
        await asyncio.sleep(self.max_wait_time)

        async with self.lock:
            if self.pending_tasks:
                await self._process_batch()

    async def _process_batch(self):
        """批量处理任务"""
        if not self.pending_tasks:
            return

        batch = self.pending_tasks.copy()
        self.pending_tasks.clear()

        logger.info(f"Processing batch of {len(batch)} tasks")

        # 并行处理（共享 RAG 索引）
        tasks = [
            self._process_single(task)
            for task in batch
        ]

        await asyncio.gather(*tasks)

    async def _process_single(self, task):
        """处理单个任务"""
        try:
            await run_pipeline_background(
                task["session_id"],
                task["files"],
                task["config"]
            )
        except Exception as e:
            logger.error(f"Task {task['session_id']} failed: {e}")
```

#### 优化 3：资源限制

```python
# core/pipeline.py
import psutil
import asyncio

class ResourceMonitor:
    """资源监控器"""

    def __init__(self, max_memory_percent=80, max_cpu_percent=90):
        self.max_memory_percent = max_memory_percent
        self.max_cpu_percent = max_cpu_percent

    def check_resources(self):
        """检查资源使用情况"""
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)

        if memory.percent > self.max_memory_percent:
            raise ResourceWarning(f"Memory usage too high: {memory.percent}%")

        if cpu > self.max_cpu_percent:
            raise ResourceWarning(f"CPU usage too high: {cpu}%")

        return {
            "memory_percent": memory.percent,
            "cpu_percent": cpu,
            "available_memory_gb": memory.available / (1024**3)
        }

    async def wait_for_resources(self, timeout=300):
        """等待资源可用"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                self.check_resources()
                return True
            except ResourceWarning:
                logger.warning("Resources exhausted, waiting...")
                await asyncio.sleep(10)

        raise TimeoutError("Resources not available within timeout")


# 在流水线中使用
monitor = ResourceMonitor()

async def run_pipeline(base_dir, config_dir, config, from_stage):
    for stage in STAGES:
        # 检查资源
        await monitor.wait_for_resources()

        # 执行阶段
        await run_stage(stage)
```

---

### 5. 添加新的图像生成提供商

**目标**：添加新的图像生成 API（如 Stability AI、DALL-E 等）

系统已实现提供商抽象，添加新提供商只需实现 `ImageGenerationProvider` 接口。

#### 步骤 1：实现提供商类

```python
# generator/providers.py

class StabilityAIProvider(ImageGenerationProvider):
    """Stability AI 提供商示例"""

    def __init__(self, api_key: str = None, model: str = "stable-diffusion-xl"):
        self.api_key = api_key or os.getenv("STABILITY_API_KEY")
        self.default_model = model

        if not self.api_key:
            raise ValueError("Stability AI API key is required")

        # 初始化客户端
        import stability_sdk
        self.client = stability_sdk.Client(api_key=self.api_key)

    def get_default_model(self) -> str:
        return self.default_model

    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """生成图像"""
        # 构建请求
        # 注意：不同 API 可能不支持参考图片
        result = self.client.generate(
            prompt=request.prompt,
            model=request.model or self.default_model
        )

        # 提取图像
        image_data = result.images[0].bytes
        mime_type = "image/png"

        return ImageGenerationResponse(image_data=image_data, mime_type=mime_type)
```

#### 步骤 2：注册到工厂

```python
# generator/providers.py

class ProviderFactory:
    PROVIDERS = {
        "openrouter": OpenRouterProvider,
        "google": GoogleGenAIProvider,
        "genai": GoogleGenAIProvider,
        "stability": StabilityAIProvider,  # 新增
    }

    @classmethod
    def from_env(cls) -> ImageGenerationProvider:
        provider_name = os.getenv("IMAGE_GEN_PROVIDER", "openrouter").lower()

        if provider_name == "stability":
            return StabilityAIProvider(
                api_key=os.getenv("STABILITY_API_KEY"),
                model=os.getenv("IMAGE_GEN_MODEL", "stable-diffusion-xl")
            )
        # ... 其他提供商
```

#### 步骤 3：更新配置文档

```bash
# .env.example 添加

# --- Stability AI Provider Settings ---
# Required when IMAGE_GEN_PROVIDER="stability"
# STABILITY_API_KEY=""
# IMAGE_GEN_MODEL="stable-diffusion-xl"
```

#### 步骤 4：添加测试

```python
# tests/test_providers.py

def test_stability_provider():
    """测试 Stability AI 提供商"""
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        pytest.skip("STABILITY_API_KEY not set")

    provider = StabilityAIProvider(api_key=api_key)

    request = ImageGenerationRequest(
        prompt="A simple test image",
        reference_images=[]
    )

    response = provider.generate_image(request)
    assert response.image_data
    assert response.mime_type == "image/png"
```

---

### 6. 添加新的文本 LLM 提供商

**目标**：支持 Anthropic Claude 作为文本模型

#### 步骤 1：创建客户端适配器

```python
# llm/providers.py
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """LLM 提供商抽象基类"""

    @abstractmethod
    async def chat(self, messages, model, **kwargs):
        """聊天补全"""
        pass

    @abstractmethod
    async def embed(self, texts, model):
        """文本嵌入"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI 提供商"""

    def __init__(self, api_key, base_url=None):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def chat(self, messages, model="gpt-4o", **kwargs):
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

    async def embed(self, texts, model="text-embedding-3-large"):
        response = await self.client.embeddings.create(
            model=model,
            input=texts
        )
        return [item.embedding for item in response.data]


class ClaudeProvider(LLMProvider):
    """Anthropic Claude 提供商"""

    def __init__(self, api_key):
        from anthropic import AsyncAnthropic
        self.client = AsyncAnthropic(api_key=api_key)

    async def chat(self, messages, model="claude-3-opus-20240229", **kwargs):
        # 转换消息格式（OpenAI → Claude）
        claude_messages = self._convert_messages(messages)

        response = await self.client.messages.create(
            model=model,
            messages=claude_messages,
            max_tokens=kwargs.get("max_tokens", 4096)
        )

        return response.content[0].text

    def _convert_messages(self, openai_messages):
        """转换消息格式"""
        claude_messages = []

        for msg in openai_messages:
            if msg["role"] == "system":
                # Claude 使用单独的 system 参数
                continue

            claude_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        return claude_messages

    async def embed(self, texts, model=None):
        # Claude 不直接提供嵌入，使用 Voyage AI
        raise NotImplementedError("Use Voyage AI for embeddings")
```

#### 步骤 2：提供商工厂

```python
# llm/factory.py
class LLMFactory:
    """LLM 提供商工厂"""

    PROVIDERS = {
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "gemini": GeminiProvider,  # 可扩展
    }

    @classmethod
    def create(cls, provider_name, **config):
        """创建提供商实例"""
        if provider_name not in cls.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider_name}")

        provider_class = cls.PROVIDERS[provider_name]
        return provider_class(**config)

    @classmethod
    def from_config(cls, config_file=".env"):
        """从配置文件创建"""
        import os
        from dotenv import load_dotenv

        load_dotenv(config_file)

        provider = os.getenv("LLM_PROVIDER", "openai")

        if provider == "openai":
            return cls.create("openai",
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL")
            )
        elif provider == "claude":
            return cls.create("claude",
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
```

#### 步骤 3：集成到代码中

```python
# 在各模块中使用
# summary/paper.py
async def extract_paper(rag_results, llm_provider=None, **kwargs):
    if llm_provider is None:
        llm_provider = LLMFactory.from_config()

    # 使用统一接口
    response = await llm_provider.chat(
        messages=[{"role": "user", "content": "..."}],
        model="gpt-4o-mini",  # 自动映射到 Claude 模型
        max_tokens=4000
    )

    return response


# 配置文件 (.env)
# LLM_PROVIDER=claude
# ANTHROPIC_API_KEY=your_key
```

---

### 7. 自定义后处理

#### 后处理器框架

```python
# generator/postprocessors.py
from abc import ABC, abstractmethod

class Postprocessor(ABC):
    """后处理器抽象基类"""

    @abstractmethod
    def process(self, image_bytes):
        """处理图片"""
        pass


class WatermarkPostprocessor(Postprocessor):
    """添加水印"""

    def __init__(self, watermark_text="Generated by Paper2Slides", position="bottom-right"):
        self.watermark_text = watermark_text
        self.position = position

    def process(self, image_bytes):
        from PIL import Image, ImageDraw, ImageFont
        import io

        # 1. 加载图片
        img = Image.open(io.BytesIO(image_bytes))
        draw = ImageDraw.Draw(img)

        # 2. 加载字体
        try:
            font = ImageFont.truetype("Arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        # 3. 计算位置
        text_bbox = draw.textbbox((0, 0), self.watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        if self.position == "bottom-right":
            x = img.width - text_width - 20
            y = img.height - text_height - 20
        # ... 其他位置

        # 4. 绘制水印
        draw.text((x, y), self.watermark_text, fill=(128, 128, 128, 128), font=font)

        # 5. 保存
        output = io.BytesIO()
        img.save(output, format='PNG')

        return output.getvalue()


class BorderPostprocessor(Postprocessor):
    """添加边框"""

    def __init__(self, border_width=10, border_color=(200, 200, 200)):
        self.border_width = border_width
        self.border_color = border_color

    def process(self, image_bytes):
        from PIL import Image, ImageOps
        import io

        img = Image.open(io.BytesIO(image_bytes))

        # 添加边框
        img_with_border = ImageOps.expand(
            img,
            border=self.border_width,
            fill=self.border_color
        )

        output = io.BytesIO()
        img_with_border.save(output, format='PNG')

        return output.getvalue()


class CompressionPostprocessor(Postprocessor):
    """压缩图片"""

    def __init__(self, quality=85, max_size_mb=5):
        self.quality = quality
        self.max_size_mb = max_size_mb

    def process(self, image_bytes):
        from PIL import Image
        import io

        img = Image.open(io.BytesIO(image_bytes))

        # 压缩
        output = io.BytesIO()
        img.save(output, format='PNG', optimize=True, quality=self.quality)

        # 检查大小
        size_mb = len(output.getvalue()) / (1024 * 1024)

        if size_mb > self.max_size_mb:
            # 进一步压缩
            scale = (self.max_size_mb / size_mb) ** 0.5
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.LANCZOS)

            output = io.BytesIO()
            img.save(output, format='PNG', optimize=True, quality=self.quality)

        return output.getvalue()


class PostprocessorPipeline:
    """后处理流水线"""

    def __init__(self, processors):
        self.processors = processors

    def process(self, image_bytes):
        """依次应用所有后处理器"""
        result = image_bytes

        for processor in self.processors:
            result = processor.process(result)

        return result


# 使用示例
# generator/image_generator.py
class ImageGenerator:
    def __init__(self, ..., postprocessors=None):
        self.postprocessors = postprocessors or []

    def generate_slides(self, plan, gen_input):
        # 生成原始图片
        images = self._generate_all(plan, gen_input)

        # 应用后处理
        if self.postprocessors:
            pipeline = PostprocessorPipeline(self.postprocessors)
            images = [pipeline.process(img) for img in images]

        return images


# 配置
postprocessors = [
    BorderPostprocessor(border_width=5, border_color=(220, 220, 220)),
    WatermarkPostprocessor(watermark_text="© 2023 My Lab"),
    CompressionPostprocessor(quality=90, max_size_mb=3)
]

generator = ImageGenerator(..., postprocessors=postprocessors)
```

---

## 🔧 调试和测试

### 单元测试示例

```python
# tests/test_content_planner.py
import pytest
from paper2slides.generator.content_planner import ContentPlanner
from paper2slides.summary.models import PaperContent, OriginalElements

@pytest.fixture
def sample_content():
    return PaperContent(
        paper_info="Title: Test Paper\nAuthors: John Doe",
        motivation="We address the problem of...",
        solution="We propose a novel method...",
        results="Experiments show 95% accuracy...",
        contributions="Main contributions: 1) ..."
    )

@pytest.fixture
def sample_origin():
    return OriginalElements(
        tables=[],
        figures=[],
        base_path="/tmp/test"
    )

def test_content_planner_short():
    """测试短幻灯片规划"""
    planner = ContentPlanner(mock_llm_client())

    plan = planner.plan(GenerationInput(
        content=sample_content(),
        origin=sample_origin(),
        output_type="slides",
        config={"slides_length": "short"}
    ))

    assert len(plan.sections) >= 5
    assert len(plan.sections) <= 8
    assert plan.sections[0].title  # 标题页

def test_content_planner_with_figures():
    """测试包含图片的规划"""
    origin = OriginalElements(
        tables=[],
        figures=[
            FigureInfo("Figure 1", "Architecture", "/path/figure1.png")
        ],
        base_path="/tmp"
    )

    planner = ContentPlanner(mock_llm_client())
    plan = planner.plan(GenerationInput(..., origin=origin))

    # 检查图片是否被分配到某一页
    has_figure = any(
        len(section.figures) > 0
        for section in plan.sections
    )
    assert has_figure
```

### 集成测试

```python
# tests/test_pipeline.py
import pytest
import asyncio
from paper2slides.core.pipeline import run_pipeline

@pytest.mark.asyncio
async def test_full_pipeline():
    """测试完整流水线"""
    config = {
        "input_path": "tests/fixtures/sample_paper.pdf",
        "content_type": "paper",
        "output_type": "slides",
        "style": "academic",
        "slides_length": "short",
        "fast_mode": True
    }

    base_dir = Path("tests/output/test_project/paper")
    config_dir = base_dir / "fast" / "slides_academic_short"

    # 运行流水线
    await run_pipeline(
        base_dir=base_dir,
        config_dir=config_dir,
        config=config,
        from_stage="rag"
    )

    # 验证输出
    assert (base_dir / "fast" / "checkpoint_rag.json").exists()
    assert (base_dir / "fast" / "checkpoint_summary.json").exists()
    assert (config_dir / "checkpoint_plan.json").exists()

    # 检查生成的图片
    output_dir = list(config_dir.glob("*"))[0]
    slides = list(output_dir.glob("slide_*.png"))
    assert len(slides) >= 5


@pytest.mark.asyncio
async def test_resume_from_checkpoint():
    """测试断点续传"""
    # 第一次运行（中断在 plan 阶段）
    # ...

    # 第二次运行（从 plan 继续）
    await run_pipeline(..., from_stage="plan")

    # 验证没有重复执行 RAG 和 Summary
    # ...
```

### 性能测试

```python
# tests/test_performance.py
import time
import psutil

def test_memory_usage():
    """测试内存使用"""
    process = psutil.Process()

    initial_memory = process.memory_info().rss / (1024 * 1024)  # MB

    # 运行流水线
    run_pipeline(...)

    final_memory = process.memory_info().rss / (1024 * 1024)
    memory_increase = final_memory - initial_memory

    # 确保内存增长在合理范围内（< 2GB）
    assert memory_increase < 2000


def test_generation_speed():
    """测试生成速度"""
    start_time = time.time()

    # 生成 10 页幻灯片
    generator.generate_slides(plan_with_10_pages, gen_input)

    elapsed = time.time() - start_time

    # 确保平均每页 < 30 秒（使用并行生成）
    avg_per_slide = elapsed / 10
    assert avg_per_slide < 30
```

---

## 📦 部署建议

### Docker 化

```dockerfile
# Dockerfile
FROM python:3.12-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制代码
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -e .

# 暴露端口
EXPOSE 8001

# 启动命令
CMD ["python", "api/server.py", "8001"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8001:8001"
    volumes:
      - ./outputs:/app/outputs
      - ./sources:/app/sources
    environment:
      - RAG_LLM_API_KEY=${RAG_LLM_API_KEY}
      - IMAGE_GEN_PROVIDER=${IMAGE_GEN_PROVIDER:-openrouter}
      - IMAGE_GEN_API_KEY=${IMAGE_GEN_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    restart: unless-stopped

  frontend:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ./frontend:/app
    ports:
      - "5173:5173"
    command: npm run dev
    depends_on:
      - backend
```

### 生产环境配置

```python
# api/config.py
import os

class Config:
    """基础配置"""
    DEBUG = False
    TESTING = False

    # API 密钥
    RAG_LLM_API_KEY = os.getenv("RAG_LLM_API_KEY")
    IMAGE_GEN_API_KEY = os.getenv("IMAGE_GEN_API_KEY")

    # 路径
    UPLOAD_DIR = "/data/uploads"
    OUTPUT_DIR = "/data/outputs"

    # 限制
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_UPLOAD_FILES = 10

    # 并发
    MAX_CONCURRENT_TASKS = 3
    MAX_WORKERS_PER_TASK = 2


class DevelopmentConfig(Config):
    """开发配置"""
    DEBUG = True
    UPLOAD_DIR = "sources/uploads"
    OUTPUT_DIR = "outputs"


class ProductionConfig(Config):
    """生产配置"""
    # 使用 Redis 存储会话
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # 使用 S3 存储输出
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")

    # 日志
    LOG_LEVEL = "INFO"
    LOG_FILE = "/var/log/paper2slides/app.log"


def get_config():
    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()
```

---

## 🎓 最佳实践

### 1. 提示词工程

**原则**：
- 详细具体：明确每个要求
- 结构化输出：使用 JSON 模式
- 示例驱动：提供少样本示例
- 迭代优化：根据输出调整

**示例**：
```python
# 差的提示词
prompt = "总结这篇论文"

# 好的提示词
prompt = """
从以下论文内容中提取结构化信息。

## 输出格式（JSON）
{
  "title": "论文完整标题",
  "authors": ["作者1", "作者2"],
  "institutions": ["机构1", "机构2"],
  "abstract": "摘要（最多200词）",
  "key_contributions": ["贡献1", "贡献2", "贡献3"]
}

## 要求
- 保留原文的专业术语
- 数字和单位保持精确
- 如果信息缺失，使用 null

## 论文内容
{paper_text}

现在请输出 JSON：
"""
```

### 2. 错误处理

```python
# 差的错误处理
def generate():
    result = api.call()
    return result


# 好的错误处理
def generate(max_retries=3):
    for attempt in range(max_retries):
        try:
            result = api.call()
            return result

        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                logger.warning(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

        except APIError as e:
            logger.error(f"API error: {e}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise


# 更好：使用装饰器
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def generate():
    return api.call()
```

### 3. 日志记录

```python
# paper2slides/utils/logging.py
import logging
import sys

def setup_logger(name, level=logging.INFO):
    """配置日志器"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # 文件处理器
    file_handler = logging.FileHandler("paper2slides.log")
    file_handler.setLevel(logging.DEBUG)

    # 格式化
    formatter = logging.Formatter(
        '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# 使用
logger = setup_logger(__name__)

logger.info("Starting pipeline...")
logger.debug(f"Config: {config}")
logger.error(f"Failed to generate: {error}")
```

---

## 🚧 常见问题和解决方案

### 问题 1：生成的图片文字模糊

**原因**：默认分辨率不够高

**解决方案**：
```python
# 在提示词中明确指定高分辨率
prompt = """
创建一张高分辨率演示幻灯片（3840x2160, 4K质量）。

文字要求：
- 所有文字清晰可读
- 最小字体大小：24pt
- 使用抗锯齿渲染
...
"""

# 或后处理提升分辨率
images = [upscale_image(img, target_width=3840) for img in images]
```

### 问题 2：RAG 查询返回不相关内容

**原因**：查询问题过于宽泛或模糊

**解决方案**：
```python
# 差的查询
"论文的方法是什么？"

# 好的查询
"论文提出了什么具体的算法或模型架构？请详细描述主要组件、输入输出、以及与现有方法的区别。"

# 或使用多个具体查询
queries = [
    "论文提出的模型架构名称是什么？",
    "模型包含哪些主要模块或组件？每个组件的作用是什么？",
    "模型的输入是什么？输出是什么？",
    "与 baseline 方法相比，新方法的关键创新在哪里？"
]
```

### 问题 3：生成速度慢

**原因**：顺序生成所有页面

**解决方案**：
```bash
# 使用并行生成
python -m paper2slides --input paper.pdf --parallel 4

# 或使用 fast 模式（跳过 RAG 索引）
python -m paper2slides --input paper.pdf --fast
```

### 问题 4：风格不一致

**原因**：每页独立生成，没有参考

**解决方案**：
```python
# 当前已实现：使用第 2 页作为风格参考

# 进一步改进：使用更强的风格约束
style_reference = {
    "figure_id": "Style Reference",
    "caption": """
        CRITICAL: Maintain EXACT style consistency:
        - Background color: #FFFFFF (no variations)
        - Primary accent: #1e3a8a
        - Font: Roboto, 48pt for headers, 32pt for body
        - Layout: 80px margins, centered alignment
        - NO decorative elements beyond simple lines
    """,
    "base64": reference_image_base64
}
```

---

## 📚 推荐学习资源

### 技术栈相关
1. **FastAPI**: https://fastapi.tiangolo.com/
2. **LightRAG**: https://github.com/HKUDS/LightRAG
3. **OpenAI API**: https://platform.openai.com/docs/
4. **React**: https://react.dev/

### RAG 和提示词工程
1. **Prompt Engineering Guide**: https://www.promptingguide.ai/
2. **RAG 最佳实践**: https://arxiv.org/abs/2312.10997
3. **多模态 LLM**: https://arxiv.org/abs/2306.13549

### 代码示例
- 本项目 GitHub: (项目仓库地址)
- 示例论文和输出: `examples/` 目录

---

## 🤝 贡献指南

如果你想为 Paper2Slides 贡献代码：

1. **Fork 项目**
2. **创建特性分支**: `git checkout -b feature/amazing-feature`
3. **编写代码和测试**
4. **提交**: `git commit -m 'Add amazing feature'`
5. **推送**: `git push origin feature/amazing-feature`
6. **创建 Pull Request**

### 代码风格
- 遵循 PEP 8
- 使用类型提示
- 编写文档字符串
- 添加单元测试

---

## 📄 许可证

本项目采用 MIT 许可证。详见 `LICENSE` 文件。

---

**生成日期**: 2025-12-10
**文档版本**: 1.1
**最后更新**: 添加图像生成提供商系统（OpenRouter/Google GenAI）
**作者**: Paper2Slides Team

---

*如有问题或建议，请提交 Issue 或联系维护者。*
