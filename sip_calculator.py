import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Tuple, Dict, Any

# Configure page
st.set_page_config(
    page_title="Advanced Financial Calculator",
    page_icon="💰",
    layout="wide"
)

def calculate_sip(monthly_amount: float, annual_rate: float, years: int, step_up: float = 0.0, initial_amount: float = 0.0) -> Tuple[float, float, pd.DataFrame]:
    """
    Calculate SIP (Systematic Investment Plan) with optional step-up and initial lumpsum.
    
    Args:
        monthly_amount: Monthly SIP amount
        annual_rate: Expected annual return rate (%)
        years: Investment duration in years
        step_up: Annual step-up percentage (default: 0.0)
        initial_amount: Initial lumpsum amount to start with (default: 0.0)
    
    Returns:
        Tuple of (final_amount, total_invested, year_wise_data)
    """
    monthly_rate = annual_rate / 12 / 100
    total_months = years * 12
    
    data = []
    current_amount = initial_amount
    total_invested = initial_amount
    current_sip = monthly_amount
    
    for month in range(1, total_months + 1):
        # Add monthly SIP
        total_invested += current_sip
        current_amount = (current_amount + current_sip) * (1 + monthly_rate)
        
        # Step up SIP amount annually
        if month % 12 == 0 and step_up > 0:
            current_sip *= (1 + step_up / 100)
        
        # Record year-end data
        if month % 12 == 0:
            year = month // 12
            data.append({
                'Year': year,
                'Amount_Invested': total_invested,
                'Current_Value': current_amount,
                'Returns': current_amount - total_invested
            })
    
    df = pd.DataFrame(data)
    return current_amount, total_invested, df

def calculate_lumpsum(principal: float, annual_rate: float, years: int, initial_amount: float = 0.0) -> Tuple[float, float, pd.DataFrame]:
    """
    Calculate Lumpsum investment growth.
    
    Args:
        principal: Lumpsum investment amount
        annual_rate: Expected annual return rate (%)
        years: Investment duration in years
        initial_amount: Initial amount to start with (default: 0.0)
    
    Returns:
        Tuple of (final_amount, total_invested, year_wise_data)
    """
    total_principal = principal + initial_amount
    total_invested = total_principal
    
    data = []
    for year in range(1, years + 1):
        current_value = total_principal * ((1 + annual_rate / 100) ** year)
        data.append({
            'Year': year,
            'Amount_Invested': total_invested,
            'Current_Value': current_value,
            'Returns': current_value - total_invested
        })
    
    final_amount = total_principal * ((1 + annual_rate / 100) ** years)
    df = pd.DataFrame(data)
    return final_amount, total_invested, df

def calculate_swp(initial_amount: float, monthly_withdrawal: float, annual_rate: float, years: int) -> Tuple[float, float, pd.DataFrame]:
    """
    Calculate SWP (Systematic Withdrawal Plan).
    
    Args:
        initial_amount: Initial investment amount
        monthly_withdrawal: Monthly withdrawal amount
        annual_rate: Expected annual return rate (%)
        years: Withdrawal duration in years
    
    Returns:
        Tuple of (remaining_amount, total_withdrawn, year_wise_data)
    """
    monthly_rate = annual_rate / 12 / 100
    total_months = years * 12
    
    data = []
    current_amount = initial_amount
    total_withdrawn = 0.0
    
    for month in range(1, total_months + 1):
        # Apply monthly return
        current_amount *= (1 + monthly_rate)
        
        # Withdraw amount (if sufficient balance)
        if current_amount >= monthly_withdrawal:
            current_amount -= monthly_withdrawal
            total_withdrawn += monthly_withdrawal
        
        # Record year-end data
        if month % 12 == 0:
            year = month // 12
            data.append({
                'Year': year,
                'Remaining_Value': current_amount,
                'Total_Withdrawn': total_withdrawn,
                'Annual_Withdrawal': monthly_withdrawal * 12
            })
    
    df = pd.DataFrame(data)
    return current_amount, total_withdrawn, df

def calculate_combined_investment(
    sip_amount: float = 0.0, 
    lumpsum_amount: float = 0.0, 
    annual_rate: float = 12.0, 
    years: int = 10, 
    step_up: float = 0.0, 
    initial_amount: float = 0.0,
    swp_withdrawal: float = 0.0,
    swp_start_year: int = 1
) -> Tuple[float, float, float, pd.DataFrame]:
    """
    Calculate combined SIP + Lumpsum investment with optional SWP.
    
    Args:
        sip_amount: Monthly SIP amount
        lumpsum_amount: Initial lumpsum investment
        annual_rate: Expected annual return rate (%)
        years: Total investment/withdrawal duration
        step_up: Annual SIP step-up percentage
        initial_amount: Initial rollover amount from previous phase
        swp_withdrawal: Monthly withdrawal amount (0 = no SWP)
        swp_start_year: Year when SWP starts (default: 1)
    
    Returns:
        Tuple of (final_amount, total_invested, total_withdrawn, year_wise_data)
    """
    monthly_rate = annual_rate / 12 / 100
    total_months = years * 12
    
    data = []
    current_amount = initial_amount + lumpsum_amount
    total_invested = initial_amount + lumpsum_amount
    total_sip_invested = 0.0
    total_withdrawn = 0.0
    current_sip = sip_amount
    
    for month in range(1, total_months + 1):
        # Add monthly SIP if specified
        if sip_amount > 0:
            total_sip_invested += current_sip
            total_invested += current_sip
            current_amount += current_sip
        
        # Apply monthly return
        current_amount *= (1 + monthly_rate)
        
        # Apply SWP withdrawal if applicable
        current_year = (month - 1) // 12 + 1
        if swp_withdrawal > 0 and current_year >= swp_start_year:
            if current_amount >= swp_withdrawal:
                current_amount -= swp_withdrawal
                total_withdrawn += swp_withdrawal
        
        # Step up SIP amount annually
        if month % 12 == 0 and step_up > 0 and sip_amount > 0:
            current_sip *= (1 + step_up / 100)
        
        # Record year-end data
        if month % 12 == 0:
            year = month // 12
            data.append({
                'Year': year,
                'SIP_Invested': total_sip_invested,
                'Lumpsum_Invested': lumpsum_amount + initial_amount,
                'Total_Invested': total_invested,
                'Current_Value': current_amount,
                'Total_Withdrawn': total_withdrawn,
                'Net_Returns': current_amount + total_withdrawn - total_invested
            })
    
    df = pd.DataFrame(data)
    return current_amount, total_invested, total_withdrawn, df

def create_growth_chart(df: pd.DataFrame, chart_type: str) -> go.Figure:
    """Create interactive growth chart using Plotly."""
    fig = go.Figure()
    
    if chart_type == "Combined":
        # Combined investment chart
        fig.add_trace(go.Scatter(
            x=df['Year'], 
            y=df['Total_Invested'],
            mode='lines+markers',
            name='Total Invested',
            line=dict(color='blue', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df['Year'], 
            y=df['Current_Value'],
            mode='lines+markers',
            name='Current Value',
            line=dict(color='green', width=3)
        ))
        if 'Total_Withdrawn' in df.columns and df['Total_Withdrawn'].sum() > 0:
            fig.add_trace(go.Scatter(
                x=df['Year'], 
                y=df['Total_Withdrawn'],
                mode='lines+markers',
                name='Total Withdrawn',
                line=dict(color='red', width=3)
            ))
        fig.update_layout(title="Combined Investment: Growth & Withdrawals Over Time")
    elif chart_type == "SWP":
        fig.add_trace(go.Scatter(
            x=df['Year'], 
            y=df['Remaining_Value'],
            mode='lines+markers',
            name='Remaining Value',
            line=dict(color='blue', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df['Year'], 
            y=df['Total_Withdrawn'],
            mode='lines+markers',
            name='Total Withdrawn',
            line=dict(color='red', width=3)
        ))
        fig.update_layout(title="SWP: Remaining Value vs Total Withdrawn")
    else:
        fig.add_trace(go.Scatter(
            x=df['Year'], 
            y=df['Amount_Invested'],
            mode='lines+markers',
            name='Amount Invested',
            line=dict(color='blue', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df['Year'], 
            y=df['Current_Value'],
            mode='lines+markers',
            name='Current Value',
            line=dict(color='green', width=3)
        ))
        fig.update_layout(title=f"{chart_type}: Investment Growth Over Time")
    
    fig.update_layout(
        xaxis_title="Years",
        yaxis_title="Amount (₹)",
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

def display_results(final_amount: float, total_invested: float, df: pd.DataFrame, chart_type: str, total_withdrawn: float = 0.0):
    """Display calculation results with metrics, table, and chart."""
    
    if chart_type == "Combined":
        # Combined investment metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Invested", f"₹{total_invested:,.2f}")
        with col2:
            st.metric("Current Value", f"₹{final_amount:,.2f}")
        with col3:
            if total_withdrawn > 0:
                st.metric("Total Withdrawn", f"₹{total_withdrawn:,.2f}")
            else:
                st.metric("Total Returns", f"₹{final_amount - total_invested:,.2f}")
        with col4:
            net_benefit = final_amount + total_withdrawn - total_invested
            st.metric("Net Benefit", f"₹{net_benefit:,.2f}")
        
        # Additional breakdown for combined investments
        if 'SIP_Invested' in df.columns:
            st.subheader("Investment Breakdown")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("SIP Investment", f"₹{df['SIP_Invested'].iloc[-1]:,.2f}")
            with col2:
                st.metric("Lumpsum Investment", f"₹{df['Lumpsum_Invested'].iloc[-1]:,.2f}")
    
    elif chart_type == "SWP":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Initial Investment", f"₹{total_invested:,.2f}")
        with col2:
            st.metric("Total Withdrawn", f"₹{df['Total_Withdrawn'].iloc[-1]:,.2f}")
        with col3:
            st.metric("Remaining Amount", f"₹{final_amount:,.2f}")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Invested", f"₹{total_invested:,.2f}")
        with col2:
            st.metric("Final Amount", f"₹{final_amount:,.2f}")
        with col3:
            returns = final_amount - total_invested
            st.metric("Total Returns", f"₹{returns:,.2f}")
    
    # Display year-wise breakdown
    st.subheader("Year-wise Breakdown")
    st.dataframe(df, width='stretch')
    
    # Display chart
    st.subheader("Growth Visualization")
    fig = create_growth_chart(df, chart_type)
    st.plotly_chart(fig, width='stretch')
    
def combined_investment_section(phase_num: int = 1, initial_amount: float = 0.0):
    """Combined investment section UI and calculations for SIP + Lumpsum + SWP."""
    st.subheader(f"� Combined Investment Calculator - Phase {phase_num}")
    
    if initial_amount > 0:
        st.info(f"Starting with rollover amount: ₹{initial_amount:,.2f}")
    
    # Investment inputs
    st.markdown("### 📈 Investment Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        # SIP inputs
        st.markdown("**SIP Investment**")
        sip_amount = st.number_input(
            "Monthly SIP Amount (₹)", 
            min_value=0.0, 
            value=0.0,
            key=f"sip_amount_{phase_num}",
            help="Set to 0 if no SIP investment"
        )
        step_up = st.number_input(
            "Annual SIP Step-up (%)", 
            min_value=0.0, 
            value=10.0,
            key=f"sip_stepup_{phase_num}"
        )
        
        # Lumpsum inputs
        st.markdown("**Lumpsum Investment**")
        lumpsum_amount = st.number_input(
            "Additional Lumpsum (₹)", 
            min_value=0.0, 
            value=0.0,
            key=f"lumpsum_amount_{phase_num}",
            help="Additional lumpsum on top of rollover amount"
        )
    
    with col2:
        # Common parameters
        st.markdown("**Common Parameters**")
        annual_rate = st.number_input(
            "Expected Annual Return (%)", 
            min_value=0.0, 
            value=12.0,
            key=f"annual_rate_{phase_num}"
        )
        years = st.number_input(
            "Duration (Years)", 
            min_value=1, 
            value=10,
            key=f"years_{phase_num}"
        )
        
        # SWP inputs
        st.markdown("**SWP (Withdrawal)**")
        swp_withdrawal = st.number_input(
            "Monthly Withdrawal (₹)", 
            min_value=0.0, 
            value=0.0,
            key=f"swp_withdrawal_{phase_num}",
            help="Set to 0 if no withdrawal needed"
        )
        swp_start_year = st.number_input(
            "SWP Start Year", 
            min_value=1, 
            value=1,
            max_value=years,
            key=f"swp_start_year_{phase_num}",
            help="Year when withdrawals begin"
        )
    
    # Validation and calculation
    has_investment = sip_amount > 0 or lumpsum_amount > 0 or initial_amount > 0
    
    if st.button(f"Calculate Combined Investment - Phase {phase_num}", key=f"calc_combined_{phase_num}"):
        if has_investment and annual_rate > 0 and years > 0:
            final_amount, total_invested, total_withdrawn, df = calculate_combined_investment(
                sip_amount=sip_amount,
                lumpsum_amount=lumpsum_amount,
                annual_rate=annual_rate,
                years=years,
                step_up=step_up,
                initial_amount=initial_amount,
                swp_withdrawal=swp_withdrawal,
                swp_start_year=swp_start_year
            )
            
            st.session_state[f'combined_result_{phase_num}'] = {
                'final_amount': final_amount,
                'total_invested': total_invested,
                'total_withdrawn': total_withdrawn,
                'df': df
            }
        else:
            st.error("Please provide at least one investment amount and valid parameters.")
    
    # Display results if available
    if f'combined_result_{phase_num}' in st.session_state:
        result = st.session_state[f'combined_result_{phase_num}']
        display_results(
            result['final_amount'], 
            result['total_invested'], 
            result['df'], 
            "Combined",
            result['total_withdrawn']
        )
        return result['final_amount']
    
    return None

def main():
    """Main application."""
    st.title("🏦 Advanced Financial Calculator")
    st.markdown("*Comprehensive financial planning with combined SIP, Lumpsum & SWP strategies*")
    st.markdown("---")
    
    # Initialize session state for phases
    if 'num_phases' not in st.session_state:
        st.session_state.num_phases = 1
    
    # Phase management
    st.sidebar.header("Investment Phases")
    st.sidebar.markdown("*Build multi-phase investment strategies*")
    
    if st.sidebar.button("➕ Add Next Phase"):
        st.session_state.num_phases += 1
        st.sidebar.success(f"Phase {st.session_state.num_phases} added!")
    
    if st.sidebar.button("🗑️ Reset All Phases"):
        st.session_state.num_phases = 1
        # Clear all results
        keys_to_remove = [key for key in st.session_state.keys() if 'result_' in key]
        for key in keys_to_remove:
            del st.session_state[key]
        st.sidebar.success("All phases reset!")
    
    st.sidebar.write(f"**Current Phases:** {st.session_state.num_phases}")
    
    # Instructions
    with st.expander("📋 How to Use This Calculator", expanded=False):
        st.markdown("""
        **Combined Investment Strategy:**
        - **SIP**: Add monthly systematic investments with optional step-up
        - **Lumpsum**: Add one-time investment amount
        - **SWP**: Set monthly withdrawals starting from any year
        - **Multi-Phase**: Chain strategies where each phase's final amount becomes the next phase's starting amount
        
        **Example Scenarios:**
        1. **Wealth Building**: Phase 1 with SIP + Lumpsum for 20 years
        2. **Retirement Planning**: Phase 2 with SWP withdrawals for 15 years
        3. **Mixed Strategy**: Combine all three in a single phase
        """)
    
    # Display phases
    rollover_amount = 0.0
    
    for phase in range(1, st.session_state.num_phases + 1):
        st.markdown(f"## 🎯 Phase {phase}")
        
        if phase > 1:
            # Add option for additional investment in subsequent phases
            additional_investment = st.number_input(
                f"💰 Additional Investment for Phase {phase} (₹)",
                min_value=0.0,
                value=0.0,
                key=f"additional_investment_{phase}",
                help="Fresh money to add on top of rollover amount"
            )
            rollover_amount += additional_investment
        
        # Combined investment section
        phase_result = combined_investment_section(phase, rollover_amount)
        
        # Update rollover amount for next phase
        if phase_result is not None:
            rollover_amount = phase_result
            if phase < st.session_state.num_phases:
                st.success(f"✅ Phase {phase} completed! Final amount ₹{rollover_amount:,.2f} will roll over to Phase {phase + 1}")
        
        st.markdown("---")
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with ❤️ using Streamlit | Financial Calculator v2.0*")

if __name__ == "__main__":
    main()
