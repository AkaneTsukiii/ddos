import tkinter as tk
from tkinter import ttk
import threading
import time
from tester import MinecraftCrashTester  # Đảm bảo file tester.py chứa class gốc bạn đã đưa

class MinecraftTesterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Server Crash Tester GUI")

        self.tester = None
        self.thread = None

        # Host
        tk.Label(root, text="Server IP:").grid(row=0, column=0, sticky="e")
        self.host_entry = tk.Entry(root)
        self.host_entry.grid(row=0, column=1)

        # Port
        tk.Label(root, text="Port:").grid(row=1, column=0, sticky="e")
        self.port_entry = tk.Entry(root)
        self.port_entry.insert(0, "25565")
        self.port_entry.grid(row=1, column=1)

        # Threads
        tk.Label(root, text="Threads:").grid(row=2, column=0, sticky="e")
        self.threads_entry = tk.Entry(root)
        self.threads_entry.insert(0, "200")
        self.threads_entry.grid(row=2, column=1)

        # Method
        tk.Label(root, text="Method:").grid(row=3, column=0, sticky="e")
        self.method_var = tk.StringVar()
        self.method_dropdown = ttk.Combobox(root, textvariable=self.method_var)
        self.method_dropdown['values'] = ['all', 'handshake_flood', 'ping_flood', 'invalid_data', 'oversized_packet', 'login_flood', 'legacy_exploit']
        self.method_dropdown.current(0)
        self.method_dropdown.grid(row=3, column=1)

        # Buttons
        self.start_button = tk.Button(root, text="Bắt đầu", command=self.start_attack)
        self.start_button.grid(row=4, column=0, pady=10)

        self.stop_button = tk.Button(root, text="Dừng", command=self.stop_attack, state='disabled')
        self.stop_button.grid(row=4, column=1)

        # Log
        self.log_label = tk.Label(root, text="Chưa chạy...", fg="gray")
        self.log_label.grid(row=5, column=0, columnspan=2)

        self.update_counter_loop()

    def start_attack(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        threads = int(self.threads_entry.get())
        method = self.method_var.get()

        self.tester = MinecraftCrashTester(host, port=port, threads=threads, method=method)
        self.tester.running = True

        self.thread = threading.Thread(target=self.tester.start)
        self.thread.start()

        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.log_label.config(text="Đang chạy...", fg="green")

    def stop_attack(self):
        if self.tester:
            self.tester.stop()
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.log_label.config(text="Đã dừng", fg="red")

    def update_counter_loop(self):
        if self.tester and self.tester.running:
            self.log_label.config(text=f"Đang gửi: {self.tester.counter} gói tin")
        self.root.after(1000, self.update_counter_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftTesterGUI(root)
    root.mainloop()
