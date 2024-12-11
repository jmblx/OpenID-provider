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

        # Целевая дата
        target_date = datetime(2024, 12, 10)
        target_date_str = target_date.strftime("%d.%m.%Y")

        for strategy in user_strategies.strategies:
            portfolio = strategy.portfolio
            for key, value in portfolio.items():
                if key not in data:
                    continue  # Пропускаем, если данных по ключу нет

                c_d = data[key]  # Данные по активу (например, облигации)

                # Проверяем, есть ли данные на целевую дату
                if target_date_str in c_d:
                    c_d = c_d[target_date_str]
                    print(f"Данные на целевую дату {target_date_str} для актива {key}: {c_d}")
                else:
                    print(f"Данных на целевую дату {target_date_str} для актива {key} нет. Пропускаем...")
                    continue

                # Обрабатываем инвестиции для каждого актива
                for el in value:
                    print(f"Обрабатываем инвестицию: {el.get('name')}")
                    investment = c_d.get(el.get("name"))
                    if investment:
                        percent_last = investment.get("last_7_day_diff_in_%")
                        percent_next = investment.get("next_7_day_diff_in_%")

                        # Обработка процентов за последние 7 дней
                        if percent_last:
                            print(f"Процентная разница за последние 7 дней для {el.get('name')}: {percent_last}")
                            percent_last = float(percent_last.replace("%", ""))  # Преобразуем в число
                            if percent_last > 3:
                                notifications.append(
                                    f"У вас есть инвестиции в {el.get('name')} с большой положительной разницей в процентном росте за последние 7 дней: {percent_last}%")
                            elif percent_last < -3:
                                notifications.append(
                                    f"У вас есть инвестиции в {el.get('name')} с большой отрицательной разницей в цене за последние 7 дней: {percent_last}%")
                            else:
                                notifications.append(
                                    f"У вас есть инвестиции в {el.get('name')} с маленькой разницей в процентном изменении за последние 7 дней: {percent_last}%")

                        # Обработка предсказанных процентов на следующие 7 дней
                        if percent_next:
                            print(f"Предсказываемая разница за следующие 7 дней для {el.get('name')}: {percent_next}")
                            percent_next = float(percent_next.replace("%", ""))
                            if percent_next > 3:
                                notifications.append(
                                    f"У вас есть инвестиции в {el.get('name')} с большой предсказываемой разницей в процентном росте на следующие 7 дней: {percent_next}%")
                            elif percent_next < -3:
                                notifications.append(
                                    f"У вас есть инвестиции в {el.get('name')} с большой предсказываемой отрицательной разницей в цене на следующие 7 дней: {percent_next}%")
                            else:
                                notifications.append(
                                    f"У вас есть инвестиции в {el.get('name')} с маленькой предсказываемой разницей в процентном изменении на следующие 7 дней: {percent_next}%")
                    else:
                        print(f"Инвестиция {el.get('name')} не найдена в данных на целевую дату.")
        return notifications
