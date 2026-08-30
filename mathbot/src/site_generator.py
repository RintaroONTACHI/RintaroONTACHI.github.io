import html
from pathlib import Path


DOCS = Path("docs")
PROBLEMS_DIR = DOCS / "problems"


MATHJAX = """
<script>
window.MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
    }
};
</script>

<script
    async
    src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js">
</script>
"""


def format_category(category):

    if isinstance(category, list):

        values = [
            str(x)
            for x in category
            if x
        ]

        if values:
            return ", ".join(values)

        return "数学"

    if category:
        return str(category)

    return "数学"


def page_start(
    title,
    css_path,
    home_path
):

    return f"""
<!DOCTYPE html>
<html lang="ja">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1">

<title>{html.escape(title)} | MathBot</title>

<link rel="stylesheet"
      href="{css_path}">

{MATHJAX}

</head>

<body>

<header>

<div class="container">

<a href="{home_path}">

<div class="site-title">
MathBot
</div>

</a>

<div class="site-description">
今日の一問を、毎日。
</div>

</div>

</header>

<main>

<div class="container">
"""


def page_end():

    return """
</div>

</main>

<footer>

<div class="container">

MathBot

</div>

</footer>

</body>

</html>
"""


def generate_site(problems):

    DOCS.mkdir(
        parents=True,
        exist_ok=True
    )

    PROBLEMS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    published = [
        p
        for p in problems
        if p.get("published_at")
    ]

    published.sort(
        key=lambda p: p["published_at"],
        reverse=True
    )

    cards = ""

    for problem in published:

        category = format_category(
            problem.get("category")
        )

        cards += f"""
<a class="problem-card"
   href="problems/{problem['id']}.html">

    <div class="problem-title">
        {html.escape(problem["title"])}
    </div>

    <div class="problem-meta">
        {html.escape(category)}
        ·
        {html.escape(problem["published_at"])}
    </div>

</a>
"""

    index = f"""
{page_start(
    "過去問",
    "../style.css",
    "../index.html"
)}

<h1>過去問</h1>

<p>
MathBotで出題した数学問題のアーカイブです。
</p>

{cards}

{page_end()}
"""

    (
        DOCS / "index.html"
    ).write_text(
        index,
        encoding="utf-8"
    )

    for problem in published:

        category = format_category(
            problem.get("category")
        )

        solution = ""

        if problem.get(
            "solution_published_at"
        ):

            solution = f"""
<section class="solution">

<h2>解答</h2>

<div class="problem-body">

{problem["japanese_solution"]}

</div>

</section>
"""

        page = f"""
{page_start(
    problem["title"],
    "../../style.css",
    "../index.html"
)}

<a class="back"
   href="../index.html">
← 過去問一覧
</a>

<h1>
{html.escape(problem["title"])}
</h1>

<div class="problem-meta">

{html.escape(category)}

·

{html.escape(problem["published_at"])}

</div>

<section>

<h2>問題</h2>

<div class="problem-body">

{problem["japanese_problem"]}

</div>

</section>

{solution}

{page_end()}
"""

        (
            PROBLEMS_DIR /
            f"{problem['id']}.html"
        ).write_text(
            page,
            encoding="utf-8"
        )
