import re

regex = r"<\d+>([A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2}) Application: (.+)"


def parse_log(log):
    """
    Parse a log file and return a list of dictionaries
    """
    logs = []
    for line in log.split("\n"):
        if not line:
            continue

        match = re.match(regex, line)

        if match:
            logs.append({
                "date": match.group(1),
                "application": match.group(2)
            })

    return logs
