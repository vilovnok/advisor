from fastapi import UploadFile

from ..schemas.advice import AdviceSchemas
from fastapi.exceptions import HTTPException

from agent.utils import LlmModelType
from agent.graphs import ConsultantGraph

class AdviceService:
    async def generate(self, data):
        contents = await data['file'].read()
        text = contents.decode("utf-8")        
        
        agent = ConsultantGraph(
            model_type=LlmModelType.QWEN,
            show_logs=True, 
            save_online_metric=False
        )        
        res = agent.invoke(query=text, catalog_name=data['fileType']).content
        
        if not isinstance(res, list):
            raise HTTPException(status_code=400, detail="Извините, по вашему запросу нет информации.")

        return {'response':res}


