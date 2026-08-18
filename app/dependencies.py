from fastapi import Request

from app.clients.starmf_client import StarMFClient


def get_client(request: Request) -> StarMFClient:
    """Returns the single shared StarMFClient instance created at startup."""
    return request.app.state.starmf_client
