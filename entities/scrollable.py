class ScrollableEntity:
    """Minimal base for horizontally scrolling entities used by Background and Ground.

    It manages two segments (x1 and x2) used to create an infinite-scrolling effect.
    Constructor signature used by callers: ScrollableEntity(width, height, y)
    """

    def __init__(self, width: int, height: int, y: int) -> None:
        self.width = width
        self.height = height
        self.y = y
        # Place two segments next to each other
        self.x1 = 0
        self.x2 = self.width

    def update(self, dx: float) -> None:
        """Move both segments left/right by dx and wrap when a segment leaves screen.

    Positive dx moves content to the right (camera moving left).
    Negative dx moves content to the left.
        """
        self.x1 += dx
        self.x2 += dx
    # If a segment moves completely off to the left,
    # wrap it to the right of the other
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
        # If a segment moves completely off to the right, wrap it to the left
        if self.x1 > self.x2 + self.width:
            self.x1 = self.x2 - self.width
        if self.x2 > self.x1 + self.width:
            self.x2 = self.x1 - self.width

    def set_region(self, index: int) -> None:
        """Placeholder for derived classes to change colors/themes."""
        pass
