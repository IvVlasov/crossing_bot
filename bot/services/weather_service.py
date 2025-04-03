import aiohttp
from settings import get_settings
from bot.models import CurrentWeather


class WeatherService:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com"
        self.endpoint = "/v1/forecast"
        self.settings = get_settings()
        self.search_params = "temperature_2m,wind_speed_10m,visibility"

    async def _get(self, url: str, params: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
        return result

    async def get_current_weather(self) -> CurrentWeather:
        params = {
            "latitude": self.settings.LATITUDE,
            "longitude": self.settings.LONGITUDE,
            "current": self.search_params,
        }
        data = await self._get(self.base_url + self.endpoint, params)
        return CurrentWeather(**data["current"])

    async def get_weather_text(self) -> str:
        result = ""
        weather = await self.get_current_weather()
        result += f"🌡 Температура: {weather.temperature}°C\n"
        result += f"💨 Скорость ветра: {weather.wind_speed_ms} м/с\n"
        # result += f"👀 Видимость: {weather.visibility} м\n"
        return result
