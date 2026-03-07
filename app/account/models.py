from sqlalchemy import String, Integer, Enum, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime, timezone
import enum

from app.commission.association import agent_commission_table
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.commission.models import Commission

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    AGENT = "agent"
    TELECALLER = "telecaller"
    COORDINATOR = "coordinator"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_roles"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )
    admin_profile = relationship("AdminProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    agent_profile = relationship("AgentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    telecaller_profile = relationship("TelecallerProfile", back_populates="user",lazy="selectin", uselist=False, cascade="all, delete-orphan")
    coordinator_profile = relationship("CoordinatorProfile", back_populates="user", lazy="selectin" ,uselist=False, cascade="all, delete-orphan")


# ---------------- ADMIN ----------------
class AdminProfile(Base):
    __tablename__ = "admin_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    phone: Mapped[str] = mapped_column(String(15))
    address: Mapped[str] = mapped_column(String(255))
    # department: Mapped[str] = mapped_column(String(100))

    user = relationship("User", back_populates="admin_profile")


# ---------------- AGENT ----------------

class AgentProfile(Base):
    __tablename__ = "agent_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(15))
    emirates_id : Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    nationality: Mapped[str] = mapped_column(String(100))

    business_name : Mapped[str] = mapped_column(String(100), nullable=True)
    year_of_experience : Mapped[str] = mapped_column(Integer, nullable=True)


    account_holder_name : Mapped[str] = mapped_column(String(255), nullable=True)
    bank_name : Mapped[str] = mapped_column(String(255), nullable=True)
    account_number: Mapped[str] = mapped_column(String)
    iban : Mapped[str] = mapped_column(String(255), nullable=True)

    # region: Mapped[str] = mapped_column(String(100))
    # team_name: Mapped[str] = mapped_column(String(100))

    user = relationship("User", back_populates="agent_profile")
    commissions: Mapped[list["Commission"]] = relationship(
    "Commission",
    secondary=agent_commission_table,
    back_populates="agents",
    lazy="selectin"
)


# ---------------- TELECALLER ----------------
class TelecallerProfile(Base):
    __tablename__ = "telecaller_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(15))
    emirates_id: Mapped[str] = mapped_column(String(100), unique=True)
    nationality: Mapped[str] = mapped_column(String(100))
    experience: Mapped[int] = mapped_column(Integer)
    account_holder_name: Mapped[str] = mapped_column(String)
    bank_name: Mapped[str] = mapped_column(String(100))
    account_number: Mapped[str] = mapped_column(String)
    iban: Mapped[str] = mapped_column(String(100))
    target_calls: Mapped[int] = mapped_column(Integer, nullable=True)
    shift_time: Mapped[str] = mapped_column(String(50), nullable=True)
    reporting_manager: Mapped[str] = mapped_column(String(100), nullable=True)

    user = relationship("User", back_populates="telecaller_profile")


# ---------------- COORDINATOR ----------------
class CoordinatorProfile(Base):
    __tablename__ = "coordinator_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(15))
    emirates_id: Mapped[str] = mapped_column(String(100), unique=True)
    nationality: Mapped[str] = mapped_column(String(100))
    experience: Mapped[int] = mapped_column(Integer)
    account_holder_name: Mapped[str] = mapped_column(String)
    bank_name: Mapped[str] = mapped_column(String(100))
    account_number: Mapped[str] = mapped_column(String)
    iban: Mapped[str] = mapped_column(String(100))
    

    user = relationship("User", back_populates="coordinator_profile")




class RefreshToken(Base):
  __tablename__ = "refresh_tokens"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
  token: Mapped[str] = mapped_column(String(255), nullable=False)
  expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  revoked: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

  user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
