# DialSmart - Malaysia's Intelligent Mobile Advisor

DialSmart is an AI-powered smartphone recommendation platform specifically designed for Malaysian consumers, featuring machine learning algorithms and a conversational chatbot interface to simplify smartphone selection decisions.

## Features

### User Features
- **AI-Powered Recommendations**: Get personalized smartphone recommendations based on your preferences and budget
- **Smart Chatbot**: Interactive AI assistant to help find the perfect phone through natural conversation
- **Phone Comparison**: Side-by-side comparison of smartphone specifications
- **Advanced Filtering**: Filter phones by brand, price, features, and specifications
- **Personalized Dashboard**: Track your recommendation history and saved comparisons
- **Recommendation Wizard**: Step-by-step guided process to find your ideal phone

### Admin Features
- **Phone Management**: Full CRUD operations for smartphone listings
- **Brand Management**: Manage smartphone brands and their information
- **User Management**: View and manage registered users
- **Analytics Dashboard**: Track system usage and popular phones
- **System Logs**: Monitor recommendation activity

## Technology Stack

- **Backend**: Python 3.8+ with Flask
- **Database**: SQLite (development) / PostgreSQL (production recommended)
- **Frontend**: Bootstrap 5, jQuery
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   cd DialSmart
   ```

2. **Create and activate virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   flask init-db
   ```

5. **Seed sample data (optional)**
   ```bash
   flask seed-data
   ```

6. **Create an admin user**
   ```bash
   flask create-admin
   ```
   Follow the prompts to create your admin account.

7. **Run the application**
   ```bash
   python run.py
   ```

   The application will be available at `http://localhost:5000`

## Default Login Credentials

After running `flask seed-data`, you can use these test credentials:

- **Test User**:
  - Email: `user@dialsmart.my`
  - Password: `password123`

- **Admin User**: Use the credentials you created with `flask create-admin`

## Project Structure

```
DialSmart/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models/                  # Database models
│   │   ├── user.py             # User and UserPreference models
│   │   ├── phone.py            # Phone and PhoneSpecification models
│   │   ├── brand.py            # Brand model
│   │   └── recommendation.py   # Recommendation, Comparison, ChatHistory models
│   ├── routes/                  # Route blueprints
│   │   ├── auth.py             # Authentication routes
│   │   ├── user.py             # User-facing routes
│   │   ├── admin.py            # Admin panel routes
│   │   ├── phone.py            # Phone details and comparison routes
│   │   └── api.py              # API endpoints
│   ├── modules/                 # Business logic modules
│   │   ├── ai_engine.py        # AI recommendation engine
│   │   ├── chatbot.py          # Chatbot NLP engine
│   │   └── comparison.py       # Phone comparison module
│   ├── templates/               # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── auth/               # Authentication templates
│   │   ├── user/               # User interface templates
│   │   ├── phone/              # Phone-related templates
│   │   └── admin/              # Admin panel templates
│   ├── static/                  # Static files
│   │   ├── css/                # Stylesheets
│   │   ├── js/                 # JavaScript files
│   │   └── uploads/            # User uploaded files
│   └── utils/                   # Utility functions
│       └── helpers.py          # Helper functions
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Usage Guide

### For Users

1. **Register/Login**: Create an account or login to access personalized features
2. **Get Recommendations**:
   - Use the AI Recommendation Wizard for step-by-step guidance
   - Chat with the AI Assistant for conversational recommendations
3. **Browse Phones**: Explore phones by brand or use advanced filters
4. **Compare Phones**: Select two phones to see detailed side-by-side comparison
5. **Track History**: View your recommendation history in your dashboard

### For Administrators

1. **Login**: Use your admin credentials to access the admin panel
2. **Manage Phones**:
   - Add new phones with detailed specifications
   - Edit existing phone information
   - Activate/deactivate phone listings
3. **Manage Brands**: Add and manage smartphone brands
4. **View Analytics**: Monitor system usage and popular phones
5. **Manage Users**: View registered users and their activity

## Key Features Explained

### AI Recommendation Engine
The AI engine analyzes user preferences including:
- Budget range
- Usage patterns (gaming, photography, business, etc.)
- Feature priorities (battery, camera, performance, etc.)
- Brand preferences
- Technical requirements (RAM, storage, 5G, etc.)

It calculates match scores for phones and provides reasoning for recommendations.

### Chatbot System
The chatbot uses natural language processing to:
- Understand user queries about phones
- Detect user intent (budget queries, recommendations, comparisons)
- Extract criteria from natural language (e.g., "phone under RM2000 with good camera")
- Provide contextual responses with phone suggestions

### Phone Comparison
Compares phones across multiple categories:
- Price and value
- Display specifications
- Performance metrics
- Camera capabilities
- Battery life
- Connectivity features
- Build quality and design

## Configuration

Edit `config.py` to customize:
- Database connection
- Secret key
- Upload folder settings
- Pagination settings
- Price ranges
- Featured brands

## Database Commands

```bash
# Initialize database
flask init-db

# Create admin user
flask create-admin

# Seed sample data
flask seed-data

# Access Flask shell with database context
flask shell
```

## API Endpoints

### Public Endpoints
- `POST /api/chat` - Chat with AI assistant
- `GET /api/phones/search` - Search phones
- `GET /api/phones/<id>` - Get phone details
- `GET /api/brands` - Get all brands

### Authenticated Endpoints
- `POST /api/recommendations` - Get AI recommendations
- `GET /api/chat/history` - Get chat history
- `POST /api/phones/filter` - Filter phones

## Support

For issues and questions:
- Email: support@dialsmart.my
- Phone: +60 3-1234 5678

## License

This project is for academic purposes.

## Acknowledgments

- Built with Flask framework
- UI powered by Bootstrap 5
- Icons by Bootstrap Icons
- Database management with SQLAlchemy

---

**DialSmart** - Simplifying smartphone decisions for Malaysians
