
def validate_phone_number(phone_number: str) -> str:
    cleaned = phone_number.replace(" ", "").replace("-", "")

    if len(cleaned) == 13 and cleaned.startswith("+233"):
        return cleaned
    if len(cleaned) == 10 and cleaned.startswith("0"):
        return "+233" + cleaned[1:]
    raise ValueError("Invalid phone number format")