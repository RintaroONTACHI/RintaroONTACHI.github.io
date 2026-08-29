from google import genai

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate(
    prompt
):
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text.strip()


def translate_problem(text):

    prompt = f"""
以下の数学問題を日本語に忠実に翻訳してください。

重要：

- 問題を解かない
- ヒントを追加しない
- 条件を変更しない
- 数値を変更しない
- 変数を変更しない
- 論理関係を変更しない
- 数式はLaTeX形式を維持する
- 問題文以外を書かない

原文：

{text}
"""

    return generate(prompt)


def translate_solution(text):

    if not text:
        return ""

    prompt = f"""
以下の数学の解答を日本語に忠実に翻訳してください。

重要：

- 解法を変更しない
- 証明を省略しない
- 証明を追加しない
- 計算を変更しない
- 論理関係を変更しない
- 数式はLaTeX形式を維持する
- 解答本文以外を書かない

原文：

{text}
"""

    return generate(prompt)
