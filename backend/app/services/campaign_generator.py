from app.schemas import CampaignCreate


def _tone_words(tone: str):
    if tone == "friendly":
        return {
            "style": "Cercano, claro y confiable",
            "cta": "Escríbenos y con gusto te asesoramos",
        }
    if tone == "premium":
        return {
            "style": "Elegante, exclusivo y tecnológico",
            "cta": "Agenda una asesoría privada",
        }
    return {
        "style": "Profesional, moderno y directo",
        "cta": "Solicita una cotización hoy",
    }


def generate_campaign_package(data: CampaignCreate) -> dict:
    idea = data.idea.strip()
    city = data.city.strip()
    company = data.company.strip()
    tone = _tone_words(data.tone)

    objective_map = {
        "leads": f"Generar prospectos interesados en {idea.lower()}",
        "sales": f"Incrementar ventas de {idea.lower()}",
        "awareness": f"Posicionar a {company} como referente en {idea.lower()}",
    }

    target_audience = [
        f"Personas y empresas ubicadas en {city}",
        "Clientes que valoran atención profesional y soluciones confiables",
        f"Usuarios con intención de compra relacionada con {idea.lower()}",
    ]

    value_proposition = (
        f"{company} ofrece {idea.lower()} en {city}, con atención personalizada, "
        "asesoría profesional y una solución adaptada a cada cliente."
    )

    video_script = [
        f"Gancho: ¿Estás buscando {idea.lower()} en {city}?",
        "Problema: Muchas personas eligen soluciones sin asesoría y terminan pagando más.",
        f"Solución: {company} analiza tu necesidad y propone una opción profesional.",
        "Beneficios: Atención personalizada, calidad, seguimiento y soporte.",
        f"Llamada a la acción: {tone['cta']}.",
    ]

    social_posts = [
        {
            "network": "Facebook",
            "text": (
                f"¿Necesitas {idea.lower()} en {city}? En {company} te ayudamos con "
                "asesoría profesional, atención personalizada y una solución a tu medida. "
                f"{tone['cta']}."
            ),
            "hashtags": ["#InnovacionesTecnológicas", "#Mérida", "#Tecnología"],
        },
        {
            "network": "Instagram",
            "text": (
                f"Convierte tu idea en una solución real con {idea.lower()}. "
                f"Servicio profesional en {city}. {tone['cta']}."
            ),
            "hashtags": ["#MéridaYucatán", "#Innovación", "#SolucionesTecnológicas"],
        },
        {
            "network": "TikTok",
            "text": (
                f"3 cosas que debes revisar antes de contratar {idea.lower()}. "
                "La tercera puede ahorrarte dinero y problemas."
            ),
            "hashtags": ["#TikTokMéxico", "#Tecnología", "#Mérida"],
        },
        {
            "network": "WhatsApp",
            "text": (
                f"Hola. En {company} ofrecemos {idea.lower()} en {city}. "
                "¿Te comparto información y una cotización preliminar?"
            ),
            "hashtags": [],
        },
    ]

    calendar = [
        {"day": 1, "content": "Flyer principal", "network": "Facebook e Instagram"},
        {"day": 2, "content": "Video educativo de 20 segundos", "network": "Reels y TikTok"},
        {"day": 3, "content": "Historia con encuesta", "network": "Instagram"},
        {"day": 4, "content": "Publicación de beneficios", "network": "Facebook"},
        {"day": 5, "content": "Caso de éxito o demostración", "network": "Instagram"},
        {"day": 6, "content": "Seguimiento a prospectos", "network": "WhatsApp"},
        {"day": 7, "content": "Oferta o llamada a la acción", "network": "Todas"},
    ]

    return {
        "campaign_name": f"{idea[:48]} | {city}",
        "objective": objective_map[data.objective],
        "target_audience": target_audience,
        "value_proposition": value_proposition,
        "tone": tone["style"],
        "video_script": video_script,
        "flyer": {
            "headline": idea.upper(),
            "subtitle": f"Soluciones profesionales en {city}",
            "benefits": [
                "Atención personalizada",
                "Asesoría profesional",
                "Cotización sin compromiso",
            ],
            "call_to_action": tone["cta"],
            "format": "1080 x 1350 px",
            "style": tone["style"],
        },
        "social_posts": social_posts,
        "calendar": calendar,
        "status": "generated",
    }
