from uuid import UUID

from fastapi import HTTPException
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier

from schemas.cart_schemas import ProductCart


# session front
cookie_params = CookieParameters()

cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)


# session backend
session_back = InMemoryBackend[UUID, ProductCart]()


# session verifier
class SimpleSessionVerifier(SessionVerifier[UUID, ProductCart]):
    def __init__(self, *, identifier: str, 
                 auto_error: bool, 
                 backend: InMemoryBackend[UUID, ProductCart], 
                 auth_http_exception: HTTPException):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: ProductCart) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = SimpleSessionVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=session_back,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)
