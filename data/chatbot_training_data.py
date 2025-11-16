# chatbot_training_data.py

TRAINING_DATA = [
    # Budget & Price Questions (35)
    {"question": "phone under 2000", "intent": "budget_query", "category": "budget", "short_form": False},
    {"question": "cheapest phone", "intent": "budget_query", "category": "budget", "short_form": False},
    {"question": "best phone under rm1000?", "intent": "budget_query", "category": "budget", "short_form": False},
    {"question": "phones below 1500", "intent": "budget_query", "category": "budget", "short_form": False},
    {"question": "budget phone recommendations", "intent": "budget_query", "category": "budget", "short_form": False},
    {"question": "affordable phones", "intent": "budget_query", "category": "budget", "short_form": False},
    {"question": "phone under 3k", "intent": "budget_query", "category": "budget", "short_form": True},
    {"question": "what's the cheapest 5g phone", "intent": "budget_5g", "category": "budget", "short_form": False},
    {"question": "rm500 phone got or not", "intent": "budget_query", "category": "budget", "short_form": True},
    {"question": "below rm1000 any good phone?", "intent": "budget_query", "category": "budget", "short_form": True},
    {"question": "student budget phone", "intent": "budget_student", "category": "budget", "short_form": False},
    {"question": "cheap but good phone", "intent": "budget_value", "category": "budget", "short_form": False},
    {"question": "under 2k with good camera", "intent": "budget_camera", "category": "budget", "short_form": True},
    {"question": "low price high quality", "intent": "budget_value", "category": "budget", "short_form": False},
    {"question": "economy phone", "intent": "budget_query", "category": "budget", "short_form": False},
    {"question": "how much is iphone 15", "intent": "price_check", "category": "price", "short_form": False},
    {"question": "samsung s24 price", "intent": "price_check", "category": "price", "short_form": False},
    {"question": "xiaomi vs samsung price", "intent": "price_comparison", "category": "price", "short_form": False},
    {"question": "is pixel cheaper than iphone", "intent": "price_comparison", "category": "price", "short_form": False},
    {"question": "honor phone price range", "intent": "price_range", "category": "price", "short_form": False},
    {"question": "which brand cheaper", "intent": "price_comparison", "category": "price", "short_form": False},
    {"question": "apple vs android price", "intent": "price_comparison", "category": "price", "short_form": False},
    {"question": "flagship phone prices", "intent": "price_range", "category": "price", "short_form": False},
    {"question": "mid range phone cost", "intent": "price_range", "category": "price", "short_form": False},
    {"question": "budget vs premium phones", "intent": "price_comparison", "category": "price", "short_form": False},
    {"question": "best value for money", "intent": "value_query", "category": "value", "short_form": False},
    {"question": "worth it or not", "intent": "value_query", "category": "value", "short_form": True},
    {"question": "good deal phones", "intent": "value_query", "category": "value", "short_form": False},
    {"question": "bang for buck phone", "intent": "value_query", "category": "value", "short_form": False},
    {"question": "overpriced phones", "intent": "value_query", "category": "value", "short_form": False},
    {"question": "best phone for the price", "intent": "value_query", "category": "value", "short_form": False},
    {"question": "value flagship", "intent": "value_query", "category": "value", "short_form": False},
    {"question": "worth the money?", "intent": "value_query", "category": "value", "short_form": False},
    {"question": "good investment phone", "intent": "value_query", "category": "value", "short_form": False},
    {"question": "price vs performance", "intent": "value_query", "category": "value", "short_form": False},
    
    # Camera Questions (30)
    {"question": "good camera phone", "intent": "camera_general", "category": "camera", "short_form": False},
    {"question": "best camera under 2000", "intent": "camera_budget", "category": "camera", "short_form": False},
    {"question": "phone with triple camera", "intent": "camera_specs", "category": "camera", "short_form": False},
    {"question": "50mp camera phone", "intent": "camera_specs", "category": "camera", "short_form": True},
    {"question": "camera quality phone", "intent": "camera_general", "category": "camera", "short_form": False},
    {"question": "photography phone", "intent": "camera_general", "category": "camera", "short_form": False},
    {"question": "best for taking pics", "intent": "camera_general", "category": "camera", "short_form": False},
    {"question": "good selfie camera", "intent": "camera_selfie", "category": "camera", "short_form": False},
    {"question": "front camera quality", "intent": "camera_selfie", "category": "camera", "short_form": False},
    {"question": "which has better camera", "intent": "camera_comparison", "category": "camera", "short_form": False},
    {"question": "night mode camera", "intent": "camera_feature", "category": "camera", "short_form": False},
    {"question": "zoom camera phone", "intent": "camera_feature", "category": "camera", "short_form": False},
    {"question": "wide angle camera", "intent": "camera_feature", "category": "camera", "short_form": False},
    {"question": "portrait mode phone", "intent": "camera_feature", "category": "camera", "short_form": False},
    {"question": "video recording phone", "intent": "camera_video", "category": "camera", "short_form": False},
    {"question": "4k video phone", "intent": "camera_video", "category": "camera", "short_form": True},
    {"question": "slow motion camera", "intent": "camera_video", "category": "camera", "short_form": False},
    {"question": "good for instagram", "intent": "camera_social", "category": "camera", "short_form": False},
    {"question": "tiktok camera phone", "intent": "camera_social", "category": "camera", "short_form": False},
    {"question": "food photography phone", "intent": "camera_photography", "category": "camera", "short_form": False},
    {"question": "iphone vs samsung camera", "intent": "camera_comparison", "category": "camera", "short_form": False},
    {"question": "pixel camera better or not", "intent": "camera_comparison", "category": "camera", "short_form": True},
    {"question": "xiaomi camera good?", "intent": "camera_comparison", "category": "camera", "short_form": False},
    {"question": "honor vs oppo camera", "intent": "camera_comparison", "category": "camera", "short_form": False},
    {"question": "which brand best camera", "intent": "camera_comparison", "category": "camera", "short_form": False},
    {"question": "flagship camera comparison", "intent": "camera_comparison", "category": "camera", "short_form": False},
    {"question": "mid range best camera", "intent": "camera_budget", "category": "camera", "short_form": False},
    {"question": "budget camera phone", "intent": "camera_budget", "category": "camera", "short_form": False},
    {"question": "apple camera vs android", "intent": "camera_comparison", "category": "camera", "short_form": False},
    {"question": "camera phone ranking", "intent": "camera_comparison", "category": "camera", "short_form": False},
    
    # Gaming Questions (30)
    {"question": "gaming phone", "intent": "gaming_general", "category": "gaming", "short_form": False},
    {"question": "best for mobile legends", "intent": "gaming_specific", "category": "gaming", "short_form": False},
    {"question": "pubg phone", "intent": "gaming_specific", "category": "gaming", "short_form": True},
    {"question": "genshin impact phone", "intent": "gaming_specific", "category": "gaming", "short_form": False},
    {"question": "cod mobile phone", "intent": "gaming_specific", "category": "gaming", "short_form": True},
    {"question": "gaming phone under 2000", "intent": "gaming_budget", "category": "gaming", "short_form": False},
    {"question": "smooth gaming phone", "intent": "gaming_performance", "category": "gaming", "short_form": False},
    {"question": "no lag phone", "intent": "gaming_performance", "category": "gaming", "short_form": False},
    {"question": "high fps phone", "intent": "gaming_performance", "category": "gaming", "short_form": True},
    {"question": "game performance phone", "intent": "gaming_performance", "category": "gaming", "short_form": False},
    {"question": "snapdragon for gaming", "intent": "gaming_specs", "category": "gaming", "short_form": False},
    {"question": "gaming processor phone", "intent": "gaming_specs", "category": "gaming", "short_form": False},
    {"question": "high refresh rate phone", "intent": "gaming_specs", "category": "gaming", "short_form": False},
    {"question": "120hz phone", "intent": "gaming_specs", "category": "gaming", "short_form": True},
    {"question": "cooling system phone", "intent": "gaming_specs", "category": "gaming", "short_form": False},
    {"question": "gaming chipset", "intent": "gaming_specs", "category": "gaming", "short_form": False},
    {"question": "gpu performance", "intent": "gaming_specs", "category": "gaming", "short_form": True},
    {"question": "ram for gaming", "intent": "gaming_specs", "category": "gaming", "short_form": False},
    {"question": "gaming phone specs", "intent": "gaming_specs", "category": "gaming", "short_form": False},
    {"question": "fastest processor phone", "intent": "gaming_specs", "category": "gaming", "short_form": False},
    {"question": "budget gaming phone", "intent": "gaming_budget", "category": "gaming", "short_form": False},
    {"question": "cheap gaming phone", "intent": "gaming_budget", "category": "gaming", "short_form": False},
    {"question": "gaming phone under 1500", "intent": "gaming_budget", "category": "gaming", "short_form": False},
    {"question": "affordable gaming", "intent": "gaming_budget", "category": "gaming", "short_form": False},
    {"question": "student gaming phone", "intent": "gaming_budget", "category": "gaming", "short_form": False},
    {"question": "entry level gaming phone", "intent": "gaming_budget", "category": "gaming", "short_form": False},
    {"question": "mid range gaming", "intent": "gaming_budget", "category": "gaming", "short_form": False},
    {"question": "flagship gaming phone", "intent": "gaming_general", "category": "gaming", "short_form": False},
    {"question": "best gaming value", "intent": "gaming_value", "category": "gaming", "short_form": False},
    {"question": "gaming phone deals", "intent": "gaming_budget", "category": "gaming", "short_form": False},
    
    # Battery Questions (30)
    {"question": "long battery life", "intent": "battery_life", "category": "battery", "short_form": False},
    {"question": "best battery phone", "intent": "battery_life", "category": "battery", "short_form": False},
    {"question": "5000mah phone", "intent": "battery_capacity", "category": "battery", "short_form": True},
    {"question": "battery last whole day", "intent": "battery_life", "category": "battery", "short_form": False},
    {"question": "heavy usage battery", "intent": "battery_life", "category": "battery", "short_form": False},
    {"question": "battery life ranking", "intent": "battery_comparison", "category": "battery", "short_form": False},
    {"question": "longest battery", "intent": "battery_life", "category": "battery", "short_form": False},
    {"question": "battery phone under 2000", "intent": "battery_budget", "category": "battery", "short_form": False},
    {"question": "all day battery", "intent": "battery_life", "category": "battery", "short_form": False},
    {"question": "battery endurance phone", "intent": "battery_life", "category": "battery", "short_form": False},
    {"question": "fast charging phone", "intent": "charging_speed", "category": "battery", "short_form": False},
    {"question": "65w charging", "intent": "charging_speed", "category": "battery", "short_form": True},
    {"question": "quick charge phone", "intent": "charging_speed", "category": "battery", "short_form": False},
    {"question": "wireless charging phone", "intent": "charging_feature", "category": "battery", "short_form": False},
    {"question": "charging speed", "intent": "charging_speed", "category": "battery", "short_form": False},
    {"question": "fastest charging phone", "intent": "charging_speed", "category": "battery", "short_form": False},
    {"question": "30min full charge", "intent": "charging_speed", "category": "battery", "short_form": True},
    {"question": "super fast charge", "intent": "charging_speed", "category": "battery", "short_form": False},
    {"question": "charging time phone", "intent": "charging_speed", "category": "battery", "short_form": False},
    {"question": "wired vs wireless charging", "intent": "charging_comparison", "category": "battery", "short_form": False},
    {"question": "battery drain phone", "intent": "battery_issue", "category": "battery", "short_form": False},
    {"question": "battery replacement cost", "intent": "battery_service", "category": "battery", "short_form": False},
    {"question": "removable battery phone", "intent": "battery_feature", "category": "battery", "short_form": False},
    {"question": "battery health", "intent": "battery_info", "category": "battery", "short_form": False},
    {"question": "battery capacity", "intent": "battery_info", "category": "battery", "short_form": False},
    {"question": "battery vs performance", "intent": "battery_comparison", "category": "battery", "short_form": False},
    {"question": "battery degradation", "intent": "battery_info", "category": "battery", "short_form": False},
    {"question": "battery warranty", "intent": "battery_service", "category": "battery", "short_form": False},
    {"question": "power saving phone", "intent": "battery_feature", "category": "battery", "short_form": False},
    {"question": "battery optimization", "intent": "battery_feature", "category": "battery", "short_form": False},
    
    # Network & Connectivity (30)
    {"question": "5g phone", "intent": "network_5g", "category": "network", "short_form": True},
    {"question": "5g under 2000", "intent": "network_5g_budget", "category": "network", "short_form": True},
    {"question": "cheapest 5g", "intent": "network_5g_budget", "category": "network", "short_form": True},
    {"question": "5g vs 4g", "intent": "network_comparison", "category": "network", "short_form": True},
    {"question": "5g phones list", "intent": "network_5g", "category": "network", "short_form": True},
    {"question": "need 5g or not", "intent": "network_advice", "category": "network", "short_form": True},
    {"question": "5g worth it", "intent": "network_advice", "category": "network", "short_form": True},
    {"question": "5g coverage malaysia", "intent": "network_local", "category": "network", "short_form": True},
    {"question": "affordable 5g", "intent": "network_5g_budget", "category": "network", "short_form": True},
    {"question": "5g phone recommendations", "intent": "network_5g", "category": "network", "short_form": True},
    {"question": "dual sim phone", "intent": "network_feature", "category": "network", "short_form": False},
    {"question": "esim phone", "intent": "network_feature", "category": "network", "short_form": True},
    {"question": "dual 5g phone", "intent": "network_feature", "category": "network", "short_form": True},
    {"question": "network bands", "intent": "network_specs", "category": "network", "short_form": False},
    {"question": "malaysia network phone", "intent": "network_local", "category": "network", "short_form": False},
    {"question": "celcom compatible", "intent": "network_carrier", "category": "network", "short_form": False},
    {"question": "maxis phone", "intent": "network_carrier", "category": "network", "short_form": False},
    {"question": "digi phone", "intent": "network_carrier", "category": "network", "short_form": False},
    {"question": "umobile phone", "intent": "network_carrier", "category": "network", "short_form": False},
    {"question": "all network phone", "intent": "network_feature", "category": "network", "short_form": False},
    {"question": "wifi 6 phone", "intent": "connectivity_feature", "category": "network", "short_form": True},
    {"question": "bluetooth 5.3", "intent": "connectivity_feature", "category": "network", "short_form": True},
    {"question": "nfc phone", "intent": "connectivity_feature", "category": "network", "short_form": True},
    {"question": "wireless features", "intent": "connectivity_general", "category": "network", "short_form": False},
    {"question": "connectivity options", "intent": "connectivity_general", "category": "network", "short_form": False},
    {"question": "hotspot phone", "intent": "connectivity_feature", "category": "network", "short_form": False},
    {"question": "network speed", "intent": "connectivity_performance", "category": "network", "short_form": False},
    {"question": "signal strength phone", "intent": "connectivity_performance", "category": "network", "short_form": False},
    {"question": "wifi calling phone", "intent": "connectivity_feature", "category": "network", "short_form": False},
    {"question": "volte phone", "intent": "connectivity_feature", "category": "network", "short_form": True},
    
    # Continue with remaining categories...
    # (Storage, Display, Brand, User Category, etc.)
]

# Intent Categories
INTENT_CATEGORIES = {
    "budget": ["budget_query", "budget_5g", "budget_student", "budget_value", "budget_camera"],
    "price": ["price_check", "price_comparison", "price_range"],
    "value": ["value_query"],
    "camera": ["camera_general", "camera_budget", "camera_specs", "camera_selfie", "camera_comparison", 
               "camera_feature", "camera_video", "camera_social", "camera_photography"],
    "gaming": ["gaming_general", "gaming_specific", "gaming_budget", "gaming_performance", 
               "gaming_specs", "gaming_value"],
    "battery": ["battery_life", "battery_capacity", "battery_comparison", "battery_budget", 
                "charging_speed", "charging_feature", "charging_comparison", "battery_issue", 
                "battery_service", "battery_feature", "battery_info"],
    "network": ["network_5g", "network_5g_budget", "network_comparison", "network_advice", 
                "network_local", "network_feature", "network_specs", "network_carrier", 
                "connectivity_feature", "connectivity_general", "connectivity_performance"],
    # Add more as needed...
}

# Short Form Mappings
SHORT_FORM_MAPPINGS = {
    "u": "you",
    "ur": "your",
    "r": "are",
    "y": "why",
    "wht": "what",
    "hw": "how",
    "thx": "thanks",
    "ty": "thank you",
    "pls": "please",
    "plz": "please",
    "k": "ok",
    "yep": "yes",
    "nope": "no",
    "idk": "i don't know",
    "gt": "got",
    "shld": "should",
    "gd": "good",
    "cn": "can",
    "whr": "where",
    "wen": "when",
    "exp": "expensive",
    "wrth": "worth",
    "afrd": "afford",
    "2k": "2000",
    "3k": "3000",
    "5g": "five g",
    "4g": "four g",
    "50mp": "fifty megapixel",
    "120hz": "one hundred twenty hertz",
    "65w": "sixty five watt",
    "5000mah": "five thousand mah",
    "8gb": "eight gigabyte",
    "12gb": "twelve gigabyte",
    "256gb": "two hundred fifty six gigabyte",
    "128gb": "one hundred twenty eight gigabyte",
    "pubg": "pubg",
    "cod": "call of duty",
    "fps": "frames per second",
    "gpu": "graphics processing unit",
    "ram": "ram",
    "nfc": "nfc",
    "ip": "ip",
    "gps": "gps",
    "wifi": "wifi",
    "fm": "fm",
    "ppi": "pixels per inch",
    "amoled": "amoled",
    "lcd": "lcd",
    "oled": "oled",
    "rm": "ringgit malaysia",
}

# Response Templates
RESPONSE_TEMPLATES = {
    "budget_query": [
        "Here are some great phones under RM {budget}:",
        "I found {count} phones within your budget:",
        "Based on your budget of RM {budget}, I recommend:",
    ],
    "camera_general": [
        "For photography, I recommend these phones with excellent cameras:",
        "Here are phones with the best camera quality:",
        "These phones have top-rated cameras:",
    ],
    "gaming_general": [
        "For gaming, these phones offer great performance:",
        "Here are the best gaming phones:",
        "These phones can handle intensive games smoothly:",
    ],
    "battery_life": [
        "For long battery life, check out these phones:",
        "These phones have excellent battery endurance:",
        "Here are phones that last all day:",
    ],
    "network_5g": [
        "Here are 5G-capable phones:",
        "These phones support 5G networks:",
        "5G phones available in Malaysia:",
    ],
    # Add more templates...
}

# Helper Functions
def normalize_question(question):
    """Convert short forms to full forms"""
    words = question.lower().split()
    normalized = []
    for word in words:
        normalized.append(SHORT_FORM_MAPPINGS.get(word, word))
    return " ".join(normalized)

def get_questions_by_category(category):
    """Get all questions for a specific category"""
    return [item for item in TRAINING_DATA if item["category"] == category]

def get_questions_by_intent(intent):
    """Get all questions for a specific intent"""
    return [item for item in TRAINING_DATA if item["intent"] == intent]

def get_short_form_questions():
    """Get all questions with short forms"""
    return [item for item in TRAINING_DATA if item["short_form"]]

def export_to_csv(filename="chatbot_training.csv"):
    """Export training data to CSV"""
    import csv
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if TRAINING_DATA:
            writer = csv.DictWriter(f, fieldnames=TRAINING_DATA[0].keys())
            writer.writeheader()
            writer.writerows(TRAINING_DATA)
    print(f"Exported {len(TRAINING_DATA)} questions to {filename}")

# Usage Examples
if __name__ == "__main__":
    print(f"Total training questions: {len(TRAINING_DATA)}")
    print(f"\nQuestions by category:")
    categories = {}
    for item in TRAINING_DATA:
        cat = item["category"]
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    print(f"\nShort form questions: {len(get_short_form_questions())}")
    
    # Test normalization
    print("\nNormalization examples:")
    test_questions = [
        "u got cheap phone?",
        "wht phone shld i get",
        "hw much is iphone 15",
        "gt 5g under 2k?"
    ]
    for q in test_questions:
        print(f"  {q} → {normalize_question(q)}")
    
    # Export to CSV
    export_to_csv()
