from processor import Sentence


def convert(sentences: list[Sentence]):
    html_output = """<style>
    #sentences {
        margin: 0 auto;
        max-width: 800px;
        font-size: 1.5em;
        position: relative;
    }

    .word {
        display: inline-block;
    }

    .tooltip {
        position: relative;
        border-bottom: 1px dotted black;
    }

    .tooltip:hover {
        border-bottom: 1px solid black;
    }

    #tooltip-container {
        box-sizing: border-box;
        position: absolute;
        z-index: 1;
        min-width: 100%;
        padding: 10px;
        border: 1px solid black;
        background-color: white;
    }

    #tooltip-container .tooltip-close {
        cursor: pointer;
        background-color: black;
        color: white;
    }
</style>
<script>
    function showTooltip(element, content) {
        const tooltipContainer = document.getElementById("tooltip-container");
        tooltipContainer.getElementsByClassName("tooltip-content")[0].innerHTML = content;
        tooltipContainer.style.visibility = 'visible';
        tooltipContainer.style.top = (window.scrollY + element.getBoundingClientRect().bottom - 8) + "px";
    }

    function hideTooltip() {
        const tooltipContainer = document.getElementById("tooltip-container");
        tooltipContainer.style.visibility = 'hidden';
    }
</script>
<div id="sentences">
    <div id="tooltip-container" style="visibility: hidden">
        <span class="tooltip-close" onclick="hideTooltip()">[x]</span><br />
        <span class="tooltip-content">This is the content of the tooltip</span>
    </div>"""
    for sentence in sentences:
        if sentence is None:
            html_output += "<br />"
            continue
        for word in sentence.words:
            html_output += f'<div class="word tooltip" onclick="showTooltip(this, \'{process_tooltips(word.tooltips)}\')">'
            html_output += write_ruby(word.writing, word.reading)
            html_output += "</ruby>"
            html_output += "</div>"
        html_output += "<br />"
    html_output += "</div>"
    return html_output


def write_ruby(writing, reading=None):
    html_output = f"<ruby>{writing}"
    if reading:
        html_output += f"<rt>{reading}</rt>"
    html_output += "</ruby>"
    return html_output


def process_tooltips(tooltips):
    output_html = ""
    for tooltip in tooltips:
        output_html += f"<b>{tooltip.title}</b><br />"
        output_html += (
            f"<span>{write_ruby(tooltip.writing, tooltip.reading)}</span><br />"
        )
        output_html += f"<span>{tooltip.content}</span><br />"
    return output_html
