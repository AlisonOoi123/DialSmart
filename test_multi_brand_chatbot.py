"""
Test chatbot's ability to understand multiple brands and complex requests
"""
from app import create_app
from app.modules.chatbot import ChatbotEngine
from app.models import User

app = create_app()

with app.app_context():
    chatbot = ChatbotEngine()

    # Test cases for multi-brand understanding
    test_cases = [
        # Single brand queries
        "show me Samsung phones",
        "Apple phones under 3000",
        "gaming phones from Xiaomi",

        # Multiple brand queries
        "show me Samsung and Apple phones",
        "compare Samsung, Xiaomi and Realme",
        "phones from Samsung or Apple",

        # Multiple brands with budget
        "Samsung and Xiaomi phones within 2000",
        "Apple or Samsung under 3000",

        # Multiple brands with usage
        "gaming phones from Samsung and Xiaomi within 3000",
        "photography phones from Apple or Samsung",

        # Complex queries
        "show me gaming phones from Samsung, Xiaomi, or Realme within 2500",
    ]

    print("=" * 80)
    print("TESTING MULTI-BRAND CHATBOT UNDERSTANDING")
    print("=" * 80)

    for i, test_msg in enumerate(test_cases, 1):
        print(f"\n{i}. Input: \"{test_msg}\"")
        print("-" * 80)

        # Extract components
        brands = chatbot._extract_multiple_brands(test_msg)
        budget = chatbot._extract_budget(test_msg)
        usage = chatbot._detect_usage_type(test_msg)
        intent = chatbot._detect_intent(test_msg.lower())

        print(f"   Intent: {intent}")
        print(f"   Brands: {brands if brands else 'None'}")
        print(f"   Budget: {budget if budget else 'None'}")
        print(f"   Usage: {usage if usage else 'None'}")

        # Check extraction success
        if "samsung" in test_msg.lower() and "Samsung" not in brands:
            print("   ❌ FAILED: Didn't detect Samsung")
        elif "apple" in test_msg.lower() and "Apple" not in brands:
            print("   ❌ FAILED: Didn't detect Apple")
        elif "xiaomi" in test_msg.lower() and "Xiaomi" not in brands:
            print("   ❌ FAILED: Didn't detect Xiaomi")
        else:
            print("   ✅ Brand extraction: PASSED")

    # Test actual chatbot responses
    print("\n" + "=" * 80)
    print("TESTING ACTUAL CHATBOT RESPONSES")
    print("=" * 80)

    test_user = User.query.filter_by(email='user@dialsmart.my').first()

    if test_user:
        response_tests = [
            "show me Samsung and Apple phones",
            "gaming phones from Samsung and Xiaomi within 3000",
            "Apple or Samsung under 2000",
        ]

        for test_msg in response_tests:
            print(f"\n📱 Query: \"{test_msg}\"")
            print("-" * 80)

            result = chatbot.process_message(test_user.id, test_msg)
            print(result['response'][:300])

            if 'metadata' in result and 'phones' in result['metadata']:
                phones = result['metadata']['phones']
                brands_in_results = set()
                for p in phones:
                    # Extract brand from model name or use metadata
                    if 'brand' in p:
                        brands_in_results.add(p['brand'])

                print(f"\n   Returned {len(phones)} phones")
                if brands_in_results:
                    print(f"   Brands in results: {', '.join(brands_in_results)}")

                # Check budget compliance
                if 'budget' in result['metadata'] and result['metadata']['budget']:
                    min_b, max_b = result['metadata']['budget']
                    over_budget = [p for p in phones if p['price'] > max_b]
                    if over_budget:
                        print(f"   ❌ {len(over_budget)} phones over budget!")
                    else:
                        print(f"   ✅ All phones within budget (RM{max_b:,.0f})")

            print()
    else:
        print("\n⚠ No test user found. Run: python seed_database.py")

    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)
