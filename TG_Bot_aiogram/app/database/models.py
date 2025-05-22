from sqlalchemy import BigInteger, String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime, timedelta

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
# створюємо асинхронний движок engine

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    # DeclarativeBase - це класовий міксін (mixin) у SQLAlchemy, який використовується
    # для визначення базового класу у схемі ORM (Object-Relational Mapping).
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)  # Первинний ключ
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)  # Telegram ID користувача
    name: Mapped[str | None] = mapped_column(String, nullable=True)  # Ім'я користувача (може бути пустим)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: (datetime.utcnow() + timedelta(hours=3)).replace(microsecond=0))
    click_count: Mapped[int] = mapped_column(Integer, default=0)  # Кількість викликів функцій бота
    last_activity: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # Дата останньої активності



async def async_main():  # асинхронна функція, яку можна виконувати в контексті асинхронної петлі подій (event loop).
    # async_main створює таблиці у базі даних асинхронним чином
    async with engine.begin() as conn:  # Встановлення асинхронного контексту з'єднання
        # забезпечує правильне відкриття і закриття з'єднання
        # engine.begin() відкриває транзакцію з базою даних і повертає об'єкт з'єднання conn
        await conn.run_sync(Base.metadata.create_all)  # Виконання синхронної функції у асинхронному контексті
        # await очікує завершення асинхронної операції
        # run_sync дозволяє виконувати синхронну функцію create_all у асинхронному контексті