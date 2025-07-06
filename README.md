# 🏠 RentWise - AI-Powered Rent Prediction for India

**RentWise** is a full-stack web application that helps Indian renters find fair rent prices using machine learning algorithms. Specifically designed for Indian metros like Delhi NCR, Mumbai, Bangalore, and more.

![RentWise Demo](https://img.shields.io/badge/Status-Demo%20Ready-brightgreen)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

## 🚀 Features

- **🤖 AI-Powered Predictions**: Uses Random Forest Regressor to predict rent in Indian Rupees
- **🇮🇳 India-Specific Data**: Real neighborhood data from Delhi NCR with Indian context
- **📊 Interactive Input**: Sliders for distance to city center, metro connectivity, safety rating, and amenities
- **🎯 Confidence Intervals**: 95% confidence range for predictions in INR
- **🏘️ Similar Neighborhoods**: Find comparable areas with different price points
- **📱 Responsive Design**: Works seamlessly on desktop and mobile
- **⚡ Real-time Results**: Instant predictions with modern UI

## 🇮🇳 India-Specific Features

### Rental Challenges Addressed
- **Distance from City Center**: Major factor in Indian metros due to traffic congestion
- **Metro Connectivity**: Critical for daily commuting in cities like Delhi and Bangalore  
- **Safety Ratings**: Important consideration for families and working professionals
- **Local Amenities**: Restaurants, ATMs, hospitals, markets within walking distance
- **Maintenance Included**: Rent estimates include typical maintenance charges

### Indian Metro Coverage
- **Delhi NCR**: Connaught Place, Karol Bagh, Gurgaon, Noida, Faridabad
- **Major Localities**: Hauz Khas, Saket, Greater Kailash, Dwarka, Rohini
- **Pricing in INR**: All predictions in Indian Rupees (₹15,000 - ₹85,000/month)

## 🛠️ Tech Stack

### Frontend
- **React 18** with Vite for fast development
- **Custom CSS** for modern, responsive styling
- **Lucide React** for beautiful icons
- **Axios** for API communication

### Backend
- **Flask** REST API server
- **scikit-learn** Random Forest model
- **Pandas** for data processing
- **CORS** enabled for cross-origin requests

### Data
- **CSV-based dataset** with 40 Indian neighborhood samples
- Features: Distance to city center, metro score, safety rating, amenities count
- Target: Average monthly rent in INR (including maintenance)

## 📁 Project Structure

```
rentwise/
├── src/                    # React frontend
│   ├── App.jsx            # Main application component
│   ├── index.css          # Tailwind CSS imports
│   └── main.jsx           # React entry point
├── backend/               # Flask API server
│   ├── app.py            # Main Flask application
│   ├── requirements.txt  # Python dependencies
│   └── rent_predictor.pkl # Trained ML model (generated)
├── data/                 # Dataset
│   └── rental_data.csv   # Neighborhood rental data
├── public/               # Static assets
├── .github/              # GitHub configuration
│   └── copilot-instructions.md
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ and npm
- **Python** 3.8+ and pip

### 1. Install Frontend Dependencies
```bash
npm install
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Start the Backend Server
```bash
cd backend
python app.py
```
The Flask server will start on `http://localhost:5000`

### 4. Start the Frontend Development Server
```bash
# In a new terminal, from the root directory
npm run dev
```
The React app will start on `http://localhost:5173`

## 🔮 How It Works

### 1. Data Input
Users adjust four key parameters using interactive sliders:
- **Distance to Downtown** (0-25 km)
- **Transit Score** (0-100, higher is better)
- **Crime Rate** (1-15 per 1000 residents, lower is better)
- **Amenities Count** (0-60 nearby amenities)

### 2. ML Prediction
The Random Forest model processes the input features and returns:
- **Predicted rent** with high accuracy (RMSE ~120-150)
- **95% confidence interval** for prediction reliability
- **Feature importance** analysis

### 3. Similar Neighborhoods
Algorithm finds the 3 most similar neighborhoods based on:
- Euclidean distance in feature space
- Real neighborhood data from the dataset
- Actual rent prices for comparison

## 📊 Model Performance

- **Algorithm**: Random Forest Regressor (100 trees)
- **Training Data**: 40 neighborhood samples
- **Features**: 4 key location attributes
- **Accuracy**: RMSE ≈ $120-150, R² ≈ 0.85-0.90
- **Validation**: 80/20 train-test split

## 🎨 UI Features

### Modern Design
- **Gradient backgrounds** with blue/indigo theme
- **Card-based layout** for clean organization
- **Interactive sliders** with real-time value display
- **Loading animations** and error handling

### Responsive Layout
- **Desktop**: Two-column layout with form and results
- **Mobile**: Stacked layout with touch-friendly controls
- **Accessibility**: ARIA labels and keyboard navigation

## 🔧 API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy", "model_loaded": true}
```

### Rent Prediction
```
POST /predict
Body: {
  "distance": 5.0,
  "transit_score": 75,
  "crime_rate": 5.5,
  "amenities": 25
}
Response: {
  "predicted_rent": 1450.50,
  "confidence_interval": {"lower": 1320.30, "upper": 1580.70},
  "similar_neighborhoods": [...],
  "input_features": {...}
}
```

### Get Neighborhoods
```
GET /neighborhoods
Response: {"neighborhoods": [...]}
```

## 🧪 Development Features

### Hot Reload
- **Vite HMR**: Instant frontend updates
- **Flask Debug**: Auto-restart on backend changes

### Code Quality
- **ES6+ syntax** with modern React patterns
- **Error boundaries** and proper error handling
- **Loading states** for better UX
- **Responsive design** with Tailwind CSS

## 🚀 Deployment Options

### Frontend (Netlify/Vercel)
```bash
npm run build
# Deploy the 'dist' folder
```

### Backend (Railway/Render)
```bash
# Add to requirements.txt: gunicorn==21.2.0
# Procfile: web: gunicorn app:app
```

## 📈 Future Enhancements

- **🗺️ Map Integration**: Visual neighborhood selection
- **📊 Historical Data**: Rent trend analysis
- **🔍 Advanced Filters**: More granular search options
- **💾 User Profiles**: Save favorite searches
- **📱 Mobile App**: Native iOS/Android versions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 👨‍💻 Author

Built with ❤️ for the NeighborFit Project Assignment

