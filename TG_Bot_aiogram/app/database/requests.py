from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with async_session() as session:  # зберігаємо асинхронну сесію у змінну sesion
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        # scalar(): This method returns the first column of the first row in the result.
        # If the result is empty, it returns None
        # user = await session.execute(select(User.id).where(User.tg_id == tg_id))
        # те ж саме, тільки без scalar()

        if not user:
            session.add(User(tg_id=tg_id))  # створюється новий об'єкт User і додається в сесію
            await session.commit()  # зберігаємо зміни в БД