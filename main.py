from builder import build
from converter import convert
from processor import process

with open("haru.jpt", "r", encoding="utf-8") as reader:
    jpt_input = reader.read()

html_output = convert(build(process(jpt_input)))

with open("index.html", "w", encoding="utf-8") as writer:
    writer.write(html_output)
