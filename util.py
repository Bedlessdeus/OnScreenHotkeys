import screeninfo

def int_to_string(value: int):
    if value < 0:
        return f"-{value}"
    else:
        return f"+{value}"

def get_primary_monitor():
    for monitor in screeninfo.get_monitors():
        if monitor.is_primary:
            return monitor

def list_keys(keys):
    if len(keys) == 0:
        return ""
    elif len(keys) == 1:
        try:
            return keys[0]
        except Exception as e:
            return ""
    else:
        return " + ".join(keys)
