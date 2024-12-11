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
                print(f"Разница между сегодняшним днем и целевой датой: {difference} дней")

                if today.strftime("%d.%m.%Y") in c_d:
                    c_d = c_d[today.strftime("%d.%m.%Y")]
                    print(f"Данные на сегодня для актива {key}: {c_d}")  # Логируем данные на сегодня
                else:
                    print(f"Данных на сегодня для актива {key} нет. Пропускаем...")
                    continue  # Пропускаем, если нет данных на сегодняшнюю дату

                if 3 >= difference >= -3:
                    print(f"Прошло {difference} дней, проверяем данные на целевую дату...")

                    if target_date.strftime("%d.%m.%Y") in c_d:
                        c_d = c_d.get(target_date.strftime("%d.%m.%Y"))
                        print(f"Данные на целевую дату {target_date.strftime('%d.%m.%Y')}: {c_d}")
                    else:
                        print(f"Данных на целевую дату {target_date.strftime('%d.%m.%Y')} нет. Пропускаем...")
                        continue  # Пропускаем, если нет данных на целевую дату

                    for el in value:
                        print(f"Обрабатываем инвестицию: {el.get('name')}")  # Логируем инвестицию
                        investment = c_d.get(el.get("name"))
                        if investment:
                            percent_last = investment.get("last_7_day_diff_in_%")
                            percent_next = investment.get("next_7_day_diff_in_%")

                            # Обработка разницы за последние 7 дней
                            if percent_last:
                                print(f"Процентная разница за последние 7 дней для {el.get('name')}: {percent_last}")
                                try:
                                    percent_last = int(percent_last.replace("%", ""))
                                    if percent_last > 3:
                                        notifications.append(
                                            f"У вас есть инвестиции в {el.get('name')} с большой положительной разницей в процентном росте за последние 7 дней: {percent_last}%")
                                        print(
                                            f"Добавлено уведомление о положительном процентном росте за последние 7 дней для {el.get('name')}: {percent_last}%")
                                    elif percent_last < 3:
                                        notifications.append(
                                            f"У вас есть инвестиции в {el.get('name')} с большой отрицательной разницей в цене за последние 7 дней: {percent_last}%")
                                        print(
                                            f"Добавлено уведомление о отрицательном процентном росте за последние 7 дней для {el.get('name')}: {percent_last}%")
                                    else:
                                        notifications.append(
                                            f"У вас есть инвестиции в {el.get('name')} с маленькой разницей в процентном изменении за последние 7 дней: {percent_last}%")
                                        print(
                                            f"Добавлено уведомление о маленькой разнице за последние 7 дней для {el.get('name')}: {percent_last}%")
                                except ValueError:
                                    print(
                                        f"Неверный формат значения процента для {el.get('name')} за последние 7 дней.")

                            # Обработка предсказываемой разницы за следующие 7 дней
                            if percent_next:
                                print(
                                    f"Предсказываемая разница за следующие 7 дней для {el.get('name')}: {percent_next}"
                                )
                                percent_next = int(percent_next.replace("%", ""))
                                if percent_next > 3:
                                    notifications.append(
                                        f"У вас есть инвестиции в {el.get('name')} с большой предсказываемой разницей в процентном росте на следующие 7 дней: {percent_next}%")
                                    print(
                                        f"Добавлено уведомление о предсказываемом положительном процентном росте на следующие 7 дней для {el.get('name')}: {percent_next}%")
                                elif percent_next < 3:
                                    notifications.append(
                                        f"У вас есть инвестиции в {el.get('name')} с большой предсказываемой отрицательной разницей в цене на следующие 7 дней: {percent_next}%")
                                    print(
                                        f"Добавлено уведомление о предсказываемом отрицательном процентном росте на следующие 7 дней для {el.get('name')}: {percent_next}%")
                                else:
                                    notifications.append(
                                        f"У вас есть инвестиции в {el.get('name')} с маленькой предсказываемая разницей в процентном изменении на следующие 7 дней: {percent_next}%")
                                    print(
                                        f"Добавлено уведомление о маленькой разнице на следующие 7 дней для {el.get('name')}: {percent_next}%")
        return notifications
