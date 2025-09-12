#!/usr/bin/env python3
"""Test script for portfolio calculation functions."""

def calculate_multiple_sips(sips):
    """Calculate total from multiple SIPs."""
    total_amount = 0.0
    for sip in sips:
        monthly_sip = sip['monthly_sip']
        annual_return = sip['annual_return'] / 100
        monthly_return = annual_return / 12
        years = sip['years']
        step_up = sip.get('step_up', 0) / 100
        
        current_sip = monthly_sip
        amount = 0.0
        
        for year in range(years):
            for month in range(12):
                amount = (amount + current_sip) * (1 + monthly_return)
            if step_up > 0:
                current_sip *= (1 + step_up)
        
        total_amount += amount
    return total_amount

def calculate_multiple_lumpsums(lumpsums):
    """Calculate total from multiple lumpsum investments."""
    total_amount = 0.0
    for lumpsum in lumpsums:
        amount = lumpsum['amount']
        annual_return = lumpsum['annual_return'] / 100
        years = lumpsum['years']
        final_amount = amount * ((1 + annual_return) ** years)
        total_amount += final_amount
    return total_amount

def apply_inflation_adjustment(nominal_values, inflation_rate, years):
    """Apply inflation adjustment to get real values."""
    inflation_rate = inflation_rate / 100
    real_values = []
    for i, nominal in enumerate(nominal_values):
        year = years[i] if isinstance(years, list) else years
        real_value = nominal / ((1 + inflation_rate) ** year)
        real_values.append(real_value)
    return real_values

def main():
    """Run portfolio tests."""
    print('🧪 PORTFOLIO CALCULATION TESTS')
    print('=' * 40)
    
    # Test 1: Multiple SIPs
    print('\n1️⃣ Multiple SIPs Test:')
    sips = [
        {'monthly_sip': 10000, 'annual_return': 15, 'years': 5, 'step_up': 10},
        {'monthly_sip': 5000, 'annual_return': 8, 'years': 5, 'step_up': 5}
    ]
    sip_result = calculate_multiple_sips(sips)
    print(f'   Total from Multiple SIPs: ₹{sip_result:,.2f}')
    
    # Test 2: Multiple Lumpsums
    print('\n2️⃣ Multiple Lumpsums Test:')
    lumpsums = [
        {'amount': 100000, 'annual_return': 12, 'years': 5},
        {'amount': 200000, 'annual_return': 18, 'years': 5}
    ]
    lumpsum_result = calculate_multiple_lumpsums(lumpsums)
    print(f'   Total from Multiple Lumpsums: ₹{lumpsum_result:,.2f}')
    
    # Test 3: Inflation Adjustment
    print('\n3️⃣ Inflation Adjustment Test:')
    nominal_values = [100000, 200000, 300000]
    years = [1, 2, 3]
    real_values = apply_inflation_adjustment(nominal_values, 6, years)
    print(f'   Nominal: {[f"₹{v:,.0f}" for v in nominal_values]}')
    print(f'   Real (6% inflation): {[f"₹{v:,.0f}" for v in real_values]}')
    
    # Test 4: Portfolio Summary
    print('\n4️⃣ Portfolio Summary:')
    total_portfolio = sip_result + lumpsum_result
    total_invested = sum([sip['monthly_sip'] * 12 * sip['years'] for sip in sips]) + sum([ls['amount'] for ls in lumpsums])
    portfolio_real = apply_inflation_adjustment([total_portfolio], 6, [5])[0]
    
    print(f'   💰 Total Invested: ₹{total_invested:,.2f}')
    print(f'   📈 Portfolio Value (Nominal): ₹{total_portfolio:,.2f}')
    print(f'   🎯 Portfolio Value (Real): ₹{portfolio_real:,.2f}')
    print(f'   📊 Nominal Returns: {((total_portfolio/total_invested - 1) * 100):.1f}%')
    
    print('\n✅ All portfolio tests completed successfully!')

if __name__ == '__main__':
    main()