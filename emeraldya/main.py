from pathlib import Path

from emeraldya.processor import process
from emeraldya.converter import convert


def run():
    for em_file in Path().glob("*.em"):
        with open(em_file, "r", encoding="utf-8") as reader:
            em_input = reader.read()

        header, body = process(em_input)
        html_output = convert(header, body)

        html_file = em_file.with_suffix(".html")
        with open(html_file, "w", encoding="utf-8") as writer:
            writer.write(html_output)
