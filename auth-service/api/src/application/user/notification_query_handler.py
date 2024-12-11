from datetime import datetime

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
        data = await self.investments_service.get_investments()
        c = 0
        for strategy in user_strategies.strategies:
            c += 1
            portfolio = strategy.portfolio
            for key, value in portfolio.items():
                if key not in data:
                    continue  # Пропускаем, если данных по ключу нет
                c_d = data[key]
                today = datetime.now()

                # Целевая дата
                target_date = datetime(2024, 12, 10)

                # Разница в днях
                difference = (target_date - today).days

                if today.strftime("%d.%m.%Y") in c_d:
                    c_d = c_d[today.strftime("%d.%m.%Y")]
                else:
                    continue  # Пропускаем, если нет данных на сегодняшнюю дату

                if difference >= 3:
                    if target_date.strftime("%d.%m.%Y") in c_d:
                        c_d = c_d.get(target_date.strftime("%d.%m.%Y"))
                    else:
                        continue  # Пропускаем, если нет данных на целевую дату

                    for el in value:
                        investment = c_d.get(el.get("name"))
                        if investment:
                            percent = investment.get("last_7_day_diff_in_%")
                            if percent:
                                percent = int(percent.replace("%", ""))
                                if percent > 3:
                                    notifications.append(
                                        f"У вас есть инвестиции в {el.get('name')} с большой положительной разницей в процентном ростом {percent}%")
                                elif percent < 3:
                                    notifications.append(
                                        f"У вас есть инвестиции в {el.get('name')} с большой отрицательной разницей в цене за последнюю неделю: {percent}%")
                                else:
                                    notifications.append(
                                        f"У вас есть инвестиции в {el.get('name')} с маленькой разницей в процентным изменением {percent}%")
        return notifications

