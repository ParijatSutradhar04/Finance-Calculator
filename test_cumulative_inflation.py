#!/usr/bin/env python3
"""Test script for cumulative inflation logic."""

import math

def apply_inflation_adjustment(nominal_values: list, inflation_rate: float, cumulative_years: list) -> list:
    """
    Apply inflation adjustment to nominal values using cumulative years since start.
    """
    if inflation_rate <= 0:
        return nominal_values
    
    real_values = []
    for i, nominal_value in enumerate(nominal_values):
        cumulative_year = cumulative_years[i] if isinstance(cumulative_years, list) else cumulative_years
        real_value = nominal_value / ((1 + inflation_rate / 100) ** cumulative_year)
        real_values.append(real_value)
    
    return real_values

def test_cumulative_inflation_logic():
    """
    Regression test for cumulative inflation handling across multiple phases.
    
    INFLATION LOGIC EXPLANATION:
    - Nominal values represent actual rupees that get invested/rolled over
    - Real values are inflation-adjusted for reporting purposes only  
    - Real values use CUMULATIVE years since start, not per-phase years
    
    Example: 2-phase scenario with 6% inflation
    - Phase 1: 10 years, Phase 2: 10 years  
    - Total investment period: 20 years
    - Phase 1 real values: discounted by years 1-10
    - Phase 2 real values: discounted by years 11-20 (cumulative)
    """
    
    print('\n🧪 CUMULATIVE INFLATION LOGIC TEST')
    print('=' * 50)
    
    # Test parameters
    inflation_rate = 6.0
    initial_lumpsum = 1_000_000
    roi = 12.0
    
    # Phase 1: 10 years
    phase1_years = 10
    phase1_nominal_final = initial_lumpsum * ((1 + roi / 100) ** phase1_years)
    # Real value at end of phase 1 (10 years cumulative)
    phase1_real_final = phase1_nominal_final / ((1 + inflation_rate / 100) ** phase1_years)
    
    print(f'\n1️⃣ Phase 1 (Years 1-10):')
    print(f'   Initial Investment: ₹{initial_lumpsum:,.2f}')
    print(f'   Nominal Final: ₹{phase1_nominal_final:,.2f}')
    print(f'   Real Final (10 years): ₹{phase1_real_final:,.2f}')
    
    # Phase 2: 10 more years (rollover the NOMINAL amount)
    phase2_years = 10
    phase2_nominal_final = phase1_nominal_final * ((1 + roi / 100) ** phase2_years)
    # Real value at end of phase 2 (20 years cumulative - this is the key fix!)
    cumulative_years_total = phase1_years + phase2_years
    phase2_real_final = phase2_nominal_final / ((1 + inflation_rate / 100) ** cumulative_years_total)
    
    print(f'\n2️⃣ Phase 2 (Years 11-20):')
    print(f'   Rollover Nominal: ₹{phase1_nominal_final:,.2f}')
    print(f'   Nominal Final: ₹{phase2_nominal_final:,.2f}')
    print(f'   Real Final (20 years cumulative): ₹{phase2_real_final:,.2f}')
    
    # Expected values for validation
    expected_phase1_nominal = 3_105_848.21
    expected_phase1_real = 1_734_289.42
    expected_phase2_nominal = 9_646_293.09
    expected_phase2_real = 3_007_759.78
    
    print(f'\n✅ Validation (with tolerance):')
    
    # Validate Phase 1
    assert math.isclose(phase1_nominal_final, expected_phase1_nominal, rel_tol=1e-2), \
        f"Phase 1 nominal: got {phase1_nominal_final:.2f}, expected {expected_phase1_nominal:.2f}"
    print(f'   ✓ Phase 1 Nominal: {phase1_nominal_final:,.2f} ≈ {expected_phase1_nominal:,.2f}')
    
    assert math.isclose(phase1_real_final, expected_phase1_real, rel_tol=1e-2), \
        f"Phase 1 real: got {phase1_real_final:.2f}, expected {expected_phase1_real:.2f}"
    print(f'   ✓ Phase 1 Real: {phase1_real_final:,.2f} ≈ {expected_phase1_real:,.2f}')
    
    # Validate Phase 2  
    assert math.isclose(phase2_nominal_final, expected_phase2_nominal, rel_tol=1e-2), \
        f"Phase 2 nominal: got {phase2_nominal_final:.2f}, expected {expected_phase2_nominal:.2f}"
    print(f'   ✓ Phase 2 Nominal: {phase2_nominal_final:,.2f} ≈ {expected_phase2_nominal:,.2f}')
    
    assert math.isclose(phase2_real_final, expected_phase2_real, rel_tol=1e-2), \
        f"Phase 2 real: got {phase2_real_final:.2f}, expected {expected_phase2_real:.2f}"
    print(f'   ✓ Phase 2 Real: {phase2_real_final:,.2f} ≈ {expected_phase2_real:,.2f}')
    
    # Test the apply_inflation_adjustment function directly
    print(f'\n🔬 Function Test:')
    nominal_values = [phase1_nominal_final, phase2_nominal_final]
    cumulative_years = [10, 20]
    real_values = apply_inflation_adjustment(nominal_values, inflation_rate, cumulative_years)
    
    assert math.isclose(real_values[0], expected_phase1_real, rel_tol=1e-2), \
        f"Function Phase 1 real: got {real_values[0]:.2f}, expected {expected_phase1_real:.2f}"
    assert math.isclose(real_values[1], expected_phase2_real, rel_tol=1e-2), \
        f"Function Phase 2 real: got {real_values[1]:.2f}, expected {expected_phase2_real:.2f}"
    
    print(f'   ✓ apply_inflation_adjustment function working correctly')
    
    # Demonstrate the bug vs fix
    print(f'\n🐛 Bug vs Fix Comparison:')
    
    # OLD (WRONG) way: using per-phase years
    phase2_real_wrong = phase2_nominal_final / ((1 + inflation_rate / 100) ** phase2_years)
    print(f'   ❌ OLD (Wrong): Phase 2 real using phase years (10): ₹{phase2_real_wrong:,.2f}')
    print(f'   ✅ NEW (Fixed): Phase 2 real using cumulative years (20): ₹{phase2_real_final:,.2f}')
    print(f'   💡 Difference: ₹{phase2_real_wrong - phase2_real_final:,.2f}')
    
    print(f'\n🎯 All tests passed! Cumulative inflation logic is correct.')
    
    return {
        'phase1_nominal': phase1_nominal_final,
        'phase1_real': phase1_real_final,
        'phase2_nominal': phase2_nominal_final,
        'phase2_real': phase2_real_final
    }

if __name__ == "__main__":
    test_cumulative_inflation_logic()