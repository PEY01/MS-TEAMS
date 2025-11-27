import io
import argparse
import sys
from flask import Flask, request, Response, send_file, render_template
from markupsafe import escape

# Optional PNG support
try:
    import cairosvg
except:
    cairosvg = None

app = Flask(__name__)

# -----------------------------
# Badge Generator Function
# -----------------------------
def make_badge_svg(label, message, color="#4c1", left_color="#555"):
    label = escape(label)
    message = escape(message)

    # simple text-width estimate
    char_width = 7.8
    left_w = max(40, int(len(label) * char_width + 20))
    right_w = max(40, int(len(message) * char_width + 20))
    total_w = left_w + right_w
    height = 20

    svg = f"""
<svg xmlns='http://www.w3.org/2000/svg' width='{total_w}' height='{height}'>
  <rect width='{left_w}' height='{height}' fill='{left_color}' />
  <rect x='{left_w}' width='{right_w}' height='{height}' fill='{color}' />
  <text x='{left_w/2}' y='14' text-anchor='middle' fill='white' font-size='11'>{label}</text>
  <text x='{left_w + right_w/2}' y='14' text-anchor='middle' fill='white' font-size='11'>{message}</text>
</svg>
"""
    return svg


# -----------------------------
# WEB GUI
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# API ENDPOINT
# -----------------------------
@app.route("/api/badge", methods=["GET"])
def api_badge():
    """
    API USAGE EXAMPLES:
      SVG: GET /api/badge?label=build&message=success&type=svg
      PNG: GET /api/badge?label=build&message=success&type=png
    """
    label = request.args.get("label", "build")
    message = request.args.get("message", "passing")
    color = request.args.get("color", "#4c1")
    left_color = request.args.get("left_color", "#555")
    out_type = request.args.get("type", "svg")

    svg = make_badge_svg(label, message, color, left_color)

    if out_type == "png":
        if cairosvg is None:
            return {"error": "Install cairosvg to enable PNG output"}, 400

        png_bytes = cairosvg.svg2png(bytestring=svg.encode())
        return send_file(io.BytesIO(png_bytes),
                         mimetype="image/png",
                         download_name=f"{label}-{message}.png")

    # default SVG
    return Response(svg, mimetype="image/svg+xml")


# -----------------------------
# CLI MODE
# -----------------------------
def cli_generate(out_file, label, message, color, left_color):
    svg = make_badge_svg(label, message, color, left_color)

    if out_file.endswith(".png"):
        if cairosvg is None:
            print("Install cairosvg to export PNG.")
            return
        png_bytes = cairosvg.svg2png(bytestring=svg.encode())
        with open(out_file, "wb") as f:
            f.write(png_bytes)
        print("PNG saved:", out_file)

    else:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(svg)
        print("SVG saved:", out_file)


# -----------------------------
# MAIN ENTRYPOINT
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--open-ngrok", action="store_true")
    parser.add_argument("--out", help="Generate badge file via CLI")
    parser.add_argument("--label", default="build")
    parser.add_argument("--message", default="passing")
    parser.add_argument("--color", default="#4c1")
    parser.add_argument("--left-color", default="#555")
    args = parser.parse_args()

    # CLI mode
    if args.out:
        cli_generate(args.out, args.label, args.message, args.color, args.left_color)
        sys.exit()

    # Flask mode with ngrok
    if args.open_ngrok:
        try:
            from pyngrok import ngrok
            public_url = ngrok.connect(args.port).public_url
            print("Public URL:", public_url)
        except Exception as e:
            print("Error starting ngrok:", e)

    app.run(port=args.port)
