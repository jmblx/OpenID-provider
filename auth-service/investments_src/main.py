import asyncio

from investments_src.di_container import container
from investments_src.investments_service import InvestmentsService


async def main():
    async with container() as ioc:
        investments_service = await ioc.get(InvestmentsService)
        await investments_service.investments()

if __name__ == '__main__':
    asyncio.run(main())
