import logging

import apprise
from fastapi import FastAPI, Request, status

from src import config
from src.config import settings
from src.exceptions import BadRequestHTTPException, InternalErrorHTTPException
from src.schemas import CreateNotificationSchema, ErrorMessageModel

app = FastAPI()
logger = logging.getLogger(__name__)


async def check_url_setting(url_setting: str) -> None:
    if url_setting not in settings.urls.keys():
        raise BadRequestHTTPException(detail=f'Wrong URL setting provided: {url_setting}')
    if not settings.urls[url_setting]:
        raise BadRequestHTTPException(detail=f'Improperly configured: the setting {url_setting} contains empty data.')


@app.post(
    '/',
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorMessageModel,
            "description": "Bad request data provided.",
            "content": {"application/json": {"example": {"detail": "No notification URL setting provided."}}},
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorMessageModel,
            "description": "Internal Service Error",
            "content": {
                "application/json": {"example": {"detail": "Something went wrong: could not send the notification."}}
            },
        },
    },
)
async def send_notification(payload: CreateNotificationSchema, request: Request) -> dict[str, str]:
    logger.info(
        f'Sending notification. Payload received: {payload.dict()}. '
        f'IP: {request.client.host if request.client else None}. '
        f'Real IP: {request.headers.get("x-real-ip")}. Forwarded for: {request.headers.get("x-forwarded-for")}.'
    )
    notifier = apprise.Apprise()

    if url := payload.url:
        notifier.add(url)
    elif url_setting := payload.setting:
        await check_url_setting(url_setting)
        notifier.add(settings.urls[url_setting])
    elif default_url := settings.urls.get(config.DEFAULT_URL_SETTING_NAME):
        notifier.add(default_url)
    else:
        raise BadRequestHTTPException(detail='No notification URL setting provided.')

    result = await notifier.async_notify(
        title=payload.title,
        body=payload.body,
    )
    if result:
        return {'detail': 'ok'}
    else:
        raise InternalErrorHTTPException(detail='Something went wrong: could not send the notification.')


@app.get('/alive', status_code=status.HTTP_200_OK)
async def healthcheck() -> dict[str, str]:
    return {'detail': 'ok'}
