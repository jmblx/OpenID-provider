from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from application.strategy.create_new_hanlder import CreateNewStrategyCommand, CreateNewStrategyHanlder

strategy_router = APIRouter(route_class=DishkaRoute, tags=["strategy"])


@strategy_router.post("/strategy")
async def add_strategy(handler: FromDishka[CreateNewStrategyHanlder], command: CreateNewStrategyCommand):
    return await handler.handle(command)
