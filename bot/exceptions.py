from aiohttp.client_exceptions import ServerConnectionError


class SocialNetworkApiException(ServerConnectionError):
    """Raises when bot can not work due to api problems"""
    pass
