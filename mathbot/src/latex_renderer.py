from pathlib import Path
from playwright.sync_api import sync_playwright


def render_latex(text: str, output_path: str) -> str:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">

<style>
body {{
    margin: 0;
    padding: 40px;
    background: white;
    color: black;
    font-family: "Noto Sans CJK JP", "Noto Sans JP", sans-serif;
    font-size: 28px;
}}

.content {{
    width: 1000px;
}}
</style>

<script>
window.MathJax = {{
    tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
    }}
}};
</script>

<script
    async
    src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js">
</script>

</head>

<body>

<div class="content">
{text}
</div>

</body>
</html>
"""

    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page(
            viewport={
                "width": 1100,
                "height": 800
            },
            device_scale_factor=2
        )

        page.set_content(html)

        # MathJaxが読み込まれるまで待つ
        page.wait_for_function(
            """
            () =>
                window.MathJax &&
                window.MathJax.startup &&
                window.MathJax.startup.promise
            """,
            timeout=30000
        )

        # MathJaxの初期化完了を待つ
        page.evaluate(
            """() => MathJax.startup.promise"""
        )

        # 明示的にtypeset
        page.evaluate(
            """() => MathJax.typesetPromise()"""
        )

        # 数式が生成されたことを確認
        page.wait_for_selector(
            "mjx-container",
            timeout=30000
        )

        page.screenshot(
            path=str(output),
            full_page=True
        )

        browser.close()

    return str(output)
