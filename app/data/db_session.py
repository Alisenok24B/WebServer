import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()  # declarative base

__factory = None  # for get session connect


def global_init(db_file):  # global initialization
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():  # check errors
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'  # address of base
    print(f"Подключение к базе данных по адресу {conn_str}")  # connect to base

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:  # create session
    global __factory
    return __factory()
