from typing import Any

import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture


@pytest.mark.anyio
async def test_health(async_client: AsyncClient) -> None:
    response = await async_client.get('/alive')

    assert response.status_code == 200
    assert response.json() == {'detail': 'ok'}


@pytest.mark.parametrize("field_name", ["body", "title"])
@pytest.mark.anyio
async def test_notify_api_without_title(async_client: AsyncClient, field_name: str) -> None:
    """Test method without required parameters."""
    data = {
      field_name: "Some message body here"
    }
    response = await async_client.post('/', json=data)

    assert response.status_code == 422
    assert '"msg":"field required","type":"value_error.missing"' in response.text


@pytest.mark.anyio
async def test_notify_api_no_target_with_settings(async_client: AsyncClient,
                                                  async_notify: Any,
                                                  mocker: MockerFixture) -> None:
    """Test method with default url."""
    mocker.patch('src.main.settings.urls', return_value={'NOTIFYME_DEFAULT': ''})
    data = {
        "title": "Service Name: Event Name",
        "body": "Some message body here"
    }

    response = await async_client.post('/', json=data)

    assert response.status_code == 202
    assert response.json() == {'detail': 'ok'}


@pytest.mark.anyio
async def test_notify_api_no_target_without_settings(async_client: AsyncClient) -> None:
    """Test method without url, settings parameters and without default url configuration."""
    data = {
      "title": "Service Name: Event Name",
      "body": "Some message body here"
    }

    response = await async_client.post('/', json=data)

    assert response.status_code == 400
    assert response.json() == {'detail': 'No notification URL setting provided.'}


@pytest.mark.anyio
async def test_notify_api_with_url(async_client: AsyncClient, async_notify: Any) -> None:
    """Test method with url parameter."""
    data = {
        "url": "test_url",
        "title": "Service Name: Event Name",
        "body": "Some message body here"
    }

    response = await async_client.post('/', json=data)

    assert response.status_code == 202
    assert response.json() == {'detail': 'ok'}


@pytest.mark.anyio
async def test_notify_api_with_settings(async_client: AsyncClient, async_notify: Any, mocker: MockerFixture) -> None:
    """Test method with settings parameter."""
    mocker.patch('src.main.settings.urls', return_value={'NOTIFYME_TEST': ''})
    data = {
        "settings": "NOTIFYME_TEST",
        "title": "Service Name: Event Name",
        "body": "Some message body here"
    }

    response = await async_client.post('/', json=data)

    assert response.status_code == 202
    assert response.json() == {'detail': 'ok'}


@pytest.mark.anyio
async def test_notify_api_target_no_reachable(async_client: AsyncClient) -> None:
    """Test method with wrong url."""
    data = {
        "url": "test",
        "setting": "NOTIFYME_TGRAM",
        "title": "Service Name: Event Name",
        "body": "Some message body here"
    }

    response = await async_client.post('/', json=data)

    assert response.status_code == 500
    assert response.json() == {'detail': 'Something went wrong: could not send the notification.'}
