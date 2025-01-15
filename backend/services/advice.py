from fastapi.exceptions import HTTPException

from agent.utils import LlmModelType
from agent.graphs import ConsultantGraph
from backend.utils.method import extract_text_from_file

class AdviceService:
    async def generate(self, data):

        type = data['file'].filename.split('.')[-1]
        contents = await data['file'].read()

        if type == 'txt':
            text = contents.decode('utf-8')
        else:
            text = extract_text_from_file(data['file'], contents)

        agent = ConsultantGraph(
            model_type=LlmModelType.QWEN,
            show_logs=True, 
            save_online_metric=False
        )        
        res = agent.invoke(query=text, activity_name=data['activity'], category_name=data['category']).content
        
        if not isinstance(res, list):
            raise HTTPException(status_code=400, detail="Извините, по вашему запросу нет информации.")

        return {'response': res}
    


