from typing import Optional

from pydantic import BaseModel, Field


class ErrorMessageModel(BaseModel):
    detail: str


class CreateNotificationSchema(BaseModel):
    setting: Optional[str] = Field(title='Notification target setting.')
    url: Optional[str] = Field(title='Notification Apprise URL.')
    title: Optional[str] = Field(title='Message title.')
    body: Optional[str] = Field(title='Message body.')
