from uuid import uuid4


def generate_id_with_prefix(prefix):
    return f"{prefix}:{uuid4()}"
