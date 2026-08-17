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


reports = []

while True:
    print("\n--- New Garbage Report ---")

    location = input(
        "Enter garbage location (or type 'done' to finish): "
    )

    if location.lower() == "done":
        break

    waste_type = input("Enter waste type: ")

    severity = input(
        "Enter severity (Low/Medium/High): "
    ).lower()

    location_type = input(
        "Location type (Hospital/School/Market/Residential/Other): "
    ).lower()

    repeat_report = input(
        "Has this location been reported before? (yes/no): "
    ).lower()

    # Calculate scores
    severity_score = calculate_priority(severity)
    location_score = calculate_location_score(location_type)

    # Add extra points for repeated reports
    if repeat_report == "yes":
        repeat_score = 15
    else:
        repeat_score = 0

    # Calculate final priority score
    priority_score = (
        severity_score
        + location_score
        + repeat_score
    )

    # Prevent score from going above 100
    if priority_score > 100:
        priority_score = 100

    priority = get_priority_level(priority_score)

    # Store report
    report = {
        "location": location,
        "waste_type": waste_type,
        "severity": severity,
        "location_type": location_type,
        "repeat_report": repeat_report,
        "priority_score": priority_score,
        "priority": priority
    }

    reports.append(report)


# Sort reports from highest to lowest priority
reports.sort(
    key=lambda report: report["priority_score"],
    reverse=True
)


# Display all reports
print("\n===== ALL GARBAGE REPORTS =====")

for report in reports:
    print("\nLocation:", report["location"])
    print("Waste Type:", report["waste_type"])
    print("Severity:", report["severity"])
    print("Location Type:", report["location_type"])
    print("Previously Reported:", report["repeat_report"])
    print("Priority Score:", report["priority_score"])
    print("Priority:", report["priority"])