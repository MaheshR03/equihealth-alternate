"""
Simple health prediction model as fallback
This provides basic predictions when the main ML model fails to load
"""

import pandas as pd
import numpy as np

def calculate_health_score(row):
    """
    Calculate a simple health score based on available indicators
    Returns a score from 0-4 (0 = best health, 4 = worst health)
    """
    try:
        # Normalize indicators (higher values = worse health for most)
        score = 0
        
        # Disease indicators (higher = worse)
        if 'TB Incidence' in row:
            score += min(row['TB Incidence'] / 100, 1) * 0.8
        if 'Diabetes Prevalence' in row:
            score += min(row['Diabetes Prevalence'] / 15, 1) * 0.7
        if 'Malaria Incidence' in row:
            score += min(row['Malaria Incidence'] / 50, 1) * 0.6
        if 'HIV/AIDS Prevalence' in row:
            score += min(row['HIV/AIDS Prevalence'] / 5, 1) * 0.9
        if 'IMR' in row:
            score += min(row['IMR'] / 50, 1) * 1.0
            
        # Positive indicators (higher = better health, so subtract)
        if 'Vaccination Rate' in row:
            score -= min(row['Vaccination Rate'] / 100, 1) * 0.8
        if 'Income Level' in row:
            score -= min(row['Income Level'] / 100000, 1) * 0.5
        if 'Employment Rate' in row:
            score -= min(row['Employment Rate'] / 100, 1) * 0.4
        if 'Education Level' in row:
            score -= min(row['Education Level'] / 100, 1) * 0.3
            
        # Environmental factors
        if 'AQI' in row:
            score += min(row['AQI'] / 300, 1) * 0.5
            
        # Convert to 0-4 scale
        score = max(0, min(score, 1))  # Clamp between 0 and 1
        return int(score * 4)
        
    except Exception as e:
        print(f"Error in health score calculation: {e}")
        return np.random.randint(0, 5)

def simple_prediction(data):
    """
    Generate predictions using simple rule-based approach
    """
    try:
        predictions = []
        for _, row in data.iterrows():
            score = calculate_health_score(row)
            predictions.append(score)
        return predictions
    except Exception as e:
        print(f"Error in simple prediction: {e}")
        # Fallback to random
        return [np.random.randint(0, 5) for _ in range(len(data))]
