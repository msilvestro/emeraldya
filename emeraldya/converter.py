from jinja2 import Environment, PackageLoader, select_autoescape

from emeraldya.processor import Sentence

env = Environment(
    loader=PackageLoader("emeraldya"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def convert(header: dict, body: list[Sentence]):
    template = env.get_template("toratore.html.jinja")
    return template.render(header=header, body=body)
