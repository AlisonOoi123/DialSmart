# Appendix G: API Documentation

## G.1 API Overview

### G.1.1 Base Information

| Property | Value |
|----------|-------|
| **Base URL** | `http://localhost:5000/api` (Development) |
| **Protocol** | HTTP (Development), HTTPS (Production) |
| **Content-Type** | `application/json` |
| **Authentication** | Session-based (Flask-Login) |
| **Response Format** | JSON |

### G.1.2 Authentication

**Authentication Method:** Session-based authentication using Flask-Login

**Authenticated Endpoints:**
- User must be logged in via web interface
- Session cookie automatically sent with requests
- No API key or token required

**Public Endpoints:**
- No authentication required
- Available to all users

---

## G.2 API Endpoints Summary

### G.2.1 Endpoint Overview

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/chat` | POST | Yes | Send message to chatbot |
| `/api/chat/history` | GET | Yes | Get chat conversation history |
| `/api/phones/search` | GET | No | Search phones (autocomplete) |
| `/api/phones/<id>` | GET | No | Get phone details |
| `/api/phones/filter` | POST | No | Filter phones by criteria |
| `/api/recommendations` | POST | Yes | Get AI recommendations |
| `/api/brands` | GET | No | Get all brands |
| `/api/stats` | GET | No | Get system statistics |

---

## G.3 Chatbot Endpoints

### G.3.1 POST /api/chat

**Description:** Send a message to the AI chatbot and receive a response

**Authentication:** Required (User must be logged in)

**Request:**

```http
POST /api/chat HTTP/1.1
Content-Type: application/json

{
    "message": "I need a phone under RM2000 with good camera",
    "session_id": "session_12345"
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | User's message to chatbot |
| `session_id` | string | No | Session identifier to group conversations (auto-generated if not provided) |

**Response (Success):**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "success": true,
    "response": "I found several great options under RM2000 with excellent cameras! Here are my top recommendations:\n\n1. XIAOMI Redmi Note 12 Pro - RM1,299\n   - 50MP Triple Camera System\n   - 6.67\" AMOLED Display\n   - 5000mAh Battery\n\n2. Samsung Galaxy A54 - RM1,899\n   - 50MP + 12MP + 5MP Camera\n   - 120Hz Super AMOLED\n   - IP67 Water Resistant\n\nWould you like more details about any of these phones?",
    "type": "recommendation",
    "metadata": {
        "recommended_phones": [15, 23],
        "criteria": {
            "max_budget": 2000,
            "feature_priority": "camera"
        }
    },
    "quick_replies": [
        "Tell me more about XIAOMI Redmi Note 12 Pro",
        "Compare these two phones",
        "Show me other options"
    ],
    "session_id": "session_12345"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `response` | string | Chatbot's text response |
| `type` | string | Response type: "text", "recommendation", "comparison" |
| `metadata` | object | Additional context data (phone IDs, criteria, etc.) |
| `quick_replies` | array | Suggested follow-up questions/actions |
| `session_id` | string | Session identifier |

**Error Response:**

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "error": "Message is required"
}
```

**Example Usage (JavaScript):**

```javascript
fetch('/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    credentials: 'same-origin',  // Include session cookie
    body: JSON.stringify({
        message: 'I need a phone under RM2000 with good camera',
        session_id: 'session_12345'
    })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Bot response:', data.response);
        displayMessage(data.response);

        // Show quick reply buttons
        if (data.quick_replies) {
            displayQuickReplies(data.quick_replies);
        }
    }
})
.catch(error => console.error('Error:', error));
```

### G.3.2 GET /api/chat/history

**Description:** Retrieve chat conversation history for current user

**Authentication:** Required

**Request:**

```http
GET /api/chat/history?session_id=session_12345&limit=50 HTTP/1.1
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `session_id` | string | No | All sessions | Filter by specific session |
| `limit` | integer | No | 50 | Maximum number of messages to return |

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "success": true,
    "history": [
        {
            "id": 1,
            "message": "I need a phone under RM2000",
            "response": "I found several great options under RM2000...",
            "intent": "budget_query",
            "created_at": "2024-01-15T10:30:00"
        },
        {
            "id": 2,
            "message": "Tell me more about the XIAOMI phone",
            "response": "The XIAOMI Redmi Note 12 Pro features...",
            "intent": "phone_details",
            "created_at": "2024-01-15T10:31:30"
        }
    ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `history` | array | Array of chat message objects |
| `history[].id` | integer | Message ID |
| `history[].message` | string | User's message |
| `history[].response` | string | Chatbot's response |
| `history[].intent` | string | Detected user intent |
| `history[].created_at` | string | ISO 8601 timestamp |

---

## G.4 Phone Endpoints

### G.4.1 GET /api/phones/search

**Description:** Search for phones by model name (for autocomplete)

**Authentication:** Not required

**Request:**

```http
GET /api/phones/search?q=galaxy&limit=10 HTTP/1.1
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | Yes | - | Search query (model name) |
| `limit` | integer | No | 10 | Maximum results to return |

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "success": true,
    "phones": [
        {
            "id": 1,
            "name": "Samsung Galaxy S23 Ultra",
            "brand": "Samsung",
            "price": 5299.00,
            "image": "/static/uploads/galaxy_s23_ultra.jpg"
        },
        {
            "id": 2,
            "name": "Samsung Galaxy A54",
            "brand": "Samsung",
            "price": 1899.00,
            "image": "/static/uploads/galaxy_a54.jpg"
        }
    ]
}
```

**Example Usage (JavaScript Autocomplete):**

```javascript
// Autocomplete search
function searchPhones(query) {
    fetch(`/api/phones/search?q=${encodeURIComponent(query)}&limit=5`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayAutocompleteResults(data.phones);
            }
        });
}

// Debounced search input
let searchTimeout;
document.getElementById('search-input').addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        searchPhones(e.target.value);
    }, 300);  // 300ms debounce
});
```

### G.4.2 GET /api/phones/<phone_id>

**Description:** Get detailed information for a specific phone

**Authentication:** Not required

**Request:**

```http
GET /api/phones/1 HTTP/1.1
```

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `phone_id` | integer | Phone ID |

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "success": true,
    "phone": {
        "id": 1,
        "model_name": "Samsung Galaxy S23 Ultra",
        "brand": "Samsung",
        "price": 5299.00,
        "main_image": "/static/uploads/galaxy_s23_ultra.jpg",
        "availability_status": "Available",
        "specs": {
            "screen_size": 6.8,
            "screen_resolution": "1440x3088",
            "screen_type": "Dynamic AMOLED 2X",
            "processor": "Snapdragon 8 Gen 2",
            "ram_options": "8GB, 12GB",
            "storage_options": "256GB, 512GB, 1TB",
            "rear_camera": "200MP + 10MP + 10MP + 12MP",
            "front_camera": "12MP",
            "battery_capacity": 5000,
            "has_5g": true,
            "operating_system": "Android 13"
        }
    }
}
```

**Error Response (Phone Not Found):**

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
    "error": "Phone not found"
}
```

### G.4.3 POST /api/phones/filter

**Description:** Filter phones based on multiple criteria with pagination

**Authentication:** Not required

**Request:**

```http
POST /api/phones/filter HTTP/1.1
Content-Type: application/json

{
    "brand_ids": [1, 3, 5],
    "min_price": 1000,
    "max_price": 3000,
    "min_ram": 6,
    "has_5g": true,
    "min_battery": 4000,
    "page": 1,
    "per_page": 12
}
```

**Request Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `brand_ids` | array | No | All brands | Array of brand IDs to filter |
| `min_price` | float | No | 0 | Minimum price in RM |
| `max_price` | float | No | Unlimited | Maximum price in RM |
| `min_ram` | integer | No | - | Minimum RAM in GB |
| `has_5g` | boolean | No | false | Filter for 5G support |
| `min_battery` | integer | No | - | Minimum battery capacity in mAh |
| `page` | integer | No | 1 | Page number for pagination |
| `per_page` | integer | No | 12 | Results per page |

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "success": true,
    "phones": [
        {
            "id": 1,
            "model_name": "Samsung Galaxy S23 Ultra",
            "brand": "Samsung",
            "price": 5299.00,
            "main_image": "/static/uploads/galaxy_s23_ultra.jpg"
        },
        {
            "id": 3,
            "model_name": "Xiaomi 13 Pro",
            "brand": "Xiaomi",
            "price": 3499.00,
            "main_image": "/static/uploads/xiaomi_13_pro.jpg"
        }
    ],
    "total": 15,
    "pages": 2,
    "current_page": 1
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `phones` | array | Array of phone objects matching criteria |
| `total` | integer | Total number of matching phones |
| `pages` | integer | Total number of pages |
| `current_page` | integer | Current page number |

---

## G.5 Recommendation Endpoint

### G.5.1 POST /api/recommendations

**Description:** Get AI-powered phone recommendations based on user criteria

**Authentication:** Required

**Request:**

```http
POST /api/recommendations HTTP/1.1
Content-Type: application/json

{
    "criteria": {
        "budget": {
            "min": 1000,
            "max": 3000
        },
        "primary_usage": ["Photography", "Social Media"],
        "important_features": ["Camera", "Battery"],
        "technical": {
            "min_ram": 6,
            "min_storage": 128,
            "requires_5g": true
        }
    },
    "top_n": 5
}
```

**Request Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `criteria` | object | No | User preferences | Recommendation criteria |
| `criteria.budget` | object | No | - | Budget range (min, max) |
| `criteria.primary_usage` | array | No | - | Usage patterns |
| `criteria.important_features` | array | No | - | Feature priorities |
| `criteria.technical` | object | No | - | Technical requirements |
| `top_n` | integer | No | 3 | Number of recommendations to return |

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "success": true,
    "recommendations": [
        {
            "phone_id": 1,
            "model_name": "Samsung Galaxy S23 Ultra",
            "brand": "Samsung",
            "price": 5299.00,
            "match_score": 95.5,
            "reasoning": "Excellent match! This phone excels in photography with its 200MP camera system and has a large 5000mAh battery. It meets all your technical requirements with 12GB RAM, 256GB storage, and 5G support.",
            "main_image": "/static/uploads/galaxy_s23_ultra.jpg",
            "key_specs": {
                "ram": "8GB, 12GB",
                "storage": "256GB, 512GB, 1TB",
                "camera": "200MP",
                "battery": "5000mAh"
            }
        },
        {
            "phone_id": 3,
            "model_name": "Xiaomi 13 Pro",
            "brand": "Xiaomi",
            "price": 3499.00,
            "match_score": 92.3,
            "reasoning": "Great value for photography enthusiasts. Features triple 50MP camera system with Leica optics, 4820mAh battery with ultra-fast 120W charging, and 5G connectivity.",
            "main_image": "/static/uploads/xiaomi_13_pro.jpg",
            "key_specs": {
                "ram": "8GB, 12GB",
                "storage": "128GB, 256GB, 512GB",
                "camera": "50MP",
                "battery": "4820mAh"
            }
        }
    ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `recommendations` | array | Array of recommended phones |
| `recommendations[].phone_id` | integer | Phone ID |
| `recommendations[].model_name` | string | Phone model name |
| `recommendations[].brand` | string | Brand name |
| `recommendations[].price` | float | Price in RM |
| `recommendations[].match_score` | float | Match score (0-100) |
| `recommendations[].reasoning` | string | Explanation for recommendation |
| `recommendations[].main_image` | string | Image URL |
| `recommendations[].key_specs` | object | Key specifications |

**Example Usage:**

```javascript
async function getRecommendations() {
    const criteria = {
        budget: { min: 1000, max: 3000 },
        primary_usage: ['Photography'],
        important_features: ['Camera', 'Battery'],
        technical: {
            min_ram: 6,
            requires_5g: true
        }
    };

    try {
        const response = await fetch('/api/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin',
            body: JSON.stringify({
                criteria: criteria,
                top_n: 5
            })
        });

        const data = await response.json();

        if (data.success) {
            displayRecommendations(data.recommendations);
        }
    } catch (error) {
        console.error('Error getting recommendations:', error);
    }
}
```

---

## G.6 Brand Endpoint

### G.6.1 GET /api/brands

**Description:** Get list of all active smartphone brands

**Authentication:** Not required

**Request:**

```http
GET /api/brands HTTP/1.1
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "success": true,
    "brands": [
        {
            "id": 1,
            "name": "Samsung",
            "logo_url": "/static/uploads/samsung_logo.png",
            "phone_count": 15
        },
        {
            "id": 2,
            "name": "Apple",
            "logo_url": "/static/uploads/apple_logo.png",
            "phone_count": 8
        },
        {
            "id": 3,
            "name": "XIAOMI",
            "logo_url": "/static/uploads/xiaomi_logo.png",
            "phone_count": 12
        }
    ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `brands` | array | Array of brand objects |
| `brands[].id` | integer | Brand ID |
| `brands[].name` | string | Brand name |
| `brands[].logo_url` | string | Brand logo image URL |
| `brands[].phone_count` | integer | Number of active phones for this brand |

---

## G.7 Statistics Endpoint

### G.7.1 GET /api/stats

**Description:** Get system statistics (total phones, brands, price range)

**Authentication:** Not required

**Request:**

```http
GET /api/stats HTTP/1.1
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "success": true,
    "stats": {
        "total_phones": 50,
        "total_brands": 10,
        "min_price": 599.00,
        "max_price": 5999.00
    }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `stats` | object | Statistics object |
| `stats.total_phones` | integer | Total number of active phones |
| `stats.total_brands` | integer | Total number of active brands |
| `stats.min_price` | float | Lowest phone price (RM) |
| `stats.max_price` | float | Highest phone price (RM) |

---

## G.8 Error Handling

### G.8.1 Standard Error Response Format

All error responses follow this format:

```json
{
    "success": false,
    "error": "Error message description",
    "error_code": "ERROR_CODE",
    "status_code": 400
}
```

### G.8.2 HTTP Status Codes

| Status Code | Meaning | Usage |
|-------------|---------|-------|
| **200** | OK | Successful request |
| **400** | Bad Request | Invalid request parameters |
| **401** | Unauthorized | Authentication required but not provided |
| **403** | Forbidden | Authenticated but insufficient permissions |
| **404** | Not Found | Resource not found |
| **500** | Internal Server Error | Server error |

### G.8.3 Common Error Responses

**Missing Required Parameter:**
```http
HTTP/1.1 400 Bad Request

{
    "error": "Message is required"
}
```

**Authentication Required:**
```http
HTTP/1.1 401 Unauthorized

{
    "error": "Authentication required. Please log in."
}
```

**Resource Not Found:**
```http
HTTP/1.1 404 Not Found

{
    "error": "Phone not found"
}
```

**Server Error:**
```http
HTTP/1.1 500 Internal Server Error

{
    "error": "An internal error occurred. Please try again later."
}
```

---

## G.9 Rate Limiting

**Current Implementation:** No rate limiting (development)

**Recommended for Production:**
- **Per User:** 100 requests per minute
- **Per IP (unauthenticated):** 30 requests per minute
- **Chatbot Endpoint:** 20 requests per minute per user

**Example Rate Limit Response:**

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 60

{
    "error": "Rate limit exceeded. Please try again in 60 seconds.",
    "retry_after": 60
}
```

---

## G.10 CORS Configuration

**Development:**
- Same-origin requests only
- No CORS headers needed

**Production (if API used by external clients):**

```python
from flask_cors import CORS

# Allow specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://dialsmart.my", "https://www.dialsmart.my"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## G.11 API Versioning

**Current Version:** v1 (implicit, no version in URL)

**Future Versioning Strategy:**
- Include version in URL: `/api/v2/phones`
- Maintain backward compatibility for at least one major version
- Deprecation notices in response headers

---

## G.12 Complete API Examples

### G.12.1 Complete Recommendation Flow

```javascript
// 1. Get user's criteria
const userCriteria = {
    budget: { min: 1000, max: 3000 },
    primary_usage: ['Photography', 'Gaming'],
    important_features: ['Camera', 'Performance', 'Battery'],
    technical: {
        min_ram: 8,
        min_storage: 128,
        requires_5g: true
    }
};

// 2. Request recommendations
const response = await fetch('/api/recommendations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin',
    body: JSON.stringify({
        criteria: userCriteria,
        top_n: 5
    })
});

const data = await response.json();

// 3. Display recommendations
if (data.success) {
    data.recommendations.forEach(rec => {
        console.log(`${rec.model_name} - RM${rec.price}`);
        console.log(`Match Score: ${rec.match_score}%`);
        console.log(`Reason: ${rec.reasoning}\n`);
    });
}

// 4. Get detailed specs for top recommendation
const phoneId = data.recommendations[0].phone_id;
const phoneResponse = await fetch(`/api/phones/${phoneId}`);
const phoneData = await phoneResponse.json();

console.log('Full specifications:', phoneData.phone.specs);
```

### G.12.2 Complete Chatbot Conversation

```javascript
// Initialize session
let sessionId = generateUUID();

// Send first message
async function sendMessage(message) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({
            message: message,
            session_id: sessionId
        })
    });

    const data = await response.json();

    if (data.success) {
        // Display bot response
        displayBotMessage(data.response);

        // Show quick reply buttons
        if (data.quick_replies && data.quick_replies.length > 0) {
            displayQuickReplies(data.quick_replies);
        }

        // If response includes phone recommendations
        if (data.metadata && data.metadata.recommended_phones) {
            displayRecommendedPhones(data.metadata.recommended_phones);
        }
    }
}

// Usage
await sendMessage("I need a phone under RM2000 with good camera");
await sendMessage("Tell me more about the XIAOMI option");
await sendMessage("Compare the top 2 phones");
```

### G.12.3 Phone Filtering and Pagination

```javascript
let currentPage = 1;

async function filterPhones(filters) {
    const response = await fetch('/api/phones/filter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            brand_ids: filters.brands,
            min_price: filters.minPrice,
            max_price: filters.maxPrice,
            min_ram: filters.minRam,
            has_5g: filters.has5G,
            min_battery: filters.minBattery,
            page: currentPage,
            per_page: 12
        })
    });

    const data = await response.json();

    if (data.success) {
        displayPhones(data.phones);
        displayPagination(data.current_page, data.pages);

        console.log(`Showing ${data.phones.length} of ${data.total} phones`);
    }
}

// Next page
function nextPage() {
    currentPage++;
    filterPhones(currentFilters);
}

// Previous page
function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        filterPhones(currentFilters);
    }
}
```

---

## G.13 Testing the API

### G.13.1 Using cURL

**Test Phone Search:**
```bash
curl -X GET "http://localhost:5000/api/phones/search?q=galaxy&limit=5"
```

**Test Phone Details:**
```bash
curl -X GET "http://localhost:5000/api/phones/1"
```

**Test Phone Filter:**
```bash
curl -X POST "http://localhost:5000/api/phones/filter" \
  -H "Content-Type: application/json" \
  -d '{
    "min_price": 1000,
    "max_price": 3000,
    "has_5g": true,
    "page": 1,
    "per_page": 12
  }'
```

**Test Brands:**
```bash
curl -X GET "http://localhost:5000/api/brands"
```

**Test Stats:**
```bash
curl -X GET "http://localhost:5000/api/stats"
```

### G.13.2 Using Postman

1. **Create New Request**
   - Method: POST
   - URL: `http://localhost:5000/api/recommendations`

2. **Set Headers**
   - Content-Type: `application/json`

3. **Set Body (raw JSON)**
   ```json
   {
     "criteria": {
       "budget": {"min": 1000, "max": 3000},
       "important_features": ["Camera", "Battery"]
     },
     "top_n": 5
   }
   ```

4. **Send Request** and view response

---

**End of Appendix G**
