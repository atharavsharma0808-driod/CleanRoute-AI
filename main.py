from datetime import datetime


print("===== CleanRoute AI =====")


# Function to calculate base priority from severity
def calculate_priority(severity):
    if severity == "high":
        return 80
    elif severity == "medium":
        return 50
    elif severity == "low":
        return 20
    else:
        return 0


# Function to calculate extra score based on location
def calculate_location_score(location_type):
    if location_type == "hospital":
        return 20
    elif location_type == "school":
        return 15
    elif location_type == "market":
        return 10
    elif location_type == "residential":
        return 5
    else:
        return 0


# Function to calculate extra score based on waste type
def calculate_waste_score(waste_type):
    if waste_type == "medical":
        return 20
    elif waste_type == "hazardous":
        return 20
    elif waste_type == "plastic":
        return 10
    elif waste_type == "food":
        return 5
    elif waste_type == "general":
        return 0
    else:
        return 0


# Function to convert score into priority level
def get_priority_level(priority_score):
    if priority_score >= 70:
        return "HIGH 🔴"
    elif priority_score >= 40:
        return "MEDIUM 🟠"
    elif priority_score > 0:
        return "LOW 🟢"
    else:
        return "INVALID ⚠️"


# List to store all reports
reports = []


while True:

    print("\n--- New Garbage Report ---")

    # Get location
    while True:

        location = input(
            "Enter garbage location (or type 'done' to finish): "
        ).strip()

        if location.lower() == "done":
            break

        if location == "":
            print("Location cannot be empty!")
        else:
            break

    # Stop if user typed done
    if location.lower() == "done":
        break


    # Get waste type
    while True:

        waste_type = input(
            "Enter waste type "
            "(Medical/Hazardous/Plastic/Food/General): "
        ).strip().lower()

        if waste_type in [
            "medical",
            "hazardous",
            "plastic",
            "food",
            "general"
        ]:
            break

        print(
            "Invalid waste type! "
            "Please enter Medical, Hazardous, Plastic, Food, or General."
        )


    # Get severity
    while True:

        severity = input(
            "Enter severity (Low/Medium/High): "
        ).strip().lower()

        if severity in ["low", "medium", "high"]:
            break

        print(
            "Invalid severity! "
            "Please enter Low, Medium, or High."
        )


    # Get location type
    while True:

        location_type = input(
            "Location type "
            "(Hospital/School/Market/Residential/Other): "
        ).strip().lower()

        if location_type in [
            "hospital",
            "school",
            "market",
            "residential",
            "other"
        ]:
            break

        print(
            "Invalid location type! "
            "Please enter Hospital, School, Market, Residential, or Other."
        )


    # Get repeat report information
    while True:

        repeat_report = input(
            "Has this location been reported before? (yes/no): "
        ).strip().lower()

        if repeat_report in ["yes", "no"]:
            break

        print(
            "Invalid input! Please enter yes or no."
        )


    # Calculate scores
    severity_score = calculate_priority(severity)

    location_score = calculate_location_score(
        location_type
    )

    waste_score = calculate_waste_score(
        waste_type
    )


    # Calculate repeat score
    if repeat_report == "yes":
        repeat_score = 15
    else:
        repeat_score = 0


    # Calculate final priority score
    priority_score = (
        severity_score
        + location_score
        + waste_score
        + repeat_score
    )


    # Prevent score from going above 100
    if priority_score > 100:
        priority_score = 100


    # Determine priority level
    priority = get_priority_level(
        priority_score
    )


    # Generate Report ID
    report_id = f"CR-{len(reports) + 1:03d}"


    # Generate timestamp
    timestamp = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )


    # Store report
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


    print("\n✅ Report successfully added!")

    print("Report ID:", report_id)

    print("Priority Score:", priority_score)

    print("Priority:", priority)

    print("Reported At:", timestamp)


# Sort reports from highest to lowest priority
reports.sort(
    key=lambda report: report["priority_score"],
    reverse=True
)


# Display all reports
print("\n===== ALL GARBAGE REPORTS =====")


if len(reports) == 0:

    print("No garbage reports were submitted.")


else:

    for number, report in enumerate(
        reports,
        start=1
    ):

        print(f"\n--- Report {number} ---")

        print(
            "Report ID:",
            report["report_id"]
        )

        print(
            "Reported At:",
            report["timestamp"]
        )

        print(
            "Location:",
            report["location"]
        )

        print(
            "Waste Type:",
            report["waste_type"]
        )

        print(
            "Severity:",
            report["severity"]
        )

        print(
            "Location Type:",
            report["location_type"]
        )

        print(
            "Previously Reported:",
            report["repeat_report"]
        )

        print(
            "Priority Score:",
            report["priority_score"]
        )

        print(
            "Priority:",
            report["priority"]
        )