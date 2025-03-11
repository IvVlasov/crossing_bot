from repository.base import BaseRepository
from bot.models.template import Template
from bot.models.crossing_config import CrossingMode


class TemplatesRepository(BaseRepository):
    table_name = "templates"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crossing_mode TEXT NOT NULL,
                button_name TEXT NOT NULL,
                message TEXT NOT NULL,
                buttons_list TEXT DEFAULT NULL
            )
        """
        await self.execute(create_table_query)
        await self.create_if_not_exists(Template(crossing_mode="winter", button_name="Движение открыто", message="Движение по ледовой переправе Салехард-Лабытнанги открыто для автомобилей массой до _ тонн.", buttons_list="30 тонн, 25 тонн, 15 тонн, 15 тонн, 5 тонн, 3.5 тонны"))
        await self.create_if_not_exists(Template(crossing_mode="winter", button_name="Закрыто из-за погоды", message="Движение по ледовой переправе Салехард-Лабытнанги закрыто из-за неблагоприятных погодных условий.", buttons_list=None))
        await self.create_if_not_exists(Template(crossing_mode="winter", button_name="Закрыто", message="Движение по ледовой переправе Салехард-Лабытнанги закрыто.", buttons_list=None))
        await self.create_if_not_exists(Template(crossing_mode="summer", button_name="Работает в обычном режиме", message="Переправа работает в обычном режиме, на линии _ парома(ов).", buttons_list="1, 2, 3, 4, 5, 6"))
        await self.create_if_not_exists(Template(crossing_mode="summer", button_name="Работает в ограниченном режиме", message="Переправа работает в ограниченном режиме. На линии _ парома(ов).", buttons_list="1, 2, 3, 4"))
        await self.create_if_not_exists(Template(crossing_mode="summer", button_name="Движение приостановлено", message="Движение паромов приостановлено.", buttons_list=None))
        await self.create_if_not_exists(Template(crossing_mode="summer", button_name="Пробный рейс для пассажиров", message="Пробный рейс для пассажиров (без авто)  в _.", buttons_list="время"))
        await self.create_if_not_exists(Template(crossing_mode="summer", button_name="Пробный рейс для авто", message="Пробный рейс для пассажиров и легковых автомобилей в _.", buttons_list="время"))
        await self.create_if_not_exists(Template(crossing_mode="interseason", button_name="Переправа закрыта Работает подушка", message="Ледовая переправа закрыта. Перевозку пассажиров осуществляют суда на воздушной подушке.", buttons_list=None))
        await self.create_if_not_exists(Template(crossing_mode="interseason", button_name="Подушка закрыта из-за погоды", message="Суда на воздушной подушке временно приостановили свою работу по погодным условиям.", buttons_list=None))
        await self.create_if_not_exists(Template(crossing_mode="interseason", button_name="Подушка закрыта", message="Суда на воздушной подушке временно приостановили свою работу.", buttons_list=None))

    async def create_or_update_template(self, template: Template):
        await self.delete(button_name=template.button_name)
        await self.insert(
            crossing_mode=template.crossing_mode,
            button_name=template.button_name,
            message=template.message,
            buttons_list=template.buttons_list,
        )

    async def create_if_not_exists(self, template: Template):
        cur_template = await self.select_one(button_name=template.button_name)
        if not cur_template:
            await self.insert(
                crossing_mode=template.crossing_mode,
                button_name=template.button_name,
                message=template.message,
                buttons_list=template.buttons_list,
            )

    async def get_all_templates(self, crossing_mode: CrossingMode) -> list[Template]:
        templates = await self.select_all(crossing_mode=crossing_mode.value)
        return [Template(**template) for template in templates]

    async def get_template(self, id: int) -> Template:
        template = await self.select_one(id=id)
        return Template(**template)
