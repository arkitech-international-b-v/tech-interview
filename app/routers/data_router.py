import json
from typing import Optional
from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from app.services.data_service import DataService
from fastapi import Depends
from bson import json_util
from datetime import datetime, timedelta
router = APIRouter()


@router.get("/data/all")
def get_all_data(
    limit: int = Query(100, gt=0, le=1000),
    topic: Optional[str] = None,
    data_service = Annotated[DataService, Depends()]    
):
    """Get all the latest HVAC data from all zones"""
    try:
            data_service = DataService()
            # Get items from MongoDB
            cursor = data_service.get_latest_items(limit, topic)
            
            # Convert to list and serialize properly
            items = list(cursor)
            
            # Use json_util to handle MongoDB-specific types
            return JSONResponse(
                content=json.loads(json_util.dumps(items))
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
