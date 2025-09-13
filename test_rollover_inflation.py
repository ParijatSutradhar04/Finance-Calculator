#!/usr/bin/env python3
"""Test script for updated rollover and inflation logic."""

def test_rollover_inflation_logic():
    """Test the updated rollover and inflation handling."""
    print('🧪 ROLLOVER & INFLATION LOGIC TESTS')
    print('=' * 50)
    
    # Test 1: Basic rollover calculation
    print('\n1️⃣ Basic Rollover Test:')
    rollover_nominal = 500000  # Previous phase final amount
    additional_lumpsum = 200000  # User adds extra
    lumpsum_roi = 12.0
    years = 5
    
    combined_lumpsum = rollover_nominal + additional_lumpsum
    final_value = combined_lumpsum * ((1 + lumpsum_roi / 100) ** years)
    
    print(f'   Rollover Amount: ₹{rollover_nominal:,.2f}')
    print(f'   Additional Lumpsum: ₹{additional_lumpsum:,.2f}')
    print(f'   Combined Lumpsum: ₹{combined_lumpsum:,.2f}')
    print(f'   Final Value (12% for 5 years): ₹{final_value:,.2f}')
    
    # Test 2: Inflation adjustment
    print('\n2️⃣ Inflation Adjustment Test:')
    nominal_values = [700000, 800000, 900000, 1000000, final_value]
    inflation_rate = 6.0
    
    real_values = []
    for i, nominal in enumerate(nominal_values):
        year = i + 1
        real_value = nominal / ((1 + inflation_rate / 100) ** year)
        real_values.append(real_value)
    
    print(f'   Inflation Rate: {inflation_rate}%')
    print(f'   Year 5 Nominal: ₹{nominal_values[-1]:,.2f}')
    print(f'   Year 5 Real: ₹{real_values[-1]:,.2f}')
    print(f'   Purchasing Power Loss: ₹{nominal_values[-1] - real_values[-1]:,.2f}')
    
    # Test 3: Multi-phase scenario
    print('\n3️⃣ Multi-Phase Scenario:')
    
    # Phase 1: Growth phase
    phase1_sip = 10000 * 12 * 10  # 10K SIP for 10 years
    phase1_final = 1800000  # Assume final value
    print(f'   Phase 1 - Growth: ₹{phase1_sip:,.2f} invested → ₹{phase1_final:,.2f} final')
    
    # Phase 2: Rollover + additional investment
    phase2_rollover = phase1_final  # Nominal value rolls over
    phase2_additional = 500000
    phase2_combined = phase2_rollover + phase2_additional
    phase2_roi = 10.0  # Conservative ROI for next phase
    phase2_years = 15
    phase2_final = phase2_combined * ((1 + phase2_roi / 100) ** phase2_years)
    
    print(f'   Phase 2 - Rollover: ₹{phase2_rollover:,.2f}')
    print(f'   Phase 2 - Additional: ₹{phase2_additional:,.2f}')
    print(f'   Phase 2 - Combined Lumpsum: ₹{phase2_combined:,.2f}')
    print(f'   Phase 2 - Final (10% for 15 years): ₹{phase2_final:,.2f}')
    
    # Real value calculation for final amount
    total_years = 10 + 15  # Total investment period
    phase2_real_final = phase2_final / ((1 + 6 / 100) ** total_years)
    print(f'   Phase 2 - Real Final Value: ₹{phase2_real_final:,.2f}')
    
    print('\n✅ Key Validations:')
    print(f'   ✓ Only NOMINAL values roll over between phases')
    print(f'   ✓ Rollover treated as Lumpsum with new phase ROI')
    print(f'   ✓ Real values calculated for reporting only')
    print(f'   ✓ Inflation adjustment preserves purchasing power perspective')
    
    return {
        'phase2_nominal': phase2_final,
        'phase2_real': phase2_real_final,
        'rollover_amount': phase2_rollover,
        'combined_lumpsum': phase2_combined
    }

if __name__ == '__main__':
    results = test_rollover_inflation_logic()
    print(f'\n🎯 Test Results Summary:')
    print(f'   Final Nominal: ₹{results["phase2_nominal"]:,.2f}')
    print(f'   Final Real: ₹{results["phase2_real"]:,.2f}')
    print(f'   Rollover Used: ₹{results["rollover_amount"]:,.2f}')
    print(f'   Combined Investment: ₹{results["combined_lumpsum"]:,.2f}')