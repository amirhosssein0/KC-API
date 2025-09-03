from rest_framework import serializers
from .models import Predict

class PredictSerializer(serializers.ModelSerializer):
    predicted_price = serializers.FloatField(read_only=True, required=False)
    
    class Meta:
        model = Predict
        fields = '__all__'
    
    def validate(self, data):
        """
        Custom validation for house features
        """
        # Validate that sqft_above + sqft_basement <= sqft_living
        if 'sqft_above' in data and 'sqft_basement' in data and 'sqft_living' in data:
            total_area = data['sqft_above'] + data['sqft_basement']
            if total_area > data['sqft_living']:
                raise serializers.ValidationError(
                    "Total area (sqft_above + sqft_basement) cannot exceed sqft_living"
                )
        
        # Validate that bedrooms is reasonable for the house size
        if 'bedrooms' in data and 'sqft_living' in data:
            if data['bedrooms'] > 0 and data['sqft_living'] / data['bedrooms'] < 100:
                raise serializers.ValidationError(
                    "House size per bedroom seems too small"
                )
        
        return data