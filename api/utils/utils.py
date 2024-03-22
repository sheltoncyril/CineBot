import re

date_expr = re.compile(r"(\([0-9]{4}\))$")


def remove_date_from_movie(string: str):
    return date_expr.sub("", string).strip()
