from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from datetime import datetime, timezone
from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"))

    customer_name: Mapped[str] = mapped_column(String(150))
    mobile_number: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(150))

    product_type: Mapped[int] = mapped_column(ForeignKey("products.id"))
    requested_amount: Mapped[float] = mapped_column(Float)

    status: Mapped[str] = mapped_column(String(50), default="new")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # relationship
    case = relationship("Case", back_populates="lead", uselist=False)