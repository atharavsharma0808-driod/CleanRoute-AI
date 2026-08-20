import tkinter as tk
from tkinter import ttk
from datetime import datetime

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


# Store all submitted reports
reports = []


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


# ==============================
# VIEW REPORT DASHBOARD
# ==============================

def view_reports():

    # Create dashboard window
    dashboard = tk.Toplevel(window)

    dashboard.title(
        "CleanRoute AI - Report Dashboard"
    )

    dashboard.geometry(
        "950x600"
    )


    # ==============================
    # DASHBOARD TITLE
    # ==============================

    dashboard_title = tk.Label(
        dashboard,
        text="📊 Report Dashboard",
        font=("Arial", 20, "bold")
    )

    dashboard_title.pack(pady=(15, 5))


    # ==============================
    # CALCULATE STATISTICS
    # ==============================

    total_reports = len(reports)

    high_reports = 0
    medium_reports = 0
    low_reports = 0


    for report in reports:

        if report["priority"].startswith("HIGH"):

            high_reports += 1

        elif report["priority"].startswith("MEDIUM"):

            medium_reports += 1

        elif report["priority"].startswith("LOW"):

            low_reports += 1


    # ==============================
    # STATISTICS DISPLAY
    # ==============================

    stats_frame = tk.Frame(
        dashboard
    )

    stats_frame.pack(
        pady=10
    )


    total_label = tk.Label(
        stats_frame,
        text=f"Total Reports: {total_reports}",
        font=("Arial", 13, "bold")
    )

    total_label.grid(
        row=0,
        column=0,
        padx=25
    )


    high_label = tk.Label(
        stats_frame,
        text=f"🔴 HIGH: {high_reports}",
        font=("Arial", 13, "bold")
    )

    high_label.grid(
        row=0,
        column=1,
        padx=25
    )


    medium_label = tk.Label(
        stats_frame,
        text=f"🟠 MEDIUM: {medium_reports}",
        font=("Arial", 13, "bold")
    )

    medium_label.grid(
        row=0,
        column=2,
        padx=25
    )


    low_label = tk.Label(
        stats_frame,
        text=f"🟢 LOW: {low_reports}",
        font=("Arial", 13, "bold")
    )

    low_label.grid(
        row=0,
        column=3,
        padx=25
    )


    # ==============================
    # NO REPORTS CHECK
    # ==============================

    if len(reports) == 0:

        empty_label = tk.Label(
            dashboard,
            text="No reports available.",
            font=("Arial", 14)
        )

        empty_label.pack(
            pady=50
        )

        return


    # ==============================
    # SORT REPORTS
    # ==============================

    sorted_reports = sorted(
        reports,
        key=lambda report: report["priority_score"],
        reverse=True
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


    # ==============================
    # HEADINGS
    # ==============================

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


    # ==============================
    # COLUMN WIDTHS
    # ==============================

    table.column(
        "ID",
        width=100
    )

    table.column(
        "Location",
        width=220
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


    # ==============================
    # ADD REPORTS
    # ==============================

    for report in sorted_reports:

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


    table.pack(
        padx=20,
        pady=10,
        fill="both",
        expand=True
    )


# ==============================
# SUBMIT REPORT FUNCTION
# ==============================

def submit_report():

    # Get values
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


    # Repeat score
    if repeat_report == "yes":

        repeat_score = 15

    else:

        repeat_score = 0


    # Final score
    priority_score = (
        severity_score
        + location_score
        + waste_score
        + repeat_score
    )


    # Maximum score
    if priority_score > 100:

        priority_score = 100


    # Priority level
    priority = get_priority_level(
        priority_score
    )


    # ==============================
    # REPORT ID
    # ==============================

    report_id = f"CR-{len(reports) + 1:03d}"


    # ==============================
    # TIMESTAMP
    # ==============================

    timestamp = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )


    # ==============================
    # STORE REPORT
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


    reports.append(report)


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


# ==============================
# SUBMIT BUTTON
# ==============================

submit_button = tk.Button(
    window,
    text="SUBMIT REPORT",
    command=submit_report,
    font=("Arial", 12, "bold"),
    width=20
)

submit_button.pack(pady=20)


# ==============================
# VIEW REPORTS BUTTON
# ==============================

dashboard_button = tk.Button(
    window,
    text="VIEW REPORTS",
    command=view_reports,
    font=("Arial", 11, "bold"),
    width=20
)

dashboard_button.pack(pady=5)


# ==============================
# RESULT
# ==============================

result_label = tk.Label(
    window,
    text="",
    font=("Arial", 14, "bold")
)

result_label.pack(pady=15)


# ==============================
# RUN APPLICATION
# ==============================

window.mainloop()