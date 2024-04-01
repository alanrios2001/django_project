from typing import Optional

from sqlalchemy import Engine, create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from djangoProject.settings import settings


class BaseModel(DeclarativeBase):
    pass


engine: Optional[Engine] = None


def _get_engine() -> Engine:
    """
    Essa é uma função auxiliar que não deve ser usada no código.
    Utilize sempre get_engine(), e para mockar o banco nos testes basta adicionar o docorator
    '@patch("core.db_alchemy._get_engine", new=get_test_engine)'
    """
    return create_engine(
        (
            f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}"
            f"@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
        ),
        future=True,
    )


def get_engine() -> Engine:
    """
    Função que retorna o engine
    """
    global engine
    if engine is None:
        engine = _get_engine()
    return engine


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150))
    password: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150))
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[str] = mapped_column(String(150))
    date_joined: Mapped[str] = mapped_column(String(150))


def feed_database():
    engine = get_engine()
    BaseModel.metadata.create_all(engine)


if __name__ == "__main__":
    feed_database()
