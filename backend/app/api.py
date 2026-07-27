from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from app.db import (
    create_campaign,
    create_lead,
    get_campaign,
    get_dashboard,
    list_campaigns,
    list_leads,
    update_lead_status,
)
from app.schemas import CampaignCreate, LeadCreate, LeadStatusUpdate
from app.services.campaign_generator import generate_campaign_package
from app.services.flyer_generator import create_flyer_svg

router = APIRouter()


@router.get("/dashboard")
def dashboard():
    return get_dashboard()


@router.post("/campaigns")
def campaigns_create(payload: CampaignCreate):
    package = generate_campaign_package(payload)
    record = create_campaign(payload, package)
    flyer_url = create_flyer_svg(record["id"], package)
    record["flyer_url"] = flyer_url
    return record


@router.get("/campaigns")
def campaigns_list():
    return list_campaigns()


@router.get("/campaigns/{campaign_id}")
def campaigns_get(campaign_id: int):
    campaign = get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaña no encontrada")
    return campaign


@router.get("/campaigns/{campaign_id}/export.txt", response_class=PlainTextResponse)
def campaigns_export(campaign_id: int):
    campaign = get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaña no encontrada")

    package = campaign["package"]
    lines = [
        f"AURA AI - {campaign['name']}",
        "=" * 60,
        f"Objetivo: {package['objective']}",
        "",
        "PÚBLICO OBJETIVO",
        *[f"- {item}" for item in package["target_audience"]],
        "",
        "GUION DE VIDEO",
        *[f"{i+1}. {item}" for i, item in enumerate(package["video_script"])],
        "",
        "PUBLICACIONES",
    ]
    for post in package["social_posts"]:
        lines.extend([
            "",
            post["network"],
            post["text"],
            " ".join(post["hashtags"]),
        ])
    return "\n".join(lines)


@router.post("/leads")
def leads_create(payload: LeadCreate):
    return create_lead(payload)


@router.get("/leads")
def leads_list():
    return list_leads()


@router.patch("/leads/{lead_id}/status")
def leads_update_status(lead_id: int, payload: LeadStatusUpdate):
    lead = update_lead_status(lead_id, payload.status)
    if not lead:
        raise HTTPException(status_code=404, detail="Prospecto no encontrado")
    return lead
