from fabric import Application
from fabric.utils import get_relative_path, monitor_file
from loguru import logger

from desktop.windows import VerticalBar
from desktop.windows.workspacestrip import WorkspaceStrip

def main():
	bar = VerticalBar()
	workspaces = WorkspaceStrip()
	app = Application(
		"default",
		workspaces,
		bar,
	)

	app.run()

if __name__ == "__main__":
	main()
