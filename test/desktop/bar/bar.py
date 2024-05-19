import psutil
from loguru import logger
from fabric.widgets.wayland import Window
from fabric.widgets.button import Button
from fabric.widgets.revealer import Revealer
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.widgets.circular_progress_bar import CircularProgressBar
from fabric.utils.fabricator import Fabricator
from fabric.system_tray.widgets import SystemTray
from fabric.utils.helpers import invoke_repeater

from desktop.bar.dateWidget import DateWidget
from desktop.utils.helpers import applySCSS

class verticalBar(Window):
	def __init__(self, side="left"):
		super().__init__(
			name = f"sideBar-{side}",
			layer = "top",
			anchor = f"top {side} bottom",
			exclusive = True,
			visible = False,
			all_visible = False,
			# open_inspector = True,
		)

		self.dateTime = DateWidget(
			name = "Time",
			orientation = "v",
		)

		self.cpu_info = CircularProgressBar(
			size = (20, 20),
			name = "progress-bar",
			vexpand = True,
			hexpand = True,
		)
		self.memory_info = CircularProgressBar(
			size = (20, 20),
			name = "progress-bar",
			vexpand = True,
			hexpand = True,
		)
		self.battery_info = CircularProgressBar(
			size = (20, 20),
			name = "progress-bar",
			vexpand = True,
			hexpand = True,
		)
		# self.system_info_var = Fabricator(
		# 	value={"ram": 0, "cpu": 0, "battery": 69},
		# 	poll_from=lambda: {
		# 		"ram": str(int(psutil.virtual_memory().percent)),
		# 		"cpu": str(int(psutil.cpu_percent())),
		# 		"battery": str(
		# 			int(
		# 				psutil.sensors_battery().percent
		# 				if psutil.sensors_battery() is not None
		# 				else 42
		# 			)
		# 		),
		# 	},
		# 	interval=1000,
		# )
		# self.system_info_var.connect(
		# 	"changed",
		# 	self.updateProgressBar
		# )
		invoke_repeater(
			1000,
			self.updateProgressBar
		)

		self.sysTrayRevealed = False
		self.sysTray = Box(
			orientation = "v",
			children = [
				Revealer(
					# child_visible = False,
					# reveal_child = False,
					children = SystemTray(
						name = 'SystemTray',
						orientation = "v"
					),
				),
				Button(
					name = "RevealerToggle",
					child = Label(label = "")
				)
			]
		)
		for btn in self.sysTray.get_children():
			if type(btn) == Button and btn.get_name() == "RevealerToggle":
				btn.connect("button-press-event", self.toggleRevealer)

		self.centerBox = CenterBox(
			name = "VerticalBar",
			orientation = "v"
		)
		self.populateCB()

		self.add(self.centerBox)
		self.show_all()

	def updateProgressBar(self):
		self.cpu_info.percentage = int(psutil.cpu_percent())
		self.memory_info.percentage = int(psutil.virtual_memory().percent)
		self.battery_info.percentage = int(
			psutil.sensors_battery().percent
			if psutil.sensors_battery() is not None
			else 42
		)
		logger.info(f"[Bar] CPU percentage: {self.cpu_info.percentage}")
		logger.info(f"[Bar] memory percentage: {self.memory_info.percentage}")
		logger.info(f"[Bar] battery percentage: {self.battery_info.percentage}")
		logger.info("[Bar] Updated circular progress bar")
		return True

	def populateCB(self):
		self.centerBox.add_end(self.sysTray)
		self.centerBox.add_end(self.cpu_info)
		self.centerBox.add_end(self.memory_info)
		self.centerBox.add_end(self.battery_info)
		self.centerBox.add_end(self.dateTime)
		logger.info("[Bar] Added items to bar (CenterBox)")

	def toggleRevealer(self, button, event):
		if event.button == 1 and event.type == 4:
			self.sysTrayRevealed = not self.sysTrayRevealed
			for rvlr in self.sysTray.get_children():
				if type(rvlr) == Revealer:
					rvlr.set_reveal_child(self.sysTrayRevealed)
					rvlr.set_child_visible(self.sysTrayRevealed)
			logger.info(f"[Bar] Systray {'revealed' if self.sysTrayRevealed else 'Hidden'}")

def main():
	import fabric
	bar = verticalBar()
	applySCSS()
	fabric.start()

if __name__ == "__main__":
	main()
