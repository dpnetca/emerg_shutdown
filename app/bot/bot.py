from fastapi import APIRouter, Body

from app.services.bot_svc import bot

router = APIRouter()


@router.post("/", include_in_schema=False)
def bot_hook(request=Body(...)):
    bot.process_request(request)

    # data = json.loads(request.body)
    # print(data)
    return {"message": "success"}
