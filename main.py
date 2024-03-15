from processor import process
from converter import convert

with open("haru.jpt", "r", encoding="utf-8") as reader:
    jpt_input = reader.read()

header, body = process(jpt_input)
html_output = convert(header, body)

with open("index.html", "w", encoding="utf-8") as writer:
    writer.write(html_output)
