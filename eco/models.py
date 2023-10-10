from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from eco.utils import format_money


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(default=500.0)

    @property
    def balance_str(self) -> str:
        return format_money(self.balance)

    @staticmethod
    async def get_or_create(session: AsyncSession, id_: int) -> "User":
        user = await session.get(User, id_)
        if user is not None:
            return user
        else:
            user = User(id=id_)
            session.add(user)
            await session.commit()
            return user
