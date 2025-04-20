"""
Indian Income Tax Calculator Module
Calculates tax liability under both old and new tax regimes
"""

def calculate_old_regime_tax(income_after_deductions):
    """
    Calculate tax under the old regime
    
    Args:
        income_after_deductions: Taxable income after all deductions
        
    Returns:
        Tax amount, cess amount, and total tax liability
    """
    tax = 0
    
    # Income Tax Slabs for Old Regime (FY 2023-24)
    if income_after_deductions <= 250000:
        tax = 0
    elif income_after_deductions <= 500000:
        tax = (income_after_deductions - 250000) * 0.05
    elif income_after_deductions <= 1000000:
        tax = 12500 + (income_after_deductions - 500000) * 0.2
    else:
        tax = 112500 + (income_after_deductions - 1000000) * 0.3
    
    # Education and Health Cess (4%)
    cess = tax * 0.04
    
    total_tax = tax + cess
    
    return {
        "base_tax": tax,
        "cess": cess,
        "total_tax": total_tax
    }

def calculate_new_regime_tax(income):
    """
    Calculate tax under the new regime
    
    Args:
        income: Total income (no deductions allowed)
        
    Returns:
        Tax amount, cess amount, and total tax liability
    """
    tax = 0
    
    # Income Tax Slabs for New Regime (FY 2023-24)
    if income <= 300000:
        tax = 0
    elif income <= 600000:
        tax = (income - 300000) * 0.05
    elif income <= 900000:
        tax = 15000 + (income - 600000) * 0.1
    elif income <= 1200000:
        tax = 45000 + (income - 900000) * 0.15
    elif income <= 1500000:
        tax = 90000 + (income - 1200000) * 0.2
    else:
        tax = 150000 + (income - 1500000) * 0.3
    
    # Education and Health Cess (4%)
    cess = tax * 0.04
    
    total_tax = tax + cess
    
    return {
        "base_tax": tax,
        "cess": cess,
        "total_tax": total_tax
    }

def get_tax_saving_tips(income, investments, health_insurance, home_loan, edu_loan):
    """
    Generate personalized tax saving tips based on user inputs
    
    Args:
        income: Annual income
        investments: 80C investments
        health_insurance: Health insurance premium
        home_loan: Home loan interest
        edu_loan: Education loan interest
        
    Returns:
        List of tax saving tips
    """
    tips = []
    
    # 80C deduction tips
    if investments < 150000:
        remaining_80c = 150000 - investments
        tips.append(f"You can invest Rs. {remaining_80c:,} more under section 80C (PPF, ELSS, NSC, etc.) to maximize your tax benefits.")
    
    # 80D health insurance tips
    if health_insurance < 25000:
        tips.append("Consider buying health insurance for yourself and family (up to Rs. 25,000 deduction under 80D).")
    
    # Home loan tips
    if home_loan > 0 and home_loan < 200000:
        tips.append(f"You can claim up to Rs. 2,00,000 for home loan interest under Section 24b. Current claim: Rs. {home_loan:,}")
    
    # Education loan tips
    if edu_loan == 0:
        tips.append("Interest paid on education loans is fully deductible under Section 80E (no upper limit).")
    
    # NPS tips
    tips.append("Consider investing in NPS (National Pension Scheme) for additional deduction of up to Rs. 50,000 under Section 80CCD(1B).")
    
    # General tips
    if income > 1000000:
        tips.append("Consider splitting income with family members (income splitting) to reduce tax burden.")
    
    return tips

def get_better_regime(old_regime_tax, new_regime_tax):
    """
    Determine which tax regime is better for the taxpayer
    
    Args:
        old_regime_tax: Tax liability under old regime
        new_regime_tax: Tax liability under new regime
        
    Returns:
        The better regime and tax savings
    """
    if old_regime_tax["total_tax"] < new_regime_tax["total_tax"]:
        return {
            "regime": "Old Regime",
            "savings": new_regime_tax["total_tax"] - old_regime_tax["total_tax"]
        }
    else:
        return {
            "regime": "New Regime",
            "savings": old_regime_tax["total_tax"] - new_regime_tax["total_tax"]
        }
