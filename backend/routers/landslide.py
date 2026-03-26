"""
backend/routers/landslide.py
=============================
POST /api/landslide — Landslide Susceptibility mapping using GE Random Forest.
"""

import asyncio
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.analysis.landslide import analyze_landslide

logger = logging.getLogger(__name__)
router = APIRouter()


class LandslideRequest(BaseModel):
    geojson: dict


@router.post("/api/landslide")
async def run_landslide(req: LandslideRequest):
    """
    Landslide susceptibility analysis for the given AOI polygon.
    Uses a Random Forest classifier on a DEM terrain stack via GEE.
    """
    try:
        logger.info("Landslide analysis requested")

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: analyze_landslide(req.geojson),
        )

        return {"status": "success", **result}

    except Exception as e:
        logger.error(f"Landslide analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
