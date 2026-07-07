from flask import Flask, jsonify, request

from narration_render import render_narrated_equation

app = Flask(__name__)


@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response


@app.route("/render", methods=["POST"])
def render_equation():
    eqn = request.get_json(silent=True)
    if not isinstance(eqn, dict) or not isinstance(eqn.get("latex"), str):
        return jsonify({"error": 'Expected JSON body shaped like {"latex": str, "narrations": [...]}'}), 400

    try:
        html = render_narrated_equation(eqn)
    except Exception as e:
        return jsonify({"error": f"{type(e).__name__}: {e}" if str(e) else type(e).__name__}), 400

    return html, 200, {"Content-Type": "text/html"}


if __name__ == "__main__":
    app.run(port=8080, debug=True)
