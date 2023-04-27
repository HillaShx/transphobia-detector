from fastapi import APIRouter

router = APIRouter(
    prefix="/interface",
    tags=["interface"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def test():
    return {"message": "hello"}
