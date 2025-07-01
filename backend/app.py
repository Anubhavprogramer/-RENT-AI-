from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global model variable
model = None
feature_columns = ['Distance_to_Downtown', 'Transit_Score', 'Crime_Rate', 'Amenities_Count', 
                  'Family_Type_Encoded', 'People_Count', 'Rooms_Required', 'Has_Children', 
                  'Parking_Required', 'Furnished_Type_Encoded']

def load_and_train_model():
    """Load data and train the model"""
    global model
    
    try:
        # Load the dataset
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'rental_data.csv')
        df = pd.read_csv(data_path)
        
        # Encode categorical variables
        # Family_Type: Bachelor=0, Executive=1, Family=2
        family_type_mapping = {'Bachelor': 0, 'Executive': 1, 'Family': 2}
        df['Family_Type_Encoded'] = df['Family_Type'].map(family_type_mapping)
        
        # Furnished_Type: Unfurnished=0, Semi-Furnished=1, Fully-Furnished=2
        furnished_type_mapping = {'Unfurnished': 0, 'Semi-Furnished': 1, 'Fully-Furnished': 2}
        df['Furnished_Type_Encoded'] = df['Furnished_Type'].map(furnished_type_mapping)
        
        # Prepare features and target
        X = df[feature_columns]
        y = df['Average_Rent']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest model (better performance than simple Linear Regression)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Calculate and print model performance
        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)
        
        train_rmse = np.sqrt(mean_squared_error(y_train, train_predictions))
        test_rmse = np.sqrt(mean_squared_error(y_test, test_predictions))
        test_r2 = r2_score(y_test, test_predictions)
        
        print(f"Model Performance:")
        print(f"Training RMSE: {train_rmse:.2f}")
        print(f"Testing RMSE: {test_rmse:.2f}")
        print(f"Testing R² Score: {test_r2:.3f}")
        
        # Save the model
        model_path = os.path.join(os.path.dirname(__file__), 'rent_predictor.pkl')
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")
        
        return True
        
    except Exception as e:
        print(f"Error loading/training model: {str(e)}")
        return False

def load_model():
    """Load pre-trained model if available"""
    global model
    
    model_path = os.path.join(os.path.dirname(__file__), 'rent_predictor.pkl')
    
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            print("Pre-trained model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading pre-trained model: {str(e)}")
    
    return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict_rent():
    """Predict rent based on input features"""
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.json
        
        # Validate input data
        required_fields = ['distance', 'transit_score', 'crime_rate', 'amenities', 
                          'family_type', 'people_count', 'rooms_required', 'has_children',
                          'parking_required', 'furnished_type']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Encode categorical variables
        family_type_mapping = {'Bachelor': 0, 'Executive': 1, 'Family': 2}
        furnished_type_mapping = {'Unfurnished': 0, 'Semi-Furnished': 1, 'Fully-Furnished': 2}
        
        # Prepare features for prediction
        features = [
            float(data['distance']),
            float(data['transit_score']),
            float(data['crime_rate']),
            float(data['amenities']),
            family_type_mapping.get(data['family_type'], 0),
            int(data['people_count']),
            int(data['rooms_required']),
            int(data['has_children']),
            int(data['parking_required']),
            furnished_type_mapping.get(data['furnished_type'], 0)
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        
        # Calculate confidence interval (using prediction std from Random Forest)
        if hasattr(model, 'estimators_'):
            # For Random Forest, we can get individual tree predictions
            tree_predictions = [tree.predict([features])[0] for tree in model.estimators_]
            prediction_std = np.std(tree_predictions)
            confidence_interval = {
                'lower': max(0, prediction - 1.96 * prediction_std),
                'upper': prediction + 1.96 * prediction_std
            }
        else:
            confidence_interval = None
        
        # Get similar neighborhoods (simple similarity based on features)
        similar_neighborhoods = get_similar_neighborhoods(features)
        
        response = {
            'predicted_rent': round(prediction, 2),
            'confidence_interval': confidence_interval,
            'similar_neighborhoods': similar_neighborhoods,
            'input_features': {
                'distance_to_downtown': features[0],
                'transit_score': features[1],
                'crime_rate': features[2],
                'amenities_count': features[3],
                'family_type': data['family_type'],
                'people_count': features[5],
                'rooms_required': features[6],
                'has_children': bool(features[7]),
                'parking_required': bool(features[8]),
                'furnished_type': data['furnished_type']
            }
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input data: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_similar_neighborhoods(input_features, top_n=3):
    """Find similar neighborhoods based on feature similarity"""
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'rental_data.csv')
        df = pd.read_csv(data_path)
        
        # Encode categorical variables for comparison
        family_type_mapping = {'Bachelor': 0, 'Executive': 1, 'Family': 2}
        furnished_type_mapping = {'Unfurnished': 0, 'Semi-Furnished': 1, 'Fully-Furnished': 2}
        
        df['Family_Type_Encoded'] = df['Family_Type'].map(family_type_mapping)
        df['Furnished_Type_Encoded'] = df['Furnished_Type'].map(furnished_type_mapping)
        
        # Calculate similarity scores (using Euclidean distance)
        similarities = []
        
        for idx, row in df.iterrows():
            neighborhood_features = [
                row['Distance_to_Downtown'],
                row['Transit_Score'],
                row['Crime_Rate'],
                row['Amenities_Count'],
                row['Family_Type_Encoded'],
                row['People_Count'],
                row['Rooms_Required'],
                row['Has_Children'],
                row['Parking_Required'],
                row['Furnished_Type_Encoded']
            ]
            
            # Calculate normalized Euclidean distance with weights for different feature types
            # Give more weight to structural features (rooms, people) and less to location features
            weights = [0.8, 0.6, 0.7, 0.5, 1.5, 1.2, 2.0, 1.0, 0.8, 1.0]  # Rooms and people count get higher weights
            
            weighted_distance = np.sqrt(sum(w * (a - b) ** 2 for w, a, b in zip(weights, input_features, neighborhood_features)))
            
            similarities.append({
                'neighborhood': row['Neighborhood'],
                'distance': weighted_distance,
                'rent': row['Average_Rent'],
                'features': {
                    'distance_to_downtown': row['Distance_to_Downtown'],
                    'transit_score': row['Transit_Score'],
                    'crime_rate': row['Crime_Rate'],
                    'amenities_count': row['Amenities_Count'],
                    'family_type': row['Family_Type'],
                    'people_count': row['People_Count'],
                    'rooms_required': row['Rooms_Required'],
                    'has_children': bool(row['Has_Children']),
                    'parking_required': bool(row['Parking_Required']),
                    'furnished_type': row['Furnished_Type']
                }
            })
        
        # Sort by similarity (lower distance = more similar)
        similarities.sort(key=lambda x: x['distance'])
        
        # Return top N similar neighborhoods
        return similarities[:top_n]
        
    except Exception as e:
        print(f"Error finding similar neighborhoods: {str(e)}")
        return []

@app.route('/neighborhoods', methods=['GET'])
def get_neighborhoods():
    """Get all neighborhoods data"""
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'rental_data.csv')
        df = pd.read_csv(data_path)
        
        neighborhoods = []
        for _, row in df.iterrows():
            neighborhoods.append({
                'name': row['Neighborhood'],
                'distance_to_downtown': row['Distance_to_Downtown'],
                'transit_score': row['Transit_Score'],
                'crime_rate': row['Crime_Rate'],
                'amenities_count': row['Amenities_Count'],
                'family_type': row['Family_Type'],
                'people_count': row['People_Count'],
                'rooms_required': row['Rooms_Required'],
                'has_children': bool(row['Has_Children']),
                'parking_required': bool(row['Parking_Required']),
                'furnished_type': row['Furnished_Type'],
                'average_rent': row['Average_Rent']
            })
        
        return jsonify({'neighborhoods': neighborhoods})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting RentWise API...")
    
    # Try to load existing model first
    if not load_model():
        print("No pre-trained model found. Training new model...")
        if load_and_train_model():
            print("Model trained successfully!")
        else:
            print("Failed to train model. API will not work properly.")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
