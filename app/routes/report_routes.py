# app/routes/report_routes.py
from fastapi import APIRouter
from app.services.list_management_service import ListManagementService  # Correct import
router = APIRouter()
service = ListManagementService()

@router.get("/report/actions")
def get_action_report():
    """
    Endpoint to get the action report.
    """
    result = service.get_action_report('admin')
    return result