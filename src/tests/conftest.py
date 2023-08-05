from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from src.main import app


@pytest.fixture
def anyio_backend() -> str:
    """Fixture to specify anyio backend. If not specified it runs multiple for asyncio and trio."""
    return 'asyncio'


@pytest.fixture
def async_notify(mocker: MockerFixture) -> None:
    """Fixture for async_notify method call."""
    mocker.patch('src.main.apprise.Apprise.async_notify', return_value=True)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture for async client creation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
