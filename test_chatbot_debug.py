"""
Debug chatbot intent detection
"""
from app import create_app
from app.modules.chatbot import ChatbotEngine
from app.models import User, Phone, PhoneSpecification

app = create_app()

with app.app_context():
    chatbot = ChatbotEngine()

    message = "a gaming phone within 3000"

    # Test intent detection
    intent = chatbot._detect_intent(message.lower())
    print(f"Message: '{message}'")
    print(f"Detected intent: {intent}")
    print()

    # Test budget extraction
    budget = chatbot._extract_budget(message)
    print(f"Budget extracted: {budget}")

    # Test usage detection
    usage = chatbot._detect_usage_type(message)
    print(f"Usage type: {usage}")
    print()

    # Check database
    total_phones = Phone.query.count()
    print(f"Total phones in database: {total_phones}")

    if total_phones == 0:
        print("❌ NO PHONES IN DATABASE! Import data first:")
        print("   python import_phones_from_csv.py")
    else:
        # Test gaming phone query
        gaming_phones = []
        all_phones = Phone.query.filter_by(is_active=True).all()

        for phone in all_phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if specs:
                # Calculate gaming score
                ram_values = [int(r.replace('GB', '').strip()) for r in (specs.ram_options or '').split(',') if 'GB' in r]
                if ram_values:
                    score = max(ram_values) * 10
                    score += (specs.refresh_rate or 60) / 10
                    score += specs.battery_capacity / 100 if specs.battery_capacity else 0

                    # Filter by budget
                    if budget:
                        min_b, max_b = budget
                        if min_b <= phone.price <= max_b:
                            gaming_phones.append((phone, specs, score))
                    else:
                        gaming_phones.append((phone, specs, score))

        # Sort by score
        gaming_phones.sort(key=lambda x: x[2], reverse=True)

        print(f"\nGaming phones found (within budget): {len(gaming_phones)}")

        if gaming_phones:
            print("\nTop 5 gaming phones:")
            for i, (phone, specs, score) in enumerate(gaming_phones[:5], 1):
                print(f"{i}. {phone.brand.name} {phone.model_name}")
                print(f"   Price: RM{phone.price:,.2f}")
                print(f"   RAM: {specs.ram_options}")
                print(f"   Gaming Score: {score:.0f}")
                print()

    # Now test the actual chatbot
    print("=" * 70)
    print("Testing chatbot.process_message()")
    print("=" * 70)

    test_user = User.query.filter_by(email='user@dialsmart.my').first()
    if test_user:
        result = chatbot.process_message(
            user_id=test_user.id,
            message=message
        )

        print(f"Response type: {result.get('type')}")
        print(f"Response:")
        print(result['response'])
        print()

        if 'metadata' in result:
            print(f"Metadata: {result['metadata'].keys()}")
            if 'phones' in result['metadata']:
                phones = result['metadata']['phones']
                print(f"Phones returned: {len(phones)}")

                over_budget = [p for p in phones if p['price'] > 3000]
                if over_budget:
                    print(f"❌ {len(over_budget)} phones over budget!")
                    for p in over_budget:
                        print(f"   {p['name']}: RM{p['price']:,.2f}")
                else:
                    print("✅ All phones within budget")
    else:
        print("No test user")
