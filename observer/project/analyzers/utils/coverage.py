
class Coverage:
    """
    Tracks how much evidence was available for an analyzer.
    Measures analysis completeness
    """

    def __init__(self):
        self.available = 0
        self.expected = 0

    def check(self, condition: bool) -> None:
        self.expected += 1

        if condition:
            self.available += 1

    def apply(self, target) -> None:
        target.metrics_available = self.available
        target.metrics_expected = self.expected

    @property
    def score(self) -> float:
        if self.expected == 0:
            return 0.0

        return round(
            self.available / self.expected * 100,
            1,
        )

