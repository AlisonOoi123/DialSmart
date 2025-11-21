# Comprehensive Fixes for Chatbot Context Issues

## Issue 1: "i not love oppo, i love vivo within 2000" shows Xiaomi + Vivo

**Root Cause**: Fresh query detection doesn't trigger for budget queries with brand preferences.

**Fix**: Update `_is_fresh_query()` method:

```python
def _is_fresh_query(self, message):
    """
    Detect if message represents a fresh query (should clear context)
    vs a refinement query (should preserve context)
    """
    message_lower = message.lower()

    # Reset patterns - phrases that indicate starting fresh
    reset_patterns = [
        r'recommend.*phone for me',
        r'recommend.*a phone',
        r'find.*phone for me',
        r'show.*phone for me',
        r'suggest.*phone',
    ]

    for pattern in reset_patterns:
        if re.search(pattern, message_lower):
            return True

    # Check for negative + positive brand combo (strong indicator of fresh query)
    if re.search(r'(not|don\'t|dont)\s+(love|like|want|prefer)', message_lower):
        # Has negative preference, check if also has positive
        if re.search(r'(i love|i want|i like|i prefer)', message_lower):
            return True  # "i not love X, i love Y" pattern

    # NEW: Check for budget with new brand preferences (e.g., "vivo within 2000")
    # If message has BOTH budget AND brand, it's likely a fresh search
    has_budget = self._extract_budget(message) is not None
    wanted, unwanted = self._extract_brand_preferences(message)
    has_brand_pref = len(wanted) > 0 or len(unwanted) > 0

    if has_budget and has_brand_pref:
        # This is a fresh query like "vivo within 2000" or "samsung under 3000"
        return True

    return False
```

## Issue 2: "i love samsung and xiaomi, gaming phone within 3000" shows Samsung + Vivo

**Root Cause**: The `recommendation` handler with usage type is not properly clearing old brands and using current brands.

**Fix**: In `elif intent == 'recommendation' or intent == 'specification':` section, when handling brands + usage:

```python
# PRIORITY 2: Brands mentioned - always prioritize brand filtering
if brands:
    phones = []

    # Brands + Usage (e.g., "apple and samsung gaming phone")
    if usage:
        # IMPORTANT: Use ONLY the brands from current message + session wanted brands
        # But if current message has explicit brands, prioritize those

        # Get current message brands
        current_wanted, current_unwanted = self._extract_brand_preferences(message)

        # If current message explicitly mentions brands, use ONLY those
        if current_wanted:
            brands_to_use = current_wanted
        else:
            # Otherwise use session brands
            brands_to_use = brands

        phones = self.ai_engine.get_phones_by_usage(usage, budget, brands_to_use, top_n=5)

        if phones:
            budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
            brands_list = ", ".join(brands_to_use[:-1]) + f" and {brands_to_use[-1]}" if len(brands_to_use) > 1 else brands_to_use[0]
            response = f"Great choice! Here are the best phones for {usage} from {brands_list}{budget_text}:\n\n"

            # ... rest of code
```

## Issue 3: "long lasting phone" then "vivo" should show Vivo with good battery

**Root Cause**: `brand_query` handler doesn't check session features.

**Fix**: Update `elif intent == 'brand_query':` section:

```python
elif intent == 'brand_query':
    # Extract all mentioned brands
    wanted_brands, unwanted_brands = self._extract_brands_with_preferences(message)
    brand_names = wanted_brands  # Use wanted brands

    # GET SESSION FEATURES AND USAGE
    session_features = context.get('last_features', [])
    session_usage = context.get('last_usage')

    if brand_names:
        # Check if budget is mentioned
        budget = self._extract_budget(message)
        if not budget and 'last_budget' in context:
            budget = context['last_budget']
        usage = self._detect_usage_type(message)

        # If no usage in current message, check session
        if not usage:
            usage = session_usage

        # PRIORITY: If we have usage (current or session), use usage-based filtering
        if usage:
            all_phones_items = self.ai_engine.get_phones_by_usage(usage, budget, brand_names, top_n=10)

            # Extract phones from items
            all_phones = []
            for item in all_phones_items:
                phone = item['phone']
                brand_name = phone.brand.name
                all_phones.append((phone, brand_name))

        # PRIORITY: If we have features (like 'battery'), use feature-based filtering
        elif session_features:
            all_phones_items = self.ai_engine.get_phones_by_features(
                features=session_features,
                budget_range=budget,
                usage_type=None,
                brand_names=brand_names,
                user_category=None,
                top_n=10
            )

            # Extract phones from items
            all_phones = []
            for item in all_phones_items:
                phone = item['phone']
                brand_name = phone.brand.name
                all_phones.append((phone, brand_name))

        # Otherwise, use regular brand query
        else:
            all_phones = []
            found_brands = []

            for brand_name in brand_names:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    query = Phone.query.filter_by(brand_id=brand.id, is_active=True)

                    # Apply budget filter if specified
                    if budget:
                        min_b, max_b = budget
                        query = query.filter(Phone.price >= min_b, Phone.price <= max_b)

                    phones = query.limit(5).all()

                    if phones:
                        found_brands.append(brand.name)
                        all_phones.extend([(p, brand.name) for p in phones])

        if all_phones:
            # Build response
            if len(brand_names) == 1:
                budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""

                # Add feature context to response
                feature_text = ""
                if session_features:
                    feature_names = {
                        'battery': 'long battery life',
                        'camera': 'excellent camera',
                        'display': 'great display',
                        'performance': 'powerful performance',
                        '5g': '5G support'
                    }
                    feature_desc = ', '.join([feature_names.get(f, f) for f in session_features])
                    feature_text = f" with {feature_desc}"

                usage_text = f" for {usage}" if usage else ""
                response = f"Here are {brand_names[0]} phones{budget_text}{feature_text}{usage_text}:\n\n"
            else:
                # ... multi-brand response
```

## Issue 4: "oppo" then "above 2000" shows multiple brands

**Root Cause**: When user says just "oppo", it should CLEAR other brands. Then "above 2000" should filter ONLY Oppo.

**Fix**: In `process_message()`, enhance brand-only detection:

```python
# Detect if message is ONLY a brand name (e.g., just "oppo" or "samsung xiaomi")
# If so, REPLACE previous brands instead of adding to them
message_words = message.lower().strip().split()
all_brand_keywords = ['apple', 'iphone', 'samsung', 'galaxy', 'xiaomi', 'vivo', 'oppo',
                       'huawei', 'honor', 'realme', 'redmi', 'poco', 'google', 'pixel',
                       'nokia', 'lenovo', 'asus']
is_brand_only = len(message_words) <= 3 and all(word in all_brand_keywords for word in message_words)

# Update session context with brand preferences
if wanted:
    if is_brand_only:
        # REPLACE: Clear previous brands and set new ones
        self.session_context[context_key]['wanted_brands'] = wanted.copy()
        # ALSO CLEAR FEATURES AND USAGE when brand-only (new search context)
        self.session_context[context_key]['last_features'] = []
        self.session_context[context_key]['last_usage'] = None
```

## Issue 5: "rm2000 for gaming" then "oppo and xiaomi" loses gaming

**Root Cause**: Usage not being retrieved from session in brand_query handler.

**Fix**: Already covered in Issue 3 fix above - the brand_query handler now checks `session_usage`.

## Issue 6: "iphone 17 pro and xiaomi 17 pro" shows all phones

**Root Cause**: Model extraction skip logic treats this as brand query.

**Fix**: Update model extraction skip logic in `_generate_response()`:

```python
# Check if multiple brands AND model numbers are mentioned
brands_mentioned = self._extract_multiple_brands(message)
has_model_numbers = bool(re.search(r'\d+\s*(?:pro|max|ultra|plus|lite|mini|se)', message_lower))

if brands_mentioned and len(brands_mentioned) >= 1 and has_model_numbers:
    # This is likely a specific model query like "iphone 17 pro and xiaomi 17"
    # Don't skip phone model extraction
    skip_phone_model = False
elif brands_mentioned and len(brands_mentioned) > 1 and ' and ' in message_lower and 'phone' in message_lower:
    # This is a brand comparison like "apple and samsung phone"
    skip_phone_model = True
```

## Summary of Changes Needed:

1. **`_is_fresh_query()`** - Add budget + brand pattern detection
2. **Recommendation handler (brands + usage)** - Prioritize current message brands
3. **brand_query handler** - Check session features and usage
4. **brand-only detection** - Clear features/usage when brand-only
5. **Model extraction skip logic** - Better handling of "iphone 17 pro and xiaomi 17"

Apply these fixes to your production code to resolve all the context management issues.
