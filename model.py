class GRN(BaseModel):
    __tablename__ = "pharmacy_grn"

    grn_number = Column(String(100), nullable=False)
    grn_status = Column(String(100), nullable=False)
    po_number = Column(String(50), nullable=True)
    po_date = Column(Date, nullable=True)
    invoice_number = Column(String(50), nullable=False)
    invoice_date = Column(Date, nullable=False)
    recieved_by = Column(String(50), nullable=True)
    remarks = Column(String(50), nullable=True)
    cancellation_remarks = Column(String(50), nullable=True)
    drawn_on = Column(Integer, nullable=True)      
    card_number = Column(String(50), nullable=True)
    cheque_no = Column(String(50), nullable=True)
    upi_number = Column(String(100), nullable=True)
    paying_amount = Column(Float, nullable=True)
    due_amount = Column(Float, nullable=True)
    payment_mode = Column(String(100), nullable=True)
    total_amount = Column(Numeric(9, 2), default=0)
    cgst_amount = Column(Numeric(9, 2), default=0)
    sgst_amount = Column(Numeric(9, 2), default=0)
    igst_amount = Column(Numeric(9, 2), default=0)
    import_duty = Column(Numeric(9, 2), default=0)
    cash_discount = Column(Numeric(9, 2), default=0)
    la_amount = Column(Numeric(9, 2), default=0)
    insurance_amount = Column(Numeric(9, 2), default=0)
    other_amount = Column(Numeric(9, 2), default=0)
    round_off_amount = Column(Numeric(9, 2), default=0)
    net_amount = Column(Numeric(9, 2), default=0)

    counter_id = Column(UUID(as_uuid=True), ForeignKey("pharmacy_counter.id", ondelete="CASCADE"), nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("pharmacy_supplier.id", ondelete="CASCADE"), nullable=False)

    counter = relationship("Counter", back_populates="grn")
    supplier = relationship("Supplier", back_populates="grn")

    medicines = relationship("GRNMedicine", back_populates="grn", cascade="all, delete-orphan")

    @property
    def supplier_name(self):
        return self.supplier.name if self.supplier else None