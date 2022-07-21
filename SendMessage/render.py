import jinja2
import os
import logging
from .jinja2_filters import format_datetime


def render_message(selected_template: str, data: dict):
    templatePath = os.path.join(os.path.dirname(__file__), "./render_templates")
    logging.debug(f"Templates path: {templatePath}")
    templateLoader = jinja2.FileSystemLoader(searchpath=templatePath)
    templateEnv = jinja2.Environment(loader=templateLoader)

    # custom filter to format date and time
    templateEnv.filters['format_datetime'] = format_datetime

    try:
        template = templateEnv.get_template(f"{selected_template}.j2")
    except jinja2.exceptions.TemplateNotFound:
        template = templateEnv.get_template("_error.j2")

    try:
        msg = template.render(data=data)
    except jinja2.exceptions.UndefinedError as e:
        msg = f"Render error: {e}"
    except Exception as e:
        msg = e

    return msg
