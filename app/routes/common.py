from fastapi import APIRouter,Depends
from app.service.scrape import ScrapeService
from fastapi.responses import JSONResponse
from app.model.request_validation import ScrapeRequestModel
from app.utils.auth import get_current_active_user
from app.model.user_model import User

router = APIRouter()

@router.get('/health')
async def health():
    return JSONResponse(status_code=200, content={"status":"ok"})


@router.post('/scrape')
async def __scrape(model : ScrapeRequestModel,current_user: User = Depends(get_current_active_user)):
    success,message = ScrapeService(model).scrape_service()
    respose_dict = {
        "success": success,
        "data": message,
    }
    if success:
        http_status_code = 200
    else:
        http_status_code = 500
    return JSONResponse(status_code=http_status_code, content=respose_dict)
