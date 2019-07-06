""" Custom filters to be used in jinja2 templates. """
from main import app
from datetime import datetime

@app.template_filter('strparsetime')
def string_parse_time_filter(value, date_format):
    return datetime.strptime(value, date_format)