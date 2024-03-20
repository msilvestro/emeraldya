from pathlib import Path

import click

from emeraldya.processor import process
from emeraldya.converter import convert


@click.command()
@click.option("--input-dir", "-i", default=".")
@click.option("--output-dir", "-o", default=".")
def run(input_dir: str, output_dir: str):
    file_found = False
    for em_file in Path(input_dir).glob("*.em"):
        file_found = True
        click.echo(f"Found file '{em_file}'...")
        with open(em_file, "r", encoding="utf-8") as reader:
            em_input = reader.read()

        header, body = process(em_input)
        html_output = convert(header, body)

        html_file = Path(output_dir) / em_file.with_suffix(".html").name
        with open(html_file, "w", encoding="utf-8") as writer:
            writer.write(html_output)
        click.echo(f"> Converted to '{html_file}'")
    if not file_found:
        click.echo("No emerald files found")
