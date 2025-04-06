from bot.models.camera import Camera
from repository.base import BaseRepository


class CamerasRepository(BaseRepository):
    table_name = "cameras"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                camera_url TEXT
            )
        """
        await self.execute(create_table_query)

    async def create_camera(self, camera: Camera):
        await self.insert(num=camera.num, name=camera.name, camera_url=camera.camera_url)

    async def get_all_cameras(self) -> list[Camera]:
        cameras = await self.select_all()
        return sorted([Camera(**camera) for camera in cameras], key=lambda x: x.num)

    async def delete_camera(self, camera_name: str):
        await self.delete(name=camera_name)

    async def get_camera_by_id(self, camera_id: int) -> Camera:
        camera = await self.select_one(id=camera_id)
        return Camera(**camera)

    async def delete_all_cameras(self):
        await self.delete_all()
