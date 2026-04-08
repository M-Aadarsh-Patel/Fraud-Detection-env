# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from .models import FraudDetectionAction, FraudDetectionObservation, FraudDetectionState
from .models import SignalResult


class FraudDetectionEnv(
    EnvClient[FraudDetectionAction, FraudDetectionObservation, State]
):
    def _step_payload(self, action: FraudDetectionAction) -> Dict:
        payload = {"action_type": action.action_type} 
        if action.reasoning is not None:
            payload["reasoning"] = action.reasoning

        return payload

    def _parse_result(self, payload: Dict) -> StepResult[FraudDetectionObservation]:
        obs_data = payload.get("observation", {})
    
        signals = [
            SignalResult(
                signal_name=s.get("signal_name", ""),
                value=s.get("value", ""),
                risk_level=s.get("risk_level", ""),
            )
            for s in obs_data.get("signals_gathered", [])
        ]
        
        observation = FraudDetectionObservation(
            order_summary=obs_data.get("order_summary", ""),
            signals_gathered=signals,
            available_actions=obs_data.get("available_actions", []),
            steps_remaining=obs_data.get("steps_remaining", 0),
            message=obs_data.get("message", ""),
            done=payload.get("done", False),
            reward=payload.get("reward"),
        )
        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> FraudDetectionState:
        return FraudDetectionState(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
            task_id=payload.get("task_id", ""),
            scenario_id=payload.get("scenario_id", ""),
            order_id=payload.get("order_id", ""),
            ground_truth=payload.get("ground_truth", ""),
            relevant_signals=payload.get("relevant_signals", []),
            signals_checked=payload.get("signals_checked", []),
            decision=payload.get("decision"),
            max_steps=payload.get("max_steps", 10),
            done=payload.get("done", False),
            score=payload.get("score"),
        )
