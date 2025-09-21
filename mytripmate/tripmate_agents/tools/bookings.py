# tripmate_agents/tools/mock_booking.py

import random, string, time
from typing import Dict, Any
from datetime import datetime

# ---- Helpers ----
def _id(prefix: str, n: int = 6) -> str:
    return f"{prefix}{''.join(random.choices(string.ascii_uppercase + string.digits, k=n))}"

def _mask_card(last4: str = "1234") -> str:
    return f"**** **** **** {last4}"

def _mask_upi(upi_id: str = "user@upi") -> str:
    # mask before '@'
    if "@" in upi_id:
        name, dom = upi_id.split("@", 1)
        return f"{name[0]}***@{dom}"
    return "****"

# ---- EMT mock offers table (you can tweak for the hackathon) ----
EMT_OFFERS = [
    {"code": "EMTUPI100", "method": "upi",   "min_payable": 2000, "discount": 100, "desc": "₹100 off on UPI (min ₹2000)"},
    {"code": "EMTCC250",  "method": "credit","min_payable": 5000, "discount": 250, "desc": "₹250 off on Credit Card (min ₹5000)"},
    {"code": "EMTDEB150", "method": "debit", "min_payable": 3000, "discount": 150, "desc": "₹150 off on Debit Card (min ₹3000)"},
]

def find_best_offer(payable: float, method: str) -> Dict[str, Any] | None:
    cand = [o for o in EMT_OFFERS if o["method"] == method and payable >= o["min_payable"]]
    if not cand: 
        return None
    best = max(cand, key=lambda o: o["discount"])
    return best

# ---- Tool: apply coupon (mock EMT) ----
def apply_coupon(cart: Dict[str, Any]) -> Dict[str, Any]:
    """
    Input: cart dict (matches Cart schema as plain dict)
    Output: updated cart with 'discount' increased if coupon valid
    """
    coupon = (cart.get("coupon_code") or "").upper()
    subtotal = float(cart["subtotal"])
    discount = float(cart.get("discount", 0.0))

    # Simple mock: EMTNEW200 gives flat ₹200 off if subtotal >= 4000
    if coupon == "EMTNEW200" and subtotal >= 4000:
        discount += 200.0
        cart["discount"] = discount
        cart["payable"] = max(0.0, subtotal + float(cart.get("fees_taxes", 0.0)) - discount)
        cart["coupon_code"] = coupon
        cart["coupon_message"] = "Applied ₹200 EMT new-user coupon"
    else:
        cart["coupon_message"] = "No valid coupon applied"

    return cart

# ---- Tool: calculate EMT payment offer after coupon ----
def apply_payment_offer(cart: Dict[str, Any]) -> Dict[str, Any]:
    if "payable" not in cart:
        raise ValueError("Cart missing 'payable'. Call compute_cart_totals first.")

    method = cart.get("payment_method")
    if not method:
        cart["offer_message"] = "No payment method chosen yet"
        return cart
    payable = float(cart["payable"])
    offer = find_best_offer(payable, method)
    if offer:
        cart["discount"] = float(cart.get("discount", 0.0)) + offer["discount"]
        cart["payable"] = max(0.0, float(cart["subtotal"]) + float(cart.get("fees_taxes", 0.0)) - float(cart["discount"]))
        cart["payment_offer_applied"] = offer["code"]
        cart["offer_message"] = offer["desc"]
    else:
        cart["offer_message"] = "No applicable EMT payment offer"
    return cart

# tripmate_agents/tools/bookings.py
# from decimal import Decimal, ROUND_HALF_UP

# def _to_money(x) -> Decimal:
#     try:
#         return Decimal(str(x))
#     except Exception:
#         return Decimal("0")

# def _round_money(x: Decimal) -> Decimal:
#     return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

# def _compute_totals(cart: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Ensure cart has subtotal, taxes, fees, discounts, payable.
#     Accepts partial cart and fills missing fields with 0.00.
#     Expected (optional) inputs:
#       transport_price, hotel_price, activities_price, other_price,
#       taxes, fees, discounts
#     """
#     transport = _to_money(cart.get("transport_price", 0))
#     hotel = _to_money(cart.get("hotel_price", 0))
#     activities = _to_money(cart.get("activities_price", 0))
#     other = _to_money(cart.get("other_price", 0))
#     taxes = _to_money(cart.get("taxes", 0))
#     fees = _to_money(cart.get("fees", 0))
#     discounts = _to_money(cart.get("discounts", 0))
#     # Prefer explicit subtotal if present, else derive
#     subtotal = _to_money(cart.get("subtotal", transport + hotel + activities + other))
#     # payable = subtotal + taxes + fees - discounts
#     payable = subtotal + taxes + fees - discounts

#     cart["subtotal"]  = _round_money(subtotal)
#     cart["taxes"]     = _round_money(taxes)
#     cart["fees"]      = _round_money(fees)
#     cart["discounts"] = _round_money(discounts)
#     cart["payable"]   = _round_money(payable if payable >= 0 else Decimal("0"))
#     return cart

# def apply_payment_offer(cart: Dict[str, Any],
#                         payment_method: str,
#                         coupon_code: str | None = None) -> Dict[str, Any]:
#     """
#     Apply mock payment & coupon offers robustly.
#     Returns an updated cart with:
#       - offers_applied: List[{type, code, amount}]
#       - discounts, payable updated (Decimal->str coerced at the end if needed by ADK)
#     """
#     cart = _compute_totals(dict(cart))  # copy defensively
#     offers_applied: List[Dict[str, Any]] = list(cart.get("offers_applied", []))

#     currency = cart.get("currency", "INR")
#     payable = _to_money(cart.get("payable", 0))

#     # ---- Mock payment-method offers (examples) ----
#     pm = (payment_method or "").lower()
#     offer_amt = Decimal("0")
#     offer_type = None
#     offer_code = None

#     # Example mock rules
#     if pm in ("upi", "upi-gpay", "upi-phonepe"):
#         # 2% off up to ₹150
#         offer_type = "payment_method"
#         offer_code = "UPI2"
#         offer_amt = min(payable * Decimal("0.02"), Decimal("150"))
#     elif pm in ("credit", "credit-visa", "credit-mastercard"):
#         # 5% off up to ₹500, minimum cart ₹4,000
#         if payable >= Decimal("4000"):
#             offer_type = "payment_method"
#             offer_code = "CC5"
#             offer_amt = min(payable * Decimal("0.05"), Decimal("500"))
#     elif pm in ("debit", "debit-visa", "debit-mastercard"):
#         # Flat ₹100 off above ₹2,000
#         if payable >= Decimal("2000"):
#             offer_type = "payment_method"
#             offer_code = "DC100"
#             offer_amt = Decimal("100")

#     if offer_amt > 0:
#         offers_applied.append({
#             "type": offer_type,
#             "code": offer_code,
#             "amount": float(_round_money(offer_amt)),
#             "currency": currency
#         })
#         cart["discounts"] = _round_money(_to_money(cart["discounts"]) + offer_amt)
#         cart["payable"] = _round_money(_to_money(cart["subtotal"]) + _to_money(cart["taxes"]) + _to_money(cart["fees"]) - _to_money(cart["discounts"]))

#     # ---- Mock coupon rules (optional) ----
#     if coupon_code:
#         c = coupon_code.strip().upper()
#         coupon_amt = Decimal("0")
#         coupon_ok = False

#         if c == "WELCOME150":
#             # Flat ₹150 off above ₹1000
#             if cart["subtotal"] >= Decimal("1000"):
#                 coupon_amt = Decimal("150")
#                 coupon_ok = True
#         elif c == "FLAT10":
#             # 10% off up to ₹700; min subtotal ₹3000
#             if cart["subtotal"] >= Decimal("3000"):
#                 coupon_amt = min(cart["subtotal"] * Decimal("0.10"), Decimal("700"))
#                 coupon_ok = True

#         if coupon_ok and coupon_amt > 0:
#             offers_applied.append({
#                 "type": "coupon",
#                 "code": c,
#                 "amount": float(_round_money(coupon_amt)),
#                 "currency": currency
#             })
#             cart["discounts"] = _round_money(_to_money(cart["discounts"]) + coupon_amt)
#             cart["payable"] = _round_money(_to_money(cart["subtotal"]) + _to_money(cart["taxes"]) + _to_money(cart["fees"]) - _to_money(cart["discounts"]))
#         else:
#             # record invalid/ignored coupon (optional)
#             cart.setdefault("offers_rejected", []).append({"type": "coupon", "code": c, "reason": "not_applicable"})

#     cart["offers_applied"] = offers_applied

#     # If ADK needs json-serializable types:
#     for k in ("subtotal", "taxes", "fees", "discounts", "payable"):
#         if isinstance(cart.get(k), Decimal):
#             cart[k] = float(cart[k])

#     return cart

# ---- Tool: collect payment (mock) ----
def collect_payment(cart: Dict[str, Any], method_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    method_payload examples:
      UPI:   {"method":"upi", "upi_id":"faiz@upi"}
      Debit: {"method":"debit", "card_last4":"4321"}
      Credit:{"method":"credit", "card_last4":"9876"}
    Returns: {"payment_intent_id": "...", "amount": cart['payable'], "currency": cart['currency']}
    """
    method = method_payload.get("method")
    cart["payment_method"] = method
    intent = {
        "payment_intent_id": _id("PAY"),
        "amount": round(float(cart["payable"]), 2),
        "currency": cart.get("currency", "INR"),
        "method": method,
        "mask": _mask_upi(method_payload["upi_id"]) if method == "upi" else _mask_card(method_payload.get("card_last4","0000")),
        "status": "REQUIRES_PIN"
    }
    return intent

# ---- Tool: confirm pin (mock) ----
def confirm_pin(payment_intent_id: str, pin: str) -> Dict[str, Any]:
    """
    Accept any 4-6 digit PIN/OTP mock; succeed if numeric and length 4-6.
    """
    ok = pin.isdigit() and 4 <= len(pin) <= 6
    return {
        "payment_intent_id": payment_intent_id,
        "status": "SUCCEEDED" if ok else "FAILED",
        "message": "Payment authorized" if ok else "Invalid PIN/OTP"
    }

# ---- Tool: book items (mock EMT booking per mode) ----
def book_flight(item: Dict[str, Any]) -> Dict[str, Any]:
    time.sleep(0.2)
    return {**item, "pnr": _id("EMTFL")}

def book_train(item: Dict[str, Any]) -> Dict[str, Any]:
    time.sleep(0.2)
    return {**item, "pnr": _id("EMTTR")}

def book_bus(item: Dict[str, Any]) -> Dict[str, Any]:
    time.sleep(0.1)
    return {**item, "pnr": _id("EMTBS")}

def book_hotel(item: Dict[str, Any]) -> Dict[str, Any]:
    time.sleep(0.2)
    return {**item, "booking_id": _id("EMTHL")}

# ---- Tool: finalize voucher/receipt ----
def generate_booking_confirmation(cart: Dict[str, Any], payment: Dict[str, Any], items: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    return {
        "provider": "EaseMyTrip",
        "booking_reference": _id("EMTBK"),
        "status": "CONFIRMED",
        "payment_status": "PAID",
        "payment_method": payment.get("method"),
        "amount_charged": payment.get("amount"),
        "currency": payment.get("currency","INR"),
        "masked_account": payment.get("mask"),
        "items": items,
        "coupon_applied": cart.get("coupon_code"),
        "offer_applied": cart.get("payment_offer_applied"),
        "created_at": now
    }
