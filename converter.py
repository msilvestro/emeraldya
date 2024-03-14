from builder import Sentence


def convert(sentences: list[Sentence]):
    html_output = """<style>
#sentences {
    margin: 0 auto;
    width: 60%;
    font-size: 1.5em;
}

.word {
    display: inline-block;
}

.tooltip {
  position: relative;
  border-bottom: 1px dotted black; 
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;
 
  position: absolute;
  z-index: 1;
  
  width: 120px;
  top: 100%;
  left: 50%;
  margin-left: -60px; /* Use half of the width (120/2 = 60), to center the tooltip */
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
<div id="sentences">"""
    for sentence in sentences:
        if sentence is None:
            html_output += "<br />"
            continue
        for word in sentence.words:
            classes = ["word"]
            if word.notes:
                classes.append("tooltip")
            classes_text = " ".join(classes)
            html_output += f'<div class="{classes_text}">'
            html_output += f"<ruby>{word.writing}"
            if word.reading:
                html_output += f"<rt>{word.reading}</rt>"
            html_output += "</ruby>"
            if word.notes:
                html_output += f'<span class="tooltiptext">{word.notes}</span>'
            html_output += "</div>"
        html_output += "<br />"
    html_output += "</div>"
    return html_output
