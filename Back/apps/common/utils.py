def format_datetime(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Utility function to format a datetime object as a string.
    Returns an empty string if dt is None.
    """
    if dt:
        return dt.strftime(format_str)
    return ""
