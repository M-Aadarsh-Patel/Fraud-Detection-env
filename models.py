from typing import Optional
from pydantic import BaseModel, Field
from openenv.core.env_server.types import Action, Observation, State


class SignalResult(BaseModel):
    signal_name: str
    value: str
    risk_level: str


class FraudDetectionAction(Action):
    action_type: str = Field(
        ...,
        description=(
            "One of: CHECK_PAYMENT_HISTORY, CHECK_IP_LOCATION, "
            "CHECK_DEVICE_FINGERPRINT, CHECK_ORDER_VALUE, "
            "CHECK_SHIPPING_ADDRESS, CHECK_CUSTOMER_HISTORY, "
            "APPROVE, REJECT, ESCALATE"
        ),
    )
    reasoning: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional reasoning for the action (not used in grading)",
    )


class FraudDetectionObservation(Observation):
    order_summary: str = Field(default="")
    signals_gathered: list[SignalResult] = Field(default_factory=list)
    available_actions: list[str] = Field(default_factory=list)
    steps_remaining: int = Field(default=0)
    message: str = Field(default="")


class FraudDetectionState(State):
    task_id: str = Field(default="")
    scenario_id: str = Field(default="")
    order_id: str = Field(default="")
    ground_truth: str = Field(default="")
    relevant_signals: list[str] = Field(default_factory=list)
    signals_checked: list[str] = Field(default_factory=list)
    decision: Optional[str] = Field(default=None)
    max_steps: int = Field(default=10)
    done: bool = Field(default=False)
    score: Optional[float] = Field(default=None)
