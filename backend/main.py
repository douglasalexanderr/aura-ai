from datetime import datetime
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


app = FastAPI(
    title="AURA AI",
    version="0.2.0",
    description="Generador autónomo de campañas de marketing",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CampaignRequest(BaseModel):
    idea: str = Field(min_length=5, max_length=500)
    city: str = "Mérida, Yucatán"
    company: str = "Innovaciones Tecnológicas"


class SocialPost(BaseModel):
    network: str
    text: str
    hashtags: List[str]


class CampaignResponse(BaseModel):
    campaign_name: str
    objective: str
    target_audience: List[str]
    value_proposition: str
    video_script: List[str]
    flyer: dict
    social_posts: List[SocialPost]
    calendar: List[dict]
    status: str
    created_at: str


@app.get("/")
def root():
    return {
        "message": "Bienvenido a AURA AI",
        "version": "0.2.0",
        "app": "http://127.0.0.1:8000/app",
        "docs": "http://127.0.0.1:8000/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "AURA AI API"}


@app.post("/api/campaigns/generate", response_model=CampaignResponse)
def generate_campaign(data: CampaignRequest):
    idea = data.idea.strip()
    city = data.city.strip()
    company = data.company.strip()

    campaign_name = f"{idea[:45]} | {city}"

    target_audience = [
        f"Personas y empresas ubicadas en {city}",
        "Clientes que buscan ahorro, seguridad y tecnología",
        "Propietarios interesados en soluciones profesionales",
    ]

    video_script = [
        f"Escena 1: Mostrar el problema que resuelve: {idea}.",
        f"Escena 2: Presentar a {company} como solución profesional.",
        "Escena 3: Mostrar beneficios, confianza y resultados.",
        f"Escena 4: Invitación a solicitar una cotización en {city}.",
        "Cierre: Contáctanos hoy y recibe atención personalizada.",
    ]

    flyer = {
        "headline": idea.upper(),
        "subtitle": f"Soluciones profesionales en {city}",
        "benefits": [
            "Atención personalizada",
            "Instalación profesional",
            "Cotización sin compromiso",
        ],
        "call_to_action": "Solicita información hoy",
        "format": "1080 x 1350 px",
        "style": "Tecnológico, moderno y profesional",
    }

    posts = [
        SocialPost(
            network="Facebook",
            text=(
                f"¿Estás buscando {idea.lower()}? En {company} ofrecemos "
                f"soluciones profesionales en {city}. Solicita una cotización."
            ),
            hashtags=["#InnovacionesTecnológicas", "#Mérida", "#Tecnología"],
        ),
        SocialPost(
            network="Instagram",
            text=(
                f"Transforma tu espacio con {idea.lower()}. "
                f"Calidad, tecnología y atención profesional en {city}."
            ),
            hashtags=["#MéridaYucatán", "#Innovación", "#SolucionesTecnológicas"],
        ),
        SocialPost(
            network="TikTok",
            text=(
                f"Esto es lo que debes saber antes de contratar "
                f"{idea.lower()}. Te mostramos la solución."
            ),
            hashtags=["#TikTokMéxico", "#Tecnología", "#Mérida"],
        ),
        SocialPost(
            network="WhatsApp",
            text=(
                f"Hola. En {company} contamos con el servicio de {idea.lower()} "
                f"en {city}. ¿Deseas recibir información o una cotización?"
            ),
            hashtags=[],
        ),
    ]

    calendar = [
        {"day": 1, "content": "Publicación de presentación", "network": "Facebook"},
        {"day": 2, "content": "Video corto educativo", "network": "Instagram"},
        {"day": 3, "content": "Historia con llamada a la acción", "network": "Instagram"},
        {"day": 4, "content": "Video vertical", "network": "TikTok"},
        {"day": 5, "content": "Publicación de beneficios", "network": "Facebook"},
        {"day": 6, "content": "Mensaje de seguimiento", "network": "WhatsApp"},
        {"day": 7, "content": "Testimonio o caso de éxito", "network": "Todas"},
    ]

    return CampaignResponse(
        campaign_name=campaign_name,
        objective=f"Generar prospectos interesados en {idea.lower()}",
        target_audience=target_audience,
        value_proposition=(
            f"{company} ofrece {idea.lower()} con atención profesional, "
            f"soluciones personalizadas y servicio en {city}."
        ),
        video_script=video_script,
        flyer=flyer,
        social_posts=posts,
        calendar=calendar,
        status="generated",
        created_at=datetime.now().isoformat(),
    )


@app.get("/app", response_class=HTMLResponse)
def web_app():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AURA AI</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0b1020;
            color: white;
        }
        .container {
            max-width: 1000px;
            margin: auto;
            padding: 40px 20px;
        }
        h1 { font-size: 42px; margin-bottom: 5px; }
        .subtitle { color: #9ca9c8; margin-bottom: 30px; }
        .card {
            background: #151d33;
            border: 1px solid #283452;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 22px;
        }
        textarea, input {
            width: 100%;
            padding: 14px;
            margin-top: 8px;
            margin-bottom: 15px;
            border-radius: 9px;
            border: 1px solid #354363;
            background: #0e1528;
            color: white;
            font-size: 16px;
        }
        textarea { min-height: 100px; resize: vertical; }
        button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 9px;
            background: #4f7cff;
            color: white;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover { background: #3b68e5; }
        button:disabled { opacity: .6; cursor: wait; }
        .result { display: none; }
        .section {
            background: #0e1528;
            border-radius: 10px;
            padding: 16px;
            margin-top: 14px;
        }
        li { margin-bottom: 8px; }
        .network {
            color: #7fa0ff;
            font-weight: bold;
        }
        .status { color: #66e0a3; }
    </style>
</head>
<body>
<div class="container">
    <h1>AURA AI</h1>
    <div class="subtitle">De una idea a una campaña completa</div>

    <div class="card">
        <label>¿Qué quieres promocionar?</label>
        <textarea id="idea"
            placeholder="Ejemplo: Instalación de paneles solares para casas"></textarea>

        <label>Ciudad</label>
        <input id="city" value="Mérida, Yucatán">

        <label>Empresa</label>
        <input id="company" value="Innovaciones Tecnológicas">

        <button id="generate" onclick="generateCampaign()">
            Crear campaña
        </button>
    </div>

    <div id="result" class="card result">
        <h2 id="campaignName"></h2>
        <div class="status">Campaña generada correctamente</div>

        <div class="section">
            <h3>Objetivo</h3>
            <p id="objective"></p>
        </div>

        <div class="section">
            <h3>Público objetivo</h3>
            <ul id="audience"></ul>
        </div>

        <div class="section">
            <h3>Propuesta de valor</h3>
            <p id="value"></p>
        </div>

        <div class="section">
            <h3>Guion del video</h3>
            <ol id="script"></ol>
        </div>

        <div class="section">
            <h3>Concepto del flyer</h3>
            <div id="flyer"></div>
        </div>

        <div class="section">
            <h3>Publicaciones</h3>
            <div id="posts"></div>
        </div>

        <div class="section">
            <h3>Calendario de 7 días</h3>
            <ol id="calendar"></ol>
        </div>
    </div>
</div>

<script>
async function generateCampaign() {
    const button = document.getElementById("generate");
    const idea = document.getElementById("idea").value.trim();

    if (idea.length < 5) {
        alert("Escribe una idea más completa.");
        return;
    }

    button.disabled = true;
    button.textContent = "AURA está creando la campaña...";

    try {
        const response = await fetch("/api/campaigns/generate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                idea: idea,
                city: document.getElementById("city").value,
                company: document.getElementById("company").value
            })
        });

        if (!response.ok) {
            throw new Error("No fue posible generar la campaña.");
        }

        const data = await response.json();

        document.getElementById("campaignName").textContent = data.campaign_name;
        document.getElementById("objective").textContent = data.objective;
        document.getElementById("value").textContent = data.value_proposition;

        document.getElementById("audience").innerHTML =
            data.target_audience.map(item => `<li>${item}</li>`).join("");

        document.getElementById("script").innerHTML =
            data.video_script.map(item => `<li>${item}</li>`).join("");

        document.getElementById("flyer").innerHTML = `
            <strong>${data.flyer.headline}</strong>
            <p>${data.flyer.subtitle}</p>
            <p>${data.flyer.benefits.join(" · ")}</p>
            <p><strong>CTA:</strong> ${data.flyer.call_to_action}</p>
            <p><strong>Estilo:</strong> ${data.flyer.style}</p>
        `;

        document.getElementById("posts").innerHTML =
            data.social_posts.map(post => `
                <div>
                    <p class="network">${post.network}</p>
                    <p>${post.text}</p>
                    <p>${post.hashtags.join(" ")}</p>
                    <hr>
                </div>
            `).join("");

        document.getElementById("calendar").innerHTML =
            data.calendar.map(item =>
                `<li>Día ${item.day}: ${item.content} — ${item.network}</li>`
            ).join("");

        document.getElementById("result").style.display = "block";
        document.getElementById("result").scrollIntoView({behavior: "smooth"});
    } catch (error) {
        alert(error.message);
    } finally {
        button.disabled = false;
        button.textContent = "Crear campaña";
    }
}
</script>
</body>
</html>
"""
