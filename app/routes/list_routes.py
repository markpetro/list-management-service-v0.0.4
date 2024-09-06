# app/routes/list_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.list_management_service import ListManagementService

router = APIRouter()


# Injecting ListManagementService through FastAPI's Depends
def get_list_service():
    return ListManagementService()


@router.get("/check/{list_type}")
async def check_value(
        list_type: str,
        value: str = Query(...),  # Use query parameter for 'value'
        list_service: ListManagementService = Depends(get_list_service)  # Inject the service
):
    """
    Check if a value exists in a list.
    - `list_type`: The type of list (e.g., 'blacklist', 'whitelist').
    - `value`: The value to check in the list.
    """
    exists = list_service.check_value(list_type, value, role="viewer")  # Assuming role is 'viewer' for now
    if 'error' in exists:
        raise HTTPException(status_code=400, detail=exists['error'])

    return {"exists": exists}