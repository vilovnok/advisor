from fastapi import APIRouter, UploadFile, File, Form
from ..services.advice import AdviceService
from ..schemas.advice import AdviceSchemas

router = APIRouter(
    prefix='/v1/advice',
    tags=['Advice']
)

@router.post('/generate', status_code=201)
async def advice(
     file: UploadFile = File(...),
    fileType: str = Form(...),
):
    data = {
        "file": file,
        "fileType": fileType,
    }
    res = await AdviceService().generate(data)
    return res
