import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from database import (
    load_problems,
    save_problems,
    add_or_update_problem,
    get_unpublished_problem,
    get_today_problem,
)

from fetch import fetch_problems

from translate import (
    translate_problem,
    translate_solution,
)

from discord import send_message

from site_generator import generate_site


JST = ZoneInfo(
    "Asia/Tokyo"
)


def import_problems(
    problems
):

    fetched = fetch_problems(
	probrems
)

    for raw in fetched:

        new_problem = {
            "id": raw["id"],
            "source": raw["source"],
            "source_url": raw.get(
                "source_url",
                ""
            ),
            "title": raw["title"],
            "category": raw.get(
                "category",
                "数学"
            ),
            "difficulty": raw.get(
                "difficulty",
                ""
            ),
            "original_problem":
                raw["original_problem"],
            "original_solution":
                raw.get(
                    "original_solution",
                    ""
                ),
            "japanese_problem":
                raw.get(
                    "japanese_problem",
                    ""
                ),
            "japanese_solution":
                raw.get(
                    "japanese_solution",
                    ""
                ),
            "published_at":
                raw.get(
                    "published_at"
                ),
            "solution_published_at":
                raw.get(
                    "solution_published_at"
                )
        }

        add_or_update_problem(
            problems,
            new_problem
        )


def morning():

    problems = load_problems()

    import_problems(
        problems
    )

    problem = get_unpublished_problem(
        problems
    )

    if problem is None:

        print(
            "出題できる問題がありません"
        )

        save_problems(
            problems
        )

        generate_site(
            problems
        )

        return

    if not problem[
        "japanese_problem"
    ]:

        problem[
            "japanese_problem"
        ] = translate_problem(
            problem[
                "original_problem"
            ]
        )

    today = datetime.now(
        JST
    ).strftime(
        "%Y-%m-%d"
    )

    problem[
        "published_at"
    ] = today

    description = (
        problem[
            "japanese_problem"
        ]
    )

    if problem.get(
        "source_url"
    ):

        description += (
            "\n\n"
            "出典: "
            + problem[
                "source_url"
            ]
        )

    send_message(
        "🧩 今日の一問",
        description
    )

    save_problems(
        problems
    )

    generate_site(
        problems
    )


def evening():

    problems = load_problems()

    today = datetime.now(
        JST
    ).strftime(
        "%Y-%m-%d"
    )

    problem = get_today_problem(
        problems,
        today
    )

    if problem is None:

        print(
            "今日の問題がありません"
        )

        return

    if problem.get(
        "solution_published_at"
    ):

        print(
            "解答は既に公開済み"
        )

        return

    if not problem[
        "original_solution"
    ]:

        print(
            "解答が存在しません"
        )

        return

    if not problem[
        "japanese_solution"
    ]:

        problem[
            "japanese_solution"
        ] = translate_solution(
            problem[
                "original_solution"
            ]
        )

    problem[
        "solution_published_at"
    ] = today

    send_message(
        "📖 今日の一問 — 解答",
        problem[
            "japanese_solution"
        ]
    )

    save_problems(
        problems
    )

    generate_site(
        problems
    )


def main():

    if len(sys.argv) != 2:

        print(
            "morning または "
            "evening を指定してください"
        )

        return

    mode = sys.argv[1]

    if mode == "morning":

        morning()

    elif mode == "evening":

        evening()

    else:

        print(
            "unknown mode"
        )


if __name__ == "__main__":
    main()
