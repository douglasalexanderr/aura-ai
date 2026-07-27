from typing import Literal

from pydantic import BaseModel, Field


class CampaignCreate(BaseModel):
    idea: str = Field(min_length=5, max_length=500)
    city: str = Field(default="Mérida, Yucatán", min_length=2, max_length=120)
    company: str = Field(default="Innovaciones Tecnológicas", min_length=2, max_length=120)
    objective: Literal["leads", "sales", "awareness"] = "leads"
    tone: Literal["professional", "friendly", "premium"] = "professional"


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=5, max_length=40)
    email: str = Field(default="", max_length=160)
    service: str = Field(min_length=2, max_length=160)
    source: str = Field(default="Manual", max_length=80)
    notes: str = Field(default="", max_length=1000)


class LeadStatusUpdate(BaseModel):
    status: Literal["Nuevo", "Contactado", "Cotizado", "Ganado", "Perdido"]
