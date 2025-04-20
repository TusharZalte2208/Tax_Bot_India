"""
TaxBot India - Income Tax Calculator and Advisor
A Streamlit-based application that helps Indian taxpayers 
compare tax regimes and save on taxes.
"""

import streamlit as st
import io
from datetime import date
from tax_calculator import (
    calculate_old_regime_tax,
    calculate_new_regime_tax,
    get_tax_saving_tips,
    get_better_regime
)
from pdf_generator import generate_tax_report
from tax_predictor import TaxRegimePredictor

# Page configuration
st.set_page_config(
    page_title="TaxBot India",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="🧾"
)

# Initialize the ML predictor
ml_predictor = TaxRegimePredictor()

# App title and description
st.title("🧾 TaxBot India")
st.subheader("Save Smarter, Grow Faster")

# Initialize session state for tab control if not already set
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0  # Default to first tab

# Navigation tabs
tab1, tab2 = st.tabs(["💰 Tax Calculator", "🤖 AI Tax Advisor"])

# Auto-select the active tab based on session state
if st.session_state.active_tab == 1:
    tab2.active = True

# Tab 1: Traditional Tax Calculator
with tab1:
    st.markdown("""
    This tool helps you calculate your income tax under both the old and new tax regimes, 
    compare them, and get personalized tax-saving recommendations.
    """)
    
    # Create two columns for the form
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Income Details")
        income = st.number_input("💰 Annual Income (in ₹)", min_value=0, value=0, step=10000, format="%d", key="income_tab1")
        investments = st.number_input("📦 80C Investments (in ₹)", min_value=0, value=0, step=5000, format="%d", 
                                help="PPF, ELSS, NSC, Tax Saving FD, LIC, etc. (Max: ₹1,50,000)", key="investments_tab1")
        health_insurance = st.number_input("🏥 Health Insurance Premium (₹)", min_value=0, value=0, step=1000, format="%d",
                                    help="Section 80D (Max: ₹25,000 for self & family)", key="health_insurance_tab1")

    with col2:
        st.markdown("### Deductions")
        home_loan = st.number_input("🏠 Home Loan Interest (₹)", min_value=0, value=0, step=10000, format="%d",
                                help="Section 24b (Max: ₹2,00,000)", key="home_loan_tab1")
        edu_loan = st.number_input("🎓 Education Loan Interest (₹)", min_value=0, value=0, step=5000, format="%d",
                            help="Section 80E (No upper limit)", key="edu_loan_tab1")
        hra = st.number_input("🏙️ HRA Exemption (₹)", min_value=0, value=0, step=10000, format="%d",
                        help="House Rent Allowance Exemption", key="hra_tab1")

# Tab 2: AI Tax Advisor
with tab2:
    st.markdown("""
    ## 🤖 AI Tax Regime Advisor
    
    Our machine learning model can predict which tax regime is likely to be better for you 
    based on your financial profile and historical tax data patterns.
    """)
    
    st.info("📊 This AI model has been trained on typical Indian taxpayer profiles and can help provide a prediction even without detailed tax calculations.")
    
    # Input fields for the ML model
    st.markdown("### Enter Your Information")
    
    col1_ml, col2_ml = st.columns(2)
    
    with col1_ml:
        income_ml = st.number_input("💰 Annual Income (in ₹)", min_value=300000, value=500000, step=50000, format="%d", key="income_ml")
        investments_ml = st.number_input("📦 80C Investments (in ₹)", min_value=0, value=50000, step=10000, format="%d", 
                                    max_value=150000, help="Max: ₹1,50,000", key="investments_ml")
        health_insurance_ml = st.number_input("🏥 Health Insurance Premium (₹)", min_value=0, value=10000, step=5000, format="%d",
                                        help="Section 80D", key="health_insurance_ml")
    
    with col2_ml:
        hra_ml = st.number_input("🏙️ HRA Exemption (₹)", min_value=0, value=0, step=10000, format="%d", key="hra_ml")
        home_loan_ml = st.number_input("🏠 Home Loan Interest (₹)", min_value=0, value=0, step=20000, format="%d", key="home_loan_ml")
        edu_loan_ml = st.number_input("🎓 Education Loan Interest (₹)", min_value=0, value=0, step=10000, format="%d", key="edu_loan_ml")
        age_ml = st.number_input("🧓 Your Age", min_value=18, max_value=100, value=30, step=1, key="age_ml")

# Add AI Advisor button
with tab1:
    st.markdown("### Try Our AI Tax Advisor")
    if st.button("🤖 Switch to AI Tax Advisor", key="switch_to_ai_btn"):
        st.session_state.active_tab = 1  # Switch to second tab
        st.rerun()

# Tab 1: Calculate button
with tab1:
    if st.button("📊 Calculate Tax", type="primary", key="calc_btn_tab1"):
        # Calculate total deductions
        total_deductions = investments + health_insurance + home_loan + edu_loan + hra
        
        # Calculate taxable income under both regimes
        old_regime_taxable = max(0, income - total_deductions)
        new_regime_taxable = income  # No deductions in new regime
        
        # Calculate taxes
        old_regime_tax = calculate_old_regime_tax(old_regime_taxable)
        new_regime_tax = calculate_new_regime_tax(income)
        
        # Determine better regime
        better_regime = get_better_regime(old_regime_tax, new_regime_tax)
        
        # Get tax saving tips
        tips = get_tax_saving_tips(income, investments, health_insurance, home_loan, edu_loan)
        
        # Display results
        st.markdown("---")
        st.markdown("### 🔍 Tax Regime Comparison")
        
        # Create two columns for tax comparison
        left_col, right_col = st.columns(2)
        
        with left_col:
            st.markdown("**Old Tax Regime**")
            st.markdown(f"Taxable Income: ₹{old_regime_taxable:,}")
            st.markdown(f"Base Tax: ₹{old_regime_tax['base_tax']:,.2f}")
            st.markdown(f"Cess (4%): ₹{old_regime_tax['cess']:,.2f}")
            st.markdown(f"**Total Tax: ₹{old_regime_tax['total_tax']:,.2f}**")
        
        with right_col:
            st.markdown("**New Tax Regime**")
            st.markdown(f"Taxable Income: ₹{new_regime_taxable:,}")
            st.markdown(f"Base Tax: ₹{new_regime_tax['base_tax']:,.2f}")
            st.markdown(f"Cess (4%): ₹{new_regime_tax['cess']:,.2f}")
            st.markdown(f"**Total Tax: ₹{new_regime_tax['total_tax']:,.2f}**")
        
        # Recommendation box
        st.markdown("---")
        st.markdown("### 🎯 Recommendation")
        
        if better_regime["regime"] == "Old Regime":
            color = "green"
        else:
            color = "blue"
        
        st.markdown(f"""
        <div style='background-color:{color}33; padding:10px; border-radius:5px;'>
            <h4 style='color:{color};'>💡 {better_regime["regime"]} is better for you!</h4>
            <p>You will save approximately <b>₹{better_regime["savings"]:,.2f}</b> by choosing this regime.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tax saving tips
        st.markdown("---")
        st.markdown("### ✅ Tax Saving Tips")
        
        for tip in tips:
            st.markdown(f"🟢 {tip}")
        
        # Prepare data for PDF generator
        user_data = {
            "income": income,
            "investments": investments,
            "health_insurance": health_insurance,
            "home_loan": home_loan,
            "edu_loan": edu_loan,
            "hra": hra,
            "total_deductions": total_deductions,
            "old_regime_taxable": old_regime_taxable,
            "new_regime_taxable": new_regime_taxable
        }
        
        # Generate PDF
        pdf_bytes = generate_tax_report(user_data, old_regime_tax, new_regime_tax, better_regime, tips)
        
        # Provide download button for PDF
        st.download_button(
            label="📄 Download Tax Report PDF",
            data=pdf_bytes,
            file_name=f"TaxBot_Report_{date.today().strftime('%d-%m-%Y')}.pdf",
            mime="application/pdf"
        )

# Tab 2: AI Prediction Button
with tab2:
    if st.button("🤖 Predict Best Regime", type="primary", key="predict_btn_tab2"):
        # Use the ML model to predict
        prediction = ml_predictor.predict_regime(
            income_ml, 
            investments_ml, 
            health_insurance_ml,
            hra_ml,
            home_loan_ml,
            edu_loan_ml,
            age_ml
        )
        
        # Show prediction with balloons for fun effect
        st.balloons()
        
        # Display the result
        if prediction["regime"] == "Old Regime":
            result_color = "green"
        else:
            result_color = "blue"
        
        st.markdown(f"""
        <div style='background-color:{result_color}33; padding:15px; border-radius:10px; margin-top:20px;'>
            <h3 style='color:{result_color};'>🎯 AI Prediction: {prediction["regime"]}</h3>
            <p>Our AI model predicts that the <b>{prediction["regime"]}</b> is better for you.</p>
            <p>Confidence Level: {prediction["confidence"]:.1f}%</p>
            <p><i>{prediction["explanation"]}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional information about the prediction
        st.markdown("### 🔍 Understanding the Prediction")
        st.markdown("""
        The AI model has analyzed your inputs and compared them with patterns from thousands of 
        taxpayer profiles to determine which regime is likely to be more beneficial for you.
        
        Factors that influenced this prediction:
        - Your total income level
        - The ratio of deductions to income
        - Specific deduction types (80C, health insurance, etc.)
        - Age-based factors
        
        Remember that this is a prediction based on common patterns. For the most accurate tax 
        assessment, use the detailed Tax Calculator in the first tab.
        """)
        
        # Calculate traditional tax for PDF report
        total_deductions_ml = investments_ml + health_insurance_ml + home_loan_ml + edu_loan_ml + hra_ml
        old_regime_taxable_ml = max(0, income_ml - total_deductions_ml)
        new_regime_taxable_ml = income_ml
        
        old_regime_tax_ml = calculate_old_regime_tax(old_regime_taxable_ml)
        new_regime_tax_ml = calculate_new_regime_tax(income_ml)
        
        better_regime_ml = get_better_regime(old_regime_tax_ml, new_regime_tax_ml)
        
        tips_ml = get_tax_saving_tips(income_ml, investments_ml, health_insurance_ml, home_loan_ml, edu_loan_ml)
        
        # Prepare data for PDF generator
        user_data_ml = {
            "income": income_ml,
            "investments": investments_ml,
            "health_insurance": health_insurance_ml,
            "home_loan": home_loan_ml,
            "edu_loan": edu_loan_ml,
            "hra": hra_ml,
            "total_deductions": total_deductions_ml,
            "old_regime_taxable": old_regime_taxable_ml,
            "new_regime_taxable": new_regime_taxable_ml
        }
        
        # Generate PDF with AI prediction included
        pdf_bytes_ml = generate_tax_report(
            user_data_ml, 
            old_regime_tax_ml, 
            new_regime_tax_ml, 
            better_regime_ml, 
            tips_ml, 
            prediction
        )
        
        # Provide download button for PDF
        st.download_button(
            label="📄 Download AI Tax Report PDF",
            data=pdf_bytes_ml,
            file_name=f"TaxBot_AI_Report_{date.today().strftime('%d-%m-%Y')}.pdf",
            mime="application/pdf",
            help="Download a comprehensive tax report that includes both traditional calculations and AI predictions"
        )
        
        # Comparison button to switch to the tax calculator with pre-filled values
        st.markdown("### 🔄 Want a detailed calculation?")
        if st.button("Switch to Tax Calculator with these values", key="switch_to_calc"):
            # Set session state to transfer values and switch tabs
            st.session_state.active_tab = 0  # Switch to first tab
            st.session_state.income_tab1 = income_ml
            st.session_state.investments_tab1 = investments_ml
            st.session_state.health_insurance_tab1 = health_insurance_ml
            st.session_state.hra_tab1 = hra_ml
            st.session_state.home_loan_tab1 = home_loan_ml
            st.session_state.edu_loan_tab1 = edu_loan_ml
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
    <p style='font-size: small;'>
        <b>TaxBot India</b> • Calculate, Compare, Save<br>
        <i>This tool is for informational purposes only. Always consult a tax professional for specific advice.</i>
    </p>
</div>
""", unsafe_allow_html=True)
