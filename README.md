---
title: Fraud Detection Agent Environment
emoji: 🔍
colorFrom: red
colorTo: orange
sdk: docker
app_port: 8000
tags:
  - openenv
---

# Fraud Detection Agent Environment

## Environment Description

This is a sequential evidence-gathering environment for e-commerce fraud investigation, built on the [OpenEnv](https://github.com/meta-pytorch/OpenEnv) framework. Unlike standard fraud detection benchmarks where a model receives all features at once and outputs a classification label, this environment requires the agent to *actively choose* which signals to investigate, interpret the results in context, and decide when it has gathered enough evidence to make a call. This mirrors how fraud analysts actually work at companies like Stripe, Shopify, and PayPal — pulling one report at a time, each costing time and money, and making a judgment call under uncertainty.

The core tradeoff is information vs. decisiveness. Each investigation step costs a small fee (simulating real API costs for identity verification, device fingerprinting, and geolocation lookups) and consumes one of the agent's limited steps. Investigating every signal guarantees a complete picture but burns budget and risks hitting the step limit. Deciding early saves steps but risks a wrong call on insufficient evidence. The agent must learn when to stop gathering and commit — a skill that single-shot classification benchmarks never test.

The environment includes 9 hand-crafted scenarios across 3 difficulty tiers. Each models a distinct real-world fraud pattern: card testing bots running automated $25 gift card purchases, reshipping mules forwarding stolen-card electronics through CMRA warehouses, synthetic identities built from deceased SSNs, business travelers ordering laptops from Tokyo hotel Wi-Fi, $9,000 engagement ring purchases from 4-year-old accounts, students shipping to new dorm addresses, triangulation fraud using legitimate account histories, employees abusing store discounts through POS bypasses, and account takeover bust-outs with credential compromise chains.

## Motivation

Existing fraud detection benchmarks treat the problem as single-shot classification: given a feature vector, output FRAUD or LEGITIMATE. But real fraud investigation is sequential. An analyst at a payment processor doesn't see all signals simultaneously — they pull a payment history report, then maybe a device fingerprint, then an address verification, each taking time and incurring vendor API costs. At some point they decide they've seen enough and make the call. The decision of *what to investigate next* and *when to stop* is as important as the final label.

This environment is the first to model that sequential decision-making process within the OpenEnv framework. Each CHECK action incurs an investigation cost of 0.02, simulating the real-world per-call pricing of services like MaxMind (geolocation), Socure (identity verification), and Fingerprint.js (device intelligence). The grading system separately evaluates decision quality and evidence quality, with the balance shifting by difficulty — easy tasks reward correct snap judgments, while hard tasks demand thorough investigation before concluding.

## Action Space

The agent has 9 available actions: 6 evidence-gathering CHECK actions and 3 terminal DECISION actions.

**Evidence Gathering:**

| Action | Description |
|---|---|
| `CHECK_PAYMENT_HISTORY` | Review payment method, card details, prior transactions, and chargeback history |
| `CHECK_IP_LOCATION` | Check IP geolocation, VPN/proxy detection, and location consistency with account history |
| `CHECK_DEVICE_FINGERPRINT` | Examine device hash, browser fingerprint, cookie history, and known fraud cluster matches |
| `CHECK_ORDER_VALUE` | Analyze order amount, item categories, quantity patterns, and purchase timing |
| `CHECK_SHIPPING_ADDRESS` | Verify shipping/billing address match, address type (residential vs. CMRA), and redirect history |
| `CHECK_CUSTOMER_HISTORY` | Review account age, email type, phone verification, social logins, and behavioral patterns |

**Terminal Decisions:**

| Action | Description |
|---|---|
| `APPROVE` | Order is legitimate — approve for fulfillment |
| `REJECT` | Order is fraudulent — block the transaction |
| `ESCALATE` | Order is ambiguous — escalate to human review |

Each action also accepts an optional `reasoning` field (max 500 characters) for interpretability. The reasoning is not used in grading but is preserved in the observation history.

## Observation Space

After each step, the agent receives an observation with the following fields:

| Field | Type | Description |
|---|---|---|
| `order_summary` | `str` | Human-readable description of the order under investigation |
| `signals_gathered` | `list[SignalResult]` | Cumulative list of all evidence collected so far. Each entry contains `signal_name`, `value` (detailed text), and `risk_level` (LOW, MEDIUM, or HIGH) |
| `available_actions` | `list[str]` | Actions the agent can still take. CHECK actions are removed once used; DECISION actions remain available until the episode ends |
| `steps_remaining` | `int` | How many steps the agent has left before forced termination |
| `message` | `str` | Environment feedback about the last action taken |
| `done` | `bool` | Whether the episode is complete |
| `reward` | `float` | Reward signal for the current step |

## Task Descriptions

### Task 1 — Easy (3 scenarios)

**Difficulty:** Beginner | **Max steps:** 8 | **Ground truth:** FRAUD | **Grading:** 100% decision accuracy, 0% evidence quality

Obvious fraud with nearly every signal at HIGH risk. These scenarios test basic comprehension and pattern recognition — any 1-2 signals are sufficient to identify the fraud. The agent should check a couple of signals for confirmation and then REJECT decisively.

**Scenarios:**
- **Card Testing Bot** — Automated $25 gift card purchases from a 3-minute-old account using a prepaid card from a dark-web leak, routed through a TOR exit node with a headless Selenium browser
- **Reshipping Mule** — Four Samsung Galaxy S24 Ultras ($5,196) on a stolen Visa, shipped to a known CMRA reshipping warehouse in Miami while the IP originates from Moscow via ExpressVPN
- **Synthetic Identity** — $7,196 in mixed high-resale electronics (TV, camera, drone) purchased with a business Amex tied to a deceased individual's SSN, with an AI-generated profile photo

### Task 2 — Medium (3 scenarios)

**Difficulty:** Intermediate | **Max steps:** 10 | **Ground truth:** LEGITIMATE | **Grading:** 50% decision accuracy, 50% evidence quality (min 4 relevant signals for full evidence score)

Legitimate orders that appear suspicious on the surface. One or two signals present as HIGH or MEDIUM risk — these are red herrings that a thorough investigator should see through. The agent must gather 3-4 signals to overcome initial suspicion and correctly APPROVE. Jumping to REJECT based on a single alarming signal is the trap.

**Scenarios:**
- **Business Traveler** — A 2.5-year customer ordering a Dell laptop from a Tokyo hotel IP (HIGH risk on IP location) while traveling for work. Device fingerprint, payment history, and customer history all confirm legitimacy
- **Engagement Ring** — A 4-year customer making a $9,049 jewelry purchase (73x their average transaction, HIGH risk on order value). Browsing analytics show 14 visits to the jewelry category over 3 weeks and a wishlist addition 8 days prior
- **Student New Address** — A 1.5-year student account shipping to a new Princeton dorm address via an institutional VPN (MEDIUM risk on IP and device). A seasonal pattern — they made an identical back-to-school purchase the previous fall

### Task 3 — Hard (3 scenarios)

**Difficulty:** Advanced | **Max steps:** 12 | **Ground truth:** FRAUD | **Grading:** 40% decision accuracy, 60% evidence quality (min 5 relevant signals for full evidence score)

Sophisticated fraud where the surface looks clean. Individual signals are predominantly MEDIUM risk — no single signal is a smoking gun. The agent must synthesize 4-5 signals to recognize cross-referential patterns that only emerge in combination. These scenarios are designed to genuinely challenge frontier LLMs.

**Scenarios:**
- **Triangulation Fraud** — An 8-month account with 15 prior clean orders. Recent card swap (after a chargeback on the old card), shared IP/device hash with 2 other flagged accounts, and shipping to an unrelated third party's home address — the classic triangulation pattern
- **Employee Discount Abuse** — A verified employee purchasing premium audio products through the customer-facing POS (bypassing the employee portal's monthly limit). 14 headphone purchases in 3 months, $4,200 in cumulative discounts, with 9 of 11 shipments re-shipped to an eBay seller's warehouse within 48 hours
- **Account Takeover Bust-Out** — A 6-month account with an 18-order history of gradually increasing purchases. A password reset 12 days ago correlates with a new device, new IP subnet, disabled 2FA, changed recovery email, and changed phone number. The original owner's unanswered fraud alerts confirm compromise

## Reward Structure

The environment provides two types of reward signals:

**Per-step rewards** (returned immediately after each CHECK action):
- **+0.08** for checking a relevant signal (0.10 signal value minus 0.02 investigation cost)
- **+0.00** for checking an irrelevant signal (0.02 signal value minus 0.02 investigation cost)
- **-0.10** for duplicate checks (the signal was already investigated)

**Terminal reward** (returned with the DECISION action):
The grader score combines decision accuracy and evidence quality into a single `[0.0, 1.0]` score.

**Penalties** (accumulated and applied to the terminal score):
- **-0.30** for making a decision without gathering any evidence
- **-0.10** per duplicate check
- **-0.20** for exceeding the maximum step count

**Efficiency bonus:**
- **+0.05** for making a correct decision (decision score >= 0.8) before the halfway point of the episode

## Grading Formula

```
final_score = (decision_weight x decision_score) + (evidence_weight x evidence_score) + penalties + bonuses
```

Clamped to **[0.0, 1.0]**.

- `decision_score` is looked up from the decision scoring matrix below
- `evidence_score = min(relevant_signals_checked / min_signals_for_full_evidence, 1.0)`
- `penalties` accumulate from duplicate checks, no-evidence decisions, and exceeded steps
- `bonuses` include the efficiency bonus for fast correct decisions

**Grading weights by task:**

| Task | Decision Weight | Evidence Weight | Min Signals for Full Evidence |
|---|---|---|---|
| `task_easy` | 1.0 | 0.0 | 2 |
| `task_medium` | 0.5 | 0.5 | 4 |
| `task_hard` | 0.4 | 0.6 | 5 |

**Decision scoring matrix:**

| Ground Truth | APPROVE | REJECT | ESCALATE |
|---|---|---|---|
| **FRAUD** | 0.0 | 1.0 | 0.6 |
| **LEGITIMATE** | 1.0 | 0.1 | 0.5 |
| **AMBIGUOUS** | 0.4 | 0.4 | 0.8 |

## Setup Instructions

```bash
# Clone the repository
git clone <repo-url>
cd fraud_detection

# Install dependencies
pip install openenv-core

# Validate the environment
openenv validate

# Build the Docker image
openenv build

# Run the server locally
uvicorn server.app:app --host 0.0.0.0 --port 8000

# Run the baseline inference
export HF_TOKEN=your_token_here
export IMAGE_NAME=fraud_detection-env:latest
python -m fraud_detection.inference
```

## Baseline Scores

| Task | Seed 0 | Seed 1 | Seed 2 | Average |
|---|---|---|---|---|
| `task_easy` | TBD | TBD | TBD | TBD |
| `task_medium` | TBD | TBD | TBD | TBD |
| `task_hard` | TBD | TBD | TBD | TBD |

Baseline scores will be updated after running inference with the evaluation model.

## Project Structure

```
fraud_detection/
├── models.py                  # Action, Observation, State Pydantic models
├── constants.py               # 9 scenarios, grading config, penalties
├── client.py                  # WebSocket client for environment communication
├── inference.py               # Baseline inference script (LLM agent)
├── openenv.yaml               # OpenEnv spec metadata
├── server/
│   ├── fraud_detection_environment.py  # Core environment logic (reset/step/state)
│   ├── app.py                 # FastAPI server with WebSocket endpoints
│   └── Dockerfile             # Multi-stage Docker build
└── README.md
```
