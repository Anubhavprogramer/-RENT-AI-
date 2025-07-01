# RentWise Development Guide - India Edition

## 🚀 Quick Start

### Option 1: Individual Setup (Recommended)

1. **Install Python Dependencies**:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

2. **Start Backend Server** (Terminal 1):
   ```bash
   cd backend
   source venv/bin/activate
   python app.py
   ```
   Backend runs on: http://localhost:5001

3. **Start Frontend Server** (Terminal 2):
   ```bash
   npm run dev
   ```
   Frontend runs on: http://localhost:5173 (or next available port)

## 🇮🇳 India-Specific Testing

### Test with Indian Localities
```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "distance": 15,
    "transit_score": 65,
    "crime_rate": 5.8,
    "amenities": 30
  }'
```

Expected response in INR:
```json
{
  "predicted_rent": 28500.75,
  "confidence_interval": {
    "lower": 22100.50,
    "upper": 34900.00
  }
}
```

### Sample Indian Neighborhoods Data
- **Connaught Place**: ₹85,000/month (Premium central location)
- **Karol Bagh**: ₹45,000/month (Good connectivity, mid-range)
- **Dwarka**: ₹28,000/month (Suburban, metro connected)
- **Rohini**: ₹25,000/month (North Delhi, affordable)

## 🏙️ Indian Metro Context

### Delhi NCR Features
- Distance measured from city center (Connaught Place/CP)
- Metro connectivity crucial for commuting
- Safety ratings important for family housing
- Local amenities include restaurants, ATMs, hospitals

### Pricing Insights
- **Central locations**: ₹50,000-₹85,000/month
- **Well-connected suburbs**: ₹25,000-₹45,000/month  
- **Outer areas**: ₹15,000-₹30,000/month
- **NCR satellites**: ₹18,000-₹35,000/month

## ✅ Project Status - India Ready
- ✅ Backend API running on port 5001 (INR predictions)
- ✅ Frontend running on port 5173 (Indian context)
- ✅ ML model trained on Indian neighborhood data
- ✅ Currency formatting in Indian Rupees
- ✅ India-specific features and terminology
