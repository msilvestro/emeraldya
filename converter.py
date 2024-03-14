from builder import Sentence


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
        tooltipContainer.getElementsByClassName("tooltip-content")[0].innerText = content;
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
            if word.notes:
                div_configuration = f' class="word tooltip" onclick="showTooltip(this, \'{word.notes}\')"'
            else:
                div_configuration = ' class="word"'
            html_output += f"<div{div_configuration}>"
            html_output += f"<ruby>{word.writing}"
            if word.reading:
                html_output += f"<rt>{word.reading}</rt>"
            html_output += "</ruby>"
            html_output += "</div>"
        html_output += "<br />"
    html_output += "</div>"
    return html_output
