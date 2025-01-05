from typing import List, Dict


class SimilarityCalculator:
    """
    A class to calculate similarity scores between a target and a set of examples.
    """

    MATCH_WEIGHT = 2.0
    EXTRA_WEIGHT = 0.5

    @staticmethod
    def parse_info(text: str) -> Dict[str, str]:
        """
        Parses structured text into a dictionary of key-value pairs.

        Args:
            text (str): The input text to parse.

        Returns:
            Dict[str, str]: A dictionary containing parsed information.
        """
        data = {}
        lines = text.strip().split("\n")
        for line in lines:
            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                data[key] = value
        return data

    @classmethod
    def calculate_skills_score(cls, target_skills: str, example_skills: str) -> float:
        """
        Calculates a similarity score for skills.

        Args:
            target_skills (str): Skills from the target.
            example_skills (str): Skills from the example.

        Returns:
            float: The similarity score.
        """
        if target_skills == "-" or example_skills == "-":
            return 0

        target_set = set(map(str.strip, target_skills.split(",")))
        example_set = set(map(str.strip, example_skills.split(",")))

        matches = target_set & example_set
        extras = example_set - matches

        total_weight = (len(matches) * cls.MATCH_WEIGHT) + (len(extras) * cls.EXTRA_WEIGHT)
        max_weight = len(target_set) * cls.MATCH_WEIGHT
        return total_weight / max_weight if max_weight > 0 else 0

    @classmethod
    def calculate_language_score(cls, target_languages: str, example_languages: str) -> float:
        """
        Calculates a similarity score for languages.

        Args:
            target_languages (str): Languages from the target.
            example_languages (str): Languages from the example.

        Returns:
            float: The similarity score.
        """
        if target_languages == "-" or example_languages == "-":
            return 0

        target_set = set(map(str.strip, target_languages.split(",")))
        example_set = set(map(str.strip, example_languages.split(",")))

        matches = target_set & example_set
        extras = example_set - matches

        total_weight = (len(matches) * cls.MATCH_WEIGHT) + (len(extras) * cls.EXTRA_WEIGHT)
        max_weight = len(target_set) * cls.MATCH_WEIGHT
        return total_weight / max_weight if max_weight > 0 else 0

    @staticmethod
    def calculate_education_score(target_education: str, example_education: str) -> float:
        """
        Calculates a similarity score for education.

        Args:
            target_education (str): Education from the target.
            example_education (str): Education from the example.

        Returns:
            float: The similarity score (1.0 if they match, otherwise 0.0).
        """
        if target_education == "-" or example_education == "-":
            return 0
        return 1.0 if target_education == example_education else 0.0

    def calculate_similarity_score(self, target: str, examples: List[str]) -> Dict[str, float]:
        """
        Calculates similarity scores for a target against multiple examples.

        Args:
            target (str): The target information.
            examples (List[str]): A list of example information.

        Returns:
            Dict[str, float]: A dictionary mapping example IDs to their similarity scores.
        """
        target_info = self.parse_info(target)
        results = {}

        for example in examples:
            example_info = self.parse_info(example)

            example_id = example_info.get("id")
            if not example_id:
                continue

            skills_score = self.calculate_skills_score(
                target_info.get("Ключевые навыки", "-"),
                example_info.get("Ключевые навыки", "-"),
            )
            language_score = self.calculate_language_score(
                target_info.get("Знание языков", "-"),
                example_info.get("Знание языков", "-"),
            )
            education_score = self.calculate_education_score(
                target_info.get("Образование", "-"),
                example_info.get("Образование", "-"),
            )

            similarity_score = (
                0.8 * skills_score + 0.15 * language_score + 0.05 * education_score
            )
            results[example_id] = round(similarity_score, 2)

        return results
