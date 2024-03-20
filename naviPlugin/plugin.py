#!/usr/bin/env python3

import subprocess
from gi.repository import Gtk, Xfce4Panel

def launch_mini_terminal(widget):
    subprocess.Popen(["xfce4-terminal", "--command=python3 /path/to/your/python_script.py"])

def main():
    plugin = Xfce4Panel.Plugin()
    button = Gtk.Button(label="Navi")
    button.connect("clicked", launch_mini_terminal)
    plugin.add(button)
    plugin.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
