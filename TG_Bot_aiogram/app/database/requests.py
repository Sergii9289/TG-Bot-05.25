from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select
from datetime import datetime, timedelta


async def set_user(tg_id: int, name: str | None) -> None:
    async with async_session() as session:  # зберігаємо асинхронну сесію у змінну sesion
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        # scalar(): This method returns the first column of the first row in the result.
        # If the result is empty, it returns None
        # user = await session.execute(select(User.id).where(User.tg_id == tg_id))
        # те ж саме, тільки без scalar()

        if not user:
            session.add(User(tg_id=tg_id, name=name))  # створюється новий об'єкт User і додається в сесію
            await session.commit()  # зберігаємо зміни в БД

async def update_user_activity(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.click_count += 1  # Збільшуємо лічильник викликів
            # Оновлюємо час останньої активності
            user.last_activity = (datetime.utcnow() + timedelta(hours=3)).replace(microsecond=0)
            # Додаємо 3 години

            await session.commit()