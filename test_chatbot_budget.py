"""
Test chatbot budget extraction
"""
from app import create_app
from app.modules.chatbot import ChatbotEngine

app = create_app()

with app.app_context():
    chatbot = ChatbotEngine()

    # Test cases for budget extraction
    test_cases = [
        "a gaming phone within 3000",
        "gaming phone under 2000",
        "phone below 1500",
        "phone max 2500",
        "show me phones within RM3000",
        "I want a phone between 1000 and 2000",
        "find phone under RM2000",
        "gaming phone around 3000",
    ]

    print("=" * 70)
    print("Testing Chatbot Budget Extraction")
    print("=" * 70)

    for test in test_cases:
        budget = chatbot._extract_budget(test)
        usage = chatbot._detect_usage_type(test)

        print(f"\nInput: \"{test}\"")
        print(f"  Budget extracted: {budget}")
        print(f"  Usage type: {usage}")

        if budget:
            min_b, max_b = budget
            print(f"  ✓ Will filter: RM{min_b:,.0f} - RM{max_b:,.0f}")
        else:
            print(f"  ✗ NO BUDGET FILTER (bug!)")

    print("\n" + "=" * 70)
    print("Testing actual recommendation with 'within 3000'")
    print("=" * 70)

    # Create a test user (use existing user or create temp)
    from app.models import User
    test_user = User.query.filter_by(email='user@dialsmart.my').first()

    if test_user:
        result = chatbot.process_message(
            user_id=test_user.id,
            message="a gaming phone within 3000"
        )

        print(f"\nChatbot Response:")
        print(result['response'])

        if 'metadata' in result and 'phones' in result['metadata']:
            phones = result['metadata']['phones']
            print(f"\n📊 Results: {len(phones)} phones")
            print(f"Budget filter applied: {'budget' in result['metadata']}")

            over_budget = [p for p in phones if p['price'] > 3000]
            if over_budget:
                print(f"\n❌ BUG: {len(over_budget)} phones OVER budget:")
                for p in over_budget:
                    print(f"   - {p['name']}: RM{p['price']:,.2f}")
            else:
                print(f"\n✅ SUCCESS: All phones within budget!")

                # Show price range
                if phones:
                    prices = [p['price'] for p in phones]
                    print(f"   Price range: RM{min(prices):,.2f} - RM{max(prices):,.2f}")
    else:
        print("\n⚠ No test user found. Create user first:")
        print("   python seed_database.py")

    print("=" * 70)
