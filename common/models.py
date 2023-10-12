from typing import Sequence

from sqlalchemy import BigInteger, ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from common.database import engine
from common.utils import format_money


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    balance: Mapped[float] = mapped_column(default=500.0)

    inventory: Mapped["UserInventory"] = relationship(back_populates="owner")
    loan_requests: Mapped["LoanRequest"] = relationship(back_populates="user")

    @property
    def balance_fmt(self) -> str:
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


class UserInventory(Base):
    __tablename__ = "user_inventories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("shop_items.id"))

    owner: Mapped[User] = relationship(back_populates="inventory")
    item: Mapped["ShopItem"] = relationship(back_populates="owners", lazy="selectin")


class ShopItem(Base):
    __tablename__ = "shop_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()

    owners: Mapped[UserInventory] = relationship(back_populates="item")

    @staticmethod
    async def all(session: AsyncSession) -> Sequence["ShopItem"]:
        return (await session.scalars(select(ShopItem))).all()


class LoanRequest(Base):
    __tablename__ = "loan_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    amount: Mapped[int] = mapped_column()
    application: Mapped[str] = mapped_column(String(100))

    user: Mapped[User] = relationship(back_populates="loan_requests", lazy="selectin")

    async def approve(self, session: AsyncSession) -> None:
        self.user.balance = User.balance + self.amount
        await session.delete(self)
        await session.commit()

    async def reject(self, session: AsyncSession) -> None:
        await session.delete(self)
        await session.commit()


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
