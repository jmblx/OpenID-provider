from application.common.id_provider import IdentityProvider
from application.user.interfaces.reader import UserReader
from infrastructure.external_services.investments.service import InvestmentsService


class NotificationQueryHandler:
    def __init__(self, idp: IdentityProvider, user_reader: UserReader, investments_service: InvestmentsService):
        self.idp = idp
        self.user_reader = user_reader
        self.investments_service = investments_service

    async def handle(self) -> list[str]:
        user_id = self.idp.get_current_user_id()
        user_strategies = await self.user_reader.get_user_strategies_by_id(user_id)

        notifications = []

        for strategy in user_strategies.strategies:
            try:
                notifications.extend(await self.investments_service.check_for_significant_changes(strategy.portfolio))
                notifications.extend(await self.investments_service.check_strategy_end_date(strategy.end_date))
            except Exception as e:
                print(f"Ошибка при обработке стратегии {strategy.strategy_id}: {e}")

        return notifications
