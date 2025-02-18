from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow, WaylandWindowExclusivity

class VerticalBar(WaylandWindow):
	def __init__(self):
		self.bar_content = CenterBox(name = "Bar")
		self.bar_content.start_children = [ Label(label="hi") ]
		super().__init__(
			layer="top",
			anchor="top left bottom",
			exclusivity="auto",
			visible=True,
			child=self.bar_content,
		)
