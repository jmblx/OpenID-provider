import json

from gigachat import GigaChat


class PredictionGateway:
    def __init__(self, gigachat: GigaChat):
        self.gigachat = gigachat

    def get_predictions(self, news: dict[str, list[str]], historical_data: dict) -> dict:
    #     # Формируем промпт для модели
        prompt_template = """
    У нас есть исторические данные по следующим типам активов: bonds (облигации), currencies (валюты), gold (золото), shares (акции). Также есть аналитика последних 7 дней и информация о политических и экономических новостях. На основе этой информации нужно сделать прогноз цен на следующие 7 дней.

    Исторические данные за последние 7 дней:
    {historical_data}

    На основе данных о последних 7 днях (анализируй рынок и динамику) и следующих новостей:
    {news_data}

    Сделай прогноз цен на следующие 7 дней для всех активов (bonds, currencies, gold, shares). Твоя цель — предсказать цены, указав дату и тип актива.
    """

        # Преобразуем данные в JSON
        historical_data_json = json.dumps(historical_data, ensure_ascii=False, indent=2)
        news_data_json = json.dumps(news, ensure_ascii=False, indent=2)

        prompt = prompt_template.format(
            historical_data=historical_data_json,
            news_data=news_data_json,
        )
    return self.gigachat.chat(prompt)
    #
    #     response = self.gigachat.chat(prompt)
    #     result = response.choices[0].message.content
    #
    #     try:
    #         predictions = json.loads(result)
    #     except json.JSONDecodeError:
    #         raise ValueError("Ошибка парсинга ответа модели GigaChat")

        return


