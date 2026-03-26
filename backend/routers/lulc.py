"""
backend/routers/lulc.py
========================
POST /api/lulc — Land Use Land Cover classification using Google Dynamic World.
"""

import asyncio
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.analysis.lulc import analyze_lulc

logger = logging.getLogger(__name__)
router = APIRouter()


class LULCRequest(BaseModel):
    geojson: dict
    year: Optional[int] = None
    season: str = "annual"


@router.post("/api/lulc")
async def run_lulc(req: LULCRequest):
    """
    Classify land use / land cover for the given AOI polygon.
    Uses Google Dynamic World (10m resolution) via GEE.
    """
    try:
        logger.info(f"LULC analysis requested — year={req.year}, season={req.season}")

        # Run blocking GEE call in a thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: analyze_lulc(req.geojson, req.year, req.season),
        )

        return {"status": "success", **result}

    except Exception as e:
        logger.error(f"LULC analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
