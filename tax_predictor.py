"""
ML-based Tax Regime Predictor Module for TaxBot India
Uses a Decision Tree model to predict the best tax regime based on user data.
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

class TaxRegimePredictor:
    """
    ML model for predicting the best tax regime (Old vs New) for a taxpayer
    based on their income and deduction details.
    """
    
    def __init__(self):
        """Initialize the model and training data"""
        # Create sample training data
        self.training_data = self._generate_training_data()
        self.model = self._train_model()
        
    def _generate_training_data(self):
        """
        Generate realistic training data based on Indian income tax patterns.
        This could be replaced with data from a CSV file or database.
        """
        # Create a dataset with 100 samples
        np.random.seed(42)  # For reproducibility
        
        # Generate random income values between 3L and 25L
        income = np.random.randint(300000, 2500000, 100)
        
        # Generate deduction values (with some correlation to income)
        ded_80c = np.clip(income * np.random.uniform(0.05, 0.15, 100), 0, 150000)
        ded_80d = np.random.randint(0, 50000, 100)
        hra = np.random.randint(0, 200000, 100)
        home_loan = np.random.randint(0, 300000, 100)
        edu_loan = np.random.randint(0, 100000, 100)
        
        # Calculate total deductions
        total_deductions = ded_80c + ded_80d + hra + home_loan + edu_loan
        
        # Age (affects tax brackets)
        age = np.random.randint(22, 70, 100)
        
        # Generate labels based on logical rules that simulate real tax benefits
        # Old regime is better when deductions are high relative to income
        deduction_income_ratio = total_deductions / income
        
        # Create a label based on this ratio - higher ratio means old regime is better
        # This is a simplification; real tax calculation would be more complex
        labels = np.where(deduction_income_ratio > 0.12, 1, 0)  # 1 for Old regime, 0 for New regime
        
        # Create DataFrame
        df = pd.DataFrame({
            'Income': income,
            '80C_Investments': ded_80c,
            'Health_Insurance': ded_80d,
            'HRA': hra,
            'Home_Loan': home_loan,
            'Edu_Loan': edu_loan,
            'Age': age,
            'Total_Deductions': total_deductions,
            'Best_Regime': labels  # 1 for Old, 0 for New
        })
        
        return df
    
    def _train_model(self):
        """Train a Decision Tree model on the training data."""
        X = self.training_data[['Income', '80C_Investments', 'Health_Insurance', 
                                'HRA', 'Home_Loan', 'Edu_Loan', 'Age', 'Total_Deductions']]
        y = self.training_data['Best_Regime']
        
        # Create and train model
        model = DecisionTreeClassifier(max_depth=5)
        model.fit(X, y)
        
        return model
    
    def predict_regime(self, income, investments_80c, health_insurance, 
                       hra, home_loan, edu_loan, age=30):
        """
        Predict the best tax regime based on user inputs.
        
        Args:
            income: Annual income
            investments_80c: 80C investments
            health_insurance: Health insurance premium
            hra: HRA exemption
            home_loan: Home loan interest
            edu_loan: Education loan interest
            age: Age of taxpayer (default 30)
            
        Returns:
            Dictionary with prediction results
        """
        # Calculate total deductions
        total_deductions = investments_80c + health_insurance + hra + home_loan + edu_loan
        
        # Format input for prediction
        input_data = np.array([[
            income, 
            investments_80c, 
            health_insurance, 
            hra,
            home_loan,
            edu_loan,
            age,
            total_deductions
        ]])
        
        # Make prediction
        prediction = self.model.predict(input_data)[0]
        probability = self.model.predict_proba(input_data)[0]
        
        # Determine regime and confidence
        regime = "Old Regime" if prediction == 1 else "New Regime"
        confidence = probability[prediction] * 100
        
        # Create explanation based on features
        if prediction == 1:  # Old Regime
            if total_deductions > 150000:
                explanation = "Your high deduction amount makes the Old Regime more beneficial."
            else:
                explanation = "Based on your profile, the Old Regime provides better tax benefits."
        else:  # New Regime
            if total_deductions < 50000:
                explanation = "With low deductions, the New Regime's reduced tax rates are more beneficial."
            else:
                explanation = "Based on your overall profile, the New Regime appears to be more advantageous."
        
        return {
            "regime": regime,
            "confidence": confidence,
            "explanation": explanation
        }