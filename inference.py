import asyncio
import os

from openai import OpenAI

try:
    from .client import FraudDetectionEnv
    from .models import FraudDetectionAction
except ImportError:
    from client import FraudDetectionEnv
    from models import FraudDetectionAction

# Configuration

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

BENCHMARK = "fraud_detection"
TASKS = ["task_easy", "task_medium", "task_hard"]
SEEDS = [0, 1, 2]
MAX_STEPS = 12
TEMPERATURE = 0.0
MAX_TOKENS = 200

# Prompts

SYSTEM_PROMPT = """\
You are a fraud detection analyst investigating suspicious e-commerce orders.

You can take these actions to gather evidence:
- CHECK_PAYMENT_HISTORY: Review payment method and transaction history
- CHECK_IP_LOCATION: Check IP address geolocation and VPN usage
- CHECK_DEVICE_FINGERPRINT: Examine device and browser fingerprint
- CHECK_ORDER_VALUE: Analyze order amount and item categories
- CHECK_SHIPPING_ADDRESS: Verify shipping and billing addresses
- CHECK_CUSTOMER_HISTORY: Review account age, email, phone, and past behavior

After gathering enough evidence, make a final decision:
- APPROVE: Order is legitimate
- REJECT: Order is fraudulent
- ESCALATE: Order is ambiguous, needs human review

Strategy:
- For obvious cases, check 2-3 signals then decide
- For mixed signals, check 4-5 signals before deciding
- Look for patterns across signals, not just individual red flags
- Consider the overall risk picture before making your decision

Respond with ONLY the action name. No explanation, no quotes, no punctuation. Just the action string.
Example: CHECK_PAYMENT_HISTORY"""


def build_user_prompt(obs):
    lines = []
    lines.append("ORDER UNDER INVESTIGATION:")
    lines.append(obs.order_summary)
    lines.append("")
    lines.append("EVIDENCE GATHERED SO FAR:")
    if obs.signals_gathered:
        for signal in obs.signals_gathered:
            lines.append(
                f"  - {signal.signal_name}: {signal.value} [Risk: {signal.risk_level}]"
            )
    else:
        lines.append("No evidence gathered yet.")
    lines.append("")
    lines.append(f"STEPS REMAINING: {obs.steps_remaining}")
    lines.append("")
    lines.append(f"AVAILABLE ACTIONS: {', '.join(obs.available_actions)}")
    lines.append("")
    lines.append("Based on the evidence so far, what is your next action?")
    return "\n".join(lines)


# LLM interaction


def get_model_action(client, obs):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(obs)},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        return response.choices[0].message.content.strip().upper()
    except Exception:
        return "CHECK_PAYMENT_HISTORY"


# Logging helpers


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    error_str = str(error) if error is not None else "null"
    done_str = "true" if done else "false"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_str} error={error_str}",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    success_str = "true" if success else "false"
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={success_str} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# Main loop


async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    if not API_KEY:
        print("[DEBUG] API_KEY / HF_TOKEN environment variable is not set", flush=True)
        return

    if not LOCAL_IMAGE_NAME:
        print("[DEBUG] LOCAL_IMAGE_NAME environment variable is not set", flush=True)
        return

    for task_id in TASKS:
        for seed in SEEDS:
            env = await FraudDetectionEnv.from_docker_image(LOCAL_IMAGE_NAME)
            rewards = []
            steps_taken = 0
            score = 0.0
            success = False

            log_start(
                task=f"{task_id}_seed{seed}", env=BENCHMARK, model=MODEL_NAME
            )

            try:
                result = await env.reset(task_id=task_id, seed=seed)
                obs = result.observation

                for step_num in range(1, MAX_STEPS + 1):
                    if result.done:
                        break

                    action_str = get_model_action(client, obs)

                    result = await env.step(
                        FraudDetectionAction(action_type=action_str)
                    )
                    obs = result.observation
                    reward = result.reward or 0.0
                    done = result.done

                    rewards.append(reward)
                    steps_taken = step_num

                    log_step(
                        step=step_num,
                        action=action_str,
                        reward=reward,
                        done=done,
                        error=None,
                    )

                    if done:
                        break

                score = rewards[-1] if rewards else 0.0
                score = min(max(score, 0.0), 1.0)
                success = score >= 0.5

            except Exception as e:
                print(f"[DEBUG] Error during episode: {e}", flush=True)
            finally:
                try:
                    await env.close()
                except Exception:
                    pass
                log_end(
                    success=success,
                    steps=steps_taken,
                    score=score,
                    rewards=rewards,
                )


if __name__ == "__main__":
    asyncio.run(main())
