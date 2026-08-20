import tkinter as tk
from tkinter import ttk
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
# MAIN WINDOW
# ==========================================================

window = tk.Tk()

window.title("CleanRoute AI")

window.geometry("620x720")

window.minsize(500, 500)


# ==========================================================
# DATA FILE
# ==========================================================

DATA_FILE = "reports.json"


# ==========================================================
# LOAD REPORTS
# ==========================================================

def load_reports():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


reports = load_reports()


# ==========================================================
# SAVE REPORTS
# ==========================================================

def save_reports():

    with open(DATA_FILE, "w") as file:
        json.dump(
            reports,
            file,
            indent=4
        )


# ==========================================================
# DISTANCE CALCULATION
# ==========================================================

def calculate_distance(lat1, lon1, lat2, lon2):

    earth_radius = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


# ==========================================================
# SCROLLABLE MAIN AREA
# ==========================================================

container = tk.Frame(window)

container.pack(
    fill="both",
    expand=True
)


canvas = tk.Canvas(
    container
)

scrollbar = ttk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)


scrollable_frame = tk.Frame(
    canvas
)


scrollable_frame.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)


canvas_window = canvas.create_window(
    (0, 0),
    window=scrollable_frame,
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
# MOUSE WHEEL
# ==========================================================

def scroll(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    scroll
)


# ==========================================================
# TITLE
# ==========================================================

title = tk.Label(
    scrollable_frame,
    text="🗑️ CleanRoute AI",
    font=("Arial", 24, "bold")
)

title.pack(
    pady=(20, 5)
)


description = tk.Label(
    scrollable_frame,
    text="Smart Garbage Priority & Route Management",
    font=("Arial", 12)
)

description.pack(
    pady=(0, 15)
)


# ==========================================================
# LOCATION
# ==========================================================

tk.Label(
    scrollable_frame,
    text="Garbage Location",
    font=("Arial", 12)
).pack(
    pady=(5, 3)
)


location_entry = tk.Entry(
    scrollable_frame,
    width=40,
    font=("Arial", 12)
)

location_entry.pack()


# ==========================================================
# LATITUDE
# ==========================================================

tk.Label(
    scrollable_frame,
    text="Latitude",
    font=("Arial", 12)
).pack(
    pady=(8, 3)
)


latitude_entry = tk.Entry(
    scrollable_frame,
    width=40,
    font=("Arial", 12)
)

latitude_entry.pack()


# ==========================================================
# LONGITUDE
# ==========================================================

tk.Label(
    scrollable_frame,
    text="Longitude",
    font=("Arial", 12)
).pack(
    pady=(8, 3)
)


longitude_entry = tk.Entry(
    scrollable_frame,
    width=40,
    font=("Arial", 12)
)

longitude_entry.pack()


# ==========================================================
# WASTE TYPE
# ==========================================================

tk.Label(
    scrollable_frame,
    text="Waste Type",
    font=("Arial", 12)
).pack(
    pady=(8, 3)
)


waste_dropdown = ttk.Combobox(
    scrollable_frame,
    values=[
        "Medical",
        "Hazardous",
        "Plastic",
        "Food",
        "General"
    ],
    state="readonly",
    width=37
)

waste_dropdown.pack()


# ==========================================================
# SEVERITY
# ==========================================================

tk.Label(
    scrollable_frame,
    text="Severity",
    font=("Arial", 12)
).pack(
    pady=(8, 3)
)


severity_dropdown = ttk.Combobox(
    scrollable_frame,
    values=[
        "Low",
        "Medium",
        "High"
    ],
    state="readonly",
    width=37
)

severity_dropdown.pack()


# ==========================================================
# LOCATION TYPE
# ==========================================================

tk.Label(
    scrollable_frame,
    text="Location Type",
    font=("Arial", 12)
).pack(
    pady=(8, 3)
)


location_type_dropdown = ttk.Combobox(
    scrollable_frame,
    values=[
        "Hospital",
        "School",
        "Market",
        "Residential",
        "Other"
    ],
    state="readonly",
    width=37
)

location_type_dropdown.pack()


# ==========================================================
# PREVIOUSLY REPORTED
# ==========================================================

tk.Label(
    scrollable_frame,
    text="Previously Reported?",
    font=("Arial", 12)
).pack(
    pady=(8, 3)
)


repeat_dropdown = ttk.Combobox(
    scrollable_frame,
    values=[
        "Yes",
        "No"
    ],
    state="readonly",
    width=37
)

repeat_dropdown.pack()


# ==========================================================
# RESULT LABEL
# ==========================================================

result_label = tk.Label(
    scrollable_frame,
    text="",
    font=("Arial", 12, "bold")
)

result_label.pack(
    pady=10
)


# ==========================================================
# SUBMIT REPORT
# ==========================================================

def submit_report():

    location = location_entry.get().strip()

    latitude_text = latitude_entry.get().strip()

    longitude_text = longitude_entry.get().strip()

    waste_type = waste_dropdown.get().lower()

    severity = severity_dropdown.get().lower()

    location_type = location_type_dropdown.get().lower()

    repeat_report = repeat_dropdown.get().lower()


    if location == "":

        result_label.config(
            text="⚠️ Please enter a garbage location."
        )

        return


    if (
        waste_type == ""
        or severity == ""
        or location_type == ""
        or repeat_report == ""
    ):

        result_label.config(
            text="⚠️ Please complete all fields."
        )

        return


    try:

        latitude = float(latitude_text)

        longitude = float(longitude_text)

    except ValueError:

        result_label.config(
            text="⚠️ Latitude and longitude must be numbers."
        )

        return


    if latitude < -90 or latitude > 90:

        result_label.config(
            text="⚠️ Latitude must be between -90 and 90."
        )

        return


    if longitude < -180 or longitude > 180:

        result_label.config(
            text="⚠️ Longitude must be between -180 and 180."
        )

        return


    # ======================================================
    # SCORE
    # ======================================================

    severity_score = calculate_priority(
        severity
    )

    location_score = calculate_location_score(
        location_type
    )

    waste_score = calculate_waste_score(
        waste_type
    )


    if repeat_report == "yes":
        repeat_score = 15
    else:
        repeat_score = 0


    priority_score = (
        severity_score
        + location_score
        + waste_score
        + repeat_score
    )


    if priority_score > 100:
        priority_score = 100


    priority = get_priority_level(
        priority_score
    )


    # ======================================================
    # REPORT ID
    # ======================================================

    report_id = (
        f"CR-{len(reports) + 1:03d}"
    )


    # ======================================================
    # TIMESTAMP
    # ======================================================

    timestamp = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )


    # ======================================================
    # REPORT
    # ======================================================

    report = {

        "report_id": report_id,

        "timestamp": timestamp,

        "location": location,

        "latitude": latitude,

        "longitude": longitude,

        "waste_type": waste_type,

        "severity": severity,

        "location_type": location_type,

        "repeat_report": repeat_report,

        "priority_score": priority_score,

        "priority": priority
    }


    reports.append(
        report
    )


    save_reports()


    result_label.config(
        text=(
            f"✅ Report submitted!\n"
            f"ID: {report_id}\n"
            f"Priority Score: {priority_score}\n"
            f"Priority: {priority}"
        )
    )


# ==========================================================
# COLLECTION QUEUE
# ==========================================================

def collection_queue():

    queue_window = tk.Toplevel(window)

    queue_window.title(
        "CleanRoute AI - Collection Queue"
    )

    queue_window.geometry(
        "850x550"
    )


    tk.Label(
        queue_window,
        text="🚛 Collection Queue",
        font=("Arial", 22, "bold")
    ).pack(
        pady=15
    )


    if not reports:

        tk.Label(
            queue_window,
            text="No reports available.",
            font=("Arial", 14)
        ).pack(
            pady=50
        )

        return


    queue = sorted(
        reports,
        key=lambda report: report["priority_score"],
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
        queue_window,
        columns=columns,
        show="headings"
    )


    for column in columns:

        table.heading(
            column,
            text=column
        )


    table.column(
        "Order",
        width=70
    )

    table.column(
        "ID",
        width=100
    )

    table.column(
        "Location",
        width=250
    )

    table.column(
        "Waste",
        width=120
    )

    table.column(
        "Score",
        width=80
    )

    table.column(
        "Priority",
        width=130
    )


    table.tag_configure(
        "high",
        background="#ffcccc"
    )

    table.tag_configure(
        "medium",
        background="#ffe5b4"
    )

    table.tag_configure(
        "low",
        background="#ccffcc"
    )


    for index, report in enumerate(
        queue,
        start=1
    ):

        priority = report["priority"]


        if priority.startswith("HIGH"):
            tag = "high"

        elif priority.startswith("MEDIUM"):
            tag = "medium"

        else:
            tag = "low"


        table.insert(
            "",
            tk.END,
            values=(
                index,
                report["report_id"],
                report["location"],
                report["waste_type"].capitalize(),
                report["priority_score"],
                priority
            ),
            tags=(tag,)
        )


    table.pack(
        padx=20,
        pady=15,
        fill="both",
        expand=True
    )


# ==========================================================
# OPTIMIZED ROUTE
# ==========================================================

def optimized_route():

    route_window = tk.Toplevel(window)

    route_window.title(
        "CleanRoute AI - Optimized Route"
    )

    route_window.geometry(
        "850x600"
    )


    tk.Label(
        route_window,
        text="🗺️ Optimized Collection Route",
        font=("Arial", 22, "bold")
    ).pack(
        pady=15
    )


    # Only reports with coordinates
    valid_reports = []

    for report in reports:

        if (
            "latitude" in report
            and "longitude" in report
        ):

            valid_reports.append(report)


    if not valid_reports:

        tk.Label(
            route_window,
            text=(
                "⚠️ No reports with coordinates found.\n\n"
                "Create a new report with latitude "
                "and longitude first."
            ),
            font=("Arial", 13)
        ).pack(
            pady=80
        )

        return


    # Highest priority first
    valid_reports.sort(
        key=lambda report: report["priority_score"],
        reverse=True
    )


    current = valid_reports[0]

    remaining = valid_reports[1:]

    route = [current]

    total_distance = 0


    # ======================================================
    # NEAREST NEIGHBOR ALGORITHM
    # ======================================================

    while remaining:

        nearest_report = None

        nearest_distance = float("inf")


        for report in remaining:

            distance = calculate_distance(

                float(current["latitude"]),

                float(current["longitude"]),

                float(report["latitude"]),

                float(report["longitude"])

            )


            if distance < nearest_distance:

                nearest_distance = distance

                nearest_report = report


        route.append(
            nearest_report
        )

        total_distance += nearest_distance

        current = nearest_report

        remaining.remove(
            nearest_report
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
        route_window,
        columns=columns,
        show="headings",
        height=16
    )


    for column in columns:

        table.heading(
            column,
            text=column
        )


    table.column(
        "Stop",
        width=70
    )

    table.column(
        "ID",
        width=100
    )

    table.column(
        "Location",
        width=250
    )

    table.column(
        "Priority",
        width=130
    )

    table.column(
        "Score",
        width=80
    )

    table.column(
        "Distance",
        width=100
    )


    table.tag_configure(
        "high",
        background="#ffcccc"
    )

    table.tag_configure(
        "medium",
        background="#ffe5b4"
    )

    table.tag_configure(
        "low",
        background="#ccffcc"
    )


    previous = None


    for index, report in enumerate(
        route,
        start=1
    ):

        distance_text = "START"


        if previous is not None:

            distance = calculate_distance(

                float(previous["latitude"]),

                float(previous["longitude"]),

                float(report["latitude"]),

                float(report["longitude"])

            )


            distance_text = (
                f"{distance:.2f} km"
            )


        priority = report["priority"]


        if priority.startswith("HIGH"):
            tag = "high"

        elif priority.startswith("MEDIUM"):
            tag = "medium"

        else:
            tag = "low"


        table.insert(
            "",
            tk.END,
            values=(
                index,
                report["report_id"],
                report["location"],
                priority,
                report["priority_score"],
                distance_text
            ),
            tags=(tag,)
        )


        previous = report


    table.pack(
        padx=20,
        pady=15,
        fill="both",
        expand=True
    )


    tk.Label(
        route_window,
        text=(
            f"🚛 Estimated route distance: "
            f"{total_distance:.2f} km"
        ),
        font=("Arial", 14, "bold")
    ).pack(
        pady=15
    )


# ==========================================================
# VIEW REPORTS
# ==========================================================

def view_reports():

    dashboard = tk.Toplevel(window)

    dashboard.title(
        "CleanRoute AI - Report Dashboard"
    )

    dashboard.geometry(
        "1000x650"
    )


    tk.Label(
        dashboard,
        text="📊 Report Dashboard",
        font=("Arial", 20, "bold")
    ).pack(
        pady=15
    )


    columns = (
        "ID",
        "Location",
        "Waste",
        "Severity",
        "Score",
        "Priority"
    )


    table = ttk.Treeview(
        dashboard,
        columns=columns,
        show="headings"
    )


    for column in columns:

        table.heading(
            column,
            text=column
        )


    table.column("ID", width=100)
    table.column("Location", width=250)
    table.column("Waste", width=120)
    table.column("Severity", width=100)
    table.column("Score", width=80)
    table.column("Priority", width=130)


    table.tag_configure(
        "high",
        background="#ffcccc"
    )

    table.tag_configure(
        "medium",
        background="#ffe5b4"
    )

    table.tag_configure(
        "low",
        background="#ccffcc"
    )


    for report in sorted(
        reports,
        key=lambda r: r["priority_score"],
        reverse=True
    ):

        priority = report["priority"]


        if priority.startswith("HIGH"):
            tag = "high"

        elif priority.startswith("MEDIUM"):
            tag = "medium"

        else:
            tag = "low"


        table.insert(
            "",
            tk.END,
            values=(
                report["report_id"],
                report["location"],
                report["waste_type"].capitalize(),
                report["severity"].capitalize(),
                report["priority_score"],
                priority
            ),
            tags=(tag,)
        )


    table.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )


# ==========================================================
# BUTTONS
# ==========================================================

tk.Button(
    scrollable_frame,
    text="SUBMIT REPORT",
    command=submit_report,
    font=("Arial", 12, "bold"),
    width=25
).pack(
    pady=8
)


tk.Button(
    scrollable_frame,
    text="VIEW REPORTS",
    command=view_reports,
    font=("Arial", 11, "bold"),
    width=25
).pack(
    pady=5
)


tk.Button(
    scrollable_frame,
    text="🚛 COLLECTION QUEUE",
    command=collection_queue,
    font=("Arial", 11, "bold"),
    width=25
).pack(
    pady=5
)


tk.Button(
    scrollable_frame,
    text="🗺️ OPTIMIZED ROUTE",
    command=optimized_route,
    font=("Arial", 11, "bold"),
    width=25
).pack(
    pady=5
)


# ==========================================================
# START APPLICATION
# ==========================================================

window.mainloop()