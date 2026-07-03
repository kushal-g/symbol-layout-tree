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
  "latex": r"\begin{pmatrix} 1 & 2 & 3 & 4 & 5 \\ a & b^{2} & \frac{c}{d} & e & f \\ x & y & z^{2} & w & v \\ \alpha & \beta & \gamma & \delta & \epsilon \end{pmatrix}",
  "narrations": [
    { "term": r"\frac{c}{d}", "narration": "Element (2,3)", "pos": "1" }
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
  function wrap(el, wrapper) {
      el.parentNode.insertBefore(wrapper, el);
      wrapper.appendChild(el);
  }
"""

for i, term in enumerate(eqn.get("narrations", [])):
  page_content += f"""

    const narrate_dom{i} =   document.getElementById("narrate-{i}")
    const eqn_dom{i} = document.getElementById("eqn-{i}")
    
    text_bounds = narrate_dom{i}.getBoundingClientRect()
    term_bounds = eqn_dom{i}.getBoundingClientRect()
    
    const mpadded{i} = document.createElementNS("http://www.w3.org/1998/Math/MathML", "mpadded")
    mpadded{i}.setAttribute("width","10em")
    mpadded{i}.setAttribute("lspace", "5em")
    mpadded{i}.setAttribute("height","10ex")
    mpadded{i}.setAttribute("depth","5ex")

    wrap(eqn_dom{i}, mpadded{i})

    narrate_dom{i}.style.left = eqn_dom{i}.getBoundingClientRect().left - Number(getComputedStyle(eqn_dom{i}).marginLeft.replace("px",""))
    narrate_dom{i}.style.top = document.querySelector("math").getBoundingClientRect().top - Number(getComputedStyle(narrate_dom{i}).height.replace("px","")) - 10
"""


page_content += """
</script>
"""

page_content += "</html>"

f = open("./index.html", mode = "w")

print(page_content)
f.write(page_content)

f.close()