import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserRole(str, enum.Enum):
    OWNER = "Owner"
    WORKER = "Worker"
    ADMIN = "Admin"

class ClosingStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

# --- MODULE 1: USERS & VENDOR PROFILES ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.OWNER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    vendor_profile = relationship("VendorProfile", back_populates="user", uselist=False)

class VendorProfile(Base):
    __tablename__ = "vendor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    business_name = Column(String, nullable=False)
    ssm_number = Column(String, nullable=True)  # SSM / NRIC / Business Permit ID
    phone_number = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    location_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="vendor_profile")
    daily_closings = relationship("DailyClosing", back_populates="vendor")

# --- MODULE 2 & 3: TRANSACTIONS, CASH FLOW & PROFIT ---
class DailyClosing(Base):
    __tablename__ = "daily_closings"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendor_profiles.id"), nullable=False)
    closing_date = Column(String, index=True, nullable=False)  # YYYY-MM-DD
    
    opening_float = Column(Float, default=0.0, nullable=False)
    counted_cash = Column(Float, default=0.0, nullable=False)
    ocr_digital_sales = Column(Float, default=0.0, nullable=False)
    total_expenses = Column(Float, default=0.0, nullable=False)
    net_profit = Column(Float, default=0.0, nullable=False)
    
    status = Column(Enum(ClosingStatus), default=ClosingStatus.OPEN)
    is_locked = Column(Boolean, default=False)
    locked_at = Column(DateTime, nullable=True)

    # Relationships
    vendor = relationship("VendorProfile", back_populates="daily_closings")
    expenses = relationship("Expense", back_populates="daily_closing")
    ocr_receipts = relationship("OCRReceipt", back_populates="daily_closing")
    audit_logs = relationship("AuditLog", back_populates="daily_closing")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    daily_closing_id = Column(Integer, ForeignKey("daily_closings.id"), nullable=False)
    category = Column(String, nullable=False)  # Raw Ingredients, Packaging, Utilities, Wages
    amount = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    daily_closing = relationship("DailyClosing", back_populates="expenses")

class OCRReceipt(Base):
    __tablename__ = "ocr_receipts"

    id = Column(Integer, primary_key=True, index=True)
    daily_closing_id = Column(Integer, ForeignKey("daily_closings.id"), nullable=False)
    image_url = Column(String, nullable=False)
    image_hash = Column(String, index=True, nullable=True)  # pHash for deduplication
    
    amount = Column(Float, nullable=False)
    transaction_date = Column(String, nullable=True)
    reference_number = Column(String, index=True, nullable=True)
    confidence_score = Column(Float, default=0.0)
    auto_accepted = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    daily_closing = relationship("DailyClosing", back_populates="ocr_receipts")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    daily_closing_id = Column(Integer, ForeignKey("daily_closings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)  # REOPEN, EDIT_FLOAT, LOCK
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    daily_closing = relationship("DailyClosing", back_populates="audit_logs")