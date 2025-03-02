from pydantic import BaseModel, Field


class CurrentWeather(BaseModel):
    temperature: float = Field(alias="temperature_2m")
    wind_speed: float = Field(alias="wind_speed_10m")
    visibility: float = Field(alias="visibility")

    @property
    def wind_speed_ms(self) -> float:
        return round(self.wind_speed * 1000 / 3600, 2)
