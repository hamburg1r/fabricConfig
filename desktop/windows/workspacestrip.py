from fabric.widgets.button import Button
from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow

class WorkspaceStrip(WaylandWindow):
	def __init__(self):
		self.workspaces : Box = Box(
			name="workspaces",
			# v_expand=True,
			h_expand=True,
		)
		self.workspaces.children = [
			Button(h_expand=True,) for i in range(5)
		]
		super().__init__(
			layer="top",
			anchor="left top right",
			exclusivity="auto",
			visible=True,
			child = self.workspaces,
		)
