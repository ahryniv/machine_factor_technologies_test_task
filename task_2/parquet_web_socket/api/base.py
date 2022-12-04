from fastapi import APIRouter, Request

router = APIRouter()

HEALTHY = 'HEALTHY'


@router.get(
    '/health',
    summary='Health check',
    response_model=str,
)
async def health() -> str:
    """Shows that the server is ready to receive connections"""
    return HEALTHY


@router.get(
    '/version',
    summary='Version',
    response_model=str,
)
async def version(request: Request) -> str:
    """Shows application version"""
    return request.app.version
