def calculate_similarity_score(target, examples):
    def parse_info(text):
        data = {}
        lines = text.strip().split("\n")
        for line in lines:
            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                data[key] = value
        return data

    def calculate_skills_score(target_skills, example_skills):
        if target_skills == "-" or example_skills == "-":
            return 0

        target_skills = set(map(str.strip, target_skills.split(",")))
        example_skills = set(map(str.strip, example_skills.split(",")))

        match_weight = 2.0
        extra_weight = 0.5
        matches = target_skills & example_skills
        extras = example_skills - matches

        total_weight = (len(matches) * match_weight) + (len(extras) * extra_weight)
        max_weight = len(target_skills) * match_weight
        return total_weight / max_weight

    def calculate_language_score(target_languages, example_languages):
        if target_languages == "-" or example_languages == "-":
            return 0

        target_languages = set(map(str.strip, target_languages.split(",")))
        example_languages = set(map(str.strip, example_languages.split(",")))

        match_weight = 2.0
        extra_weight = 0.5
        matches = target_languages & example_languages
        extras = example_languages - matches

        total_weight = (len(matches) * match_weight) + (len(extras) * extra_weight)
        max_weight = len(target_languages) * match_weight
        return total_weight / max_weight

    def calculate_education_score(target_education, example_education):
        if target_education == "-" or example_education == "-":
            return 0

        return 1.0 if target_education == example_education else 0.0

    target_info = parse_info(target)
    results = {}

    for idx, example in enumerate(examples, 1):
        example_info = parse_info(example)

        title = example_info.get("Резюме") or example_info.get("Вакансия")
        if not title:
            continue

        skills_score = calculate_skills_score(
            target_info.get("Ключевые навыки", "-"), example_info.get("Ключевые навыки", "-")
        )
        language_score = calculate_language_score(
            target_info.get("Знание языков", "-"), example_info.get("Знание языков", "-")
        )
        education_score = calculate_education_score(
            target_info.get("Образование", "-"), example_info.get("Образование", "-")
        )

        similarity_score = (
            0.8 * skills_score + 0.15 * language_score + 0.05 * education_score
        )

        # formatted_result = (
        #     f'\n{"`"*50}\n'
        #     f"ID: {example_info.get('id')}\n"
        #     f"{'Резюме' if 'Резюме' in example_info else 'Вакансия'}: {title}\n"
        #     f"Описание: {example_info.get('Описание', '-')}\n"
        #     f"similarity_score = {round(similarity_score, 2)}\n"
        #     f'{"``"*50}\n'
        # )
        results[example_info.get('id')] = round(similarity_score, 2)

    return results
