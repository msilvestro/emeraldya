from furigana import split_characters
from processor import Sentence


def convert(header: dict, body: list[Sentence]):
    html_output = """<style>
        #sentences {
        margin: 0 auto;
        max-width: 800px;
        font-size: 1.5em;
        position: relative;
    }

    .word {
        display: inline-block;
        border-bottom: 5px solid white;
        height: 1.5em;  /* otherwise kanjis might have different heights */
        margin-bottom: 20px;
    }
    
    .word:hover {
        border-bottom: 5px solid black;
    }

    /* Customize ruby appearance to avoid spacing issues */
    ruby {
        display: inline-block;
        position: relative;
    }

    ruby rt {
        display: inline-block;
        position: absolute;
        left: 0;
        right: 0;
        top: -1em;
        text-align: center;
    }

    #tooltip {
        box-sizing: border-box;
        position: absolute;
        z-index: 1;
        min-width: 100%;
        padding: 10px;
        border: 1px solid black;
        background-color: white;
    }

    #tooltip .tooltip-close {
        cursor: pointer;
        background-color: black;
        color: white;
    }
</style>
<script>
    function showTooltip(element, content) {
        const tooltip = document.getElementById("tooltip");
        tooltip.getElementsByClassName("tooltip-content")[0].innerHTML = content;
        tooltip.style.visibility = 'visible';
        tooltip.style.top = (window.scrollY + element.getBoundingClientRect().bottom - 8) + "px";
    }

    function hideTooltip() {
        const tooltipContainer = document.getElementById("tooltip");
        tooltipContainer.style.visibility = 'hidden';
    }
</script><div id="sentences">"""
    html_output += "<h1>" + header["title"] + " - " + header["author"] + "</h1>"
    html_output += """
    <div id="tooltip" style="visibility: hidden">
        <span class="tooltip-close" onclick="hideTooltip()">[x]</span><br />
        <span class="tooltip-content">This is the content of the tooltip</span>
    </div>"""
    for sentence in body:
        if sentence is None:
            html_output += "<br />"
            continue
        for word in sentence.words:
            html_output += f'<div class="word tooltip" onclick="showTooltip(this, \'{process_tooltips(word.tooltips)}\')">'
            html_output += write_ruby(word.writing, word.reading)
            html_output += "</ruby>"
            html_output += "</div>"
        html_output += f' <div class="word tooltip" onclick="showTooltip(this, \'{process_translation(sentence.translation)}\')">🔄</div>'
        html_output += "<br />"
    html_output += "</div>"
    return html_output


def write_ruby(writing, reading=None):
    if not reading:
        return writing

    html_output = ""
    characters = split_characters(writing, reading)
    for character in characters:
        if not character.furigana:
            html_output += character.main
        else:
            html_output += f"<ruby>{character.main}<rt>{character.furigana}</rt></ruby>"

    return html_output


def process_tooltips(tooltips):
    output_html = ""
    for tooltip in tooltips:
        output_html += f"<b>{tooltip.title}</b><br />"
        output_html += (
            f"<span>{write_ruby(tooltip.writing, tooltip.reading)}</span><br />"
        )
        output_html += f"<span>{tooltip.content}</span><br />"
    return output_html.replace("'", "\\'")


def process_translation(translation):
    output_html = ""
    output_html += "<b>Translation</b><br />"
    output_html += f"<span>{translation}</span>"
    return output_html.replace("'", "\\'")
