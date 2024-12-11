from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ReadStrategyDTO:



class StrategyReader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def read_by_id(self, strategy_id: int) -> ReadStrategyDTO:

