import re
import latex2mathml.converter
import xml.etree.ElementTree as ET

def pretty_print_mathml(mathml: str):
    element = ET.XML(mathml)
    ET.indent(element)
    return ET.tostring(element, encoding='unicode').replace("ns0:","")

def replace_nth(s: str, old: str, new: str, n: int) -> str:
    idx = -1
    for _ in range(n):
        idx = s.find(old, idx + 1)
        if idx == -1:
            return s
    return s[:idx] + new + s[idx + len(old):]

def strip_math_tags(mml: str) -> str:
    mml = re.sub(r'^<math[^>]*>', '', mml)
    mml = re.sub(r'</math>$', '', mml)
    # latex2mathml always wraps content in a single <mrow>; strip it so
    # the fragment matches within the full equation's outer <mrow>
    mml = re.sub(r'^<mrow>', '', mml)
    mml = re.sub(r'</mrow>$', '', mml)
    return mml.strip()

def narration_layer(id: int, text: str):
    return f"""
  <div id="narrate-{id}" style="max-width:4rem; font-size: 0.5em; border:1px solid black; text-align: center; position: absolute">
   {text}
  </div>

"""

eqn = {
  "latex": r"| E_i | = \binom{8}{i} . 5^i . 21^{8-i}",
  "narrations": [
    { "term": r"| E_i |",       "narration": "Number of 8-letter strings with i vowels", "pos": "1" },
    { "term": r"\binom{8}{i}",  "narration": "Choose i locations for the vowels",         "pos": "1" },
        { "term": r"i",      "narration": "Exponent for choose the remaining letters",               "pos": "3" },

    { "term": r"21^{8-i}",      "narration": "Choose the remaining letters",               "pos": "1" },
  ],
}

page_content = """<html> 
<style>math{margin:150px}</style>

  """


page_content += "<div style='margin-bottom: 50px'>"
mml = latex2mathml.converter.convert(eqn["latex"])

for i, term in enumerate(eqn.get("narrations", [])):
    t = strip_math_tags(latex2mathml.converter.convert(term["term"]))
    pos = int(term.get("pos", 1))

    mml = replace_nth(mml, t, f"<mrow id='eqn-{i}'>{t}</mrow>", pos)
    page_content += narration_layer(i, term["narration"])

page_content += mml
page_content += "</div>"


page_content += """
<script>
  console.log(document.getElementById("narrate-0").getBoundingClientRect())
  let narrate_dom, eqn_dom;
"""

for i, term in enumerate(eqn.get("narrations", [])):
  page_content += f"""

     narrate_dom =   document.getElementById("narrate-{i}")
     eqn_dom = document.getElementById("eqn-{i}")
    
    text_bounds = narrate_dom.getBoundingClientRect()
    term_bounds = eqn_dom.getBoundingClientRect()
    
    h_margin = (text_bounds.width - term_bounds.width) / 2

    eqn_dom.style.marginLeft = "max(" + h_margin + "px, 0.5em)" 
    eqn_dom.style.marginRight = "max(" + h_margin + "px, 0.5em)" 

    
    narrate_dom.style.left = eqn_dom.getBoundingClientRect().left - Number(getComputedStyle(eqn_dom).marginLeft.replace("px",""))
    narrate_dom.style.top = eqn_dom.getBoundingClientRect().top - Number(getComputedStyle(narrate_dom).height.replace("px","")) - 10
"""


page_content += """
</script>
"""

page_content += "</html>"

f = open("./index.html", mode = "w")

print(page_content)
f.write(page_content)

f.close()