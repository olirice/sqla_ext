import json
import os
import subprocess
import time
from typing import AsyncGenerator, Generator

import pytest
import sqlalchemy
from sqlalchemy import Column, Integer, MetaData, Table
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapper, Session, mapper, sessionmaker

from sqla_ext.protocols import ORMTableProtocol


@pytest.fixture(scope="function")
def core_table() -> Table:
    return Table(
        "some_tab", MetaData(), Column("q", Integer, primary_key=True), schema="public"
    )


@pytest.fixture(scope="function")
def orm_table(core_table: Table) -> ORMTableProtocol:

    Meta = MetaData()
    Base = declarative_base(metadata=Meta)

    class SomeTable(Base):
        __table__ = core_table

    return SomeTable  # type: ignore


@pytest.fixture(scope="function")
def mapper_table(core_table: Table) -> Mapper:
    class SomeTable:
        def __init__(self, q: int):
            self.q = q

    return mapper(SomeTable, core_table)


@pytest.fixture(scope="session")
def dockerize_database() -> Generator[None, None, None]:
    container_name = "sqla_ext_pg_test"

    def is_ready() -> bool:
        out = subprocess.check_output(["docker", "inspect", container_name])
        container_info = json.loads(out)
        container_health_status = container_info[0]["State"]["Health"]["Status"]
        if container_health_status == "healthy":
            return True
        return False

    # Skip container setup if in CI
    if not "GITHUB_SHA" in os.environ and not is_ready():

        subprocess.call(
            [
                "docker",
                "run",
                "--rm",
                "--name",
                container_name,
                "-p",
                "6012:5432",
                "-d",
                "-e",
                "POSTGRES_DB=sqla_ext_pg_test",
                "-e",
                "POSTGRES_PASSWORD=pytest_password",
                "-e",
                "POSTGRES_USER=pytest",
                "--health-cmd",
                "pg_isready",
                "--health-interval",
                "3s",
                "--health-timeout",
                "3s",
                "--health-retries",
                "10",
                "postgres:13",
            ]
        )
        # Wait for postgres to become healthy
        for _ in range(10):
            if is_ready():
                break
            time.sleep(1)
        else:
            raise Exception("Container never became healthy")
        yield
        # Optional teardown here
        return
    yield


@pytest.fixture(scope="function")
async def async_engine(dockerize_database: None) -> AsyncGenerator[AsyncEngine, None]:

    eng = create_async_engine(
        "postgresql+asyncpg://pytest:pytest_password@localhost:6012/sqla_ext_pg_test"
    )

    yield eng
    await eng.dispose()


@pytest.fixture(scope="function")
async def sess(async_engine: AsyncEngine) -> AsyncGenerator[Session, None]:

    Session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

    async with async_engine.begin() as conn:

        # Bind a session to the top level transaction
        _session = Session(bind=conn)

        # Start a savepoint that we can rollback to in the transaction
        _session.begin_nested()

        @sqlalchemy.event.listens_for(_session.sync_session, "after_transaction_end")
        def restart_savepoint(sess, trans):  # type: ignore
            """Register event listener to clean up the sqla objects of a session after a transaction ends"""
            if trans.nested and not trans._parent.nested:
                # Expire all objects registered against the session
                sess.expire_all()
                sess.begin_nested()

            yield _session

        yield _session

        # Close the session object
        await _session.close()

        # Rollback to the savepoint, eliminating everything that happend to the _session
        await conn.rollback()
