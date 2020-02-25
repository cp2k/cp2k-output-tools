# floating point regex
FLOAT = r"[\+\-]?(\d*[\.]\d+|\d+[\.]?\d*)([Ee][\+\-]?\d+)?"


# convert possibly problematic characters to underscores
def safe_string(string):
    return (
        string.replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("[", "_")
        .replace("]", "_")
        .replace(".", "_")
        .replace("|", "_")
        .replace("^", "_")
        .replace("(", "_")
        .replace(")", "_")
        .replace("{", "_")
        .replace("}", "_")
    )
