import gi
import psutil
import platform
import socket
from gi.repository import Gtk, GLib

gi.require_version("Gtk", "4.0")

class SystemInfoWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("System Information")
        self.set_default_size(400, 300)

        grid = Gtk.Grid()
        self.set_child(grid)

        self.info_label = Gtk.Label()
        grid.attach(self.info_label, 0, 0, 1, 1)

        self.update_info()
        GLib.timeout_add_seconds(5, self.update_info)

    def update_info(self):
        info = self.get_system_info()
        self.info_label.set_text(info)
        return True

    def get_system_info(self):
        uname = platform.uname()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_if_addrs()
        cpu = psutil.cpu_percent(interval=1)

        info = (
            f"System: {uname.system}\n"
            f"Node Name: {uname.node}\n"
            f"Release: {uname.release}\n"
            f"Version: {uname.version}\n"
            f"Machine: {uname.machine}\n"
            f"Processor: {uname.processor}\n"
            f"Memory: {mem.total / (1024 ** 3):.2f} GB\n"
            f"Disk Usage: {disk.percent}%\n"
            f"CPU Usage: {cpu}%\n"
            f"Network Interfaces:\n"
        )

        for interface, addrs in net.items():
            info += f"  {interface}:\n"
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    info += f"    IP Address: {addr.address}\n"
                elif addr.family == socket.AF_PACKET:
                    info += f"    MAC Address: {addr.address}\n"

        return info

class SystemInfoApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.systeminfo")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        win = SystemInfoWindow(self)
        win.present()

app = SystemInfoApp()
app.run(None)
