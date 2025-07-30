# NextStep Backend API 🚀

Production-ready FastAPI backend for the NextStep social services platform, designed to work with separate social worker and patient frontend applications.

## 🌟 Live Deployment

**Backend API**: Ready for Railway deployment  
**Frontend Apps**:
- Social Worker: https://frontend-e9okwz36q-next-steps-projects-62eea6ae.vercel.app
- Patient Mobile: https://momo-8dih2mkbm-next-steps-projects-62eea6ae.vercel.app

## 🏗️ Architecture

This backend serves as the central API for a dual-frontend architecture:
- **Social Worker Frontend**: Professional dashboard for case management
- **Patient Mobile App**: Mobile-first interface for resource access
- **Shared Backend**: This FastAPI server handling all data and communication

## 🎯 Key Features

### Core API Services
- **Resource Management**: AI-powered resource matching and assignment
- **Client Data**: Comprehensive client profile and case management
- **Real-time Communication**: WebSocket-based messaging system
- **Analytics Engine**: Data insights and progress tracking
- **Authentication**: Firebase-integrated user management

### External Integrations
- **OpenAI**: Intelligent resource recommendations
- **Twilio**: SMS notifications and communications
- **SendGrid**: Email service integration
- **Google Sheets**: External data synchronization
- **ChromaDB**: Vector-based semantic search

### Deployment Features
- **Railway Ready**: Configured for Railway deployment
- **Health Monitoring**: `/health` endpoint for uptime checks
- **Environment Config**: Secure environment variable management
- **CORS Setup**: Configured for Vercel frontend connections

## 🚀 Quick Deployment

### Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway deploy
```

### Environment Variables
Set these in Railway dashboard:
```env
OPENAI_API_KEY=your_openai_api_key
FIREBASE_ADMIN_SDK=your_firebase_credentials_json
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
```

### Local Development
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
python server.py
```

## 📁 Key Files

- **`server.py`**: Main FastAPI application
- **`start.py`**: Railway startup script
- **`railway.json`**: Railway deployment configuration
- **`requirements.txt`**: Python dependencies
- **`rag_resource_matcher.py`**: AI-powered resource matching
- **`analytics_engine.py`**: Data analytics and insights
- **`email_service.py`**: Email notification system
- **`google_sheets_integration.py`**: External data sync

## 🔌 API Endpoints

### Core Endpoints
- `GET /health` - Health check
- `GET /api/resources` - Resource catalog
- `POST /api/resource-match` - AI resource matching
- `GET /api/clients` - Client management
- `POST /api/send-message` - Real-time messaging

### Authentication
- `POST /auth/login` - User authentication
- `POST /auth/register` - User registration
- `GET /auth/profile` - User profile

### Analytics
- `GET /api/analytics` - System analytics
- `GET /api/client-progress` - Client progress tracking

## 🛠️ Technology Stack

- **FastAPI**: High-performance Python web framework
- **LangChain**: AI/ML integration framework
- **ChromaDB**: Vector database for semantic search
- **OpenAI**: GPT integration for intelligent features
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for production

## 📱 Dual-Frontend Support

This backend is designed to serve two distinct frontend applications:

### Social Worker Interface
- Professional dashboard for case management
- Resource assignment and tracking
- Client communication tools
- Analytics and reporting

### Patient Mobile App
- Mobile-optimized resource access
- Direct messaging with social workers
- Appointment management
- Profile updates

## 🔐 Security Features

- **Firebase Authentication**: Secure user management
- **Role-based Access**: Different permissions for social workers and patients
- **Input Validation**: Comprehensive data validation
- **CORS Protection**: Configured for approved domains
- **Environment Security**: Sensitive data in environment variables

## 📊 Monitoring & Analytics

- Health check endpoint for uptime monitoring
- Comprehensive logging for debugging
- Analytics engine for usage insights
- Client progress tracking
- Resource effectiveness metrics

## 🚨 Production Readiness

- ✅ Railway deployment configuration
- ✅ Environment variable management
- ✅ Health check endpoint
- ✅ Error handling and logging
- ✅ CORS configuration for frontends
- ✅ Database connection management
- ✅ AI service integration

## 📈 Scalability

Designed for production scale with:
- Async/await patterns for high concurrency
- Connection pooling for database efficiency
- Caching strategies for frequently accessed data
- Microservice-ready architecture
- Cloud-native deployment approach

---

**NextStep Backend** - Powering social services through technology 