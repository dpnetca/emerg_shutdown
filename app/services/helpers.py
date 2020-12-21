import uuid


def is_uuid(value: str) -> bool:
    """check if parameter matches a uuid format

    Args:
        value (str): possible uuid to check

    Returns:
        bool: True if value is a uuid
    """
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False
