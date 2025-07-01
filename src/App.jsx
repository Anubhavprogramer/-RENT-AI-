import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Home, MapPin, Train, Shield, Store, DollarSign, TrendingUp, AlertCircle } from 'lucide-react';

const API_BASE_URL = 'http://localhost:5001';

function App() {
  const [formData, setFormData] = useState({
    distance: 5,
    transit_score: 70,
    crime_rate: 5,
    amenities: 25
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [neighborhoods, setNeighborhoods] = useState([]);

  useEffect(() => {
    fetchNeighborhoods();
  }, []);

  const fetchNeighborhoods = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/neighborhoods`);
      setNeighborhoods(response.data.neighborhoods || []);
    } catch (err) {
      console.log('Could not fetch neighborhoods:', err.message);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, formData);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to predict rent. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="container">
      {/* Header */}
      <div className="header">
        <div className="header-title">
          <Home className="icon-large" />
          <h1>RentWise</h1>
        </div>
        <p className="header-subtitle">
          AI-powered rent prediction for Indian metros • Find the perfect home within your budget
        </p>
      </div>

      <div className="main-grid">
        {/* Input Form */}
        <div className="card">
          <h2 className="card-title">Property Details</h2>
          
          <form onSubmit={handleSubmit}>
            {/* Distance to City Center */}
            <div className="form-group">
              <label className="form-label">
                <MapPin className="icon" />
                Distance to City Center (km)
              </label>
              <input
                type="range"
                name="distance"
                min="0"
                max="45"
                step="0.1"
                value={formData.distance}
                onChange={handleInputChange}
                className="slider"
              />
              <div className="slider-labels">
                <span>0 km</span>
                <span className="slider-value">{formData.distance} km</span>
                <span>45 km</span>
              </div>
            </div>

            {/* Metro/Transport Connectivity */}
            <div className="form-group">
              <label className="form-label">
                <Train className="icon" />
                Metro/Transport Connectivity Score
              </label>
              <input
                type="range"
                name="transit_score"
                min="0"
                max="100"
                value={formData.transit_score}
                onChange={handleInputChange}
                className="slider"
              />
              <div className="slider-labels">
                <span>Poor (0)</span>
                <span className="slider-value">{formData.transit_score}/100</span>
                <span>Excellent (100)</span>
              </div>
            </div>

            {/* Safety Rating */}
            <div className="form-group">
              <label className="form-label">
                <Shield className="icon" />
                Safety Rating (1-10, higher is safer)
              </label>
              <input
                type="range"
                name="crime_rate"
                min="1"
                max="10"
                step="0.1"
                value={11 - formData.crime_rate}
                onChange={(e) => setFormData(prev => ({...prev, crime_rate: 11 - parseFloat(e.target.value)}))}
                className="slider"
              />
              <div className="slider-labels">
                <span>Unsafe (1)</span>
                <span className="slider-value">{(11 - formData.crime_rate).toFixed(1)}/10</span>
                <span>Very Safe (10)</span>
              </div>
            </div>

            {/* Amenities (Restaurants, ATMs, Hospitals, etc.) */}
            <div className="form-group">
              <label className="form-label">
                <Store className="icon" />
                Local Amenities (Restaurants, ATMs, Hospitals)
              </label>
              <input
                type="range"
                name="amenities"
                min="0"
                max="70"
                value={formData.amenities}
                onChange={handleInputChange}
                className="slider"
              />
              <div className="slider-labels">
                <span>Few (0)</span>
                <span className="slider-value">{formData.amenities}</span>
                <span>Many (70)</span>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary"
            >
              {loading ? (
                <div className="spinner"></div>
              ) : (
                <DollarSign className="icon" />
              )}
              {loading ? 'Predicting...' : 'Predict Rent'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="results-column">
          {error && (
            <div className="alert-error">
              <div className="alert-content">
                <AlertCircle className="icon" />
                <p>{error}</p>
              </div>
            </div>
          )}

          {prediction && (
            <>
              {/* Main Prediction */}
              <div className="card prediction-card">
                <h3 className="card-title">
                  <TrendingUp className="icon" style={{ display: 'inline', marginRight: '0.5rem' }} />
                  Rent Prediction
                </h3>
                <div className="prediction-amount">
                  {formatCurrency(prediction.predicted_rent)}
                </div>
                <p className="prediction-label">Estimated monthly rent (including maintenance)</p>
                
                {prediction.confidence_interval && (
                  <div className="confidence-range">
                    <p className="confidence-label">95% Confidence Range:</p>
                    <p className="confidence-value">
                      {formatCurrency(prediction.confidence_interval.lower)} - {formatCurrency(prediction.confidence_interval.upper)}
                    </p>
                  </div>
                )}
              </div>

              {/* Similar Neighborhoods */}
              {prediction.similar_neighborhoods && prediction.similar_neighborhoods.length > 0 && (
                <div className="card similar-neighborhoods">
                  <h3 className="card-title">Similar Neighborhoods</h3>
                  <div className="neighborhood-list">
                    {prediction.similar_neighborhoods.map((neighborhood, index) => (
                      <div key={index} className="neighborhood-card">
                        <div className="neighborhood-header">
                          <h4 className="neighborhood-name">{neighborhood.neighborhood}</h4>
                          <span className="neighborhood-rent">
                            {formatCurrency(neighborhood.rent)}
                          </span>
                        </div>
                        <div className="neighborhood-features">
                          <div>📍 {neighborhood.features.distance_to_downtown}km from center</div>
                          <div>🚇 Metro: {neighborhood.features.transit_score}/100</div>
                          <div>🛡️ Safety: {(11 - neighborhood.features.crime_rate).toFixed(1)}/10</div>
                          <div>🏪 Amenities: {neighborhood.features.amenities_count}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          {/* Sample Neighborhoods */}
          {neighborhoods.length > 0 && (
            <div className="card sample-neighborhoods">
              <h3 className="card-title">Sample Neighborhoods</h3>
              <div className="neighborhood-list">
                {neighborhoods.slice(0, 5).map((neighborhood, index) => (
                  <div key={index} className="neighborhood-card">
                    <div className="neighborhood-info">
                      <h4>{neighborhood.name}</h4>
                      <p>
                        {neighborhood.distance_to_downtown}km • Metro: {neighborhood.transit_score}/100
                      </p>
                    </div>
                    <span className="neighborhood-rent">
                      {formatCurrency(neighborhood.average_rent)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="footer">
        <p>Built with ❤️ for Indian renters • Covering Delhi NCR, Mumbai, Bangalore & more</p>
      </div>
    </div>
  );
}

export default App
