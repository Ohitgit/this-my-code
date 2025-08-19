import uuid
from typing import Optional,List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate
from config.audit_messages import AuditMessageBuilder
from config.dependencies import VerifyUserToken, get_db
from database_utils.doctors import DoctorUtils
from database_utils.logs import AuditLogService
from database_utils.supplierpayment import SupplierPaymentUtils
from models import GRN,User
from schemas.v1.common import ApiResponse, Pagination
from schemas.v1.supplierpayment import SuplierPaymentUpdate,SuplierPaymentRead
from utils.base_utils import CustomParams, hash_value, remove_space
from fastapi import HTTPException

supplierpayment_router = APIRouter(prefix="/supplierpayment")
current_user = VerifyUserToken()


@supplierpayment_router.put("/update/{grn_id}", response_model=ApiResponse)
async def updates_supplierpayment(
    grn_id: uuid.UUID,
    request: Request,
    response: Response,
    supplierpayment: SuplierPaymentUpdate,
    current_user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update supplier payment details in the database.

    Args:
        db (AsyncSession): Database session.
        supplierpayment (SuplierPaymentUpdate): Updated supplier payment data.

    Returns:
        ApiResponse: Updated GRN details or error response.
    """
    try:
        # Fetch GRN by ID
        grn = await SupplierPaymentUtils.get_grn_by_id(db, grn_id)
        if not grn:
            response.status_code = status.HTTP_404_NOT_FOUND
            return ApiResponse(
                success=False,
                status=404,
                error="GRN not found"
            )

        # Check due_amount condition
        if supplierpayment.due_amount is not None and supplierpayment.due_amount <= 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ApiResponse(
                success=False,
                status=400,
                error="Due amount must be greater than 0"
            )

        # Update GRN
        updated_grn = await SupplierPaymentUtils.update_supplierpayment(db, supplierpayment, grn)

        user_data = {
            "id": updated_grn.id,
            "paying_amount": updated_grn.paying_amount,
            "due_amount": updated_grn.due_amount,
            "payment_mode": updated_grn.payment_mode,
            "drawn_on": updated_grn.drawn_on,
            "card_number": updated_grn.card_number,
            "cheque_no": updated_grn.cheque_no,
            "upi_number": updated_grn.upi_number,
        }

        return ApiResponse(success=True, status=200, data=user_data)

    except Exception as e:
        await db.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ApiResponse(
            success=False,
            status=400,
            error=f"Update failed: {str(e)}"
        )

 

@supplierpayment_router.get("/", response_model=ApiResponse)
async def get_supplier_payment(
    db: AsyncSession = Depends(get_db),
    params: CustomParams = Depends(),
    current_user: User = Depends(current_user),
):
    try:
        query = SupplierPaymentUtils.get_supplier_payment()  # <-- no await, just query

        paginated_result = await paginate(db, query, params)

        serialized_users = [
            SuplierPaymentRead.model_validate(user).model_dump()
            for user in paginated_result.items
        ]
        pagination = Pagination.get_paginated_result(paginated_result)

        return ApiResponse(
            success=True,
            data=serialized_users,
            pagination=pagination
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            status=500,
            error=f"Failed to fetch users: {str(e)}"
        )
