from dateutil.parser import parse as datetime_parser


# custom filter to format date and time
def format_datetime(date_time_str: str, format: str = "%d/%m/%y %H:%M:%S %Z"):
    d = datetime_parser(date_time_str)
    return d.strftime(format)
