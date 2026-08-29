import json
from pathlib import Path

from config import DATA_FILE


def load_problems():
    path = Path(DATA_FILE)

    if not path.exists():
        return []

    with path.open(
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_problems(problems):
    path = Path(DATA_FILE)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with path.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            problems,
            f,
            ensure_ascii=False,
            indent=2
        )


def get_problem(
    problems,
    problem_id
):
    for problem in problems:

        if problem["id"] == problem_id:
            return problem

    return None


def add_or_update_problem(
    problems,
    new_problem
):
    existing = get_problem(
        problems,
        new_problem["id"]
    )

    if existing is None:

        problems.append(
            new_problem
        )

    else:

        existing.update(
            new_problem
        )

    return problems


def get_unpublished_problem(
    problems
):
    for problem in problems:

        if not problem.get(
            "published_at"
        ):
            return problem

    return None


def get_today_problem(
    problems,
    date
):
    for problem in problems:

        if problem.get(
            "published_at"
        ) == date:

            return problem

    return None
