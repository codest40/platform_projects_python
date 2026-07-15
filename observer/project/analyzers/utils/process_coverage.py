from project.analyzers.utils.coverage import Coverage as _Coverage

""" For Process resurce coverage oly
"""

class Coverage(_Coverage):
    def __init__(self):
        super().__init__()

    def apply(self, metrics):
        super().apply(
            metrics,
            "total_analyzed",
            "total_available",
        )

    def score(self, metrics):
        score = super().score(
            metrics,
            "total_scores",
        )

        if score is not None:
            if score == 1.0:
                return "COMPLETE"
            elif score == 0.0:
                return "UNAVAILABLE"
            else:
                return "PARTIAL"
        else:
                return "N/S"
