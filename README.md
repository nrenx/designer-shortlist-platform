# 🏠 EmptyCup Designer Shortlist Platform

📐 **Design Specification**
- Pixel-perfect, mobile-first layout (320px–480px) matching the provided Figma design file.
- Use same fonts and icons downloaded directly from Figma.

**Find and connect with the best interior designers for your project.**

A mobile-first web application that lists all interior designers active on EmptyCup's platform. Homeowners and businesses can browse, filter, and shortlist designers to find the perfect match for their interior design projects. Built following Figma design specifications with pixel-perfect styling and full-stack functionality.

## 📖 Table of Contents
- [Quick Start](#-quick-start)
  - [Option 1: Run with Docker](#option-1-run-with-docker-easiest)
  - [Option 2: Run Locally](#option-2-run-locally)
- [⚙️ Configuration](#️-configuration)
- [✨ Core Features](#️-core-features-assignment-requirements)
- [📁 Project Structure](#️-project-structure)
- [🔧 For Administrators](#🔧-for-administrators)
- [🛠️ Backend API](#️-backend-api)
- [🗄️ Database Schema](#️-database-schema)
- [🌐 Deploy to the Internet](#️-deploy-to-the-internet)
- [💡 Built With](#️-built-with)
- [📞 Support](#️-support)


## 🚀 Quick Start

### Option 1: Run with Docker (Easiest)
```bash
# Clone the project
git clone <repository-url>
cd designer-shortlist-platform

# Start everything with one command
docker-compose up -d

# Open in your browser
# Main App: http://localhost:8080
# Admin Panel: http://localhost:5001
```

### Option 2: Run Locally
```bash
# Frontend: Install & build
npm install
npm run build

# Frontend dev server
npm run dev

# Backend: Install Python dependencies & start API
cd api
pip install -r requirements.txt
python app.py

# Open in your browser
# Main App: http://localhost:8080
# Admin Panel: http://localhost:5001
```

## ✨ Core Features (Assignment Requirements)

### 🖌 **1. Styling & Layout**
- Fully responsive, mobile-focused user interface following Figma specs
- Consistent color scheme, professional typography, and touch-friendly spacing

### ⭐ **2. Interactive Shortlisting**
- **Toggle shortlist** button with icon swap (outline ↔ filled)
- **Shortlisted filter** to view only your favorites
- **Persistent state** stored per session via backend & local updates

### 🔍 **3. Sorting & Hide Functionality**
- **Sort by Experience, Price, or Projects** with ascending/descending options
- **Hide listing** with undo option
- **Multiple views**: Switch between List, Contacts, Gallery, and Map views

### 🎯 **4. Designer Actions**
- **View Details**: Open modal with full profile, portfolio, rating, etc.
- **Shortlist**: Mark/unmark designers as favorites
- **Hide**: Temporarily remove a listing from view
- **Report**: Submit inappropriate content via modal form

## 🔧 For Administrators

### Add New Designers
1. Go to the Admin Panel: `http://localhost:5001`
2. Click "Add Designer"
3. Fill out the simple form
4. Click "Save" - that's it!

### Upload Multiple Designers
1. Prepare a JSON file with designer information
2. Go to "Upload JSON" in the admin panel
3. Select your file and upload
4. All designers will be added automatically

### Manage Existing Designers
- View all designers in one place
- Edit information anytime
- See how many designers you have
- Simple web interface - no technical knowledge needed

## 📁 Project Structure

```
📂 api/                    # Backend (handles data)
📂 src/                    # Frontend (what users see)
📂 public/                 # Images and static files
📄 docker-compose.yml      # Easy setup file
📄 package.json           # Project dependencies
```

## 🛠️ Need Help Setting Up?

### Requirements
- A computer with internet connection
- Docker installed (recommended) OR Node.js

### Step-by-Step Setup

**Method 1: Super Easy (Docker)**
1. Download Docker from docker.com
2. Clone this project
3. Run `docker-compose up -d`
4. Open http://localhost:8080

**Method 2: Manual Setup**
1. Install Node.js from nodejs.org
2. Clone this project
3. Run `npm install`
4. Run `npm run build`
5. Open the built files in a web browser

### Having Issues?
- Make sure Docker is running
- Check that ports 8080 and 5001 aren't being used
- Try restarting your computer
- Contact support if you're still stuck

## 🌐 Deploy to the Internet

Want to put your designer platform online? Here's the simplest, most cost-effective approach:

### Backend + Database (All-in-One)
**Railway** - Complete backend solution ($5/month for everything!)
1. Sign up at [railway.app](https://railway.app)
2. Create a new project
3. Add PostgreSQL database service (automatic setup)
4. Deploy from GitHub (uses `Dockerfile.backend`)
5. Railway automatically connects everything!

**Why Railway?**
- ✅ Database + API hosting in one platform
- ✅ Only $5/month total (vs $30+ with separate services)
- ✅ Automatic configuration and internal networking
- ✅ Built-in monitoring and backups

### Frontend (User Interface)
**Netlify** - Free and simple
1. Sign up at [netlify.com](https://netlify.com)
2. Connect your GitHub account
3. Select this project
4. Set environment variable: `VITE_API_BASE_URL=https://your-app.railway.app/api`
5. It will automatically deploy!

## 🔗 How It All Works

The platform has three main parts that work together seamlessly:

1. **Frontend** (Netlify) - What users see and interact with
2. **Backend API** (Railway) - Handles data processing and admin functions
3. **Database** (Railway PostgreSQL) - Stores all designer information securely

**Local Development:**
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:5001`
- Database: SQLite (automatic)

**Production:**
- Frontend: `https://your-app.netlify.app`
- Backend: `https://your-app.railway.app`
- Database: Railway PostgreSQL (automatic)

Everything connects automatically - no complex configuration needed!

## 💡 Built With

**Modern, reliable technologies optimized for cost and performance:**

### Frontend
- **React** - Interactive user interface
- **TypeScript** - Type-safe, reliable code
- **Tailwind CSS** - Beautiful, responsive design
- **Vite** - Fast development and building

### Backend
- **Flask** - Lightweight Python web framework
- **PostgreSQL** - Enterprise-grade database
- **Gunicorn** - Production WSGI server
- **Docker** - Containerized deployment

### Hosting & Deployment
- **Railway** - Backend + Database ($5/month total)
- **Netlify** - Frontend hosting (free tier available)
- **Total Cost**: ~$5/month for full production deployment
- **Integrated Architecture** - Everything works together seamlessly

### 💰 Cost Comparison
| Solution | Monthly Cost | Setup Complexity |
|----------|-------------|------------------|
| **Railway + Netlify** | **$5** | ✅ Simple |
| Traditional (Railway + Supabase) | $30+ | ❌ Complex |
| AWS/GCP Full Stack | $50+ | ❌ Very Complex |

## 🎯 Perfect For

- **Interior Design Companies** - Showcase your team of designers
- **Freelance Designers** - Get discovered by potential clients
- **Homeowners** - Find the right designer for your project
- **Businesses** - Source designers for office spaces
- **Anyone** - Who needs interior design services

## 📞 Support

Need help? Here's how to get it:

1. **Check the setup guide above** - Most issues are covered there
2. **Look at the error messages** - They usually tell you what's wrong
3. **Try the Docker option** - It's the most reliable way to run the app
4. **Ask for help** - Contact the development team if you're stuck

## 🛠️ Backend API

Frontend communicates with the Flask API (default `http://localhost:5001/api` or override via `VITE_API_BASE_URL`):

- **GET /api/health**: Health check endpoint
- **GET /api/designers**: Retrieve all designer records
- **POST /api/designers/:id/shortlist**
  - Body: `{ "user_session": "<session_id>" }`
  - Toggles shortlist status; responds with `{ "shortlisted": true|false }`
- **POST /api/designers/:id/report**
  - Body: `{ "reason": "<reason>", "description": "<text>", "user_session": "<session_id>" }`
  - Submits a report for a designer

## 🗄️ Database Schema

**Smart database abstraction** - automatically uses SQLite for development and PostgreSQL for production:

### Tables
- **designers**: `id, name, rating, description, projects, experience, price_range, phone1, phone2, location, specialties (JSONB), portfolio (JSONB), created_at, updated_at`
- **shortlists**: `id, designer_id (FK), user_session, created_at, UNIQUE(designer_id, user_session)`
- **reports**: `id, designer_id (FK), reason, description, user_session, created_at`

### Environment Detection
- **Development**: Uses SQLite (`sqlite:///emptycup.db`) - no setup required
- **Production**: Uses PostgreSQL when `DATABASE_URL` is provided by Railway
- **Automatic Migration**: App detects database type and adjusts queries accordingly

---

**Ready to find your perfect interior designer? Get started now!** 🏡✨