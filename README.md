# 🏦 Advanced Financial Calculator

A comprehensive financial planning tool built with **Streamlit** that supports **combined investment strategies** including SIP, Lumpsum, and SWP (Systematic Withdrawal Plan) within the same phase, with advanced multi-phase investment planning.

## 🚀 Key Features

### 💼 **Combined Investment Strategy**
Unlike traditional calculators that handle investments separately, this calculator allows you to combine multiple investment types within a single phase:

- **SIP + Lumpsum**: Start with a lumpsum and add monthly SIP investments
- **SIP + Lumpsum + SWP**: Build wealth with SIP & Lumpsum, then withdraw systematically
- **Flexible SWP Timing**: Start withdrawals from any year within the investment period
- **Automatic Integration**: All investments work together with unified returns calculation

### 📈 **Investment Components**

#### SIP (Systematic Investment Plan)
- Monthly investment amount with optional annual step-up
- Compound growth with monthly compounding
- Flexible start and duration

#### Lumpsum Investment
- One-time investment amount
- Combines with rollover amounts from previous phases
- Compound growth calculation

#### SWP (Systematic Withdrawal Plan)
- Monthly withdrawals from the total invested corpus
- Start withdrawals from any specified year
- Remaining amount continues to earn returns
- No separate investment needed - uses combined SIP + Lumpsum corpus

### 🔗 **Multi-Phase Investment Planning**

#### Seamless Phase Transitions
- **Automatic Rollover**: Final amount from each phase becomes the starting corpus for the next
- **Additional Investments**: Add fresh money at the start of any new phase
- **Strategy Evolution**: Change investment approach across phases (e.g., accumulation → withdrawal)

#### Real-World Scenarios
1. **Wealth Building → Retirement**:
   - Phase 1: SIP ₹15,000/month + Lumpsum ₹5 lakhs for 25 years
   - Phase 2: SWP ₹75,000/month from the accumulated corpus for 20 years

2. **Aggressive Growth → Balanced Approach**:
   - Phase 1: High SIP with 15% return expectation for 15 years
   - Phase 2: Conservative approach with 8% returns + partial SWP for 10 years

3. **Single Phase Combined Strategy**:
   - SIP ₹10,000/month + Lumpsum ₹2 lakhs for 15 years
   - SWP ₹25,000/month starting from year 10

## 🛠️ Technical Features

### Advanced Calculation Engine
- **Combined Investment Logic**: Unified calculation for SIP + Lumpsum + SWP
- **Monthly Compounding**: Accurate month-by-month calculations
- **Flexible SWP Timing**: Start withdrawals from any year within the investment period
- **Step-up Support**: Annual increase in SIP amounts

### Data & Visualization
- **Comprehensive DataFrames**: Year-by-year breakdown with all investment components
- **Interactive Plotly Charts**: Multi-line charts showing investments, growth, and withdrawals
- **Real-time Calculations**: Instant results as you change inputs
- **Currency Formatting**: Indian Rupee (₹) formatting with proper number formatting

### User Interface
- **Single Page Design**: All investment types combined in one interface
- **Responsive Layout**: Works perfectly on desktop and mobile
- **Session State Management**: Maintains data across phases and interactions
- **Input Validation**: Prevents calculation errors with helpful hints
- **Progress Indicators**: Clear rollover notifications between phases

### Code Architecture
- **Modular Functions**: Clean, reusable calculation functions
- **Type Hints**: Full type annotation for better IDE support
- **Comprehensive Documentation**: Detailed docstrings for all functions
- **Extensible Design**: Easy to add new investment features

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Quick Start
```bash
# Clone or download the project
git clone <repository-url>
cd Finance-Calculator

# Install dependencies
pip install streamlit pandas plotly

# Run the application
streamlit run sip_calculator.py
```

The application will open in your default browser at `http://localhost:8501`

## 🎯 Usage Guide

### Single Phase Combined Investment
1. **Set Investment Parameters**:
   - Add monthly SIP amount (set to 0 if not needed)
   - Add additional lumpsum amount (beyond rollover)
   - Set expected annual return rate
   - Choose investment duration

2. **Configure SWP (Optional)**:
   - Set monthly withdrawal amount (0 = no withdrawals)
   - Choose when withdrawals should start (year 1-N)

3. **Calculate and Review**:
   - Click "Calculate Combined Investment"
   - Review detailed metrics, year-wise breakdown, and interactive charts

### Multi-Phase Investment Planning
1. **Complete Phase 1** with your chosen investment strategy
2. **Add Next Phase** using the sidebar button
3. **Phase 2 automatically starts** with Phase 1's final amount
4. **Add additional investment** for Phase 2 if desired
5. **Configure new strategy** for Phase 2 (can be completely different)
6. **Continue adding phases** as needed for long-term planning

### Example Scenarios

#### Scenario 1: Complete Retirement Planning
```
Phase 1: Wealth Accumulation (25 years)
- Monthly SIP: ₹20,000
- Annual Step-up: 10%
- Additional Lumpsum: ₹5,00,000
- Expected Return: 12%
- Duration: 25 years

Result: Builds ₹4.2 crores

Phase 2: Retirement Income (20 years)  
- Monthly Withdrawal: ₹1,00,000
- Expected Return: 8% (conservative)
- Duration: 20 years

Result: Provides sustainable retirement income
```

#### Scenario 2: Mixed Strategy in Single Phase
```
Combined Investment (15 years)
- Monthly SIP: ₹15,000 (10% step-up)
- Lumpsum: ₹10,00,000
- Expected Return: 11%
- SWP: ₹30,000/month starting Year 8
- Duration: 15 years

Result: Build wealth early, start income generation mid-term
```

## 🧮 Calculation Methodology

### SIP Calculation
- Uses compound interest with monthly compounding
- Supports annual step-up increases
- Formula: `FV = PMT × [((1 + r)^n - 1) / r] × (1 + r)`

### Lumpsum Calculation  
- Simple compound interest calculation
- Formula: `FV = PV × (1 + r)^n`

### SWP Calculation
- Monthly withdrawals from invested corpus
- Remaining amount earns monthly returns
- Tracks sustainability of withdrawal strategy

## 🔧 Customization

### Adding New Investment Types
1. Create a new calculation function following the existing pattern
2. Add a new section function for the UI
3. Include the new tab in the main application
4. Update the visualization function if needed

### Modifying Return Calculations
- All calculation functions are in the main file
- Easy to modify formulas or add new parameters
- Type hints ensure parameter safety

## 📊 Output Features

### Metrics Display
- **Total Invested**: Sum of all investments
- **Final Amount**: Maturity value or remaining balance
- **Total Returns**: Profit/loss from investments

### Year-wise Breakdown Table
- Year-by-year progression
- Investment amounts
- Current values  
- Returns earned

### Interactive Charts
- **Growth Charts**: Investment vs Current Value
- **SWP Charts**: Remaining Value vs Total Withdrawn
- **Hover Details**: Year-wise information
- **Responsive Design**: Scales with screen size

## 🤝 Contributing

Feel free to contribute by:
- Adding new investment calculators
- Improving UI/UX
- Adding more visualization options
- Enhancing calculation accuracy
- Adding export features (PDF, Excel)

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Known Issues & Future Enhancements

### Planned Features
- [ ] Export results to PDF/Excel
- [ ] Goal-based planning (house, car, education)
- [ ] Tax calculation integration
- [ ] Inflation adjustment options
- [ ] Comparison between different strategies
- [ ] Email/SMS alerts for milestones

### Performance Notes
- Calculations are performed client-side for instant results
- Large datasets (>50 years) may take slightly longer to render charts
- Session state maintains data across page refreshes

---

**Happy Financial Planning! 💰📈**