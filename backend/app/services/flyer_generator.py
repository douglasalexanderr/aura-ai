import html
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = BASE_DIR / "data" / "media"


def create_flyer_svg(campaign_id: int, package: dict) -> str:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    flyer = package["flyer"]

    headline = html.escape(flyer["headline"][:58])
    subtitle = html.escape(flyer["subtitle"][:70])
    cta = html.escape(flyer["call_to_action"][:70])
    benefits = [html.escape(item[:55]) for item in flyer["benefits"][:3]]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350">
    <defs>
      <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0%" stop-color="#071126"/>
        <stop offset="100%" stop-color="#182c62"/>
      </linearGradient>
    </defs>
    <rect width="1080" height="1350" fill="url(#bg)"/>
    <circle cx="930" cy="160" r="220" fill="#4f7cff" opacity="0.22"/>
    <circle cx="150" cy="1180" r="260" fill="#34d399" opacity="0.12"/>
    <text x="80" y="120" font-family="Arial" font-size="42" fill="#8fb0ff" font-weight="700">AURA AI</text>
    <text x="80" y="250" font-family="Arial" font-size="66" fill="white" font-weight="800">{headline}</text>
    <text x="80" y="335" font-family="Arial" font-size="36" fill="#cad7ff">{subtitle}</text>
    <rect x="80" y="430" width="920" height="430" rx="28" fill="#ffffff" opacity="0.08"/>
    <text x="130" y="535" font-family="Arial" font-size="38" fill="white">✓ {benefits[0]}</text>
    <text x="130" y="635" font-family="Arial" font-size="38" fill="white">✓ {benefits[1]}</text>
    <text x="130" y="735" font-family="Arial" font-size="38" fill="white">✓ {benefits[2]}</text>
    <rect x="80" y="980" width="920" height="140" rx="28" fill="#4f7cff"/>
    <text x="540" y="1068" text-anchor="middle" font-family="Arial" font-size="42" fill="white" font-weight="800">{cta}</text>
    <text x="80" y="1255" font-family="Arial" font-size="30" fill="#9fb1d8">Innovaciones Tecnológicas · itecnologicas.mx</text>
    </svg>"""

    filename = f"flyer_{campaign_id}.svg"
    (MEDIA_DIR / filename).write_text(svg, encoding="utf-8")
    return f"/media/{filename}"
