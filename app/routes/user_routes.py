# app/routes/user_routes.py
from fastapi import APIRouter, HTTPException, Body
from app.services.list_management_service import ListManagementService
router = APIRouter()
service = ListManagementService()


@router.post("/user/create")
def create_user(username: str = Body(...), password: str = Body(...), role: str = Body(...)):
    """
    Endpoint to create a new user.
    """
    result = service.create_user(username, password, role)

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return result