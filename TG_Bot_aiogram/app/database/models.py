from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
# створюємо асинхронний движок engine

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    # DeclarativeBase - це класовий міксін (mixin) у SQLAlchemy, який використовується
    # для визначення базового класу у схемі ORM (Object-Relational Mapping).
    pass


class User(Base):
    __tablename__ = 'users'  # створюємо таблицю users

    id: Mapped[int] = mapped_column(primary_key=True)  # Mapped використовується для аннотування типів даних у моделях
    # mapped_column(primary_key=True) вказує на те, що цей стовпець є первинним ключем
    tg_id = mapped_column(BigInteger)  # tg_id є стовпцем типу BigInteger (велике ціле число)



async def async_main():  # асинхронна функція, яку можна виконувати в контексті асинхронної петлі подій (event loop).
    # async_main створює таблиці у базі даних асинхронним чином
    async with engine.begin() as conn:  # Встановлення асинхронного контексту з'єднання
        # забезпечує правильне відкриття і закриття з'єднання
        # engine.begin() відкриває транзакцію з базою даних і повертає об'єкт з'єднання conn
        await conn.run_sync(Base.metadata.create_all)  # Виконання синхронної функції у асинхронному контексті
        # await очікує завершення асинхронної операції
        # run_sync дозволяє виконувати синхронну функцію create_all у асинхронному контексті