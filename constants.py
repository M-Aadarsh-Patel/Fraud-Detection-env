# ──────────────────────────────────────────────────────────────────────
#  EASY SCENARIOS  (ground_truth: FRAUD, all signals HIGH, max_steps: 8)
# ──────────────────────────────────────────────────────────────────────

easy_card_testing_bot = {
    "scenario_id": "easy_card_testing_bot",
    "task_id": "task_easy",
    "order_id": "ORD-20250715-3341",
    "order_summary": (
        "Order #ORD-20250715-3341: Customer 'test_user_48271' placed an order "
        "for 5x $25 Amazon Gift Cards totaling $125.00. Account was created "
        "3 minutes ago. Payment via prepaid Mastercard. Delivery method: "
        "email (digital delivery)."
    ),
    "ground_truth": "FRAUD",
    "relevant_signals": [
        "CHECK_PAYMENT_HISTORY",
        "CHECK_DEVICE_FINGERPRINT",
        "CHECK_CUSTOMER_HISTORY",
    ],
    "max_steps": 8,
    "signals": {
        "CHECK_PAYMENT_HISTORY": {
            "value": (
                "Prepaid Mastercard ending 1092. Card issued earlier today. "
                "14 declined authorization attempts across 6 different merchants "
                "in the last 20 minutes before this transaction succeeded. "
                "BIN matches a batch of card numbers leaked on a dark-web "
                "marketplace 36 hours ago. No prior successful transactions on this card."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_IP_LOCATION": {
            "value": (
                "IP 185.220.xx.xx geolocates to Bucharest, Romania. Connection "
                "identified as a TOR exit node (relay fingerprint matches known "
                "exit list). Browser timezone is set to America/Chicago but "
                "system locale reports ro_RO. JavaScript Date object returns "
                "UTC+2 offset despite the spoofed timezone string."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_DEVICE_FINGERPRINT": {
            "value": (
                "Device hash: first-time-seen. Headless Chromium 121 with "
                "Selenium WebDriver flags (navigator.webdriver = true). Screen "
                "resolution reported as 1x1 pixel, consistent with a non-visual "
                "automation harness. Canvas fingerprint matches known automated "
                "testing framework signature AT-0447. No cookies or local "
                "storage from any prior session."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_ORDER_VALUE": {
            "value": (
                "Order total $125.00. Five identical $25 digital gift cards — "
                "gift cards are untraceable once redeemed and are a top target "
                "for card-testing fraud. Order was placed 3 minutes after "
                "account creation with zero browsing history. Pattern matches "
                "known card-validation workflow: low-value, instant-delivery, "
                "non-reversible digital goods."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_SHIPPING_ADDRESS": {
            "value": (
                "Delivery is digital — gift card codes sent via email to "
                "xkq8821@tempmail.lol. The email domain (tempmail.lol) is a "
                "known disposable/temporary email service with a 24-hour inbox "
                "lifespan. No physical shipping address was provided or required. "
                "Digital delivery eliminates any address-verification check."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_CUSTOMER_HISTORY": {
            "value": (
                "Account age: 3 minutes. Zero prior orders or browsing sessions. "
                "Username follows an auto-generated pattern (test_user_NNNNN). "
                "Email: xkq8821@tempmail.lol (disposable). No phone number on "
                "file. CAPTCHA on registration was solved in 0.4 seconds, "
                "consistent with a CAPTCHA-solving API service. Account was "
                "created via the API, not the web storefront."
            ),
            "risk_level": "HIGH",
        },
    },
}

easy_reshipping_mule = {
    "scenario_id": "easy_reshipping_mule",
    "task_id": "task_easy",
    "order_id": "ORD-20250718-5582",
    "order_summary": (
        "Order #ORD-20250718-5582: Customer 'sandra.k.johnson' placed an order "
        "for 4x Samsung Galaxy S24 Ultra totaling $5,196.00. Account was created "
        "45 minutes ago. Payment via Visa credit card. Shipping to Miami, FL "
        "while billing address is in New York, NY."
    ),
    "ground_truth": "FRAUD",
    "relevant_signals": [
        "CHECK_PAYMENT_HISTORY",
        "CHECK_SHIPPING_ADDRESS",
        "CHECK_CUSTOMER_HISTORY",
    ],
    "max_steps": 8,
    "signals": {
        "CHECK_PAYMENT_HISTORY": {
            "value": (
                "Visa ending 7293. Cardholder name on card: 'Michael R. Thornton' "
                "— does not match account holder name 'Sandra K. Johnson'. Card "
                "was reported stolen by the real cardholder 2 days ago via issuing "
                "bank. BIN country: United States. Three declined attempts with "
                "different card numbers preceded this successful transaction."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_IP_LOCATION": {
            "value": (
                "IP 91.134.xx.xx geolocates to Moscow, Russia. VPN detected: "
                "Yes (ExpressVPN exit node, server ID: russia-moscow-01). Browser "
                "Accept-Language header is set to ru-RU,ru;q=0.9 despite the "
                "account profile claiming a United States location. System clock "
                "offset indicates UTC+3 (Moscow time)."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_DEVICE_FINGERPRINT": {
            "value": (
                "Device hash: first-time-seen. Browser: Chrome 122 running on "
                "an Android emulator (BlueStacks 5 detected via WebGL renderer "
                "string). Screen resolution matches BlueStacks default 1600x900. "
                "Canvas fingerprint is associated with fraud cluster FC-4418 "
                "(linked to 23 confirmed fraud cases this month). No cookies "
                "from prior sessions."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_ORDER_VALUE": {
            "value": (
                "Order total $5,196.00. Four identical flagship smartphones in "
                "a single order — a high-resale electronics category. Quantity "
                "of 4 far exceeds the typical single-customer purchase average "
                "of 1.0 for this SKU. Total exceeds the new-account velocity "
                "threshold of $500 by 10x. Items are supply-constrained with "
                "active secondary-market demand."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_SHIPPING_ADDRESS": {
            "value": (
                "Shipping to: 2200 NW 129th St, Unit 8, Miami, FL 33167. This "
                "address is registered in the USPS Commercial Mail Receiving "
                "Agency (CMRA) database as a known reshipping warehouse operated "
                "by 'Global Express Forwarding LLC'. Billing address: 445 Park "
                "Ave, New York, NY 10022 — a commercial office building lobby "
                "address with no residential units."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_CUSTOMER_HISTORY": {
            "value": (
                "Account age: 45 minutes. Zero prior orders or site visits. "
                "Email: s.k.johnson8827@protonmail.com (encrypted email provider, "
                "account creation date unknown). Phone: Google Voice VoIP number, "
                "not tied to any mobile carrier. Account name 'Sandra K. Johnson' "
                "does not match payment card name 'Michael R. Thornton'. No "
                "social logins connected."
            ),
            "risk_level": "HIGH",
        },
    },
}

easy_synthetic_identity = {
    "scenario_id": "easy_synthetic_identity",
    "task_id": "task_easy",
    "order_id": "ORD-20250720-9914",
    "order_summary": (
        "Order #ORD-20250720-9914: Customer 'david.martinez.store' placed an "
        "order for 1x 65\" LG OLED C4 TV ($2,499.00), 1x Sony A7 IV Camera "
        "($2,498.00), and 1x DJI Mavic 3 Pro Drone ($2,199.00) totaling "
        "$7,196.00. Account is 2 days old. Payment via Amex card."
    ),
    "ground_truth": "FRAUD",
    "relevant_signals": [
        "CHECK_PAYMENT_HISTORY",
        "CHECK_DEVICE_FINGERPRINT",
        "CHECK_CUSTOMER_HISTORY",
    ],
    "max_steps": 8,
    "signals": {
        "CHECK_PAYMENT_HISTORY": {
            "value": (
                "Amex card ending 6601. Card was added to account 15 minutes "
                "ago. Only one prior transaction exists on this card: a $0.50 "
                "charity micro-donation made 3 hours ago — a classic stolen-card "
                "validation pattern. BIN traces to a business Amex issued to "
                "'DM Holdings LLC', an entity with no verifiable business "
                "registration or web presence."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_IP_LOCATION": {
            "value": (
                "IP 172.58.xx.xx geolocates to a DigitalOcean data center in "
                "Dallas, TX — not a residential ISP. This IP is flagged as a "
                "known cloud-hosting provider address. Browser timezone is set "
                "to America/Denver, which does not match the Dallas IP location. "
                "Seven other accounts flagged for fraud have connected from this "
                "same IP block in the past 14 days."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_DEVICE_FINGERPRINT": {
            "value": (
                "Device hash has been observed on 7 other accounts in the past "
                "30 days, all flagged or confirmed as fraud. Browser: Firefox 121 "
                "with privacy.resistFingerprinting enabled. WebGL rendering is "
                "deliberately disabled. Canvas API returns a blank image — active "
                "anti-fingerprint countermeasures detected. User-agent string "
                "shows signs of manual spoofing (mismatched OS build number)."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_ORDER_VALUE": {
            "value": (
                "Order total $7,196.00. Three unrelated high-resale electronics "
                "categories in a single order: TV, camera, and drone. All items "
                "are top-resale-value SKUs in their category. Combined total "
                "exceeds the new-account risk threshold ($500) by 14x. The items "
                "have no logical coherence as a personal purchase bundle."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_SHIPPING_ADDRESS": {
            "value": (
                "Shipping to: 8875 Hidden River Pkwy, Suite 300, Tampa, FL "
                "33637. Address is a Regus co-working space — a virtual office "
                "and mailbox rental facility, not a residence. Billing address: "
                "1200 Elm St, Apt 4A, Denver, CO 80220 — USPS records list "
                "this unit as vacant for the past 6 months. No forwarding "
                "address on file."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_CUSTOMER_HISTORY": {
            "value": (
                "Account age: 2 days. Zero completed orders. Email: "
                "d.martinez.store@outlook.com, created 3 days ago per header "
                "metadata. Phone: TextNow VoIP number, not tied to a physical "
                "SIM. The SSN associated with the Amex application matches a "
                "deceased individual in the SSA Death Master File (died 2019). "
                "Profile photo flagged by automated analysis as AI-generated "
                "(GAN artifact patterns detected)."
            ),
            "risk_level": "HIGH",
        },
    },
}

# ──────────────────────────────────────────────────────────────────────
#  MEDIUM SCENARIOS  (ground_truth: LEGITIMATE, max_steps: 10)
#  1–2 signals MEDIUM/HIGH (red herrings), rest LOW
# ──────────────────────────────────────────────────────────────────────

medium_business_traveler = {
    "scenario_id": "medium_business_traveler",
    "task_id": "task_medium",
    "order_id": "ORD-20250722-2104",
    "order_summary": (
        "Order #ORD-20250722-2104: Customer 'patricia.nguyen.dev' placed an "
        "order for 1x Dell XPS 15 Laptop ($1,849.00) and 1x USB-C Docking "
        "Station ($89.00) totaling $1,938.00. Account is 2.5 years old. "
        "Payment via Visa credit card on file. Shipping to a hotel address "
        "in Tokyo, Japan."
    ),
    "ground_truth": "LEGITIMATE",
    "relevant_signals": [
        "CHECK_IP_LOCATION",
        "CHECK_DEVICE_FINGERPRINT",
        "CHECK_ORDER_VALUE",
        "CHECK_CUSTOMER_HISTORY",
    ],
    "max_steps": 10,
    "signals": {
        "CHECK_PAYMENT_HISTORY": {
            "value": (
                "Visa ending 5578. Card on file for 2 years. 31 prior successful "
                "transactions ranging from $15 to $1,200. Zero chargebacks. "
                "Average transaction: $245. This purchase amount ($1,938) is "
                "within 2 standard deviations of the customer's spending pattern "
                "and does not trigger the card issuer's velocity alert."
            ),
            "risk_level": "LOW",
        },
        "CHECK_IP_LOCATION": {
            "value": (
                "IP 126.78.xx.xx geolocates to Tokyo, Japan. VPN detected: No. "
                "ISP: NTT Communications (hotel/hospitality Wi-Fi network). "
                "Customer's historical logins are 100 percent from San Francisco, CA, "
                "USA. However: customer's linked Instagram account shows geotagged "
                "posts from Shibuya, Tokyo uploaded 6 hours ago, and the customer "
                "updated their account's travel notification flag 5 days ago."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_DEVICE_FINGERPRINT": {
            "value": (
                "Device hash matches the primary device on file — MacBook Pro "
                "running Safari 17.3. Canvas fingerprint is consistent with all "
                "prior sessions. Cookies from 14 previous sessions are present. "
                "OS was recently updated to macOS 15.2, which is the only change "
                "from the last login. All device attributes match the known profile."
            ),
            "risk_level": "LOW",
        },
        "CHECK_ORDER_VALUE": {
            "value": (
                "Order total $1,938.00. This is 7.9x the customer's average "
                "transaction of $245. However: the customer purchased a Dell XPS "
                "13 for $1,649.00 approximately 2.5 years ago — a tech-refresh "
                "cycle is plausible. The inclusion of a USB-C docking station "
                "suggests a work-setup replacement. Purchase timing: Tuesday "
                "2:15 PM PT, within the customer's typical active hours."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_SHIPPING_ADDRESS": {
            "value": (
                "Shipping to: 2-6-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 160-8330, "
                "Japan (Hilton Tokyo). Billing address: 582 Valencia St, San "
                "Francisco, CA 94110. Addresses are in different countries. "
                "However: the shipping address is a verified Hilton property and "
                "the customer's account has a business-travel flag enabled. Dell "
                "supports international shipping for business-tier accounts."
            ),
            "risk_level": "LOW",
        },
        "CHECK_CUSTOMER_HISTORY": {
            "value": (
                "Account age: 2 years, 7 months. 31 prior orders, all fulfilled "
                "without incident. Email: p.nguyen@techcorp.io (verified corporate "
                "email, established domain). Phone: verified US mobile number, "
                "unchanged since signup. Social login: connected Google Workspace "
                "account. Customer has left 8 product reviews and holds Gold "
                "loyalty tier."
            ),
            "risk_level": "LOW",
        },
    },
}

medium_engagement_ring = {
    "scenario_id": "medium_engagement_ring",
    "task_id": "task_medium",
    "order_id": "ORD-20250725-6678",
    "order_summary": (
        "Order #ORD-20250725-6678: Customer 'james.oconnor.52' placed an order "
        "for 1x 1.5ct Diamond Solitaire Engagement Ring ($8,750.00) and 1x "
        "Ring Insurance Plan ($299.00) totaling $9,049.00. Account is 4 years "
        "old. Payment via Mastercard credit card on file. Shipping to home "
        "address on record."
    ),
    "ground_truth": "LEGITIMATE",
    "relevant_signals": [
        "CHECK_PAYMENT_HISTORY",
        "CHECK_ORDER_VALUE",
        "CHECK_SHIPPING_ADDRESS",
        "CHECK_CUSTOMER_HISTORY",
    ],
    "max_steps": 10,
    "signals": {
        "CHECK_PAYMENT_HISTORY": {
            "value": (
                "Mastercard ending 3390. Card on file for 3.5 years. 47 prior "
                "successful transactions ranging from $8 to $450. Zero "
                "chargebacks. Average transaction: $124. However: a second card "
                "on file (Visa ending 8812) has been used for larger purchases "
                "up to $1,800. Customer has a consistent history of using "
                "different cards for different price tiers."
            ),
            "risk_level": "LOW",
        },
        "CHECK_IP_LOCATION": {
            "value": (
                "IP 68.105.xx.xx geolocates to Naperville, IL, USA. VPN "
                "detected: No. ISP: AT&T residential broadband. This IP is "
                "consistent with 90% of the customer's historical logins. "
                "Location matches the billing address city. No geographic "
                "anomalies detected."
            ),
            "risk_level": "LOW",
        },
        "CHECK_DEVICE_FINGERPRINT": {
            "value": (
                "Device hash matches the primary device observed in 38 of 47 "
                "prior sessions — Windows 11 desktop running Chrome 123. Canvas "
                "fingerprint is consistent with prior sessions. Cookies from 12 "
                "recent sessions present. Browser version was updated normally "
                "through Chrome's auto-update mechanism."
            ),
            "risk_level": "LOW",
        },
        "CHECK_ORDER_VALUE": {
            "value": (
                "Order total $9,049.00. This is 73x the customer's average "
                "transaction of $124. Highest prior order was $450. Category: "
                "fine jewelry — customer has never purchased from this category "
                "before on this platform. However: browsing analytics show the "
                "customer visited the jewelry category 14 times over the past "
                "3 weeks and added this item to their wishlist 8 days ago before "
                "purchasing, indicating deliberate research rather than impulse."
            ),
            "risk_level": "HIGH",
        },
        "CHECK_SHIPPING_ADDRESS": {
            "value": (
                "Shipping to: 1247 Benton Ave, Naperville, IL 60540. This is "
                "the customer's billing address on file — billing and shipping "
                "match exactly. Address verified via USPS as a single-family "
                "residential home. No address changes have been made on the "
                "account in 4 years."
            ),
            "risk_level": "LOW",
        },
        "CHECK_CUSTOMER_HISTORY": {
            "value": (
                "Account age: 4 years, 1 month. 47 prior orders, all fulfilled "
                "successfully. Email: joconnor52@comcast.net (long-standing ISP "
                "email, not disposable). Phone: verified landline, same number "
                "since account creation. No social login connected, but email "
                "verified via confirmation link. Customer has contacted support "
                "twice (both were shipping inquiries, resolved positively)."
            ),
            "risk_level": "LOW",
        },
    },
}

medium_student_new_address = {
    "scenario_id": "medium_student_new_address",
    "task_id": "task_medium",
    "order_id": "ORD-20250801-3390",
    "order_summary": (
        "Order #ORD-20250801-3390: Customer 'emma.liu.2003' placed an order for "
        "1x iPad Air M2 ($749.00) and 3x college textbooks ($187.00 combined) "
        "totaling $936.00. Account is 1.5 years old. Payment via Discover card "
        "on file. Shipping address was recently changed to New Jersey."
    ),
    "ground_truth": "LEGITIMATE",
    "relevant_signals": [
        "CHECK_IP_LOCATION",
        "CHECK_DEVICE_FINGERPRINT",
        "CHECK_SHIPPING_ADDRESS",
        "CHECK_CUSTOMER_HISTORY",
    ],
    "max_steps": 10,
    "signals": {
        "CHECK_PAYMENT_HISTORY": {
            "value": (
                "Discover card ending 4455. Card on file for 8 months. 12 prior "
                "successful transactions ranging from $9 to $320. Zero "
                "chargebacks. Average transaction: $67. Card billing name "
                "matches account name exactly. Card issuer confirms no fraud "
                "alerts on this account."
            ),
            "risk_level": "LOW",
        },
        "CHECK_IP_LOCATION": {
            "value": (
                "IP 128.112.xx.xx geolocates to Princeton, NJ. VPN detected: "
                "Yes — identified as an institutional VPN (Princeton University "
                "network, ASN AS88). Customer's historical logins are all from "
                "Seattle, WA (residential Comcast). However: the IP resolves to "
                "Princeton University's ResNet residential dormitory network, "
                "consistent with a student who recently relocated for the fall "
                "semester."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_DEVICE_FINGERPRINT": {
            "value": (
                "Device hash: new device, not previously seen on this account. "
                "Browser: Safari 17 on macOS 14 (MacBook Air). Customer's prior "
                "12 sessions were all from Chrome on Windows 10. However: this "
                "new device was first used 5 days ago to log in, change the "
                "account password (via email verification link sent to the "
                "account's verified email), and update the shipping address — "
                "a pattern consistent with a normal device transition."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_ORDER_VALUE": {
            "value": (
                "Order total $936.00. While higher than the average transaction "
                "of $67, the customer purchased a similar back-to-school bundle "
                "(laptop + textbooks) during the previous fall semester for "
                "$892.00. Purchase timing is August, aligning with the academic "
                "calendar pre-semester preparation period. The combination of "
                "an iPad and textbooks is a common student purchase pattern."
            ),
            "risk_level": "LOW",
        },
        "CHECK_SHIPPING_ADDRESS": {
            "value": (
                "Shipping to: 221 Nassau Hall, Princeton University, Princeton, "
                "NJ 08544. Billing address: 14320 NE 21st St, Bellevue, WA "
                "98007. Addresses are in different states. However: customer "
                "updated their shipping address 6 days ago in the same session "
                "as the password change. The new address is a verified Princeton "
                "University dormitory listed in the university's public housing "
                "directory."
            ),
            "risk_level": "LOW",
        },
        "CHECK_CUSTOMER_HISTORY": {
            "value": (
                "Account age: 1 year, 6 months. 12 prior orders, all fulfilled "
                "successfully. Email: emma.liu.2003@gmail.com (established Gmail, "
                "not disposable). Phone: verified mobile with 206 area code "
                "(Seattle). Social login: connected Apple ID. Customer has left "
                "3 product reviews for previous textbook purchases. Loyalty tier: "
                "Student (verified .edu email emma.liu@princeton.edu on file)."
            ),
            "risk_level": "LOW",
        },
    },
}

# ──────────────────────────────────────────────────────────────────────
#  HARD SCENARIOS  (ground_truth: FRAUD, mostly MEDIUM risk, max_steps: 12)
#  Fraud only becomes clear when 4–5 signals are synthesized together
# ──────────────────────────────────────────────────────────────────────

hard_triangulation_fraud = {
    "scenario_id": "hard_triangulation_fraud",
    "task_id": "task_hard",
    "order_id": "ORD-20250805-7721",
    "order_summary": (
        "Order #ORD-20250805-7721: Customer 'market_deals_prime' placed an "
        "order for 1x Dyson V15 Detect Vacuum ($749.99) and 1x Dyson Airwrap "
        "($599.99) totaling $1,349.98. Account is 8 months old with 15 prior "
        "orders. Payment via Visa credit card. Shipping to Charlotte, NC."
    ),
    "ground_truth": "FRAUD",
    "relevant_signals": [
        "CHECK_PAYMENT_HISTORY",
        "CHECK_IP_LOCATION",
        "CHECK_DEVICE_FINGERPRINT",
        "CHECK_SHIPPING_ADDRESS",
        "CHECK_CUSTOMER_HISTORY",
    ],
    "max_steps": 12,
    "signals": {
        "CHECK_PAYMENT_HISTORY": {
            "value": (
                "Visa ending 2918. Card was added to account 2 weeks ago, "
                "replacing a prior Mastercard ending 6650 that was removed. "
                "Three transactions on the new card, all successful ($120–$500 "
                "range). However: the removed Mastercard was involved in a "
                "chargeback dispute on a different merchant 10 days ago. The new "
                "Visa's BIN is issued by a credit union in rural Ohio, while the "
                "account profile lists a Los Angeles, CA address."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_IP_LOCATION": {
            "value": (
                "IP 104.28.xx.xx geolocates to Los Angeles, CA — matches the "
                "account's stated location. VPN detected: No. ISP: Spectrum "
                "residential. However: this specific IP has appeared on 2 other "
                "accounts that placed similar high-value Dyson orders in the past "
                "3 weeks. The IP's association with this account only began 3 "
                "weeks ago; prior logins used a different Spectrum IP range."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_DEVICE_FINGERPRINT": {
            "value": (
                "Device hash: seen on this account for 3 weeks (since the card "
                "change event). Browser: Chrome 122 on Windows 11. However: this "
                "exact device hash also appears on 2 other unrelated accounts — "
                "the same accounts that share the IP address. The prior device "
                "used on this account (Chrome on macOS) was last seen 4 weeks "
                "ago and has not logged in since."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_ORDER_VALUE": {
            "value": (
                "Order total $1,349.98. Amount falls within the range of the "
                "account's recent purchases. Dyson products are popular legitimate "
                "home-appliance purchases. Quantity of 1 each is normal consumer "
                "behavior. Purchase timing: Thursday 1:42 PM PT, a typical "
                "weekday shopping window. No value-based anomaly on its own."
            ),
            "risk_level": "LOW",
        },
        "CHECK_SHIPPING_ADDRESS": {
            "value": (
                "Shipping to: 4512 Maple Ridge Dr, Charlotte, NC 28277. Billing "
                "address: 9100 Wilshire Blvd, Apt 320, Los Angeles, CA 90212. "
                "Addresses are in different states (~2,200 miles apart). However: "
                "the Charlotte address is a verified residential home belonging "
                "to a real individual with a different name than the account "
                "holder — matching the triangulation pattern of buying with stolen "
                "payment and shipping to an unwitting third-party customer."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_CUSTOMER_HISTORY": {
            "value": (
                "Account age: 8 months. 15 total orders. First 12 orders (months "
                "1–7) were all small household items ($15–$80), shipped to the "
                "LA billing address. The last 3 orders (past 3 weeks only) shifted "
                "to high-value electronics shipped to various out-of-state "
                "residential addresses. However: the account email "
                "(market.deals.prime@gmail.com) is verified and the phone is a "
                "real mobile number. No support tickets or complaints on file."
            ),
            "risk_level": "MEDIUM",
        },
    },
}

hard_employee_discount_abuse = {
    "scenario_id": "hard_employee_discount_abuse",
    "task_id": "task_hard",
    "order_id": "ORD-20250808-4455",
    "order_summary": (
        "Order #ORD-20250808-4455: Customer 'kevin.r.walsh' placed an order "
        "for 2x Bose QuietComfort Ultra Headphones ($429.00 each) and 2x "
        "Apple AirPods Max ($549.00 each) totaling $1,956.00 before employee "
        "discount. After 40% employee discount, charged $1,173.60. Account is "
        "1 year old with employee verification."
    ),
    "ground_truth": "FRAUD",
    "relevant_signals": [
        "CHECK_PAYMENT_HISTORY",
        "CHECK_IP_LOCATION",
        "CHECK_DEVICE_FINGERPRINT",
        "CHECK_ORDER_VALUE",
        "CHECK_SHIPPING_ADDRESS",
        "CHECK_CUSTOMER_HISTORY",
    ],
    "max_steps": 12,
    "signals": {
        "CHECK_PAYMENT_HISTORY": {
            "value": (
                "Debit card ending 8810. Card on file for 11 months. 28 prior "
                "transactions, all successful. Zero chargebacks. Average "
                "transaction: $156. Card issuer name and account holder name "
                "match. No anomalies in payment method itself — clean payment "
                "history with no declined transactions or alerts."
            ),
            "risk_level": "LOW",
        },
        "CHECK_IP_LOCATION": {
            "value": (
                "IP 10.0.xx.xx — internal corporate network, Store #0447, "
                "Austin, TX. All purchases on this account have been made from "
                "the corporate network during store hours (11 AM–7 PM CT). "
                "However: the employee's scheduled shifts for the past month are "
                "6 AM–2 PM CT. The purchases between 5–7 PM occur after the "
                "employee's shift ends, suggesting off-the-clock access or "
                "credential sharing."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_DEVICE_FINGERPRINT": {
            "value": (
                "Device hash matches an in-store POS terminal (Terminal #12, "
                "Store #0447). This same terminal has been used for all 28 prior "
                "purchases on this account. However: company policy requires "
                "employee discount purchases to be processed through the dedicated "
                "employee portal (emp.store.com), not the customer-facing POS "
                "system. Processing through the POS bypasses the monthly employee "
                "purchase limit enforcement system."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_ORDER_VALUE": {
            "value": (
                "Order total after 40 percent employee discount: $1,173.60 "
                "(pre-discount: $1,956.00). All four items are premium audio "
                "products with high resale margins. The employee has purchased "
                "14 headphone and audio products across 28 orders in the past "
                "3 months. Cumulative employee discount applied this quarter: "
                "$4,200. All discounted items fall within the same product "
                "category (premium audio) rather than a diverse personal-use "
                "mix."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_SHIPPING_ADDRESS": {
            "value": (
                "Shipping to: 3321 S Lamar Blvd, Austin, TX 78704 — matches "
                "the employee's home address in the HR file. No address mismatch. "
                "However: USPS and UPS tracking cross-reference shows that 9 of "
                "the last 11 employee-discount shipments delivered to this address "
                "were re-shipped within 48 hours via a separate UPS pickup. "
                "Re-shipment destination: a registered eBay seller's warehouse "
                "address in Houston, TX."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_CUSTOMER_HISTORY": {
            "value": (
                "Account age: 1 year, 1 month. Employee-verified account (badge "
                "#E-4471, Store #0447 Austin). 28 prior orders. Email: "
                "kevin.walsh@company.com (corporate email). Phone: verified "
                "mobile. HR status: active full-time associate. No disciplinary "
                "actions on this employee's record. However: two other employees "
                "at the same store had their accounts terminated 6 months ago "
                "for an identical purchasing pattern — high-volume audio products "
                "via POS bypass."
            ),
            "risk_level": "MEDIUM",
        },
    },
}

hard_bust_out_account_takeover = {
    "scenario_id": "hard_bust_out_account_takeover",
    "task_id": "task_hard",
    "order_id": "ORD-20250812-1189",
    "order_summary": (
        "Order #ORD-20250812-1189: Customer 'sarah.m.patel.91' placed an order "
        "for 1x 75\" Samsung Neo QLED TV ($2,799.00), 1x Sonos Arc Soundbar "
        "($899.00), and 1x PlayStation 5 Pro ($699.00) totaling $4,397.00. "
        "Account is 6 months old with 18 prior orders. Payment via Visa credit "
        "card on file. Shipping to home address on record."
    ),
    "ground_truth": "FRAUD",
    "relevant_signals": [
        "CHECK_PAYMENT_HISTORY",
        "CHECK_IP_LOCATION",
        "CHECK_DEVICE_FINGERPRINT",
        "CHECK_ORDER_VALUE",
        "CHECK_SHIPPING_ADDRESS",
        "CHECK_CUSTOMER_HISTORY",
    ],
    "max_steps": 12,
    "signals": {
        "CHECK_PAYMENT_HISTORY": {
            "value": (
                "Visa ending 3147. Card on file for 5 months. 18 prior "
                "successful transactions ($22–$340 range). Zero chargebacks. "
                "Average transaction: $95. However: a new secondary Mastercard "
                "ending 0092 was added 11 days ago but has not been used yet. "
                "The Visa issuing bank sent a fraud-alert inquiry 3 days ago "
                "that went unanswered by the cardholder — the alert expired "
                "without confirmation."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_IP_LOCATION": {
            "value": (
                "IP 73.222.xx.xx geolocates to Denver, CO — matches the "
                "customer's billing city. VPN detected: No. ISP: Xfinity "
                "residential. However: the customer's historical logins used "
                "IP range 73.222.14.x, while all sessions in the past 12 days "
                "originate from 73.222.91.x — same city but a different "
                "neighborhood subnet. The IP shift correlates exactly with "
                "a password-reset event 12 days ago."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_DEVICE_FINGERPRINT": {
            "value": (
                "Device hash has been seen on this account for 12 days only. "
                "Browser: Chrome 123 on Windows 11 (Dell hardware). The prior "
                "5 months of sessions used Safari on macOS exclusively. However: "
                "the device transition occurred on the same day as the password "
                "reset, and the original macOS device has not logged in since. "
                "The new device's system language is en-GB, while the old device "
                "consistently used en-US."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_ORDER_VALUE": {
            "value": (
                "Order total $4,397.00. This is 46x the customer's average "
                "transaction of $95. All three items are high-resale electronics. "
                "However: the customer's spending had been gradually increasing "
                "over 6 months ($22 → $85 → $150 → $340), which could suggest "
                "organic growth. Order was placed at 2:14 AM MT — well outside "
                "the customer's historical activity window of 9 AM–9 PM."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_SHIPPING_ADDRESS": {
            "value": (
                "Shipping to: 4700 E Alameda Ave, Denver, CO 80246 — this is "
                "the customer's verified home address on file. Billing and "
                "shipping match. However: a shipping redirect request to hold "
                "at a FedEx Office location (7200 Smith Rd, Denver, CO 80207) "
                "was filed via FedEx's portal 30 minutes after order placement. "
                "The FedEx account used for the redirect had its password changed "
                "10 days ago."
            ),
            "risk_level": "MEDIUM",
        },
        "CHECK_CUSTOMER_HISTORY": {
            "value": (
                "Account age: 6 months, 3 weeks. 18 prior orders, all small and "
                "fulfilled without issues. Email: sarah.m.patel.91@gmail.com "
                "(established, not disposable). However: the account's recovery "
                "email was changed 12 days ago (same day as the password reset). "
                "The original recovery email (sarahpatel91@yahoo.com) generated "
                "3 'unauthorized change' alerts that were never actioned. "
                "Two-factor authentication was disabled during the password reset. "
                "The linked phone number was changed 9 days ago from a 303 area "
                "code (Denver) to a 718 area code (New York)."
            ),
            "risk_level": "HIGH",
        },
    },
}


TASK_SCENARIOS: dict[str, list[dict]] = {
    "task_easy": [
        easy_card_testing_bot,
        easy_reshipping_mule,
        easy_synthetic_identity,
    ],
    "task_medium": [
        medium_business_traveler,
        medium_engagement_ring,
        medium_student_new_address,
    ],
    "task_hard": [
        hard_triangulation_fraud,
        hard_employee_discount_abuse,
        hard_bust_out_account_takeover,
    ],
}

# Flat dict keyed by scenario_id — for backward compatibility
SCENARIOS: dict[str, dict] = {
    s["scenario_id"]: s
    for pool in TASK_SCENARIOS.values()
    for s in pool
}


# GRADING CONFIGURATION

# Grading configuration per task
GRADING_CONFIG: dict[str, dict] = {
    "task_easy": {
        "decision_weight": 1.0,
        "evidence_weight": 0.0,
        "min_signals_for_full_evidence": 2,
    },
    "task_medium": {
        "decision_weight": 0.5,
        "evidence_weight": 0.5,
        "min_signals_for_full_evidence": 4,
    },
    "task_hard": {
        "decision_weight": 0.4,
        "evidence_weight": 0.6,
        "min_signals_for_full_evidence": 5,
    },
}


# Decision scoring matrix: (ground_truth, decision) → score
DECISION_SCORES: dict[tuple[str, str], float] = {
    ("FRAUD", "REJECT"): 1.0,
    ("FRAUD", "ESCALATE"): 0.6,
    ("FRAUD", "APPROVE"): 0.0,
    ("LEGITIMATE", "APPROVE"): 1.0,
    ("LEGITIMATE", "ESCALATE"): 0.5,
    ("LEGITIMATE", "REJECT"): 0.1,
    ("AMBIGUOUS", "ESCALATE"): 0.8,
    ("AMBIGUOUS", "APPROVE"): 0.4,
    ("AMBIGUOUS", "REJECT"): 0.4,
}


# PENALTIES, REWARDS, AND COSTS

PENALTY_NO_EVIDENCE = -0.3
PENALTY_DUPLICATE_CHECK = -0.1
PENALTY_EXCEEDED_STEPS = -0.2

REWARD_RELEVANT_SIGNAL = 0.1
REWARD_IRRELEVANT_SIGNAL = 0.02
INVESTIGATION_COST_PER_CHECK = 0.02


# ACTION LISTS

CHECK_ACTIONS = [
    "CHECK_PAYMENT_HISTORY",
    "CHECK_IP_LOCATION",
    "CHECK_DEVICE_FINGERPRINT",
    "CHECK_ORDER_VALUE",
    "CHECK_SHIPPING_ADDRESS",
    "CHECK_CUSTOMER_HISTORY",
]

DECISION_ACTIONS = ["APPROVE", "REJECT", "ESCALATE"]

ALL_ACTIONS = CHECK_ACTIONS + DECISION_ACTIONS

# Legacy alias
MAX_ACTIONS = ALL_ACTIONS
