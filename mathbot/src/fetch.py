import random

from datasets import load_dataset


DATASET_NAME = "ShadenA/MathNet"


def load_mathnet():
    print("Loading MathNet (streaming)...")

    return load_dataset(
        DATASET_NAME,
        split="train",
        streaming=True,
    )


def get_mathnet_id(row):
    return (
        row.get("unique_id")
        or row.get("id")
    )


def is_valid_problem(
    row,
    used_ids
):
    mathnet_id = get_mathnet_id(row)

    if not mathnet_id:
        return False

    if mathnet_id in used_ids:
        return False

    # MathNet側で画像付きと判定されている問題を除外
    if row.get("has_images", False):
        return False

    problem = row.get(
        "problem_markdown"
    )

    if not problem:
        return False

    if not problem.strip():
        return False

    # Markdown画像を含む問題を除外
    # 例:
    # ![](image.png)
    # ![figure](...)
    if "![" in problem:
        return False

    # HTML画像を含む問題も除外
    # 例:
    # <img src="...">
    if "<img" in problem.lower():
        return False

    # 画像ファイルへの直接参照も除外
    image_extensions = (
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".svg",
    )

    lower_problem = problem.lower()

    if any(
        ext in lower_problem
        for ext in image_extensions
    ):
        return False

    return True


def choose_problem(
    dataset,
    existing_problems
):
    used_ids = {
        problem.get("mathnet_id")
        for problem in existing_problems
        if problem.get("mathnet_id")
    }

    # ストリーミングでは全件をメモリに持たない
    candidates = []

    # 最大1000問まで探索
    max_scan = 1000

    # 候補を20問集めたら終了
    target_candidates = 20

    for i, row in enumerate(dataset):

        if is_valid_problem(
            row,
            used_ids
        ):
            candidates.append(row)

            if len(candidates) >= target_candidates:
                break

        if i >= max_scan:
            break

    if not candidates:
        raise RuntimeError(
            "No unused MathNet problems found."
        )

    return random.choice(
        candidates
    )


def convert_problem(row):

    mathnet_id = get_mathnet_id(row)

    solutions = (
        row.get("solutions_markdown")
        or []
    )

    if isinstance(
        solutions,
        str
    ):
        solution = solutions

    else:
        solution = "\n\n".join(
            s
            for s in solutions
            if isinstance(s, str)
            and s.strip()
        )

    topics = (
        row.get("topics_flat")
        or []
    )

    if isinstance(
        topics,
        str
    ):
        topics = [topics]

    return {
        "id": f"mathnet-{mathnet_id}",

        "mathnet_id": mathnet_id,

        "source": "MathNet",

        "source_url": (
            "https://huggingface.co/"
            "datasets/ShadenA/MathNet"
        ),

        "title": (
            f'{row.get("competition", "MathNet")} '
            f'Problem '
            f'{row.get("problem_number", "")}'
        ).strip(),

        "country": row.get(
            "country"
        ),

        "competition": row.get(
            "competition"
        ),

        "year": row.get(
            "year"
        ),

        "section": row.get(
            "section"
        ),

        "problem_number": row.get(
            "problem_number"
        ),

        "language": row.get(
            "language"
        ),

        "category": topics,

        "difficulty": "Olympiad",

        "original_problem":
            row["problem_markdown"],

        "original_solution":
            solution,

        "japanese_problem": "",

        "japanese_solution": "",

        "published_at": None,

        "solution_published_at": None,
    }


def fetch_problems(
    existing_problems
):
    dataset = load_mathnet()

    problem = choose_problem(
        dataset,
        existing_problems
    )

    converted = convert_problem(
        problem
    )

    print(
        "Selected MathNet problem:"
    )

    print(
        converted["id"]
    )

    print(
        converted["title"]
    )

    return [converted]
