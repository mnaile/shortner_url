from asyncio import Future
from datetime import datetime, timedelta

import pytest
from fastapi.exceptions import HTTPException

from app.data.model import UrlShortner
from app.schemas.schema import ShortnerUrlData
from app.services.service import ShortnerUrlService


@pytest.fixture
def url_data_mock():

    return UrlShortner(
        **{
            "id": "1eecf52b-d8ef-4d9d-9875-8f57f460b819",
            "short_url": "https://itlab.com/19y044023",
            "url": "https://www.geeksforgeeks.org/get-current-timestamp-using-python/",
            "expire_time": "2023-01-28T20:51:59.044013",
            "created": "2023-01-22T16:51:59.062991+00:00",
            "updated": None,
        }
    )


@pytest.mark.asyncio
async def test_create_shortner_url(mocker, url_data_mock):

    data = data = {
        "url": "https://www.geeksforgeeks.org/get-current-timestamp-using-python/",
        "expire_day": 6,
    }

    schema = ShortnerUrlData(**data)
    result = Future()
    result.set_result(None)

    mock_create = mocker.patch("app.services.service.UrlShortner.create")
    mock_create.return_value = url_data_mock

    fetched_data = await ShortnerUrlService().create_shortner_url(schema)

    assert url_data_mock.url == fetched_data.url
    assert url_data_mock.short_url == fetched_data.short_url
    assert url_data_mock.expire_time == fetched_data.expire_time
    assert url_data_mock.created == fetched_data.created
    assert url_data_mock.id == fetched_data.id


@pytest.mark.asyncio
async def test_get_url(mocker, url_data_mock):

    short_url = "https://itlab.com/95J7067862"

    mock_query = mocker.patch("app.services.service.UrlShortner.query")

    url_data_mock.expire_time = datetime.now() + timedelta(days=90)

    result = Future()
    result.set_result(url_data_mock)

    mock_data = mock_query.where
    mock_data.return_value.gino.first.return_value = result

    fetched_data = await ShortnerUrlService().get_url(short_url)
    assert url_data_mock.url == fetched_data["url"]


@pytest.mark.asyncio
async def test_get_url_fail(mocker, url_data_mock):

    short_url = "https://itlab.com/95J7067862"

    mock_query = mocker.patch("app.services.service.UrlShortner.query")

    url_data_mock.expire_time = datetime.now()

    result = Future()
    result.set_result(url_data_mock)

    mock_data = mock_query.where
    mock_data.return_value.gino.first.return_value = result

    with pytest.raises(HTTPException) as err:
        await ShortnerUrlService().get_url(short_url)

    assert err.value.detail == "Url has expired!"
    assert err.value.status_code == 400
