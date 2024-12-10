import json

from gigachat import GigaChat


class PredictionGateway:
    def __init__(self, gigachat: GigaChat):
        self.gigachat = gigachat

    def get_predictions(self, news: dict[str, list[str]], last_7_days_results: dict[str, dict]) -> dict:
        # Формируем исторические данные отдельно
        historical_data_example = {
            "bonds": {
                "10.12.2024": {
                    "Облигация ОФЗ-26238-ПД": {
                        "price": "506,96 ₽",
                        "sector": "Потребительские услуги",
                        "country": "Россия",
                        "exchange": "Московская биржа",
                    }
                }
            },
            "currencies": {
                "10.12.2024": {
                    "Доллар США": {
                        "price": 99.3759,
                        "code": "USD",
                    }
                }
            },
            "gold": {"10.12.2024": {"price": 8426.19}},
            "shares": {
                "10.12.2024": {
                    "Акции Аэрофлот (AFLT)": {
                        "price": "51,18 ₽",
                        "sector": "Транспорт",
                        "country": "Россия",
                        "exchange": "Московская биржа",
                    }
                }
            },
        }

        # Формируем промпт для модели
        prompt_template = """
    У нас есть исторические данные по следующим типам активов: bonds (облигации), currencies (валюты), gold (золото), shares (акции). Также есть аналитика последних 7 дней и информация о политических и экономических новостях. На основе этой информации нужно сделать прогноз цен на следующие 7 дней.

    Пример исторических данных:
    {historical_data}

    На основе данных о последних 7 днях (анализируй рынок и динамику) и следующих новостей:
    {news_data}
    Вот данные прошедших 7 дней:
    {last_7_days_results}
    Сделай прогноз цен на следующие 7 дней для всех активов (bonds, currencies, gold, shares). Твоя цель — предсказать цены, указав дату и тип актива. Прогноз новостей учитывай как дополнительное подспорье, основной акцент на рынке и динамике.

    Верни результат строго в следующем формате JSON:
{
    "2024-12-11": {
        "bonds": {
            "Облигация ОФЗ-26238-ПД": {
                "predicted_price": "512,00 ₽",
                "predicted_change": "1.00%"
            }
        },
        "currencies": {
            "Доллар США": {
                "predicted_price": 100.50,
                "predicted_change": "1.13%"
            }
        },
        "gold": {
            "predicted_price": 8500.00,
            "predicted_change": "0.88%"
        },
        "shares": {
            "Акции Аэрофлот (AFLT)": {
                "predicted_price": "52,50 ₽",
                "predicted_change": "2.57%"
            }
        }
    },
    "2024-12-12": {
        ...
    }
}

Твои прогнозы должны учитывать текущие цены как базу для расчета изменений (predicted_change). 
Прогноз предоставь на 7 следующих дней.

Описание формата ответа

    Каждый ключ (дата) — прогноз на конкретный день.
    Вложенные категории (bonds, currencies, gold, shares) — типы активов.
    Детализация каждого актива:
        predicted_price: спрогнозированная цена.
        predicted_change: процент изменения по сравнению с текущей ценой.

Обработка ответа и объединение данных

После получения прогноза данные объединяются с существующими:

    Последний известный день содержит:
        Текущие цены.
        Аналитику изменений за прошедшие 7 дней.
        Прогнозируемое изменение для дня через 7 дней.

    Для следующих 7 дней используется только спрогнозированная моделью информация.
    """
        historical_data_json = json.dumps(historical_data_example, ensure_ascii=False, indent=2)
        news_data_json = json.dumps(news, ensure_ascii=False, indent=2)

        prompt = prompt_template.format(
            historical_data=historical_data_json,
            news_data=news_data_json,
        )

        # Отправляем запрос в модель
        response = self.gigachat.chat(prompt)
        result = response.choices[0].message.content

        # Преобразуем текстовый ответ в словарь
        try:
            predictions = json.loads(result)
        except json.JSONDecodeError:
            raise ValueError("Ошибка парсинга ответа модели GigaChat")

        return predictions

