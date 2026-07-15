class Coverage:
    """
    Tracks how much evidence was available for an analyzer.
    Used within a single analyzer to record
    how many metrics were expected and how many were successfully
    analyzed.
    """

    def __init__(self):
        self.available = 0
        self.expected = 0
        self.result = 0.0

    def check(
        self,
        condition: bool,
    ) -> None:

        self.expected += 1
        if condition:
            self.available += 1

    def apply( self, target, available: str, total: str,) -> None:

        setattr(target, available, self.available,)
        setattr(target, total, self.expected,)

    def score(self, target, value: str,) -> float:
        if self.expected == 0:
            self.result = 0.0
        else:
            self.result = round(
                self.available / self.expected,
                2,
            )

        setattr(target, value, self.result,)
        return self.result
