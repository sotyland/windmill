from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from typing import cast
from typing import Dict
from ...models.list_resource_type_response_200_item import ListResourceTypeResponse200Item
from typing import cast, List



def _get_kwargs(
    workspace: str,

) -> Dict[str, Any]:
    

    cookies = {}


    

    

    

    return {
        "method": "get",
        "url": "/w/{workspace}/resources/type/list".format(workspace=workspace,),
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[List['ListResourceTypeResponse200Item']]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = ListResourceTypeResponse200Item.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[List['ListResourceTypeResponse200Item']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[List['ListResourceTypeResponse200Item']]:
    """ list resource_types

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListResourceTypeResponse200Item']]
     """


    kwargs = _get_kwargs(
        workspace=workspace,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[List['ListResourceTypeResponse200Item']]:
    """ list resource_types

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListResourceTypeResponse200Item']
     """


    return sync_detailed(
        workspace=workspace,
client=client,

    ).parsed

async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[List['ListResourceTypeResponse200Item']]:
    """ list resource_types

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListResourceTypeResponse200Item']]
     """


    kwargs = _get_kwargs(
        workspace=workspace,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[List['ListResourceTypeResponse200Item']]:
    """ list resource_types

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListResourceTypeResponse200Item']
     """


    return (await asyncio_detailed(
        workspace=workspace,
client=client,

    )).parsed