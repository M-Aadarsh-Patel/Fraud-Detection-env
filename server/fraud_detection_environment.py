import random
from typing import Any, Optional
from uuid import uuid4

from openenv.core.env_server.interfaces import Environment

try:
    from ..models import (
        FraudDetectionAction,
        FraudDetectionObservation,
        FraudDetectionState,
        SignalResult,
    )
    from ..constants import (
        ALL_ACTIONS,
        CHECK_ACTIONS,
        DECISION_ACTIONS,
        DECISION_SCORES,
        GRADING_CONFIG,
        INVESTIGATION_COST_PER_CHECK,
        PENALTY_DUPLICATE_CHECK,
        PENALTY_EXCEEDED_STEPS,
        PENALTY_NO_EVIDENCE,
        REWARD_IRRELEVANT_SIGNAL,
        REWARD_RELEVANT_SIGNAL,
        TASK_SCENARIOS,
    )
except ImportError:
    from models import (
        FraudDetectionAction,
        FraudDetectionObservation,
        FraudDetectionState,
        SignalResult,
    )
    from constants import (
        ALL_ACTIONS,
        CHECK_ACTIONS,
        DECISION_ACTIONS,
        DECISION_SCORES,
        GRADING_CONFIG,
        INVESTIGATION_COST_PER_CHECK,
        PENALTY_DUPLICATE_CHECK,
        PENALTY_EXCEEDED_STEPS,
        PENALTY_NO_EVIDENCE,
        REWARD_IRRELEVANT_SIGNAL,
        REWARD_RELEVANT_SIGNAL,
        TASK_SCENARIOS,
    )


class FraudDetectionEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        super().__init__()
        self._state = FraudDetectionState()
        self._scenario: dict = {}
        self._signals_gathered: list[SignalResult] = []
        self._available_actions: list[str] = []
        self._penalties: float = 0.0

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        task_id: str = "",
        **kwargs: Any,
    ) -> FraudDetectionObservation:

        if not task_id:
            task_id = kwargs.get("task_id", "")

        if not task_id or task_id not in TASK_SCENARIOS:
            task_id = random.choice(list(TASK_SCENARIOS.keys()))

        scenarios = TASK_SCENARIOS[task_id]
        if seed is not None:
            scenario = scenarios[seed % len(scenarios)]
        else:
            scenario = random.choice(scenarios)

        self._scenario = scenario
        self._signals_gathered = []
        self._available_actions = list(ALL_ACTIONS)
        self._penalties = 0.0

        self._state = FraudDetectionState(
            episode_id=episode_id or str(uuid4()),
            step_count=0,
            task_id=task_id,
            scenario_id=scenario["scenario_id"],
            order_id=scenario["order_id"],
            ground_truth=scenario["ground_truth"],
            relevant_signals=list(scenario["relevant_signals"]),
            signals_checked=[],
            decision=None,
            max_steps=scenario.get("max_steps", 10),
            done=False,
            score=None,
        )

        return FraudDetectionObservation(
            order_summary=scenario["order_summary"],
            signals_gathered=[],
            available_actions=list(ALL_ACTIONS),
            steps_remaining=self._state.max_steps,
            message=(
                f"Welcome! You are investigating order {scenario['order_id']}. "
                "Review the order summary and use CHECK actions to gather evidence "
                "before making a decision (APPROVE, REJECT, or ESCALATE)."
            ),
            done=False,
            reward=0.0,
        )

    def step(
        self,
        action: FraudDetectionAction,  # type: ignore[override]
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> FraudDetectionObservation:

        if not self._state.episode_id:
            return FraudDetectionObservation(
                order_summary="",
                signals_gathered=[],
                available_actions=[],
                steps_remaining=0,
                message="Reset the environment first.",
                done=True,
                reward=0.0,
            )

        if self._state.done:
            return self._make_observation(
                message="This episode is already complete. Please reset the environment.",
                reward=0.0,
                done=True,
            )

        action_type = action.action_type

        if action_type in CHECK_ACTIONS:
            return self._handle_check(action_type)
        elif action_type in DECISION_ACTIONS:
            return self._handle_decision(action_type)
        else:
            return self._handle_unknown(action_type)

    def _handle_check(self, action_type: str) -> FraudDetectionObservation:
        """Handle a CHECK_* action."""
        self._state.step_count += 1
        if action_type in self._state.signals_checked:
            # Duplicate check
            self._penalties += PENALTY_DUPLICATE_CHECK

            if self._state.step_count >= self._state.max_steps:
                self._state.done = True
                self._penalties += PENALTY_EXCEEDED_STEPS
                return self._make_observation(
                    message=(
                        f"Duplicate check: {action_type} was already investigated. "
                        "You have exceeded the maximum number of steps."
                    ),
                    reward=PENALTY_DUPLICATE_CHECK,
                    done=True,
                )

            return self._make_observation(
                message=f"Duplicate check: {action_type} was already investigated. Penalty applied.",
                reward=PENALTY_DUPLICATE_CHECK,
                done=False,
            )

        # New check
        signal_data = self._scenario["signals"][action_type]
        signal_result = SignalResult(
            signal_name=action_type,
            value=signal_data["value"],
            risk_level=signal_data["risk_level"],
        )
        self._signals_gathered.append(signal_result)
        self._state.signals_checked.append(action_type)

        if action_type in self._available_actions:
            self._available_actions.remove(action_type)

        is_relevant = action_type in self._state.relevant_signals
        reward = (REWARD_RELEVANT_SIGNAL if is_relevant else REWARD_IRRELEVANT_SIGNAL) - INVESTIGATION_COST_PER_CHECK

        if self._state.step_count >= self._state.max_steps:
            self._state.done = True
            self._penalties += PENALTY_EXCEEDED_STEPS
            return self._make_observation(
                message=(
                    f"Checked {action_type}: {signal_data['risk_level']} risk. "
                    "You have exceeded the maximum number of steps."
                ),
                reward=reward,
                done=True,
            )

        return self._make_observation(
            message=f"Checked {action_type}: {signal_data['risk_level']} risk.",
            reward=reward,
            done=False,
        )

    def _handle_decision(self, action_type: str) -> FraudDetectionObservation:
        """Handle a DECISION action (APPROVE / REJECT / ESCALATE)."""
        self._state.step_count += 1
        if not self._state.signals_checked:
            self._penalties += PENALTY_NO_EVIDENCE

        self._state.decision = action_type
        self._state.done = True

        # --- grading ---
        config = GRADING_CONFIG[self._state.task_id]
        decision_weight = config["decision_weight"]
        evidence_weight = config["evidence_weight"]
        min_signals = config["min_signals_for_full_evidence"]

        decision_score = DECISION_SCORES.get(
            (self._state.ground_truth, action_type), 0.0
        )

        relevant_checked = len(
            set(self._state.signals_checked) & set(self._state.relevant_signals)
        )
        evidence_score = (
            min(relevant_checked / min_signals, 1.0) if min_signals > 0 else 1.0
        )

        combined = (decision_weight * decision_score) + (evidence_weight * evidence_score)
        combined += self._penalties
        if decision_score >= 0.8 and self._state.step_count <= self._state.max_steps // 2:
            combined += 0.05
        final_score = max(0.01, min(0.99, combined))

        self._state.score = final_score

        return self._make_observation(
            message=f"Decision: {action_type}. Final score: {final_score:.2f}.",
            reward=final_score,
            done=True,
        )

    def _handle_unknown(self, action_type: str) -> FraudDetectionObservation:
        """Handle an unrecognized action type."""
        if self._state.step_count >= self._state.max_steps:
            self._state.done = True
            self._penalties += PENALTY_EXCEEDED_STEPS
            return self._make_observation(
                message=(
                    f"Unknown action: {action_type}. "
                    "You have exceeded the maximum number of steps."
                ),
                reward=0.0,
                done=True,
            )

        return self._make_observation(
            message=(
                f"Unknown action: {action_type}. "
                f"Use one of: {', '.join(ALL_ACTIONS)}."
            ),
            reward=0.0,
            done=False,
        )

    def _make_observation(
        self, message: str, reward: float, done: bool
    ) -> FraudDetectionObservation:
        """Build an observation from current state."""
        return FraudDetectionObservation(
            order_summary=self._scenario["order_summary"],
            signals_gathered=list(self._signals_gathered),
            available_actions=list(self._available_actions),
            steps_remaining=max(0, self._state.max_steps - self._state.step_count),
            message=message,
            done=done,
            reward=reward,
        )

    @property
    def state(self) -> FraudDetectionState:
        """Get the current environment state."""
        if self._state is None:
            return FraudDetectionState(episode_id="", step_count=0)
        return self._state
