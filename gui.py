import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import math

from main import (
    calculate_priority,
    calculate_location_score,
    calculate_waste_score,
    get_priority_level
)


# ==========================================================
# DATA
# ==========================================================

DATA_FILE = "reports.json"


def load_reports():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_reports():
    with open(DATA_FILE, "w") as file:
        json.dump(reports, file, indent=4)


reports = load_reports()


# ==========================================================
# DISTANCE
# ==========================================================

def calculate_distance(lat1, lon1, lat2, lon2):

    radius = 6371

    lat1, lon1, lat2, lon2 = map(
        math.radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return radius * 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )


# ==========================================================
# COLORS
# ==========================================================

BG = "#F4F7F5"
WHITE = "#FFFFFF"
GREEN = "#2E7D32"
DARK_GREEN = "#174A2B"
LIGHT_GREEN = "#E8F5E9"
TEXT = "#263238"
MUTED = "#607D8B"


# ==========================================================
# MAIN WINDOW
# ==========================================================

window = tk.Tk()
window.title("CleanRoute AI")
window.geometry("850x760")
window.minsize(750, 650)
window.configure(bg=BG)


# ==========================================================
# STYLE
# ==========================================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    padding=7,
    font=("Arial", 10)
)

style.configure(
    "Treeview",
    rowheight=32,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)


# ==========================================================
# HEADER
# ==========================================================

header = tk.Frame(
    window,
    bg=DARK_GREEN,
    height=105
)

header.pack(fill="x")
header.pack_propagate(False)


title_frame = tk.Frame(
    header,
    bg=DARK_GREEN
)

title_frame.pack(
    side="left",
    padx=30,
    pady=18
)


tk.Label(
    title_frame,
    text="🗑️ CleanRoute AI",
    font=("Arial", 25, "bold"),
    bg=DARK_GREEN,
    fg=WHITE
).pack(anchor="w")


tk.Label(
    title_frame,
    text="Smart Waste Management & Route Optimization",
    font=("Arial", 10),
    bg=DARK_GREEN,
    fg="#C8E6C9"
).pack(anchor="w")


status = tk.Frame(
    header,
    bg="#245F38",
    padx=12,
    pady=7
)

status.pack(
    side="right",
    padx=30
)


tk.Label(
    status,
    text="● SYSTEM ONLINE",
    font=("Arial", 10, "bold"),
    bg="#245F38",
    fg="#A5D6A7"
).pack()


# ==========================================================
# SCROLLABLE CONTENT
# ==========================================================

outer = tk.Frame(
    window,
    bg=BG
)

outer.pack(
    fill="both",
    expand=True
)


canvas = tk.Canvas(
    outer,
    bg=BG,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    outer,
    orient="vertical",
    command=canvas.yview
)

content = tk.Frame(
    canvas,
    bg=BG
)


content.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)


canvas.create_window(
    (0, 0),
    window=content,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ==========================================================
# STATISTICS
# ==========================================================

stats = tk.Frame(
    content,
    bg=BG
)

stats.pack(
    fill="x",
    padx=25,
    pady=20
)


def stat_card(parent, title, value, icon):

    card = tk.Frame(
        parent,
        bg=WHITE,
        padx=18,
        pady=12,
        highlightbackground="#DDE5DF",
        highlightthickness=1
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    tk.Label(
        card,
        text=icon,
        font=("Arial", 20),
        bg=WHITE
    ).pack(anchor="w")

    tk.Label(
        card,
        text=value,
        font=("Arial", 20, "bold"),
        bg=WHITE,
        fg=DARK_GREEN
    ).pack(anchor="w")

    tk.Label(
        card,
        text=title,
        font=("Arial", 9),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w")


high_count = sum(
    r.get("priority", "").startswith("HIGH")
    for r in reports
)


stat_card(
    stats,
    "Total Reports",
    str(len(reports)),
    "📋"
)

stat_card(
    stats,
    "High Priority",
    str(high_count),
    "🔴"
)

stat_card(
    stats,
    "Locations",
    str(len({
        r.get("location")
        for r in reports
    })),
    "📍"
)


# ==========================================================
# REPORT CARD
# ==========================================================

report_card = tk.Frame(
    content,
    bg=WHITE,
    padx=30,
    pady=22,
    highlightbackground="#DDE5DF",
    highlightthickness=1
)

report_card.pack(
    fill="x",
    padx=30,
    pady=5
)


tk.Label(
    report_card,
    text="📍 Report New Garbage Issue",
    font=("Arial", 17, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="w",
    pady=(0, 18)
)


report_card.columnconfigure(0, weight=1)
report_card.columnconfigure(1, weight=1)


def add_label(text, row, col):

    tk.Label(
        report_card,
        text=text,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).grid(
        row=row,
        column=col,
        sticky="w",
        padx=8,
        pady=(5, 4)
    )


def add_entry(row, col, width=30):

    box = tk.Entry(
        report_card,
        width=width,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    box.grid(
        row=row,
        column=col,
        sticky="ew",
        padx=8,
        pady=(0, 8)
    )

    return box


def add_combo(values, row, col):

    box = ttk.Combobox(
        report_card,
        values=values,
        state="readonly",
        width=27
    )

    box.grid(
        row=row,
        column=col,
        sticky="ew",
        padx=8,
        pady=(0, 8)
    )

    return box


# ==========================================================
# FORM
# ==========================================================

add_label(
    "Garbage Location",
    1,
    0
)

location_entry = add_entry(
    2,
    0,
    65
)


add_label(
    "Latitude",
    3,
    0
)

add_label(
    "Longitude",
    3,
    1
)

latitude_entry = add_entry(
    4,
    0
)

longitude_entry = add_entry(
    4,
    1
)


add_label(
    "Waste Type",
    5,
    0
)

add_label(
    "Severity",
    5,
    1
)

waste_dropdown = add_combo(
    [
        "Medical",
        "Hazardous",
        "Plastic",
        "Food",
        "General"
    ],
    6,
    0
)

severity_dropdown = add_combo(
    [
        "Low",
        "Medium",
        "High"
    ],
    6,
    1
)


add_label(
    "Location Type",
    7,
    0
)

add_label(
    "Previously Reported",
    7,
    1
)

location_type_dropdown = add_combo(
    [
        "Hospital",
        "School",
        "Market",
        "Residential",
        "Other"
    ],
    8,
    0
)

repeat_dropdown = add_combo(
    [
        "Yes",
        "No"
    ],
    8,
    1
)


# ==========================================================
# SUBMIT
# ==========================================================

result_label = tk.Label(
    report_card,
    text="",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=GREEN
)

result_label.grid(
    row=10,
    column=0,
    columnspan=2,
    pady=5
)


def submit_report():

    location = location_entry.get().strip()
    waste_type = waste_dropdown.get().lower()
    severity = severity_dropdown.get().lower()
    location_type = location_type_dropdown.get().lower()
    repeat_report = repeat_dropdown.get().lower()

    try:
        latitude = float(latitude_entry.get())
        longitude = float(longitude_entry.get())
    except ValueError:
        result_label.config(
            text="⚠️ Enter valid latitude and longitude."
        )
        return

    if not location:
        result_label.config(
            text="⚠️ Please enter a garbage location."
        )
        return

    if not all([
        waste_type,
        severity,
        location_type,
        repeat_report
    ]):
        result_label.config(
            text="⚠️ Please complete all fields."
        )
        return

    if not -90 <= latitude <= 90:
        result_label.config(
            text="⚠️ Latitude must be between -90 and 90."
        )
        return

    if not -180 <= longitude <= 180:
        result_label.config(
            text="⚠️ Longitude must be between -180 and 180."
        )
        return

    repeat_score = 15 if repeat_report == "yes" else 0

    score = (
        calculate_priority(severity)
        + calculate_location_score(location_type)
        + calculate_waste_score(waste_type)
        + repeat_score
    )

    score = min(score, 100)

    priority = get_priority_level(score)

    report = {
        "report_id": f"CR-{len(reports) + 1:03d}",
        "timestamp": datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        ),
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "waste_type": waste_type,
        "severity": severity,
        "location_type": location_type,
        "repeat_report": repeat_report,
        "priority_score": score,
        "priority": priority
    }

    reports.append(report)
    save_reports()

    result_label.config(
        text=(
            f"✓ {report['report_id']} submitted  •  "
            f"Score: {score}  •  {priority}"
        )
    )

    location_entry.delete(0, tk.END)
    latitude_entry.delete(0, tk.END)
    longitude_entry.delete(0, tk.END)

    for box in [
        waste_dropdown,
        severity_dropdown,
        location_type_dropdown,
        repeat_dropdown
    ]:
        box.set("")


tk.Button(
    report_card,
    text="🚨  SUBMIT GARBAGE REPORT",
    command=submit_report,
    font=("Arial", 11, "bold"),
    bg=GREEN,
    fg=WHITE,
    activebackground=DARK_GREEN,
    activeforeground=WHITE,
    relief="flat",
    padx=20,
    pady=11,
    cursor="hand2"
).grid(
    row=9,
    column=0,
    columnspan=2,
    pady=10
)


# ==========================================================
# DASHBOARD
# ==========================================================

def view_reports():

    win = tk.Toplevel(window)
    win.title("CleanRoute AI • Dashboard")
    win.geometry("1000x600")

    tk.Label(
        win,
        text="📊 Report Dashboard",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    columns = (
        "ID",
        "Location",
        "Waste",
        "Severity",
        "Score",
        "Priority"
    )

    table = ttk.Treeview(
        win,
        columns=columns,
        show="headings"
    )

    for col in columns:
        table.heading(col, text=col)

    table.column(
        "Location",
        width=260
    )

    for report in sorted(
        reports,
        key=lambda x: x["priority_score"],
        reverse=True
    ):
        table.insert(
            "",
            tk.END,
            values=(
                report["report_id"],
                report["location"],
                report["waste_type"].capitalize(),
                report["severity"].capitalize(),
                report["priority_score"],
                report["priority"]
            )
        )

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


# ==========================================================
# COLLECTION QUEUE
# ==========================================================

def collection_queue():

    win = tk.Toplevel(window)
    win.title("CleanRoute AI • Collection Queue")
    win.geometry("900x600")

    tk.Label(
        win,
        text="🚛 Collection Queue",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    queue = sorted(
        reports,
        key=lambda x: x["priority_score"],
        reverse=True
    )

    columns = (
        "Order",
        "ID",
        "Location",
        "Waste",
        "Score",
        "Priority"
    )

    table = ttk.Treeview(
        win,
        columns=columns,
        show="headings"
    )

    for col in columns:
        table.heading(col, text=col)

    table.column(
        "Location",
        width=270
    )

    for index, report in enumerate(queue, 1):

        table.insert(
            "",
            tk.END,
            values=(
                index,
                report["report_id"],
                report["location"],
                report["waste_type"].capitalize(),
                report["priority_score"],
                report["priority"]
            )
        )

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


# ==========================================================
# OPTIMIZED ROUTE
# ==========================================================

def optimized_route():

    valid = [
        r for r in reports
        if "latitude" in r
        and "longitude" in r
    ]

    if not valid:
        messagebox.showinfo(
            "No Route",
            "No reports with coordinates available."
        )
        return

    # Highest-priority report becomes starting point
    current = max(
        valid,
        key=lambda r: r["priority_score"]
    )

    remaining = [
        r for r in valid
        if r != current
    ]

    route = [current]
    total_distance = 0

    while remaining:

        def route_score(report):

            distance = calculate_distance(
                float(current["latitude"]),
                float(current["longitude"]),
                float(report["latitude"]),
                float(report["longitude"])
            )

            priority = report["priority_score"]

            # Balance urgency and travel distance
            return (priority * 2) - (distance * 5)

        next_stop = max(
            remaining,
            key=route_score
        )

        distance = calculate_distance(
            float(current["latitude"]),
            float(current["longitude"]),
            float(next_stop["latitude"]),
            float(next_stop["longitude"])
        )

        total_distance += distance

        route.append(next_stop)

        remaining.remove(next_stop)

        current = next_stop

    # ======================================================
    # ROUTE WINDOW
    # ======================================================

    win = tk.Toplevel(window)
    win.title("CleanRoute AI • Optimized Route")
    win.geometry("950x700")
    win.configure(bg=BG)

    tk.Label(
        win,
        text="🗺️ Optimized Collection Route",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=DARK_GREEN
    ).pack(pady=(20, 5))

    tk.Label(
        win,
        text=(
            f"🚛 {len(route)} stops   •   "
            f"📏 {total_distance:.2f} km total distance"
        ),
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=MUTED
    ).pack(pady=(0, 15))

    # ======================================================
    # VISUAL ROUTE
    # ======================================================

    route_box = tk.Frame(
        win,
        bg=WHITE,
        padx=20,
        pady=15,
        highlightbackground="#DDE5DF",
        highlightthickness=1
    )

    route_box.pack(
        fill="x",
        padx=30,
        pady=10
    )

    for index, report in enumerate(route):

        priority = report["priority"]

        if priority.startswith("HIGH"):
            icon = "🔴"
        elif priority.startswith("MEDIUM"):
            icon = "🟠"
        else:
            icon = "🟢"

        prefix = (
            "START →"
            if index == 0
            else "↓"
        )

        tk.Label(
            route_box,
            text=(
                f"{prefix} {icon} "
                f"{report['report_id']}  "
                f"{report['location']}  "
                f"({report['priority_score']})"
            ),
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=TEXT,
            anchor="w"
        ).pack(
            fill="x",
            pady=4
        )

    # ======================================================
    # ROUTE TABLE
    # ======================================================

    columns = (
        "Stop",
        "ID",
        "Location",
        "Priority",
        "Score",
        "Distance"
    )

    table = ttk.Treeview(
        win,
        columns=columns,
        show="headings"
    )

    for col in columns:
        table.heading(
            col,
            text=col
        )

    table.column(
        "Stop",
        width=60
    )

    table.column(
        "ID",
        width=80
    )

    table.column(
        "Location",
        width=280
    )

    table.column(
        "Priority",
        width=100
    )

    table.column(
        "Score",
        width=70
    )

    table.column(
        "Distance",
        width=100
    )

    previous = None

    for index, report in enumerate(route, 1):

        distance_text = "START"

        if previous:

            distance = calculate_distance(
                float(previous["latitude"]),
                float(previous["longitude"]),
                float(report["latitude"]),
                float(report["longitude"])
            )

            distance_text = f"{distance:.2f} km"

        table.insert(
            "",
            tk.END,
            values=(
                index,
                report["report_id"],
                report["location"],
                report["priority"],
                report["priority_score"],
                distance_text
            )
        )

        previous = report

    table.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=15
    )


# ==========================================================
# NAVIGATION
# ==========================================================

nav = tk.Frame(
    content,
    bg=BG
)

nav.pack(
    fill="x",
    padx=30,
    pady=20
)

nav.columnconfigure(0, weight=1)
nav.columnconfigure(1, weight=1)
nav.columnconfigure(2, weight=1)


def nav_button(text, command):

    return tk.Button(
        nav,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=DARK_GREEN,
        activebackground=LIGHT_GREEN,
        relief="solid",
        bd=1,
        padx=15,
        pady=10,
        cursor="hand2"
    )


nav_button(
    "📊 Dashboard",
    view_reports
).grid(
    row=0,
    column=0,
    sticky="ew",
    padx=5
)


nav_button(
    "🚛 Collection Queue",
    collection_queue
).grid(
    row=0,
    column=1,
    sticky="ew",
    padx=5
)


nav_button(
    "🗺️ Optimize Route",
    optimized_route
).grid(
    row=0,
    column=2,
    sticky="ew",
    padx=5
)


# ==========================================================
# FOOTER
# ==========================================================

tk.Label(
    content,
    text="CleanRoute AI • Smart • Efficient • Sustainable",
    font=("Arial", 9),
    bg=BG,
    fg=MUTED
).pack(
    pady=(0, 15)
)


# ==========================================================
# START
# ==========================================================

window.mainloop()