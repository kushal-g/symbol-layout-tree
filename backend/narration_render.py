import re
import xml.etree.ElementTree as ET

import latex2mathml.converter

MATHML_NS = "http://www.w3.org/1998/Math/MathML"
ET.register_namespace("", MATHML_NS)


def pretty_print_mathml(mathml: str):
    element = ET.XML(mathml)
    ET.indent(element)
    return ET.tostring(element, encoding='unicode').replace("ns0:", "")


def _collapse_redundant_mrow(elem: ET.Element) -> None:
    """Remove <mrow> nodes that wrap a single child.

    latex2mathml is inconsistent about adding this wrapper depending on
    context: converting a term on its own (e.g. "b^{2}") can produce an
    <mrow> around a token that wouldn't be wrapped had it been converted
    as part of a larger expression (e.g. "\\frac{a}{b^2}"). Collapsing
    these redundant wrappers on both sides before substring-matching a
    narrated term against the full equation's MathML means the match
    isn't sensitive to that variance.
    """
    for child in list(elem):
        _collapse_redundant_mrow(child)

    i = 0
    while i < len(elem):
        child = elem[i]
        if child.tag.endswith("mrow") and len(child) == 1:
            grandchild = child[0]
            elem.remove(child)
            elem.insert(i, grandchild)
        else:
            i += 1


def convert_latex(latex: str) -> str:
    """Convert LaTeX to MathML, normalized so equivalent sub-expressions
    serialize identically whether converted standalone or as part of a
    larger expression (see `_collapse_redundant_mrow`)."""
    root = ET.XML(latex2mathml.converter.convert(latex))
    _collapse_redundant_mrow(root)
    return ET.tostring(root, encoding='unicode')


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
  <div id="narrate-{id}" style="max-width:4rem; font-size: 0.5em; border:1px solid black; text-align: center; position: absolute; padding: 2px 8px;">
   {text}
  </div>

"""


def render_narrated_equation(eqn: dict) -> str:
    """Render an equation + narrations into a standalone HTML page.

    `eqn` is shaped like:
      { "latex": str, "narrations": [{"term": str, "narration": str, "pos": str}] }

    Each narrated term is located within the equation's MathML (by its
    nth occurrence, 1-based) and wrapped in an <mpadded> element sized to
    make room for its narration label, positioned via the inline <script>.
    """
    narrations = eqn.get("narrations", [])

    page_content = """<!DOCTYPE html>
<html>
<style>math{margin:150px}</style>
<body>
  """

    page_content += "<div style='margin-bottom: 50px'>"
    mml = convert_latex(eqn["latex"])

    for i, term in enumerate(narrations):
        t = strip_math_tags(convert_latex(term["term"]))
        pos = int(term.get("pos", 1))

        mml = replace_nth(mml, t, f"<mrow id='eqn-{i}'>{t}</mrow>", pos)
        page_content += narration_layer(i, term["narration"])

    page_content += mml
    page_content += "</div>"

    page_content += """
</body>
<script>
  function wrap(el, wrapper) {
      el.parentNode.insertBefore(wrapper, el);
      wrapper.appendChild(el);
  }

  function positionNarration(){
  console.log("Positioning Narrations")

  // Wrapping a term in <mpadded> adds real layout space, shifting every
  // later element in the equation. All wraps must be applied before any
  // label is measured/positioned, or earlier positions computed against
  // a not-yet-fully-padded layout go stale as later wraps shift things.
  const pending = []
"""

    for i, term in enumerate(narrations):
        page_content += f"""

    const narrate_dom{i} = document.getElementById("narrate-{i}")
    const eqn_dom{i} = document.getElementById("eqn-{i}")

    if (narrate_dom{i} && eqn_dom{i}) {{
      // Chromium doesn't honor the legacy "+Nunit" mpadded syntax (it's
      // parsed as a plain absolute length, not "natural size + N"), which
      // used to shift the highlighted term right and make width/lspace
      // asymmetric. Compute literal width/lspace/height/depth from the
      // term's actual pre-wrap size instead, so the added space is
      // symmetric on both sides.
      const term_bounds{i} = eqn_dom{i}.getBoundingClientRect()
      const eqnStyle{i} = getComputedStyle(eqn_dom{i})
      const fontSizePx{i} = parseFloat(eqnStyle{i}.fontSize) || 16

      // ex is the font's x-height, not simply half of em, so measure the
      // actual px-per-1ex for this font context rather than assuming a
      // ratio. mrow can't host an HTML span as layout content, so probe
      // in document.body with the same font instead.
      const exProbe{i} = document.createElement("span")
      exProbe{i}.style.cssText = "position:absolute; visibility:hidden; display:inline-block; height:1ex; width:0; margin:0; padding:0; border:0;"
      exProbe{i}.style.fontFamily = eqnStyle{i}.fontFamily
      exProbe{i}.style.fontSize = eqnStyle{i}.fontSize
      document.body.appendChild(exProbe{i})
      const exPx{i} = exProbe{i}.getBoundingClientRect().height || fontSizePx{i} / 2
      document.body.removeChild(exProbe{i})

      const padEm{i} = 4
      const padEx{i} = 4
      const widthEm{i} = term_bounds{i}.width / fontSizePx{i} + 2 * padEm{i}
      const heightEx{i} = term_bounds{i}.height / 2 / exPx{i} + padEx{i}

      const mpadded{i} = document.createElementNS("http://www.w3.org/1998/Math/MathML", "mpadded")
      mpadded{i}.setAttribute("width", widthEm{i} + "em")
      mpadded{i}.setAttribute("lspace", padEm{i} + "em")
      mpadded{i}.setAttribute("height", heightEx{i} + "ex")
      mpadded{i}.setAttribute("depth", heightEx{i} + "ex")

      wrap(eqn_dom{i}, mpadded{i})

      pending.push([narrate_dom{i}, eqn_dom{i}])
    }} else {{
      console.warn("Could not locate narration/term element for narration index {i} (term did not match the equation's MathML)")
    }}
"""

    page_content += """
    const mathTop = document.querySelector("math").getBoundingClientRect().top

    pending.forEach(([narrateEl, eqnEl]) => {
      const eqnRect = eqnEl.getBoundingClientRect()
      const narrateRect = narrateEl.getBoundingClientRect()
      const left = (eqnRect.left + eqnRect.width / 2 - narrateRect.width / 2) + "px"
      const top = (mathTop - narrateRect.height - 10) + "px"

      narrateEl.style.left = left
      narrateEl.style.top = top

      console.log("left", left)
      console.log("top", top)
    })

    console.log("Positioned Narrations")
    }
    positionNarration()
</script>
"""

    page_content += "</html>"
    return page_content
