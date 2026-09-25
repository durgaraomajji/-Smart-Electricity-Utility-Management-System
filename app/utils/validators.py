def positive(value: float) -> float:
    if value <= 0:
        raise ValueError("Value must be greater than zero")
    return value
