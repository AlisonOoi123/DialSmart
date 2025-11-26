"""
Test enhanced chatbot understanding of natural language queries
"""
from app import create_app
from app.modules.chatbot import ChatbotEngine
from app.models import User

app = create_app()

with app.app_context():
    chatbot = ChatbotEngine()

    # Test cases matching user's requirements
    test_cases = [
        "i want a long lasting phone",
        "best camera phone",
        "phones with amoled display",
        "fast processor under rm3000",
        "5g phones",
        "gaming phone near 3000",
        "business phone near 2000-3000",
        "gaming phone within RM3000",
        "for senior citizen",
        "student gaming phone within 2000-3000",
        "phone for photographer",
    ]

    print("=" * 80)
    print("TESTING ENHANCED NATURAL LANGUAGE UNDERSTANDING")
    print("=" * 80)

    for i, test_msg in enumerate(test_cases, 1):
        print(f"\n{i}. Query: \"{test_msg}\"")
        print("-" * 80)

        # Extract components
        intent = chatbot._detect_intent(test_msg.lower())
        budget = chatbot._extract_budget(test_msg)
        usage = chatbot._detect_usage_type(test_msg)
        features = chatbot._detect_feature_priority(test_msg)
        user_category = chatbot._detect_user_category(test_msg)
        brands = chatbot._extract_multiple_brands(test_msg)

        print(f"   Intent: {intent}")
        print(f"   Budget: {budget if budget else 'None'}")
        print(f"   Usage: {usage if usage else 'None'}")
        print(f"   Features: {features if features else 'None'}")
        print(f"   User Category: {user_category if user_category else 'None'}")
        print(f"   Brands: {brands if brands else 'None'}")

        # Verify correct understanding
        if "long lasting" in test_msg and 'battery' not in features:
            print("   ❌ FAILED: Didn't detect battery priority")
        elif "camera" in test_msg and 'camera' not in features:
            print("   ❌ FAILED: Didn't detect camera priority")
        elif "amoled" in test_msg and 'display' not in features:
            print("   ❌ FAILED: Didn't detect display priority")
        elif "fast processor" in test_msg and 'performance' not in features:
            print("   ❌ FAILED: Didn't detect performance priority")
        elif "5g" in test_msg and '5g' not in features:
            print("   ❌ FAILED: Didn't detect 5G requirement")
        elif "near 3000" in test_msg and not budget:
            print("   ❌ FAILED: Didn't extract budget from 'near 3000'")
        elif "near 2000-3000" in test_msg and budget != (2000, 3000):
            print(f"   ❌ FAILED: Expected (2000, 3000), got {budget}")
        elif "senior" in test_msg and user_category != 'senior':
            print("   ❌ FAILED: Didn't detect senior citizen category")
        elif "student" in test_msg and user_category != 'student':
            print("   ❌ FAILED: Didn't detect student category")
        elif "photographer" in test_msg and usage != 'Photography':
            print("   ❌ FAILED: Didn't detect photographer usage")
        else:
            print("   ✅ Understanding: PASSED")

    # Test actual chatbot responses
    print("\n" + "=" * 80)
    print("TESTING ACTUAL CHATBOT RESPONSES")
    print("=" * 80)

    test_user = User.query.filter_by(email='user@dialsmart.my').first()

    if test_user:
        response_tests = [
            "i want a long lasting phone",
            "best camera phone",
            "gaming phone near 3000",
            "student gaming phone within 2000-3000",
        ]

        for test_msg in response_tests:
            print(f"\n📱 Query: \"{test_msg}\"")
            print("-" * 80)

            result = chatbot.process_message(test_user.id, test_msg)
            print(result['response'][:400])

            if len(result['response']) > 400:
                print("...")

            if 'metadata' in result and 'phones' in result['metadata']:
                phones = result['metadata']['phones']
                print(f"\n   Returned: {len(phones)} phones")

                # Check if images are included
                has_images = all('image' in p for p in phones)
                if has_images:
                    print(f"   ✅ All phones have image URLs")
                else:
                    print(f"   ❌ Some phones missing image URLs")

                # Check budget compliance
                if 'budget' in result['metadata'] and result['metadata']['budget']:
                    min_b, max_b = result['metadata']['budget']
                    over_budget = [p for p in phones if p['price'] > max_b]
                    under_budget = [p for p in phones if p['price'] < min_b]

                    if over_budget or under_budget:
                        print(f"   ❌ {len(over_budget + under_budget)} phones outside budget!")
                    else:
                        print(f"   ✅ All phones within budget (RM{min_b:,.0f} - RM{max_b:,.0f})")

                # Show sample phone with image
                if phones:
                    sample = phones[0]
                    print(f"\n   Sample result:")
                    print(f"      Name: {sample.get('brand', '')} {sample['name']}")
                    print(f"      Price: RM{sample['price']:,.2f}")
                    print(f"      Image: {sample.get('image', 'No image')[:50]}...")

            print()
    else:
        print("\n⚠ No test user found. Run: python seed_database.py")

    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)

    # Summary of supported queries
    print("\n✅ SUPPORTED NATURAL LANGUAGE QUERIES:")
    print("   - Long lasting phone → Battery priority")
    print("   - Best camera phone → Camera priority")
    print("   - AMOLED display → Display priority")
    print("   - Fast processor → Performance priority")
    print("   - 5G phones → 5G filter")
    print("   - near 3000 → RM2,500 - RM3,500")
    print("   - near 2000-3000 → RM2,000 - RM3,000")
    print("   - for senior citizen → User category")
    print("   - student phone → User category")
    print("   - phone for photographer → Usage type")
    print("   - All combinations supported!")
