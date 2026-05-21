def validate_exam(title, duration):
    if len(title) < 3:
        return False

    if duration <= 0:
        return False

    return True


def create_exam(title, duration, user_role):
    print("Creating exam...")

    if user_role == "admin":
        if validate_exam(title, duration):
            exam = {
                "title": title,
                "duration": duration
            }
            return exam

    return {"error": "permission denied"}