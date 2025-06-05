import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import ipaddress
import subprocess
import platform
import threading
import socket
import time
import json
from datetime import datetime
from PIL import Image, ImageTk


# Function that pings an IP address
def ping_ip(ip):
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        result = subprocess.run(["ping", param, "1", str(ip)],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False


# Function that scans a range of IP addresses
def scan_network(ip_range, output_widget, button, progress_var):
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
    except ValueError:
        messagebox.showerror("Error", "Invalid IP range. Use format ex. 192.168.1.0/24")
        return

    output_widget.delete("1.0", tk.END)
    button.config(state=tk.DISABLED)
    results = []
    total = sum(1 for _ in network.hosts())
    done = 0

    def scan():
        nonlocal done
        for ip in network.hosts():
            active = ping_ip(ip)
            hostname = get_hostname(ip) if active else ""
            ports = scan_ports(ip) if active else []

            if active:
                result = {
                    "ip": str(ip),
                    "hostname": hostname,
                    "ports": ports
                }
                results.append(result)
                output_widget.insert(tk.END, f"[✓] Reachable: {ip} | {hostname} | Open ports: {ports}\n")
            else:
                output_widget.insert(tk.END, f"[ ] {ip} not reachable\n")

            done += 1
            progress_var.set((done / total) * 100)
            output_widget.see(tk.END)

        save_results(results)
        messagebox.showinfo("Scan Complete", "Results saved to JSON file.")
        button.config(state=tk.NORMAL)

    threading.Thread(target=scan, daemon=True).start()


# Function that scans a list of ports on a given IP address
def scan_ports(ip, ports=[22, 80, 443, 8080]):
    open_ports = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                if sock.connect_ex((str(ip), port)) == 0:
                    open_ports.append(port)
        except Exception:
            continue
    return open_ports


# Function that gets the hostname of a given IP address
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except Exception:
        return "Hostname not found"


# Function that scans a network and saves the results to a JSON file
def save_results(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)


# Function to show the loading screen
def show_loading_screen(root):
    # Set the loading screen background
    bg_img = Image.open("assets/logo.png").resize((600, 400))
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Add progress bar above the image
    progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=300)
    progress.place(relx=0.5, rely=0.8, anchor="center")
    progress.start()

    # Switch to the main GUI after 4 seconds
    def switch_to_main_gui():
        bg_label.destroy()
        progress.destroy()
        create_main_gui(root)

    root.after(4000, switch_to_main_gui)


# Function to create the main GUI
def create_main_gui(root):
    # Set the main GUI background
    bg_img = Image.open("assets/loading_background.png").resize((600, 400))
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Add widgets to the main GUI
    label_frame = tk.Frame(root, bg="#444444", padx=10, pady=5)
    label_frame.pack(pady=5)
    tk.Label(label_frame, text="Write an IP range (ex. 192.168.1.0):", bg="#444444", fg="white").pack()

    ip_entry = tk.Entry(root, width=30)
    ip_entry.pack()

    output = scrolledtext.ScrolledText(root, width=70, height=20)
    output.pack(pady=10)

    progress = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress, maximum=100)
    progress_bar.pack(pady=5)

    style = ttk.Style()
    style.configure("Blue.TButton", foreground="white", background="#007BFF", font=("Helvetica", 12, "bold"), borderwidth=0)
    scan_button = ttk.Button(root, text="Scan", style="Blue.TButton",
                              command=lambda: scan_network(ip_entry.get(), output, scan_button, progress))
    scan_button.pack()


# Main function to create the GUI
def create_gui():
    root = tk.Tk()
    root.title("Network Scanner")
    root.geometry("600x410")
    root.resizable(False, False)

    show_loading_screen(root)

    root.mainloop()


if __name__ == "__main__":
    create_gui()