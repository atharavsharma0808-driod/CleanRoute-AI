import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os

from main import (
    calculate_priority,
    calculate_location_score,
    calculate_waste_score,
    get_priority_level
)


# ==============================
# CREATE MAIN WINDOW
# ==============================

window = tk.Tk()

window.title("CleanRoute AI")

window.geometry("600x750")

window.resizable(False, False)


# ==============================
# DATA FILE
# ==============================

DATA_FILE = "reports.json"


# ==============================
# LOAD REPORTS
# ==============================

def load_reports():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


reports = load_reports()


# ==============================
# SAVE REPORTS
# ==============================

def save_reports():

    with open(DATA_FILE, "w") as file:

        json.dump(
            reports,
            file,
            indent=4
        )


# ==============================
# TITLE
# ==============================

title = tk.Label(
    window,
    text="🗑️ CleanRoute AI",
    font=("Arial", 24, "bold")
)

title.pack(pady=25)


description = tk.Label(
    window,
    text="Smart Garbage Priority & Route Management",
    font=("Arial", 12)
)

description.pack()


# ==============================
# LOCATION
# ==============================

location_label = tk.Label(
    window,
    text="Garbage Location",
    font=("Arial", 12)
)

location_label.pack(pady=(25, 5))


location_entry = tk.Entry(
    window,
    width=40,
    font=("Arial", 12)
)

location_entry.pack()


# ==============================
# WASTE TYPE
# ==============================

waste_label = tk.Label(
    window,
    text="Waste Type",
    font=("Arial", 12)
)

waste_label.pack(pady=(15, 5))


waste_dropdown = ttk.Combobox(
    window,
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


# ==============================
# SEVERITY
# ==============================

severity_label = tk.Label(
    window,
    text="Severity",
    font=("Arial", 12)
)

severity_label.pack(pady=(15, 5))


severity_dropdown = ttk.Combobox(
    window,
    values=[
        "Low",
        "Medium",
        "High"
    ],
    state="readonly",
    width=37
)

severity_dropdown.pack()


# ==============================
# LOCATION TYPE
# ==============================

location_type_label = tk.Label(
    window,
    text="Location Type",
    font=("Arial", 12)
)

location_type_label.pack(pady=(15, 5))


location_type_dropdown = ttk.Combobox(
    window,
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


# ==============================
# PREVIOUSLY REPORTED
# ==============================

repeat_label = tk.Label(
    window,
    text="Previously Reported?",
    font=("Arial", 12)
)

repeat_label.pack(pady=(15, 5))


repeat_dropdown = ttk.Combobox(
    window,
    values=[
        "Yes",
        "No"
    ],
    state="readonly",
    width=37
)

repeat_dropdown.pack()


# ==========================================================
# VIEW REPORT DASHBOARD
# ==========================================================

def view_reports():

    dashboard = tk.Toplevel(window)

    dashboard.title(
        "CleanRoute AI - Report Dashboard"
    )

    dashboard.geometry(
        "1000x650"
    )


    # ==============================
    # TITLE
    # ==============================

    dashboard_title = tk.Label(
        dashboard,
        text="📊 Report Dashboard",
        font=("Arial", 20, "bold")
    )

    dashboard_title.pack(
        pady=(15, 5)
    )


    # ==============================
    # SEARCH FRAME
    # ==============================

    filter_frame = tk.Frame(
        dashboard
    )

    filter_frame.pack(
        pady=10
    )


    search_label = tk.Label(
        filter_frame,
        text="Search Location:"
    )

    search_label.grid(
        row=0,
        column=0,
        padx=5
    )


    search_entry = tk.Entry(
        filter_frame,
        width=25
    )

    search_entry.grid(
        row=0,
        column=1,
        padx=5
    )


    priority_label = tk.Label(
        filter_frame,
        text="Priority:"
    )

    priority_label.grid(
        row=0,
        column=2,
        padx=5
    )


    priority_filter = ttk.Combobox(
        filter_frame,
        values=[
            "All",
            "HIGH",
            "MEDIUM",
            "LOW"
        ],
        state="readonly",
        width=12
    )

    priority_filter.set("All")

    priority_filter.grid(
        row=0,
        column=3,
        padx=5
    )


    # ==============================
    # STATISTICS
    # ==============================

    stats_frame = tk.Frame(
        dashboard
    )

    stats_frame.pack(
        pady=10
    )


    total_label = tk.Label(
        stats_frame,
        text="Total Reports: 0",
        font=("Arial", 12, "bold")
    )

    total_label.grid(
        row=0,
        column=0,
        padx=20
    )


    high_label = tk.Label(
        stats_frame,
        text="🔴 HIGH: 0",
        font=("Arial", 12, "bold")
    )

    high_label.grid(
        row=0,
        column=1,
        padx=20
    )


    medium_label = tk.Label(
        stats_frame,
        text="🟠 MEDIUM: 0",
        font=("Arial", 12, "bold")
    )

    medium_label.grid(
        row=0,
        column=2,
        padx=20
    )


    low_label = tk.Label(
        stats_frame,
        text="🟢 LOW: 0",
        font=("Arial", 12, "bold")
    )

    low_label.grid(
        row=0,
        column=3,
        padx=20
    )


    # ==============================
    # TABLE
    # ==============================

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
        show="headings",
        height=15
    )


    table.heading(
        "ID",
        text="Report ID"
    )

    table.heading(
        "Location",
        text="Location"
    )

    table.heading(
        "Waste",
        text="Waste Type"
    )

    table.heading(
        "Severity",
        text="Severity"
    )

    table.heading(
        "Score",
        text="Score"
    )

    table.heading(
        "Priority",
        text="Priority"
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
        "Severity",
        width=100
    )

    table.column(
        "Score",
        width=80
    )

    table.column(
        "Priority",
        width=130
    )


    # ==============================
    # PRIORITY COLORS
    # ==============================

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


    # ==========================================================
    # UPDATE TABLE
    # ==========================================================

    def update_table():

        # Remove old rows
        for item in table.get_children():

            table.delete(item)


        search_text = (
            search_entry
            .get()
            .strip()
            .lower()
        )


        selected_priority = (
            priority_filter.get()
        )


        filtered_reports = []


        for report in reports:

            location_matches = (
                search_text
                in report["location"].lower()
            )


            if selected_priority == "All":

                priority_matches = True

            else:

                priority_matches = report[
                    "priority"
                ].startswith(
                    selected_priority
                )


            if (
                location_matches
                and priority_matches
            ):

                filtered_reports.append(
                    report
                )


        # Sort by score
        filtered_reports.sort(
            key=lambda report: report["priority_score"],
            reverse=True
        )


        # ==============================
        # STATISTICS
        # ==============================

        total_reports = len(
            filtered_reports
        )

        high_reports = 0
        medium_reports = 0
        low_reports = 0


        for report in filtered_reports:

            if report["priority"].startswith("HIGH"):

                high_reports += 1

            elif report["priority"].startswith("MEDIUM"):

                medium_reports += 1

            elif report["priority"].startswith("LOW"):

                low_reports += 1


        total_label.config(
            text=f"Total Reports: {total_reports}"
        )

        high_label.config(
            text=f"🔴 HIGH: {high_reports}"
        )

        medium_label.config(
            text=f"🟠 MEDIUM: {medium_reports}"
        )

        low_label.config(
            text=f"🟢 LOW: {low_reports}"
        )


        # ==============================
        # ADD REPORTS
        # ==============================

        for report in filtered_reports:

            priority_text = report["priority"]


            if priority_text.startswith("HIGH"):

                tag = "high"

            elif priority_text.startswith("MEDIUM"):

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
                    report["priority"]
                ),
                tags=(tag,)
            )


    # ==============================
    # SEARCH BUTTON
    # ==============================

    search_button = tk.Button(
        filter_frame,
        text="🔎 Search",
        command=update_table
    )

    search_button.grid(
        row=0,
        column=4,
        padx=5
    )


    # ==============================
    # SHOW ALL
    # ==============================

    def show_all():

        search_entry.delete(
            0,
            tk.END
        )

        priority_filter.set(
            "All"
        )

        update_table()


    show_all_button = tk.Button(
        filter_frame,
        text="Show All",
        command=show_all
    )

    show_all_button.grid(
        row=0,
        column=5,
        padx=5
    )


    # ==============================
    # DISPLAY TABLE
    # ==============================

    table.pack(
        padx=20,
        pady=10,
        fill="both",
        expand=True
    )


    # Load reports immediately
    update_table()


# ==========================================================
# SUBMIT REPORT
# ==========================================================

def submit_report():

    location = location_entry.get().strip()

    waste_type = waste_dropdown.get().lower()

    severity = severity_dropdown.get().lower()

    location_type = location_type_dropdown.get().lower()

    repeat_report = repeat_dropdown.get().lower()


    # ==============================
    # VALIDATION
    # ==============================

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


    # ==============================
    # CALCULATE SCORES
    # ==============================

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


    # ==============================
    # REPORT ID
    # ==============================

    report_id = (
        f"CR-{len(reports) + 1:03d}"
    )


    # ==============================
    # TIMESTAMP
    # ==============================

    timestamp = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )


    # ==============================
    # CREATE REPORT
    # ==============================

    report = {

        "report_id": report_id,

        "timestamp": timestamp,

        "location": location,

        "waste_type": waste_type,

        "severity": severity,

        "location_type": location_type,

        "repeat_report": repeat_report,

        "priority_score": priority_score,

        "priority": priority
    }


    # Add report
    reports.append(
        report
    )


    # ==============================
    # SAVE TO JSON
    # ==============================

    save_reports()


    # ==============================
    # DISPLAY RESULT
    # ==============================

    result_label.config(
        text=(
            f"Report ID: {report_id}\n"
            f"Reported At: {timestamp}\n\n"
            f"Priority Score: {priority_score}\n"
            f"Priority: {priority}"
        )
    )


# ==========================================================
# SUBMIT BUTTON
# ==========================================================

submit_button = tk.Button(
    window,
    text="SUBMIT REPORT",
    command=submit_report,
    font=("Arial", 12, "bold"),
    width=20
)

submit_button.pack(
    pady=20
)


# ==========================================================
# VIEW REPORTS BUTTON
# ==========================================================

dashboard_button = tk.Button(
    window,
    text="VIEW REPORTS",
    command=view_reports,
    font=("Arial", 11, "bold"),
    width=20
)

dashboard_button.pack(
    pady=5
)


# ==========================================================
# RESULT
# ==========================================================

result_label = tk.Label(
    window,
    text="",
    font=("Arial", 14, "bold")
)

result_label.pack(
    pady=15
)


# ==========================================================
# RUN APPLICATION
# ==========================================================

window.mainloop()