from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Predict
from .serializers import PredictSerializer
import joblib
import os
import pandas as pd
import numpy as np


class PredictView(APIView):
    
    def post(self, request):
        """
        POST endpoint for house price prediction
        """
        try:
            # Validate input data
            serializer = PredictSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'error': 'Invalid input data',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get validated data
            house_data = serializer.validated_data
            
            # Load the trained model
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'best_model.pkl')
            
            if not os.path.exists(model_path):
                return Response({
                    'error': 'Machine learning model not found'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Load the model
            model = joblib.load(model_path)
            
            # Prepare features for prediction (exclude non-feature fields)
            feature_fields = [
                'bedrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront',
                'yr_built', 'sqft_above', 'sqft_basement', 'grade', 'view',
                'condition', 'house_renovated', 'long', 'lat'
            ]
            
            # Create feature array for prediction
            features = []
            for field in feature_fields:
                features.append(house_data[field])
            
            # Convert to numpy array and reshape for prediction
            features_array = np.array(features).reshape(1, -1)
            
            # Make prediction
            predicted_price = model.predict(features_array)[0]
            
            # Save prediction to database
            prediction_instance = serializer.save()
            
            # Return prediction result
            return Response({
                'message': 'Price prediction successful',
                'predicted_price': float(predicted_price),
                'house_features': serializer.data,
                'prediction_id': prediction_instance.id,
                'created_at': prediction_instance.created_at
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': 'Prediction failed',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """
        GET endpoint to retrieve all predictions
        """
        try:
            predictions = Predict.objects.all()
            serializer = PredictSerializer(predictions, many=True)
            
            return Response({
                'message': 'Predictions retrieved successfully',
                'count': len(predictions),
                'predictions': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Failed to retrieve predictions',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)