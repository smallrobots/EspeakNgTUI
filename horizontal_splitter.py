from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static
from textual import events
from textual.reactive import reactive

class HorizontalSplitter(Horizontal):
    """A simple horizontal splitter with draggable handle."""

    DEFAULT_CSS = """
    HorizontalSplitter {
        height: 1fr;
    }
    HorizontalSplitter > .split-handle {
        width: 1;
        background: $accent;
        text-style: bold;
        color: $text;
    }
    """

    dragging: reactive[bool] = reactive(False)
    ratio: reactive[float] = reactive(0.5)

    def on_mount(self) -> None:
        children = list(self.children)
        if len(children) != 2:
            raise RuntimeError("HorizontalSplitter requires exactly two children")
        self.left, self.right = children
        self.handle = Static("│", classes="split-handle")
        self.mount(self.handle, after=self.left)
        self.update_layout()

    def update_layout(self) -> None:
        left_width = int(self.ratio * 100)
        right_width = 100 - left_width
        self.left.styles.width = f"{left_width}%"
        self.right.styles.width = f"{right_width}%"
        self.refresh(layout=True)

    def on_mouse_down(self, event: events.MouseDown) -> None:
        if event.target is self.handle:
            self.dragging = True
            event.capture(self)
            event.stop()

    def on_mouse_up(self, event: events.MouseUp) -> None:
        if self.dragging:
            self.dragging = False
            event.stop()

    def on_mouse_move(self, event: events.MouseMove) -> None:
        if self.dragging:
            proportion = event.offset.x / self.size.width
            proportion = min(max(proportion, 0.1), 0.9)
            self.ratio = proportion
            self.update_layout()
            event.stop()
