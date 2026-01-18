# 🚀 SolveStack Integration Guide

## ✅ Current Status

### Running Services
- **Backend**: http://localhost:8000 ✅
- **Frontend**: http://localhost:3001 ✅

### Backend Features
- 📝 REST API with 20+ endpoints
- 🔐 JWT Authentication
- 💾 SQLite Database (problems.db)
- 🤖 AI Quality Scoring
- 👥 Collaboration System
- ⭐ Favorites/Interests System

### Frontend Features
- 🎨 Dark metallic theme with aqua accents
- 📱 Fully responsive design
- 🔐 Authentication (Login/Register)
- 📊 Dashboard with search & filters
- 💬 Problem details & collaboration
- ⭐ Favorites management
- 👤 User profiles

---

## 🔗 API Integration

### Base Configuration
```javascript
// Located in: src/api/index.js
const API_BASE = 'http://localhost:8000'
```

### Key API Endpoints

#### Authentication
```
POST   /register        - User signup
POST   /login          - User login  
GET    /me             - Get current user
```

#### Problems
```
GET    /problems       - List all problems (skip, limit params)
GET    /problems/{id}  - Get problem details
POST   /problems/{id}/score - Calculate quality score
```

#### Interests (Favorites)
```
POST   /interest       - Mark problem as favorite
DELETE /interest/{id}  - Remove from favorites
```

#### Collaboration
```
POST   /collaborate/request       - Request collaboration
POST   /collaborate/accept        - Accept collaboration request
POST   /collaborate/reject        - Reject collaboration request
GET    /collaborate/{id}          - Get collaboration status
GET    /collaborate/suggestions/{id} - Get collaboration suggestions
```

#### Recommendations
```
GET    /recommendations - Get recommended problems
```

---

## 📊 Data Flow

### User Registration Flow
```
Frontend (Register Form)
    ↓
    POST /register (email, username, password)
    ↓
Backend (models.py - User)
    ↓
    Database (SQLite)
    ↓
Response: Token & User Info
    ↓
Frontend (Store token in localStorage)
```

### Problem Fetching Flow
```
Frontend (Dashboard Page)
    ↓
    GET /problems?skip=0&limit=50
    ↓
Backend (queries Problem table)
    ↓
Database (problems.db)
    ↓
Response: Array of problems with:
  - id, title, description
  - source, suggested_tech
  - author_name, reference_link
  - quality_score, interested_count
    ↓
Frontend (Renders ProblemCard components)
```

### Favorite System Flow
```
Frontend (Heart icon click)
    ↓
    POST /interest (problemId)
    ↓
Backend (Creates Interest entry)
    ↓
Database (interest table)
    ↓
Response: Success/Error
    ↓
Frontend (Updates UI - toggle heart)
```

---

## 🔧 Testing Integration

### 1. Test Backend Health
```bash
curl http://localhost:8000/
```
**Expected**: `{"status":"healthy","message":"SolveStack API is running"}`

### 2. Test API Docs
```bash
# Interactive API documentation
open http://localhost:8000/docs
```

### 3. Test Problems Endpoint
```bash
curl http://localhost:8000/problems
```
**Expected**: Array of problem objects

### 4. Test Frontend Connection
1. Open http://localhost:3001
2. Try to register/login
3. Check browser DevTools > Network tab
4. Verify requests go to localhost:8000
5. Check for successful responses

---

## 📋 Frontend Pages & Backend Integration

| Page | Route | Backend Endpoints Used | Data Flow |
|------|-------|----------------------|-----------|
| Landing | / | None (static) | UI only |
| Register | /register | POST /register | User data → Backend |
| Login | /login | POST /login | Credentials → Backend |
| Dashboard | /dashboard | GET /problems | Backend → Problem list |
| Problem Detail | /problem/:id | GET /problems/:id | Backend → Full details |
| Profile | /profile | GET /me | User data from Backend |
| Favorites | /favorites | GET /problems (filtered) | User interests → Backend |
| Collaboration | /collaboration/:id | GET /collaborate/:id | Collaboration data |

---

## 🔑 Authentication Flow

### Login Process
```
1. User enters email & password
2. Frontend sends: POST /login
3. Backend validates & returns JWT token
4. Frontend stores token in localStorage
5. Token auto-added to all future requests via interceptor
6. User redirected to /dashboard
```

### Token Persistence
- Stored in: `localStorage.access_token`
- Auto-attached to requests via axios interceptor
- Auto-fetched on app load via `useAuth()` hook
- Clears on logout

---

## 📱 Data Validation

### Frontend Validation (Before sending to backend)
```javascript
// Register
- Email: Must be valid format
- Username: 3-50 characters
- Password: Minimum 6 characters

// Login
- Email & password required
- Format validation
```

### Backend Validation (In schemas.py)
```python
# UserCreate
- email: EmailStr (pydantic validation)
- username: str, min_length=3, max_length=50
- password: str, min_length=6

# ProblemResponse
- title: str (required)
- description: str
- source: str
- suggested_tech: str
```

---

## 🐛 Debugging Tips

### Check Frontend → Backend Connection
1. **DevTools Network Tab**
   - Look for requests to `localhost:8000`
   - Check Response tab for data
   - Check Headers for Authorization token

2. **Console Errors**
   - Check for CORS errors
   - Check for 401 Unauthorized (token issue)
   - Check for 404 (endpoint not found)

### Check Backend Logs
```bash
# Terminal running backend shows:
- Request logs: GET /problems
- Database queries
- Errors/warnings
```

### Test Specific Endpoints
```bash
# With token (after login)
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/me

# Problems
curl http://localhost:8000/problems?skip=0&limit=10

# Specific problem
curl http://localhost:8000/problems/1
```

---

## 🚀 Adding New Features (Backend → Frontend)

### Example: Add a new problem filter
1. **Backend (main.py)**
   ```python
   @app.get("/problems/filter/{source}")
   def get_problems_by_source(source: str):
       # Implementation
   ```

2. **Frontend (api/index.js)**
   ```javascript
   getBySource: (source) =>
       api.get(`/problems/filter/${source}`)
   ```

3. **Frontend Component**
   ```javascript
   const data = await problemsAPI.getBySource('reddit')
   ```

---

## ✅ Integration Checklist

- [x] Backend running on http://localhost:8000
- [x] Frontend running on http://localhost:3001
- [x] API endpoints connected
- [x] Authentication working
- [x] CORS configured
- [x] Token management setup
- [x] Data flows both directions
- [x] Database populated with sample data
- [x] Error handling in place
- [x] Loading states implemented

---

## 📚 Key Files for Integration

### Frontend
- `src/api/index.js` - All API calls
- `src/context/AuthContext.jsx` - Auth state & token management
- `src/pages/Dashboard.jsx` - Example of API usage
- `src/components/ProtectedRoute.jsx` - Route protection

### Backend
- `main.py` - All API endpoints
- `models.py` - Database models
- `schemas.py` - Data validation
- `database.py` - Database connection
- `auth.py` - Authentication logic

---

## 🎯 Next Steps

1. **Test Registration**
   - Go to http://localhost:3001/register
   - Fill form and submit
   - Check backend logs for success

2. **Test Problem Feed**
   - Go to http://localhost:3001/dashboard
   - Should see list of problems
   - Try search & filters

3. **Test Favorites**
   - Click heart icon on problem
   - Go to /favorites page
   - Should show marked problems

4. **Monitor Integration**
   - Keep browser DevTools open
   - Watch Network tab for API calls
   - Check backend terminal for logs

---

**Version**: 1.0.0
**Status**: ✅ Fully Integrated
**Last Updated**: January 17, 2026
