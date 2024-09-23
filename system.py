import gi
import psutil
import platform
import socket
from gi.repository import Gtk, GLib
import cpuinfo

gi.require_version("Gtk", "4.0")


class SystemInfoWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("System Information")
        self.set_default_size(400, 300)
        
        self.set_resizable(False)

        grid = Gtk.Grid()
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        self.set_child(grid)

        self.info_label = Gtk.Label()
        grid.attach(self.info_label, 0, 0, 1, 1)

        self.update_info()
        GLib.timeout_add_seconds(5, self.update_info)

    def update_info(self):
        info = self.get_system_info()
        self.info_label.set_markup(info)
        return True

    def get_system_info(self):
        uname = platform.uname()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_if_addrs()
        cpu = psutil.cpu_percent(interval=1)

        info = (
            f"<b>System:</b> {uname.system}\n"
            f"<b>Node Name:</b> {uname.node}\n"
            f"<b>Release:</b> {uname.release}\n"
            f"<b>Version:</b> {uname.version}\n"
            f"<b>Machine:</b> {uname.machine}\n"
            f"<b>Processor Details:</b>\n"
        )

        cpu_info = cpuinfo.get_cpu_info()
        try:
            info += f"  Brand: {cpu_info['brand_raw']}\n"
        except KeyError:
            info += f"  Brand: Information unavailable\n"

        info += f"  Hz: {cpu_info['hz_advertised_friendly']}\n"
        info += f"  Cache (L1): {cpu_info['l1_data_cache_size']}\n"

        info += (
            f"<b>Memory:</b> {mem.total / (1024 ** 3):.2f} GB\n"
            f"<b>Disk Usage:</b> {disk.percent}%\n"
            f"<b>CPU Usage:</b> {cpu}%\n"
            f"<b>Network Interfaces:</b>\n"
        )

        for interface, addrs in net.items():
            info += f"  {interface}:\n"
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    info += f"    <b>IP Address:</b> {addr.address}\n"
                elif addr.family == socket.AF_PACKET:
                    info += f"    <b>MAC Address:</b> {addr.address}\n"

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
