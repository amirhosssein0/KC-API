from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Predict(models.Model):
    bedrooms = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(15)]
    )
    sqft_living = models.IntegerField(
        validators=[MinValueValidator(300), MaxValueValidator(15000)]
    )
    sqft_lot = models.IntegerField(
        validators=[MinValueValidator(500), MaxValueValidator(2000000)]
    )
    floors = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(3.5)]
    )
    waterfront = models.IntegerField(
        choices=[(0, 'No'), (1, 'Yes')],
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    yr_built = models.IntegerField(
        validators=[MinValueValidator(1934), MaxValueValidator(2014)]
    )
    sqft_above = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(15000)]
    )
    sqft_basement = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )
    grade = models.IntegerField(
        choices=[(i, f"Grade {i}") for i in range(1, 14)],
        validators=[MinValueValidator(1), MaxValueValidator(13)]
    )
    view = models.IntegerField(
        choices=[(i, f"View {i}") for i in range(0, 5)],
        validators=[MinValueValidator(0), MaxValueValidator(4)]
    )
    condition = models.IntegerField(
        choices=[(i, f"Condition {i}") for i in range(1, 6)],
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    house_renovated = models.IntegerField(
        choices=[(0, 'No'), (1, 'Yes')],
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    long = models.FloatField(
        validators=[MinValueValidator(-122.5), MaxValueValidator(-121.3)]
    )
    lat = models.FloatField(
        validators=[MinValueValidator(47.1), MaxValueValidator(47.8)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "House Prediction"
        verbose_name_plural = "House Predictions"
        ordering = ['-created_at']

    def __str__(self):
        return f"Prediction for {self.bedrooms}BR, {self.sqft_living}sqft - ${self.predicted_price or 'TBD'}"
