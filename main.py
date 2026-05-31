#main.py
from src.classifier import predict_disaster, predict_help
from src.verifier import verify_event
from src.rule_engine import rule_engine
from src.notifier import notify_authority
from src.tweet_fetcher import get_latest_post


# -----------------------------
# STEP 1 — Choose input method
# -----------------------------
print("\n========== Disaster Detection System ==========\n")
print("Choose input method:")
print("1️⃣  Enter post manually")
print("2️⃣  Fetch latest tweet (Web Scraping)")

choice = input("\nEnter option (1 or 2): ").strip()


# -----------------------------
# STEP 2 — Get text
# -----------------------------
if choice == "1":
    text = input("\nEnter social media post:\n")

elif choice == "2":
    print("\nFetching latest disaster tweet...\n")
    text = get_latest_post("Top_Disaster")
    #PTI_News
    if not text:
        print("❌ No tweet fetched.")
        exit()

else:
    print("❌ Invalid option selected.")
    exit()


# -----------------------------
# STEP 3 — Run Pipeline
# -----------------------------
print("\nRunning pipeline...\n")

disaster_prob = predict_disaster(text)
help_prob = predict_help(text)
verification = verify_event(text)
result = rule_engine(disaster_prob, help_prob, verification)


# -----------------------------
# STEP 4 — Show Results
# -----------------------------
print("Post:", text)
print("Disaster Probability:", disaster_prob)
print("Help Probability:", help_prob)
print("Verification:", verification)
print("Final Decision:", result)


# -----------------------------
# STEP 5 — Notify Authorities
# -----------------------------
if result["decision"] == "REAL":
    notify_authority(text)
else:
    print("\n⚠️ Post not considered REAL. No alert sent.")