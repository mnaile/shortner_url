from asyncio import Future

import pytest


@pytest.fixture
def url_operation(mocker):
    return mocker.patch("app.controllers.controller.ShortnerUrlService")


@pytest.mark.asyncio
def test_create_short_url(client, url_operation):

    data = {
        "url": "https://www.geeksforgeeks.org/get-current-timestamp-using-python/",
        "expire_day": 6,
    }

    response_data = {
        "id": "1eecf52b-d8ef-4d9d-9875-8f57f460b819",
        "short_url": "https://itlab.com/19y044023",
        "url": "https://www.geeksforgeeks.org/get-current-timestamp-using-python/",
        "expire_time": "2023-01-28T20:51:59.044013",
        "created": "2023-01-22T16:51:59.062991+00:00",
    }

    result = Future()
    result.set_result(response_data)

    url_operation.return_value.create_shortner_url.return_value = result

    response = client.post("api/v1/", json=data)

    assert response.status_code == 200
    assert response.json() == response_data


@pytest.mark.asyncio
def test_get_url(client, url_operation):

    data = {"short_url": "https://itlab.com/95J7067862"}

    response_data = {
        "url": "https://www.geeksforgeeks.org/get-current-timestamp-using-python/"
    }

    result = Future()
    result.set_result(response_data)

    url_operation.return_value.get_url.return_value = result

    response = client.get("api/v1/", params=data)

    assert response.status_code == 200
    assert response.json() == response_data
