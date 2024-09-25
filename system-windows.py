import psutil
import platform
import socket
import cpuinfo
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont


class SystemInfoWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("System Information Beta")
        self.geometry("400x300")
        self.resizable(False, False)

        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=int(self.default_font.actual('size') * 1.25))

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_label = ttk.Label(self.scrollable_frame, justify="left", anchor="nw")
        self.info_label.pack(padx=10, pady=10, fill="both", expand=True)

        self.update_info()
        self.after(2000, self.update_info)

    def update_info(self):
        info = self.get_system_info()
        self.info_label.config(text=info)

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
            f"Processor Details:\n"
        )

        cpu_info = cpuinfo.get_cpu_info()
        info += f"  Brand: {cpu_info.get('brand_raw', 'Information unavailable')}\n"
        info += f"  Hz: {cpu_info.get('hz_advertised_friendly', 'Information unavailable')}\n"
        info += f"  Cache (L1): {cpu_info.get('l1_data_cache_size', 'Information unavailable')}\n"

        info += (
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

        return info


if __name__ == "__main__":
    app = SystemInfoWindow()
    app.mainloop()
