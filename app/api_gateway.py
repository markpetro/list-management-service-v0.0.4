# api_gateway.py
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_limiter.depends import RateLimiter
from datetime import timedelta
from typing import List
from app.services.list_management_service import ListManagementService
from app.tasks.celery_tasks import bulk_add_task, bulk_delete_task
from app.utils.auth import authenticate_user, create_access_token

# Initialize the router
router = APIRouter()
list_service = ListManagementService()


@router.post("/login")
def login(username: str = Body(...), password: str = Body(...)):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Generate JWT token
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/add", dependencies=[Depends(RateLimiter(times=50, seconds=60))])
async def add_value(
        list_id: int = Body(...),
        value: str = Body(...),
        comment: str = Body(default=''),
        user: dict = Depends(authenticate_user)
):
    """
    Add a new value to a list.
    Rate limit: 50 requests per minute.
    """
    try:
        username, role = user.get("username"), user.get("role")
        result = list_service.add_value(list_id, value, comment, username, role)
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except Exception as e:
        # Log the exception and return generic message
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/check/{list_type}", dependencies=[Depends(RateLimiter(times=100, seconds=60))])
async def check_value(
        list_type: str,
        value: str = Body(...),
        user: dict = Depends(authenticate_user)
):
    """
    Check if a value exists in a list.
    Rate limit: 100 requests per minute.
    """
    try:
        username, role = user.get("username"), user.get("role")
        exists = list_service.check_value(list_type, value, role)
        if isinstance(exists, dict) and 'error' in exists:
            raise HTTPException(status_code=400, detail=exists['error'])
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/bulk-add", dependencies=[Depends(RateLimiter(times=20, seconds=60))])
async def bulk_add_values(
        list_id: int = Body(...),
        values: List[str] = Body(...),
        comment: str = Body(default=''),
        user: dict = Depends(authenticate_user)
):
    """
    Bulk add values to a list.
    Rate limit: 20 requests per minute.
    """
    try:
        username, role = user.get("username"), user.get("role")
        task = bulk_add_task.apply_async(args=[list_id, values, comment, username, role])
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/bulk-delete", dependencies=[Depends(RateLimiter(times=20, seconds=60))])
async def bulk_delete_values(
        list_id: int = Body(...),
        values: List[str] = Body(...),
        user: dict = Depends(authenticate_user)
):
    """
    Bulk delete values from a list.
    Rate limit: 20 requests per minute.
    """
    try:
        username, role = user.get("username"), user.get("role")
        task = bulk_delete_task.apply_async(args=[list_id, values, role])
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/edit", dependencies=[Depends(RateLimiter(times=50, seconds=60))])
async def edit_value(
        list_id: int = Body(...),
        old_value: str = Body(...),
        new_value: str = Body(...),
        comment: str = Body(default=''),
        user: dict = Depends(authenticate_user)
):
    """
    Edit an existing value in a list.
    Rate limit: 50 requests per minute.
    """
    try:
        username, role = user.get("username"), user.get("role")
        result = list_service.edit_value(list_id, old_value, new_value, comment, username, role)
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=50, seconds=60))])
async def delete_value(
        list_id: int = Body(...),
        value: str = Body(...),
        user: dict = Depends(authenticate_user)
):
    """
    Delete a value from a list.
    Rate limit: 50 requests per minute.
    """
    try:
        username, role = user.get("username"), user.get("role")
        result = list_service.delete_value(list_id, value, role)
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/change-type", dependencies=[Depends(RateLimiter(times=20, seconds=60))])
async def change_list_type(
        list_id: int = Body(...),
        new_type: str = Body(...),
        user: dict = Depends(authenticate_user)
):
    """
    Change the type of list.
    Rate limit: 20 requests per minute.
    """
    try:
        username, role = user.get("username"), user.get("role")
        result = list_service.change_list_type(list_id, new_type, role)
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/roles", response_model=List[str])
async def get_roles():
    """
    Retrieve all roles.
    """
    try:
        roles = ["admin", "user", "guest"]  # Replace with actual role retrieval logic
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# New Endpoints
@router.get("/lists", response_model=List[str])
async def get_lists():
    """
    Retrieve all lists.
    """
    try:
        lists = list_service.get_all_lists()  # Replace with actual list retrieval logic
        return lists
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
