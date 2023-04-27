from fastapi import APIRouter

router = APIRouter(
    prefix="/scraping",
    tags=["scraping"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def test():

    return {"message": "hello"}
