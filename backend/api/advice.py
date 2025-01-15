from fastapi import APIRouter, UploadFile, File, Form
from ..services.advice import AdviceService

router = APIRouter(
    prefix='/v1/advice',
    tags=['Advice']
)

@router.post('/generate', status_code=201)
async def advice(
    file: UploadFile = File(...),
    activity: str = Form(...),
    category: str = Form(...),
):
    data = {
        "file": file,
        "activity": activity,
        "category": category
    }
    res = await AdviceService().generate(data)
    return res
