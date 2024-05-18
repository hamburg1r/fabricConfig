import fabric, sys, psutil
from os.path import join, dirname
from desktop.bar.bar import verticalBar
from desktop.utils.helpers import applySCSS

def main():
	bar = verticalBar()
	applySCSS(file = join(dirname(__file__), 'assets', 'main.scss'))
	fabric.start()
