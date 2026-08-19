# ==============================
# CleanRoute AI - Backend Logic
# ==============================


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