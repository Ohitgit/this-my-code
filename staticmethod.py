import uuid
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from config.console_logger import get_logger
from config.exceptions import FlowVascularException
from models import GRN
from schemas.v1.supplierpayment import SuplierPaymentUpdate
from utils.base_utils import hash_value, remove_space

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = get_logger(__name__)

class SupplierPaymentUtils:
    """Utility class for handling supplier payment operations"""

    @staticmethod
    async def get_grn_by_id(db: AsyncSession, grn_id: uuid.UUID) -> GRN:
        """Get a GRN by ID"""
        result = await db.execute(select(GRN).where(GRN.id == grn_id))
        return result.scalars().first()

    @staticmethod
    async def update_supplierpayment(
        db: AsyncSession,
        supplierpayment: SuplierPaymentUpdate,
        grn: GRN
    ) -> GRN:
        """
        Update supplier payment details in the database.

        Args:
            db (AsyncSession): Database session.
            supplierpayment (SuplierPaymentUpdate): Updated supplier payment data.
            grn (GRN): Existing GRN object to update.

        Returns:
            GRN: Updated GRN object.
        """
        # Update only provided fields from supplierpayment
        for field, value in supplierpayment.model_dump(exclude_unset=True).items():
            setattr(grn, field, value)

        db.add(grn)
        await db.commit()
        await db.refresh(grn)
        return grn
   
    
    @staticmethod
    def get_supplier_payment():
        """Return query for Supplier Payment (GRN)"""
        return (
            select(GRN)
            .options(selectinload(GRN.supplier))  # eager load supplier
            .where(GRN.paying_amount.isnot(None),GRN.paying_amount > 0)
        )

        
                     
      
   