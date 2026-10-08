"""
Sample complaint dataset modeled after the CFPB Consumer Complaints Database.
Each entry has a complaint narrative and category/urgency labels.
In production, replace this with a full CFPB CSV download from:
https://www.consumerfinance.gov/data-research/consumer-complaints/
"""

COMPLAINTS = [
    # ── Card Issues ──────────────────────────────────────────────────────
    {"text": "I was charged twice on my credit card for the same purchase at the grocery store. The merchant says they only charged once but my statement shows two identical charges of $47.50.", "category": "card_issue", "urgency": "medium"},
    {"text": "My debit card was declined at the ATM even though I have sufficient balance. The machine ate my card and did not return it.", "category": "card_issue", "urgency": "high"},
    {"text": "I received a new credit card that I never applied for. Someone may have opened an account in my name using my personal information.", "category": "card_issue", "urgency": "critical"},
    {"text": "The annual fee on my credit card was increased without prior notice. I was charged $150 instead of the usual $95 fee.", "category": "card_issue", "urgency": "low"},
    {"text": "My card's EMI conversion option is not working on the app. Every time I try to convert a transaction to EMI it shows a generic error message.", "category": "card_issue", "urgency": "medium"},
    {"text": "I requested a credit card replacement three weeks ago and still have not received the new card. The old card has been blocked.", "category": "card_issue", "urgency": "high"},
    {"text": "International transactions on my card are being declined despite having enabled international usage from the app.", "category": "card_issue", "urgency": "medium"},
    {"text": "My credit card reward points were deducted without my authorization. Over 10,000 points disappeared from my account overnight.", "category": "card_issue", "urgency": "medium"},
    {"text": "The contactless payment feature on my new debit card is not working at any terminal. I have tried multiple merchants.", "category": "card_issue", "urgency": "low"},
    {"text": "I am being charged late payment fees even though I set up auto-pay and my bank account has sufficient funds.", "category": "card_issue", "urgency": "high"},
    {"text": "My virtual card number generated from the app does not work for any online purchases. It keeps getting declined.", "category": "card_issue", "urgency": "medium"},
    {"text": "Card was swiped at petrol pump but amount charged is different from what was shown at the terminal.", "category": "card_issue", "urgency": "medium"},

    # ── UPI Failures ─────────────────────────────────────────────────────
    {"text": "I sent money through UPI to my friend but the amount was debited from my account and not credited to the receiver. Transaction ID shows success on my end.", "category": "upi_failure", "urgency": "high"},
    {"text": "UPI payments are failing with error code U69 timeout for the past two days. I am unable to make any payments.", "category": "upi_failure", "urgency": "high"},
    {"text": "My UPI ID has been deregistered without my consent. When I try to re-register it says the ID is already taken by another account.", "category": "upi_failure", "urgency": "critical"},
    {"text": "I received a UPI collect request from an unknown number claiming to be from the bank. After accepting it, money was debited from my account.", "category": "upi_failure", "urgency": "critical"},
    {"text": "The UPI transaction limit has been reduced to Rs 5000 per transaction without any notification. I used to transact up to Rs 1 lakh.", "category": "upi_failure", "urgency": "medium"},
    {"text": "My UPI PIN is not being accepted even though I am entering the correct PIN. I have tried resetting it but the OTP never arrives.", "category": "upi_failure", "urgency": "high"},
    {"text": "Autopay mandate set up via UPI is failing every month. The subscription payment for my streaming service keeps bouncing.", "category": "upi_failure", "urgency": "low"},
    {"text": "Double debit happened for a single UPI transaction. Rs 2000 was debited twice but merchant received only one payment.", "category": "upi_failure", "urgency": "high"},
    {"text": "UPI lite balance is showing incorrect amount. I loaded Rs 2000 but only Rs 500 is reflecting.", "category": "upi_failure", "urgency": "medium"},
    {"text": "Unable to link my new bank account to UPI app. It says account not eligible for UPI services.", "category": "upi_failure", "urgency": "medium"},
    {"text": "Refund for a cancelled UPI transaction has not been received even after 10 business days.", "category": "upi_failure", "urgency": "high"},
    {"text": "QR code payment went through but the merchant's device shows payment failed and they are asking me to pay again.", "category": "upi_failure", "urgency": "high"},

    # ── Loan Issues ──────────────────────────────────────────────────────
    {"text": "My home loan interest rate was changed from fixed to floating without my consent. The new EMI amount is significantly higher than what I agreed to.", "category": "loan", "urgency": "high"},
    {"text": "I have fully repaid my personal loan but the bank has not released the NOC certificate. It has been over 30 days since the last payment.", "category": "loan", "urgency": "medium"},
    {"text": "The loan processing fee charged is higher than what was mentioned in the sanction letter. They charged 2% instead of the agreed 1%.", "category": "loan", "urgency": "medium"},
    {"text": "My education loan moratorium period was not honored. The bank started demanding EMI payments while I am still studying.", "category": "loan", "urgency": "high"},
    {"text": "Pre-closure charges for my car loan are excessively high. The bank is charging 5% of outstanding principal which was not in the agreement.", "category": "loan", "urgency": "medium"},
    {"text": "I was promised a personal loan at 10.5% but the actual rate applied is 14.5%. The bank says the lower rate was only indicative.", "category": "loan", "urgency": "high"},
    {"text": "My loan application has been pending for over 45 days with no communication from the bank regarding its status.", "category": "loan", "urgency": "medium"},
    {"text": "The bank is calling my emergency contacts and harassing them about my loan payment which is only 5 days overdue.", "category": "loan", "urgency": "critical"},
    {"text": "CIBIL score shows a default on a loan that I fully paid off two years ago. The bank has not updated the records.", "category": "loan", "urgency": "high"},
    {"text": "Loan insurance premium was added to my EMI without explicit consent. I never opted for loan protection insurance.", "category": "loan", "urgency": "medium"},
    {"text": "My business loan top-up request was rejected without reason even though all my existing EMIs are paid on time.", "category": "loan", "urgency": "low"},
    {"text": "The bank is refusing to provide the loan amortization schedule despite multiple requests over email and branch visits.", "category": "loan", "urgency": "low"},

    # ── Account Access ───────────────────────────────────────────────────
    {"text": "My net banking account has been locked after three failed login attempts. I am unable to reset the password because the registered mobile number is old.", "category": "account_access", "urgency": "high"},
    {"text": "I cannot access my savings account online. The app shows 'account dormant' even though I made a transaction last month.", "category": "account_access", "urgency": "medium"},
    {"text": "My KYC update was rejected and now my account is frozen. I cannot withdraw my own money or make any transactions.", "category": "account_access", "urgency": "critical"},
    {"text": "The mobile banking app keeps crashing after the latest update. I am unable to check my balance or make transfers.", "category": "account_access", "urgency": "medium"},
    {"text": "I changed my registered mobile number at the branch but the OTPs are still going to my old number. I cannot authenticate any transaction.", "category": "account_access", "urgency": "high"},
    {"text": "My joint account holder removed me from the account without my signature or consent.", "category": "account_access", "urgency": "critical"},
    {"text": "Password reset link sent to my email expired before I could use it. Now the system says I have exceeded maximum reset attempts.", "category": "account_access", "urgency": "medium"},
    {"text": "After updating Aadhaar details, my account shows someone else's name and address. This is extremely concerning.", "category": "account_access", "urgency": "critical"},
    {"text": "Mini statement at ATM shows transactions I never made. But the full statement online matches my records. Very confusing.", "category": "account_access", "urgency": "medium"},
    {"text": "My salary account was downgraded to a regular savings account and I lost all the premium features I was getting.", "category": "account_access", "urgency": "low"},
    {"text": "Unable to add beneficiary for fund transfer. The app throws an error every time I enter the IFSC code.", "category": "account_access", "urgency": "medium"},
    {"text": "My fixed deposit linked to the savings account is not visible in the app anymore even though it has not matured yet.", "category": "account_access", "urgency": "high"},

    # ── Fraud ────────────────────────────────────────────────────────────
    {"text": "Someone withdrew Rs 50,000 from my account using a cloned debit card at an ATM in a city I have never visited. I need immediate help.", "category": "fraud", "urgency": "critical"},
    {"text": "I received a call from someone claiming to be bank staff who asked for my OTP. After I shared it, Rs 25,000 was transferred out of my account.", "category": "fraud", "urgency": "critical"},
    {"text": "Multiple transactions of small amounts (Rs 99 each) are showing on my credit card statement. I did not make any of these purchases.", "category": "fraud", "urgency": "high"},
    {"text": "My account shows a NEFT transfer of Rs 1,00,000 to an account I do not recognize. I did not authorize this transaction at all.", "category": "fraud", "urgency": "critical"},
    {"text": "Someone opened a loan account using my PAN card and Aadhaar number. I am getting collection calls for a loan I never took.", "category": "fraud", "urgency": "critical"},
    {"text": "I found unauthorized UPI transactions on my account happening at 3 AM. My phone was with me and I was sleeping.", "category": "fraud", "urgency": "critical"},
    {"text": "A fraudulent SIM swap was done on my number and subsequently all my bank accounts were emptied.", "category": "fraud", "urgency": "critical"},
    {"text": "I received a phishing SMS with a link that looked exactly like my bank's website. I entered my credentials before realizing it was fake.", "category": "fraud", "urgency": "critical"},
    {"text": "My cheque was altered and cashed for a higher amount than what I wrote. The bank processed it without verifying.", "category": "fraud", "urgency": "high"},
    {"text": "Someone is using my credit card details for recurring subscription payments on a platform I have never used.", "category": "fraud", "urgency": "high"},
    {"text": "I noticed a new nominee added to my account that I did not authorize. This looks like an insider fraud.", "category": "fraud", "urgency": "critical"},
    {"text": "Suspicious login attempts on my net banking from multiple foreign IP addresses. The bank did not alert me about any of them.", "category": "fraud", "urgency": "high"},
]


def get_training_data():
    """Return texts, categories, and urgencies as separate lists."""
    texts = [c["text"] for c in COMPLAINTS]
    categories = [c["category"] for c in COMPLAINTS]
    urgencies = [c["urgency"] for c in COMPLAINTS]
    return texts, categories, urgencies
