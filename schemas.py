from datetime import datetime, date, timezone
from uuid import UUID
from pydantic import (BaseModel, Field, field_validator, model_validator)
from typing import Optional
from .enums import PaymentType
from pydantic_core import PydanticCustomError
import uuid


# Shared properties
class SuplierPaymentBase(BaseModel):
    paying_amount: float
    due_amount: float   # better as float
    payment_mode: PaymentType
    drawn_on: Optional[int] = None
    card_number: Optional[str] = None
    cheque_no: Optional[str] = None
    upi_number: Optional[str] = None
    class Config:
        from_attributes = True

    @field_validator('payment_mode', mode='before')
    @classmethod
    def validate_payment_mode(cls, v):
        try:
            PaymentType(v)
        except ValueError:
            raise PydanticCustomError('custom_error', 'Payment Mode is incorrect.')
        return v

    @model_validator(mode="after")
    def validate_payment_fields(self):
        if self.payment_mode == PaymentType.card and not self.card_number:
            raise PydanticCustomError(
                "custom_error",
                "Card Number is mandatory.",
                {"field": "card_number"}
            )

        if self.payment_mode == PaymentType.cheque:
            if not self.cheque_no:
                raise PydanticCustomError(
                    "custom_error",
                    "Cheque Number is mandatory.",
                    {"field": "cheque_no"}
                )
            if not self.drawn_on:
                raise PydanticCustomError(
                    "custom_error",
                    "Drawn Date is mandatory.",
                    {"field": "drawn_on"}
                )

        if self.payment_mode == PaymentType.upi and not self.upi_number:
            raise PydanticCustomError(
                "custom_error",
                "UPI Number is mandatory.",
                {"field": "upi_number"}
            )

        return self


# Create schema (input)
class SuplierPaymentUpdate(SuplierPaymentBase):
    pass


# Read schema (output)
class SuplierPaymentRead(BaseModel):
    id: uuid.UUID
    supplier_name: Optional[str]  
    paying_amount: float
    due_amount: float   # better as float
    payment_mode: PaymentType
    drawn_on: Optional[int] = None
    card_number: Optional[str] = None
    cheque_no: Optional[str] = None
    upi_number: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
    