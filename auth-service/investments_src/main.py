import asyncio

from di_container import container
from investments_service import InvestmentsService


async def main():
    async with container() as ioc:
        investments_service: InvestmentsService = await ioc.get(InvestmentsService)
        await investments_service.collect_all_data()

if __name__ == '__main__':
    asyncio.run(main())
