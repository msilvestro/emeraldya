from dataclasses import dataclass

from emeraldya.furigana import split_characters
from emeraldya.processor import Sentence


def convert(header: dict, body: list[Sentence]):
    html_output = """<style>
    #wrapper {
        margin: 0 auto;
        max-width: 768px;
        font-size: 1.2em;
        position: relative;
    }
    
    .sentence {
        padding-top: 0.5em;
        margin-bottom: 0.5em;
    }

    .word, .translation {
        display: inline-block;
        border-bottom: 5px solid white;
        height: 1.5em;  /* otherwise kanjis might have different heights */
    }
    
    .word:hover, .word.active {
        border-bottom: 5px solid cornflowerblue;
    }
    
    .translation:hover {
        cursor: pointer;
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
        border: 1px solid black;
        background-color: white;
    }

    #tooltip .section {
        margin-bottom: 10px;
    }

    #tooltip .section:last-child {
        margin-bottom: 0;
    }

    #tooltip .section-header {
        background-color: cornflowerblue;
        padding: 10px;
        color: white;
    }

    #tooltip .section-content {
        padding: 10px;
    }
    
    #tooltip .section-content p {
        margin: 0;
        padding: 0;
    }

    #tooltip .tooltip-close {
        cursor: pointer;
        float: right;
        line-height: 100%;
    }

    #tooltip ruby {
        margin-top: 0.5em;
    }
</style>
<script>
    let justClicked = false;
    let activeElements = [];

    function cleanActiveElements() {
        for (let child of activeElements) {
            child.classList.remove("active");
        }
        activeElements = [];
    }

    function showTooltip(element, content) {
        cleanActiveElements();
        const tooltip = document.getElementById("tooltip");
        tooltip.innerHTML = content;
        tooltip.style.visibility = 'visible';
        tooltip.style.top = (window.scrollY + element.getBoundingClientRect().bottom - 8) + "px";
        justClicked = true;
    }

    function hideTooltip() {
        cleanActiveElements();
        const tooltip = document.getElementById("tooltip");
        tooltip.style.visibility = 'hidden';
    }
    
    function activateWord(element) {
        element.classList.add("active");
        activeElements = [element];
    }
    
    function activateSentence(element) {
        activeElements = [];
        const sentence = element.parentNode;
        for (let child of sentence.children) {
            if (child.classList.contains("word")) {
                child.classList.add("active");
                activeElements.push(child);
            }
        }
    }

    window.onload = function() {
        const tooltip = document.getElementById("tooltip");

        document.onclick =function(event) {
            if (justClicked) {
                justClicked = false;
                return;
            }

            if (tooltip.style.visibility === 'visible' && !tooltip.contains(event.target)) {
                hideTooltip();
            }
        }

        document.onkeydown = function (event) {
            if(event.key === 'Escape' && tooltip.style.visibility === 'visible') {
                hideTooltip();
            }
        }
    }
</script><div id="wrapper">"""
    html_output += "<h1>" + header["title"] + " - " + header["author"] + "</h1>"
    html_output += """
    <div id="tooltip" style="visibility: hidden">
    </div>"""
    for sentence in body:
        if sentence is None:
            html_output += "<br />"
            continue
        html_output += '<div class="sentence">'
        for word in sentence.words:
            html_output += f'<div class="word" onclick="showTooltip(this, \'{process_tooltips(word.tooltips)}\');activateWord(this)">'
            html_output += write_ruby(word.writing, word.reading)
            html_output += "</ruby>"
            html_output += "</div>"
        html_output += (
            f' <div class="translation" title="translation"'
            f" onclick=\"showTooltip(this, '{process_translation(sentence.translation)}');activateSentence(this)\">🔄</div>"
        )
        html_output += "</div>"
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


@dataclass
class TooltipSection:
    title: str
    content: str


def create_tooltip_sections(*sections: TooltipSection):
    output_html = "<div class='section'>"
    is_first_header = True
    for section in sections:
        output_html += f"<div class='section-header'><span>{section.title}</span>"
        if is_first_header:
            output_html += (
                "<span class='tooltip-close' onclick='hideTooltip()'>x</span>"
            )
            is_first_header = False
        output_html += "</div>"
        output_html += f"<div class='section-content'>{section.content}</div>"
    output_html += "</div>"
    return output_html.replace("'", "\\'")


def process_tooltips(tooltips):
    sections = []
    for tooltip in tooltips:
        content = f"<p>{write_ruby(tooltip.writing, tooltip.reading)}</p>"
        content += f"<p>{tooltip.content}</p>"
        sections.append(TooltipSection(title=tooltip.title, content=content))
    return create_tooltip_sections(*sections)


def process_translation(translation):
    return create_tooltip_sections(
        TooltipSection(title="Translation", content=translation)
    )
