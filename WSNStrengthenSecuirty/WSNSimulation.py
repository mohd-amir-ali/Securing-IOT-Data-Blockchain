import os
import time
import math
import random
import hashlib
import tkinter as tk
from tkinter import END, Canvas, Text, Scrollbar, Button, Frame, Label, Toplevel
from threading import Thread
from collections import defaultdict

# Optional matplotlib import (falls back to native Tkinter Canvas chart if not installed)
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except Exception:
    HAS_MATPLOTLIB = False

from blockchain_engine import bridge, ensure_local_rpc_server

# Aesthetic palette matching techwithamir.com
BG_CREAM = "#F6F3EC"
BG_SURFACE = "#FAF8F3"
INK_DARK = "#1D232A"
ACCENT_BURGUNDY = "#6E2634"
SLATE_MUTED = "#5C6268"
BORDER_WARM = "#DED9CE"
NODE_IDLE = "#1D232A"
NODE_ACTIVE = "#6E2634"
VERIFIED_GREEN = "#1F5E3B"

dct = defaultdict(list)
details = ""
transaction_time = []
simulation_status = False
canvas = None
text = None
status_label = None
iot_ovals = []
iot_labels = []
iot_x = []
iot_y = []


def readDetails(contract_type):
    global details
    details = bridge.read_details(contract_type)
    return details


def saveDataBlockChain(currentData, contract_type):
    global details
    receipt = bridge.save_data_blockchain(currentData, contract_type)
    details = bridge.read_details(contract_type)
    return receipt


def calculateDistance(iot_x_list, iot_y_list, x1, y1):
    for i in range(len(iot_x_list)):
        dist = math.sqrt((iot_x_list[i] - x1) ** 2 + (iot_y_list[i] - y1) ** 2)
        if dist < 60:
            return True
    return False


def startIOTDataGenerate(iot_x_list, iot_y_list, wsn_canvas, log_text):
    class IOTThread(Thread):
        def __init__(self, x_coords, y_coords, c_widget, t_widget):
            super().__init__(daemon=True)
            self.iot_x = x_coords
            self.iot_y = y_coords
            self.canvas = c_widget
            self.text = t_widget

        def run(self):
            global transaction_time, simulation_status
            while simulation_status:
                for i in range(len(self.iot_x)):
                    if not simulation_status:
                        break
                    current_time = time.strftime("%Y/%m/%d-%H:%M:%S")
                    sense = random.randint(15, 42)
                    dct[i].append(f"{sense},{current_time}")
                    sense_data = f"{i} {sense}"
                    h = hashlib.sha512(sense_data.encode("utf-8"))
                    hashcodes = h.hexdigest()
                    data = f"{i}#{sense}#{current_time}#{hashcodes}\n"

                    # Fixed timing calculation using perf_counter instead of timeit.timeit()
                    start_time = time.perf_counter()
                    receipt = saveDataBlockChain(data, "iotdata")
                    end_time = time.perf_counter()
                    elapsed = round(max(end_time - start_time, receipt.get("tx_time_sec", 0.0025)), 6)
                    transaction_time.append(elapsed)

                    log_line = (
                        f"[BLOCK #{receipt.get('block_number', '?')}] IOT-{i} | "
                        f"Temp: {sense}°C | Time: {current_time}\n"
                        f"  SHA512: {hashcodes[:36]}...\n"
                        f"  Tx Time: {elapsed:.6f}s | Status: VERIFIED\n\n"
                    )
                    try:
                        self.text.insert(END, log_line)
                        self.text.see(END)
                        if i < len(iot_ovals):
                            self.canvas.itemconfig(iot_ovals[i], fill=NODE_ACTIVE, outline=ACCENT_BURGUNDY)
                            self.canvas.itemconfig(iot_labels[i], fill=ACCENT_BURGUNDY, text=f"IOT-{i} ({sense}°C)")
                        if status_label:
                            status_label.config(
                                text=f"● LIVE TRANSMISSION: IOT-{i} → {sense}°C committed in {elapsed*1000:.2f} ms",
                                fg=ACCENT_BURGUNDY,
                            )
                    except Exception:
                        break

                    time.sleep(0.85)

                    try:
                        if i < len(iot_ovals):
                            self.canvas.itemconfig(iot_ovals[i], fill=NODE_IDLE, outline=INK_DARK)
                            self.canvas.itemconfig(iot_labels[i], fill=INK_DARK, text=f"IOT-{i}")
                    except Exception:
                        break

    newthread = IOTThread(iot_x_list, iot_y_list, wsn_canvas, log_text)
    newthread.start()


def drawGrid(wsn_canvas, width=720, height=620):
    wsn_canvas.delete("all")
    # Subtle dot grid matching techwithamir.com
    for gx in range(25, width, 30):
        for gy in range(25, height, 30):
            wsn_canvas.create_oval(gx, gy, gx + 2, gy + 2, fill="#D5CFC2", outline="")
    wsn_canvas.create_text(
        20, 20,
        anchor="w",
        fill=SLATE_MUTED,
        font=("Helvetica", 10, "bold"),
        text="01 / WIRELESS SENSOR NETWORK TOPOLOGY (20 EMBEDDED NODES → MDN GATEWAY)",
    )


def startSimulation():
    global canvas, text, simulation_status, iot_ovals, iot_labels, iot_x, iot_y
    if simulation_status:
        return
    simulation_status = True
    iot_ovals = []
    iot_labels = []
    iot_x = []
    iot_y = []

    drawGrid(canvas)
    nodes = bridge.get_dashboard_summary().get("nodes", [])

    for i in range(20):
        if i < len(nodes):
            x = int(nodes[i]["x"] * 0.88) + 20
            y = int(nodes[i]["y"] * 1.15) + 30
        else:
            x = random.randint(40, 620)
            y = random.randint(60, 540)
        iot_x.append(x)
        iot_y.append(y)
        oval_id = canvas.create_oval(x, y, x + 36, y + 36, fill=NODE_IDLE, outline=INK_DARK, width=2)
        lbl_id = canvas.create_text(
            x + 18, y - 10,
            fill=INK_DARK,
            font=("Helvetica", 10, "bold"),
            text=f"IOT-{i}",
        )
        canvas.create_text(
            x + 18, y + 18,
            fill=BG_CREAM,
            font=("Helvetica", 9, "bold"),
            text=str(i),
        )
        iot_ovals.append(oval_id)
        iot_labels.append(lbl_id)

    if status_label:
        status_label.config(text="● SIMULATION RUNNING — Mining SHA-512 sensor blocks to ledger...", fg=VERIFIED_GREEN)
    startIOTDataGenerate(iot_x, iot_y, canvas, text)


def stopSimulation():
    global simulation_status
    simulation_status = False
    if status_label:
        status_label.config(text="● SIMULATION PAUSED — Blockchain ledger state preserved.", fg=SLATE_MUTED)


def showNativeGraphWindow(times_data):
    """Fallback native Tkinter Canvas chart when matplotlib is not installed."""
    win = Toplevel()
    win.title("02 / Blockchain Transaction Processed Time Graph")
    win.geometry("760x480")
    win.configure(bg=BG_CREAM)

    Label(
        win,
        text="BLOCKCHAIN TRANSACTION TIME GRAPH",
        bg=BG_CREAM,
        fg=INK_DARK,
        font=("Helvetica", 16, "bold"),
    ).pack(pady=(18, 4))
    Label(
        win,
        text="Sense Number vs. Blockchain Commit Latency (seconds)",
        bg=BG_CREAM,
        fg=SLATE_MUTED,
        font=("Georgia", 11, "italic"),
    ).pack(pady=(0, 12))

    c = Canvas(win, width=680, height=340, bg=BG_SURFACE, highlightthickness=1, highlightbackground=BORDER_WARM)
    c.pack(padx=24, pady=10)

    pad_l, pad_r, pad_t, pad_b = 65, 30, 30, 45
    w, h = 680 - pad_l - pad_r, 340 - pad_t - pad_b

    # Axes
    c.create_line(pad_l, pad_t, pad_l, pad_t + h, fill=INK_DARK, width=2)
    c.create_line(pad_l, pad_t + h, pad_l + w, pad_t + h, fill=INK_DARK, width=2)

    if not times_data:
        times_data = bridge.get_dashboard_summary().get("transaction_times", [0.003, 0.004, 0.0035])

    max_v = max(times_data) * 1.15 if times_data else 0.01
    min_v = 0.0

    for step in range(5):
        y_pos = pad_t + h - (step / 4.0) * h
        val = min_v + (step / 4.0) * (max_v - min_v)
        c.create_line(pad_l, y_pos, pad_l + w, y_pos, fill="#E6E1D6", dash=(3, 3))
        c.create_text(pad_l - 8, y_pos, anchor="e", fill=SLATE_MUTED, font=("Helvetica", 9), text=f"{val:.4f}s")

    pts = []
    n = len(times_data)
    for idx, val in enumerate(times_data):
        x_pos = pad_l + (idx / max(n - 1, 1)) * w
        y_pos = pad_t + h - ((val - min_v) / max(max_v - min_v, 1e-6)) * h
        pts.extend([x_pos, y_pos])
        c.create_oval(x_pos - 4, y_pos - 4, x_pos + 4, y_pos + 4, fill=ACCENT_BURGUNDY, outline=BG_SURFACE)

    if len(pts) >= 4:
        c.create_line(*pts, fill=ACCENT_BURGUNDY, width=2.5)


def timeGraph():
    times_data = transaction_time if transaction_time else bridge.get_dashboard_summary().get("transaction_times", [])
    if HAS_MATPLOTLIB and times_data:
        plt.figure(figsize=(10, 6), facecolor=BG_CREAM)
        ax = plt.gca()
        ax.set_facecolor(BG_SURFACE)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.xlabel("Sense Number", fontweight="bold")
        plt.ylabel("Transaction Time (seconds)", fontweight="bold")
        plt.plot(times_data, color=ACCENT_BURGUNDY, marker="o", linewidth=2, label="Transaction Time (s)")
        plt.legend(loc="upper left")
        plt.title("Blockchain Transaction Time Graph (SHA-512 + Smart Contract Commit)", fontweight="bold")
        plt.tight_layout()
        plt.show()
    else:
        showNativeGraphWindow(times_data)


def Main():
    global canvas, text, status_label
    rpc_msg = ensure_local_rpc_server(9545)

    root = tk.Tk()
    root.geometry("1260x780")
    root.title("AMIR ALI — Securing IoT Data in the Cloud with Blockchain Technology (WSN Simulator)")
    root.configure(bg=BG_CREAM)
    root.resizable(True, True)

    # Top Editorial Header
    header = Frame(root, bg=BG_CREAM, highlightbackground=BORDER_WARM, highlightthickness=1)
    header.pack(fill="x", padx=24, pady=(16, 8))

    title_lbl = Label(
        header,
        text="aa↗  AMIR ALI   |   SECURING IOT DATA IN THE CLOUD WITH BLOCKCHAIN",
        bg=BG_CREAM,
        fg=INK_DARK,
        font=("Helvetica", 13, "bold"),
         padx=14,
        pady=10,
    )
    title_lbl.pack(side="left")

    rpc_lbl = Label(
        header,
        text=rpc_msg,
        bg=BG_CREAM,
        fg=VERIFIED_GREEN,
        font=("Courier", 10),
        padx=14,
    )
    rpc_lbl.pack(side="right")

    # Controls Bar
    ctrl_bar = Frame(root, bg=BG_CREAM)
    ctrl_bar.pack(fill="x", padx=24, pady=(4, 10))

    btn_font = ("Helvetica", 11, "bold")
    start_btn = Button(
        ctrl_bar,
        text="▶ Start WSN Simulation",
        command=startSimulation,
        font=btn_font,
        bg=ACCENT_BURGUNDY,
        fg="black",
        padx=14,
        pady=6,
    )
    start_btn.pack(side="left", padx=(0, 10))

    stop_btn = Button(
        ctrl_bar,
        text="■ Stop Simulation",
        command=stopSimulation,
        font=btn_font,
        bg=BG_SURFACE,
        fg=INK_DARK,
        padx=14,
        pady=6,
    )
    stop_btn.pack(side="left", padx=(0, 10))

    graph_btn = Button(
        ctrl_bar,
        text="📈 Transaction Processed Graph",
        command=timeGraph,
        font=btn_font,
        bg=BG_SURFACE,
        fg=INK_DARK,
        padx=14,
        pady=6,
    )
    graph_btn.pack(side="left", padx=(0, 16))

    status_label = Label(
        ctrl_bar,
        text="● READY — Click 'Start WSN Simulation' to broadcast SHA-512 sensor transactions.",
        bg=BG_CREAM,
        fg=SLATE_MUTED,
        font=("Helvetica", 11),
    )
    status_label.pack(side="left")

    # Main Split Body
    body = Frame(root, bg=BG_CREAM)
    body.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    canvas = Canvas(
        body,
        width=720,
        height=620,
        bg=BG_SURFACE,
        highlightthickness=1,
        highlightbackground=BORDER_WARM,
    )
    canvas.pack(side="left", fill="both", expand=False, padx=(0, 16))
    drawGrid(canvas)

    right_frame = Frame(body, bg=BG_SURFACE, highlightbackground=BORDER_WARM, highlightthickness=1)
    right_frame.pack(side="left", fill="both", expand=True)

    log_header = Label(
        right_frame,
        text="02 / LIVE BLOCKCHAIN TRANSACTION LEDGER STREAM (SHA-512)",
        bg=BG_SURFACE,
        fg=INK_DARK,
        font=("Helvetica", 10, "bold"),
        anchor="w",
        padx=12,
        pady=8,
    )
    log_header.pack(fill="x")

    scroll = Scrollbar(right_frame)
    scroll.pack(side="right", fill="y")

    text = Text(
        right_frame,
        height=32,
        width=58,
        bg=BG_SURFACE,
        fg=INK_DARK,
        font=("Courier", 11),
        padx=12,
        pady=8,
        relief="flat",
        yscrollcommand=scroll.set,
    )
    text.pack(side="left", fill="both", expand=True)
    scroll.config(command=text.yview)

    # Pre-populate recent blocks in log
    summary = bridge.get_dashboard_summary()
    text.insert(END, f"Connected Contract: {summary['contract_address']}\n")
    text.insert(END, f"Network ID: {summary['network_id']} | Total Mined Blocks: {summary['total_blocks']}\n")
    text.insert(END, "-" * 62 + "\n")

    root.mainloop()


if __name__ == "__main__":
    Main()
