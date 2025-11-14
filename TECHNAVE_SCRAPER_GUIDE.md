# TechNave Scraper & Enhanced AI Guide

Complete guide for scraping TechNave Malaysia and using the enhanced AI recommendation system.

---

## 🌐 TechNave Web Scraper

### Overview

The TechNave scraper collects comprehensive phone data with **MYR pricing** directly from TechNave Malaysia, the leading tech review site in Malaysia.

**Website**: https://www.technave.com/

**Data Collected:**
- ✅ Phone model names
- ✅ MYR prices (Malaysian Ringgit)
- ✅ Complete specifications
- ✅ Screen details (size, type, resolution)
- ✅ Processor information
- ✅ RAM and storage options
- ✅ Camera specifications
- ✅ Battery capacity
- ✅ 5G support
- ✅ Operating system

---

## 📦 Setup

### 1. Install Web Scraping Dependencies

```powershell
pip install --upgrade -r requirements.txt
```

This will install:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML/HTML parser

### 2. Verify Installation

```powershell
pip list | findstr "requests beautifulsoup4 lxml"
```

You should see:
```
beautifulsoup4    4.12.3
lxml              5.1.0
requests          2.31.0
```

---

## 🚀 Using the TechNave Scraper

### Basic Usage

Scrape 30 phones from TechNave:
```powershell
python scrape_technave.py
```

### Scrape More Phones

Scrape 50 phones:
```powershell
python scrape_technave.py 50
```

Scrape 100 phones:
```powershell
python scrape_technave.py 100
```

### What Happens During Scraping:

```
============================================================
TechNave Phone Scraper for DialSmart
============================================================

[INFO] Scraping phone list from TechNave...
[INFO] Found 50 phone review URLs

[INFO] Scraping 30 phones...

[1/30] Processing...
  [•] Scraping: https://www.technave.com/devices/...
  [+] Created brand: Samsung
  [✓] Added: Samsung Galaxy S24 Ultra - RM 5,999

[2/30] Processing...
  [•] Scraping: https://www.technave.com/devices/...
  [✓] Added: iPhone 15 Pro Max - RM 6,299

...

============================================================
SCRAPING COMPLETE
============================================================
  ✓ Successfully added: 28 phones
  ✗ Failed/Skipped: 2 phones
============================================================
```

---

## 🎯 Enhanced AI Recommendation Engine

### Key Features

The enhanced AI engine provides **smarter recommendations** by considering:

1. **User Demographics**
   - Age range (18-25, 26-35, 36-45, 46-55, 56+)
   - Occupation (Student, Working Professional, Senior Citizen, Freelancer, Gamer)

2. **Budget Intelligence**
   - Age-appropriate pricing
   - Occupation-based budget comfort zones
   - Value-for-money scoring

3. **Usage Patterns**
   - Gaming requirements (high refresh rate, powerful processor)
   - Photography needs (camera quality, megapixels)
   - Business use (battery, dual SIM, reliability)
   - Entertainment (screen size, battery)

4. **Feature Matching**
   - 5G connectivity
   - Wireless charging
   - Water resistance
   - Fast charging
   - Large display

### Scoring Algorithm

The enhanced AI uses a **weighted scoring system**:

- **Budget Fit**: 25%
- **Demographic Fit**: 20%
- **Specs Match**: 30%
- **Usage Alignment**: 15%
- **Feature Match**: 10%

**Total: 100%**

### Age-Based Profiles

#### 18-25 (Students / Young Adults)
- **Priorities**: Performance, Gaming, Social Media, Camera
- **Budget**: Up to RM 2,500
- **Features**: 5G, High Refresh Rate, Fast Charging
- **Examples**: Realme GT, Xiaomi Redmi Note series

#### 26-35 (Young Professionals)
- **Priorities**: Camera, Performance, Battery, Design
- **Budget**: Up to RM 4,000
- **Features**: 5G, Wireless Charging, Water Resistance
- **Examples**: Samsung Galaxy S series, iPhone 14/15

#### 36-45 (Professionals)
- **Priorities**: Battery, Camera, Reliability, Business Features
- **Budget**: Up to RM 5,000
- **Features**: Dual SIM, Expandable Storage, 5G
- **Examples**: iPhone 15 Pro, Samsung Galaxy S24 Ultra

#### 46-55 (Senior Professionals)
- **Priorities**: Battery, Ease of Use, Camera, Display
- **Budget**: Up to RM 3,000
- **Features**: Large Screen, Good Battery, Simple Interface
- **Examples**: Samsung Galaxy A series, Oppo Reno

#### 56+ (Senior Citizens)
- **Priorities**: Battery, Ease of Use, Display, Camera
- **Budget**: Up to RM 2,000
- **Features**: Large Display, Long Battery, Loud Speaker
- **Examples**: Samsung Galaxy A15, Oppo A79

### Occupation-Based Profiles

#### Student
- **Max Budget**: RM 2,000
- **Usage**: Social Media, Gaming, Entertainment
- **Recommended**: Redmi Note, Realme, Samsung A-series

#### Working Professional
- **Max Budget**: RM 4,500
- **Usage**: Business, Communication, Photography
- **Recommended**: iPhone, Samsung S/A series, Oppo Reno

#### Senior Citizen
- **Max Budget**: RM 2,500
- **Usage**: Communication, Entertainment
- **Recommended**: Easy-to-use phones with large displays

#### Freelancer
- **Max Budget**: RM 3,500
- **Usage**: Photography, Work, Social Media
- **Recommended**: Phones with excellent cameras

#### Gamer
- **Max Budget**: RM 3,000
- **Usage**: Gaming, Entertainment, Performance
- **Recommended**: High refresh rate, powerful processors

---

## 💻 Using Enhanced AI in Your Code

### Method 1: Direct Integration

```python
from app.modules.enhanced_ai_engine import get_ai_recommendations

# Get smart recommendations for a user
recommendations = get_ai_recommendations(user_id=1, top_n=5)

for rec in recommendations:
    print(f"{rec['phone'].model_name} - {rec['match_score']}%")
    print(f"Reason: {rec['reasoning']}")
```

### Method 2: In Routes

Update `app/routes/user.py`:

```python
from app.modules.enhanced_ai_engine import EnhancedAIRecommendationEngine

@bp.route('/smart-recommendations')
@login_required
def smart_recommendations():
    ai_engine = EnhancedAIRecommendationEngine()
    recommendations = ai_engine.get_smart_recommendations(
        current_user.id,
        top_n=5
    )
    return render_template('user/smart_recommendations.html',
                         recommendations=recommendations)
```

### Method 3: In Chatbot

Update `app/modules/chatbot.py` to use enhanced AI:

```python
from app.modules.enhanced_ai_engine import get_ai_recommendations

# In ChatbotEngine class
def _generate_response(self, user_id, message, intent):
    if intent == 'recommendation':
        # Use enhanced AI
        recommendations = get_ai_recommendations(user_id, top_n=3)
        # ... format response
```

---

## 📊 Example Recommendation Output

```python
{
    'phone': <Samsung Galaxy A55 5G>,
    'specifications': <PhoneSpecification>,
    'match_score': 87.5,
    'reasoning': 'Perfect for Working Professionals in the 26-35 age group • Fits your budget of RM 1,000 - RM 3,000 • Excellent 50MP camera for photography • Long-lasting 5000mAh battery',
    'demographic_fit': 'Excellent'
}
```

---

## 🔄 Integration Workflow

### Complete Setup Flow:

1. **Scrape TechNave Data**
   ```powershell
   python scrape_technave.py 50
   ```

2. **Verify Database**
   ```powershell
   python phone_data_updater.py report
   ```

3. **Run Application**
   ```powershell
   python run.py
   ```

4. **Test Enhanced AI**
   - Login as user
   - Update your age and occupation in profile
   - Use "Get AI Recommendation" wizard
   - See personalized results!

---

## 🛠️ Customization

### Adjust Age Profiles

Edit `app/modules/enhanced_ai_engine.py`:

```python
self.age_profiles = {
    '18-25': {
        'priorities': ['Performance', 'Gaming', 'Camera'],
        'max_price_comfort': 2500,  # Adjust this
        'features': ['5G', 'Fast Charging']
    },
    # ... customize other age groups
}
```

### Adjust Occupation Profiles

```python
self.occupation_profiles = {
    'Student': {
        'max_budget': 2000,  # Adjust budget
        'recommended_features': ['Fast Charging', '5G'],
        'usage': ['Social Media', 'Gaming']
    },
    # ... add more occupations
}
```

---

## ⚠️ Important Notes

### Web Scraping Ethics

1. **Respect robots.txt**: TechNave's terms of service
2. **Rate Limiting**: Built-in 2-second delays between requests
3. **User-Agent**: Proper browser identification
4. **Fair Use**: For educational/personal use only

### TechNave HTML Structure

The scraper is built based on TechNave's current HTML structure. If the website changes:

1. **Inspect the website** using browser DevTools
2. **Update CSS selectors** in `scrape_technave.py`
3. **Test with small sample** first

### Error Handling

The scraper handles:
- ✅ Network timeouts
- ✅ Missing data fields
- ✅ Price format variations
- ✅ Duplicate phones
- ✅ Unknown brands

---

## 📈 Performance Tips

### Optimize Scraping

```python
# Scrape in batches
python scrape_technave.py 20  # First batch
# Wait 10 minutes
python scrape_technave.py 20  # Second batch
```

### Update Existing Data

Run the updater to refresh prices:
```powershell
python phone_data_updater.py prices
```

### Schedule Regular Updates

```powershell
# Run scheduler for automatic updates
python scheduler.py
```

---

## 🆘 Troubleshooting

### Scraper Returns No Data

**Problem**: `[INFO] Found 0 phone review URLs`

**Solutions**:
1. Check internet connection
2. Verify TechNave is accessible: https://www.technave.com/
3. TechNave HTML structure may have changed
4. Check firewall/proxy settings

### Price Not Found

**Problem**: Phone added with RM 0 price

**Solutions**:
1. Price might be on separate page
2. Update `_parse_specs()` method
3. Manually update price:
   ```powershell
   python phone_data_updater.py manual "Phone Name" 1999.00
   ```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'bs4'`

**Solution**:
```powershell
pip install beautifulsoup4 requests lxml
```

---

## 🎓 Learning Resources

- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Requests Library**: https://requests.readthedocs.io/
- **Web Scraping Best Practices**: https://www.scraperapi.com/blog/web-scraping-best-practices/

---

## ✅ Next Steps

1. ✅ Install dependencies
2. ✅ Run TechNave scraper
3. ✅ Verify scraped data
4. ✅ Test enhanced AI recommendations
5. ✅ Customize profiles for your users
6. ✅ Schedule automatic updates

---

**Happy Scraping! 📱🤖**

For support: support@dialsmart.my
