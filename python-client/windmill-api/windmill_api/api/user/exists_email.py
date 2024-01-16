from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors




def _get_kwargs(
    email: str,

) -> Dict[str, Any]:
    

    cookies = {}


    

    

    

    return {
        "method": "get",
        "url": "/users/exists/{email}".format(email=email,),
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[bool]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(bool, response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[bool]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    email: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[bool]:
    """ exists email

    Args:
        email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[bool]
     """


    kwargs = _get_kwargs(
        email=email,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    email: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[bool]:
    """ exists email

    Args:
        email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        bool
     """


    return sync_detailed(
        email=email,
client=client,

    ).parsed

async def asyncio_detailed(
    email: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[bool]:
    """ exists email

    Args:
        email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[bool]
     """


    kwargs = _get_kwargs(
        email=email,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    email: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[bool]:
    """ exists email

    Args:
        email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        bool
     """


    return (await asyncio_detailed(
        email=email,
client=client,

    )).parsed