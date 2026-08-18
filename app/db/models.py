from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer,
    Numeric, String, Text, func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


# ---------------------------------------------------------------------------
# Phase 1 — Authentication
# ---------------------------------------------------------------------------

class BseAuth(Base):
    __tablename__ = "bse_auth"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_code: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    access_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    login_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class BseApiLog(Base):
    __tablename__ = "bse_api_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    http_method: Mapped[str] = mapped_column(String(10), nullable=False)
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    bse_status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    error_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    request_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    response_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)


# ---------------------------------------------------------------------------
# Phase 3 — Mutual Fund Master
# ---------------------------------------------------------------------------

class BseAmc(Base):
    __tablename__ = "bse_amcs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amc_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    amc_name: Mapped[str] = mapped_column(String(255), nullable=False)
    rta_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    schemes: Mapped[list[BseScheme]] = relationship("BseScheme", back_populates="amc")


class BseScheme(Base):
    __tablename__ = "bse_schemes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    amc_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_amcs.id"), nullable=False)
    scheme_name: Mapped[str] = mapped_column(String(500), nullable=False)
    isin: Mapped[str | None] = mapped_column(String(50), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sub_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    amc: Mapped[BseAmc] = relationship("BseAmc", back_populates="schemes")
    plans: Mapped[list[BseSchemePlan]] = relationship("BseSchemePlan", back_populates="scheme")


class BseSchemePlan(Base):
    __tablename__ = "bse_scheme_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_schemes.id"), nullable=False)
    plan: Mapped[str | None] = mapped_column(String(50), nullable=True)
    option: Mapped[str | None] = mapped_column(String(50), nullable=True)
    purchase_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    redemption_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    switch_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    sip_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    minimum_purchase: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    minimum_sip: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    scheme: Mapped[BseScheme] = relationship("BseScheme", back_populates="plans")


# ---------------------------------------------------------------------------
# Phase 4 — Investment
# ---------------------------------------------------------------------------

class BseOrder(Base):
    __tablename__ = "bse_orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    scheme_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_schemes.id"), nullable=True)
    order_type: Mapped[str] = mapped_column(String(50), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    units: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    folio_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bse_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bse_order_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    order_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bse_response_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bse_response_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    scheme: Mapped[BseScheme | None] = relationship("BseScheme")
    statuses: Mapped[list[BseOrderStatus]] = relationship("BseOrderStatus", back_populates="order")
    payments: Mapped[list[BsePayment]] = relationship("BsePayment", back_populates="order")


class BseOrderStatus(Base):
    __tablename__ = "bse_order_status"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_orders.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    bse_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    response_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    response_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    order: Mapped[BseOrder] = relationship("BseOrder", back_populates="statuses")


class BsePayment(Base):
    __tablename__ = "bse_payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_orders.id"), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    payment_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bse_payment_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    payment_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    payment_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    response_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    response_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    order: Mapped[BseOrder] = relationship("BseOrder", back_populates="payments")


# ---------------------------------------------------------------------------
# Phase 5 — SIP
# ---------------------------------------------------------------------------

class BseSip(Base):
    __tablename__ = "bse_sips"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    scheme_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_schemes.id"), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    frequency: Mapped[str] = mapped_column(String(30), nullable=False)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    installment_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bse_sip_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    scheme: Mapped[BseScheme | None] = relationship("BseScheme")
    installments: Mapped[list[BseSipInstallment]] = relationship("BseSipInstallment", back_populates="sip")


class BseSipInstallment(Base):
    __tablename__ = "bse_sip_installments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sip_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_sips.id"), nullable=False)
    installment_number: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    order_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_orders.id"), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sip: Mapped[BseSip] = relationship("BseSip", back_populates="installments")
    order: Mapped[BseOrder | None] = relationship("BseOrder")


# ---------------------------------------------------------------------------
# Phase 6 — Transactions
# ---------------------------------------------------------------------------

class BseTransaction(Base):
    __tablename__ = "bse_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    order_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_orders.id"), nullable=True)
    scheme_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_schemes.id"), nullable=True)
    transaction_type: Mapped[str] = mapped_column(String(50), nullable=False)
    transaction_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    units: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    nav: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    bse_transaction_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    order: Mapped[BseOrder | None] = relationship("BseOrder")
    scheme: Mapped[BseScheme | None] = relationship("BseScheme")


# ---------------------------------------------------------------------------
# Phase 7 — Other Transactions
# ---------------------------------------------------------------------------

class BseRedemption(Base):
    __tablename__ = "bse_redemptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    scheme_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_schemes.id"), nullable=True)
    order_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_orders.id"), nullable=True)
    folio_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    redemption_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    units: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    bse_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    scheme: Mapped[BseScheme | None] = relationship("BseScheme")
    order: Mapped[BseOrder | None] = relationship("BseOrder")


class BseSwitch(Base):
    __tablename__ = "bse_switches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    from_scheme_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_schemes.id"), nullable=True)
    to_scheme_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_schemes.id"), nullable=True)
    order_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("bse_orders.id"), nullable=True)
    units: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    bse_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    from_scheme: Mapped[BseScheme | None] = relationship("BseScheme", foreign_keys=[from_scheme_id])
    to_scheme: Mapped[BseScheme | None] = relationship("BseScheme", foreign_keys=[to_scheme_id])
    order: Mapped[BseOrder | None] = relationship("BseOrder")
