from typing import Any


class PrefixMatch:
    def __init__(
        self,
    ):
        pass

    def __call__(self, doc, ground_truth, results) -> Any:
        """Take a single document and the LM input/output/ground_truth.
        Returns the  values of the metric for that one document
        """
        
        if isinstance(ground_truth, str):
            return 1.0 if results[0].strip().startswith(ground_truth.strip()) else 0.0
        elif isinstance(ground_truth, list):
            return 1.0 if any(results[0].strip().startswith(g.strip()) for g in ground_truth) else 0.0
        else:
            raise ValueError("Invalid input type for results")
        