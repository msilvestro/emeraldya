from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

from emeraldya.processor import Sentence


def get_template(template_name: str):
    loader = PackageLoader("emeraldya")
    if Path(template_name).exists():
        template_path = Path(template_name)
        loader = FileSystemLoader(template_path.parent)
        template_name = template_path.name

    env = Environment(
        loader=loader,
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    return env.get_template(template_name)


def convert(header: dict, body: list[Sentence], template_name: str):
    return get_template(template_name).render(header=header, body=body)
