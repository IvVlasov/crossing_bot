from bot.models.camera import Camera
from repository.base import BaseRepository


class CamerasRepository(BaseRepository):
    table_name = "cameras"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                camera_url TEXT
            )
        """
        await self.execute(create_table_query)

    async def create_or_update_camera(self, camera: Camera):
        await self.insert(name=camera.name, camera_url=camera.camera_url)
        await self.update(
            set_conditions={"camera_url": camera.camera_url}, name=camera.name
        )

    async def get_all_cameras(self) -> list[Camera]:
        cameras = await self.select_all()
        return [Camera(**camera) for camera in cameras]

    async def delete_camera(self, camera_name: str):
        await self.delete(name=camera_name)

    # async def get_camera_by_id(self, camera_id: int) -> Camera:
    #     camera = await self.select_one(id=camera_id)
    #     return Camera(**camera)

    # async def get_crossings_by_ids(
    #     self, crossings_ids: list[int] | None
    # ) -> list[Camera]:
    #     if not crossings_ids:
    #         return []
    #     query = f"SELECT {self.table_name}.* FROM {self.table_name} WHERE id IN ({', '.join(map(str, crossings_ids))})"
    #     result = await self.execute_fetchall(query)
    #     return [Camera(**crossing) for crossing in result]
