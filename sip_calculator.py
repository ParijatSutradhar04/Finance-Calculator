import streamlit as st

# Configure page - must be first Streamlit command
st.set_page_config(
    page_title="Advanced Financial Calculator",
    page_icon="💰",
    layout="wide"
)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Tuple, Dict, Any

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

def calculate_multiple_sips(sips_list: list, years: int, initial_amount: float = 0.0) -> Tuple[float, float, pd.DataFrame]:
    """
    Calculate multiple SIP investments running in parallel.
    
    Args:
        sips_list: List of dictionaries with SIP parameters
                  [{'amount': 5000, 'rate': 12, 'step_up': 10}, ...]
        years: Investment duration in years
        initial_amount: Initial amount (from previous phase)
    
    Returns:
        Tuple of (total_final_amount, total_invested, combined_year_wise_data)
    """
    if not sips_list:
        return initial_amount, initial_amount, pd.DataFrame()
    
    total_final_amount = initial_amount
    total_invested = initial_amount
    combined_data = []
    
    # Calculate each SIP separately
    for i, sip in enumerate(sips_list):
        final_amount, invested, df = calculate_sip(
            sip['amount'], sip['rate'], years, sip.get('step_up', 0), 0
        )
        total_final_amount += final_amount
        total_invested += invested
        
        # Add SIP identifier to the data
        df[f'SIP_{i+1}_Value'] = df['Current_Value']
        df[f'SIP_{i+1}_Invested'] = df['Amount_Invested']
        
        if i == 0:
            combined_data = df[['Year']].copy()
        
        combined_data[f'SIP_{i+1}_Value'] = df['Current_Value']
        combined_data[f'SIP_{i+1}_Invested'] = df['Amount_Invested']
    
    # Calculate totals for each year
    sip_value_cols = [col for col in combined_data.columns if 'Value' in col]
    sip_invested_cols = [col for col in combined_data.columns if 'Invested' in col]
    
    combined_data['Total_SIP_Value'] = combined_data[sip_value_cols].sum(axis=1)
    combined_data['Total_SIP_Invested'] = combined_data[sip_invested_cols].sum(axis=1)
    
    return total_final_amount, total_invested, combined_data

def calculate_multiple_lumpsums(lumpsums_list: list, years: int, initial_amount: float = 0.0) -> Tuple[float, float, pd.DataFrame]:
    """
    Calculate multiple Lumpsum investments running in parallel.
    
    Args:
        lumpsums_list: List of dictionaries with Lumpsum parameters
                      [{'amount': 100000, 'rate': 12}, ...]
        years: Investment duration in years
        initial_amount: Initial amount (from previous phase)
    
    Returns:
        Tuple of (total_final_amount, total_invested, combined_year_wise_data)
    """
    if not lumpsums_list:
        return initial_amount, initial_amount, pd.DataFrame()
    
    total_final_amount = initial_amount
    total_invested = initial_amount
    combined_data = []
    
    # Calculate each Lumpsum separately
    for i, lumpsum in enumerate(lumpsums_list):
        final_amount, invested, df = calculate_lumpsum(
            lumpsum['amount'], lumpsum['rate'], years, 0
        )
        total_final_amount += final_amount
        total_invested += invested
        
        # Add Lumpsum identifier to the data
        df[f'Lumpsum_{i+1}_Value'] = df['Current_Value']
        df[f'Lumpsum_{i+1}_Invested'] = df['Amount_Invested']
        
        if i == 0:
            combined_data = df[['Year']].copy()
        
        combined_data[f'Lumpsum_{i+1}_Value'] = df['Current_Value']
        combined_data[f'Lumpsum_{i+1}_Invested'] = df['Amount_Invested']
    
    # Calculate totals for each year
    lumpsum_value_cols = [col for col in combined_data.columns if 'Value' in col]
    lumpsum_invested_cols = [col for col in combined_data.columns if 'Invested' in col]
    
    combined_data['Total_Lumpsum_Value'] = combined_data[lumpsum_value_cols].sum(axis=1)
    combined_data['Total_Lumpsum_Invested'] = combined_data[lumpsum_invested_cols].sum(axis=1)
    
    return total_final_amount, total_invested, combined_data

def calculate_multiple_swps(swps_list: list, portfolio_values: list, years: int) -> Tuple[float, float, pd.DataFrame]:
    """
    Calculate multiple SWP withdrawals from portfolio values.
    
    Args:
        swps_list: List of dictionaries with SWP parameters
                  [{'amount': 10000, 'rate': 8, 'start_year': 1}, ...]
        portfolio_values: List of portfolio values for each year
        years: Total duration in years
    
    Returns:
        Tuple of (remaining_amount, total_withdrawn, combined_year_wise_data)
    """
    if not swps_list or not portfolio_values:
        return 0, 0, pd.DataFrame()
    
    # Start with the final portfolio value
    current_amount = portfolio_values[-1] if portfolio_values else 0
    total_withdrawn = 0
    combined_data = []
    
    # For simplicity, apply SWPs to the total portfolio value
    # In reality, you might want more sophisticated allocation
    for i, swp in enumerate(swps_list):
        remaining_amount, withdrawn, df = calculate_swp(
            current_amount, swp['amount'], swp['rate'], years
        )
        total_withdrawn += withdrawn
        current_amount = remaining_amount
        
        if i == 0:
            combined_data = df.copy()
            combined_data[f'SWP_{i+1}_Withdrawn'] = df['Total_Withdrawn']
            combined_data[f'SWP_{i+1}_Remaining'] = df['Remaining_Value']
        else:
            combined_data[f'SWP_{i+1}_Withdrawn'] = df['Total_Withdrawn']
            combined_data[f'SWP_{i+1}_Remaining'] = df['Remaining_Value']
    
    return current_amount, total_withdrawn, combined_data

def apply_inflation_adjustment(nominal_values: list, inflation_rate: float, cumulative_years: list) -> list:
    """
    Apply inflation adjustment to nominal values using cumulative years since start.
    
    Args:
        nominal_values: List of nominal values
        inflation_rate: Annual inflation rate (%)
        cumulative_years: List of cumulative years since the very start of investment plan
    
    Returns:
        List of real (inflation-adjusted) values
    """
    if inflation_rate <= 0:
        return nominal_values
    
    real_values = []
    for i, nominal_value in enumerate(nominal_values):
        cumulative_year = cumulative_years[i] if isinstance(cumulative_years, list) else cumulative_years
        real_value = nominal_value / ((1 + inflation_rate / 100) ** cumulative_year)
        real_values.append(real_value)
    
    return real_values

def calculate_combined_portfolio_parallel(
    sips_list: list = None,
    lumpsums_list: list = None, 
    swps_list: list = None,
    years: int = 10,
    rollover_nominal: float = 0.0,
    additional_lumpsum: float = 0.0,
    lumpsum_roi: float = 12.0,
    inflation_rate: float = 0.0,
    phase_start_year: int = 0
) -> Tuple[float, float, float, float, float, pd.DataFrame]:
    """
    Calculate combined portfolio with multiple parallel investments and inflation adjustment.
    
    Args:
        sips_list: List of SIP configurations
        lumpsums_list: List of Lumpsum configurations (additional lumpsums only)
        swps_list: List of SWP configurations
        years: Investment duration for this phase
        rollover_nominal: Nominal rollover amount from previous phase (treated as lumpsum)
        additional_lumpsum: Additional lumpsum amount specified by user
        lumpsum_roi: ROI for combined lumpsum (rollover + additional)
        inflation_rate: Annual inflation rate (%)
        phase_start_year: Cumulative years elapsed before this phase starts
    
    Returns:
        Tuple of (nominal_final, real_final, total_invested, total_withdrawn, net_benefit, portfolio_df)
    """
    sips_list = sips_list or []
    lumpsums_list = lumpsums_list or []
    swps_list = swps_list or []
    
    # Calculate SIPs
    sip_final, sip_invested, sip_df = calculate_multiple_sips(sips_list, years, 0)
    
    # Handle rollover + additional lumpsum as combined lumpsum investment
    combined_lumpsum_amount = rollover_nominal + additional_lumpsum
    combined_lumpsum_invested = combined_lumpsum_amount
    
    # Calculate growth of combined lumpsum (rollover + additional) using specified ROI
    if combined_lumpsum_amount > 0:
        combined_lumpsum_final = combined_lumpsum_amount * ((1 + lumpsum_roi / 100) ** years)
    else:
        combined_lumpsum_final = 0
    
    # Calculate other lumpsums separately (if any)
    other_lumpsum_final, other_lumpsum_invested, lumpsum_df = calculate_multiple_lumpsums(lumpsums_list, years, 0)
    
    # Combine all lumpsum results
    total_lumpsum_final = combined_lumpsum_final + other_lumpsum_final
    total_lumpsum_invested = combined_lumpsum_invested + other_lumpsum_invested
    
    # Combine SIP and Lumpsum results
    total_invested = sip_invested + total_lumpsum_invested
    portfolio_value_nominal = sip_final + total_lumpsum_final
    
    # Apply SWPs (simplified - apply to total portfolio)
    if swps_list:
        portfolio_values = [portfolio_value_nominal]  # Simplified for now
        remaining_after_swp, total_withdrawn, swp_df = calculate_multiple_swps(swps_list, portfolio_values, years)
        portfolio_value_nominal = remaining_after_swp
    else:
        total_withdrawn = 0
        swp_df = pd.DataFrame()
    
    # Create combined portfolio DataFrame with cumulative timeline
    portfolio_data = []
    for year in range(1, years + 1):
        # Calculate cumulative years since the very start of investment plan
        cumulative_year = phase_start_year + year
        
        year_data = {
            'Year': year,
            'Cumulative_Years': cumulative_year  # Total years since start of entire plan
        }
        
        # Get SIP data for this year
        if not sip_df.empty:
            year_sip_data = sip_df[sip_df['Year'] == year]
            if not year_sip_data.empty:
                year_data['Total_SIP_Invested'] = year_sip_data['Total_SIP_Invested'].iloc[0]
                year_data['Total_SIP_Value'] = year_sip_data['Total_SIP_Value'].iloc[0]
            else:
                year_data['Total_SIP_Invested'] = 0
                year_data['Total_SIP_Value'] = 0
        else:
            year_data['Total_SIP_Invested'] = 0
            year_data['Total_SIP_Value'] = 0
        
        # Calculate combined lumpsum value for this year (rollover + additional)
        if combined_lumpsum_amount > 0:
            year_combined_lumpsum_value = combined_lumpsum_amount * ((1 + lumpsum_roi / 100) ** year)
        else:
            year_combined_lumpsum_value = 0
        
        # Get other lumpsum data for this year
        if not lumpsum_df.empty:
            year_lumpsum_data = lumpsum_df[lumpsum_df['Year'] == year]
            if not year_lumpsum_data.empty:
                year_other_lumpsum_value = year_lumpsum_data['Total_Lumpsum_Value'].iloc[0]
            else:
                year_other_lumpsum_value = 0
        else:
            year_other_lumpsum_value = 0
        
        # Combine all lumpsum values
        year_data['Rollover_Lumpsum_Invested'] = rollover_nominal
        year_data['Additional_Lumpsum_Invested'] = additional_lumpsum + other_lumpsum_invested
        year_data['Total_Lumpsum_Invested'] = combined_lumpsum_invested + other_lumpsum_invested
        year_data['Total_Lumpsum_Value'] = year_combined_lumpsum_value + year_other_lumpsum_value
        
        # Calculate portfolio totals
        nominal_portfolio_value = year_data['Total_SIP_Value'] + year_data['Total_Lumpsum_Value']
        
        # Get SWP data for this year
        if not swp_df.empty:
            year_swp_data = swp_df[swp_df['Year'] == year]
            if not year_swp_data.empty:
                year_data['Total_Withdrawn'] = year_swp_data['Total_Withdrawn'].iloc[0]
                nominal_portfolio_value = year_swp_data['Remaining_Value'].iloc[0]
            else:
                year_data['Total_Withdrawn'] = 0
        else:
            year_data['Total_Withdrawn'] = 0
        
        year_data['Nominal_Portfolio_Value'] = nominal_portfolio_value
        
        portfolio_data.append(year_data)
    
    portfolio_df = pd.DataFrame(portfolio_data)
    
    # Apply inflation adjustment using cumulative years for reporting only
    if inflation_rate > 0 and not portfolio_df.empty:
        nominal_values = portfolio_df['Nominal_Portfolio_Value'].tolist()
        cumulative_years = portfolio_df['Cumulative_Years'].tolist()
        real_values = apply_inflation_adjustment(nominal_values, inflation_rate, cumulative_years)
        portfolio_df['Real_Portfolio_Value'] = real_values
        portfolio_value_real = real_values[-1] if real_values else 0
    else:
        portfolio_df['Real_Portfolio_Value'] = portfolio_df['Nominal_Portfolio_Value']
        portfolio_value_real = portfolio_value_nominal
    
    # Calculate net benefit
    net_benefit = portfolio_value_nominal + total_withdrawn - total_invested
    
    return portfolio_value_nominal, portfolio_value_real, total_invested, total_withdrawn, net_benefit, portfolio_df

def create_growth_chart(df: pd.DataFrame, chart_type: str) -> go.Figure:
    """Create interactive growth chart using Plotly."""
    fig = go.Figure()
    
    if chart_type == "Portfolio":
        # Portfolio chart with nominal vs real values
        if 'Total_SIP_Invested' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['Year'], 
                y=df['Total_SIP_Invested'],
                mode='lines+markers',
                name='SIP Invested',
                line=dict(color='lightblue', width=2),
                fill=None
            ))
        
        if 'Total_Lumpsum_Invested' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['Year'], 
                y=df['Total_Lumpsum_Invested'],
                mode='lines+markers',
                name='Lumpsum Invested',
                line=dict(color='lightgreen', width=2),
                fill=None
            ))
        
        fig.add_trace(go.Scatter(
            x=df['Year'], 
            y=df['Nominal_Portfolio_Value'],
            mode='lines+markers',
            name='Nominal Portfolio Value',
            line=dict(color='blue', width=3)
        ))
        
        if 'Real_Portfolio_Value' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['Year'], 
                y=df['Real_Portfolio_Value'],
                mode='lines+markers',
                name='Real Portfolio Value (Inflation Adjusted)',
                line=dict(color='red', width=3, dash='dash')
            ))
        
        if 'Total_Withdrawn' in df.columns and df['Total_Withdrawn'].sum() > 0:
            fig.add_trace(go.Scatter(
                x=df['Year'], 
                y=df['Total_Withdrawn'],
                mode='lines+markers',
                name='Total Withdrawn',
                line=dict(color='orange', width=3)
            ))
        
        fig.update_layout(title="Portfolio Growth: Nominal vs Real Values")
        
    elif chart_type == "Combined":
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
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def display_results(final_amount: float, total_invested: float, df: pd.DataFrame, chart_type: str, total_withdrawn: float = 0.0, real_final_amount: float = None, inflation_rate: float = 0.0):
    """Display calculation results with metrics, table, and chart."""
    
    if chart_type == "Portfolio":
        # Portfolio-level metrics with inflation adjustment
        st.subheader("📊 Portfolio Summary")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Invested", f"₹{total_invested:,.2f}")
        with col2:
            st.metric("Nominal Final Value", f"₹{final_amount:,.2f}")
        with col3:
            if real_final_amount is not None and inflation_rate > 0:
                st.metric("Real Final Value", f"₹{real_final_amount:,.2f}", 
                         delta=f"-₹{final_amount - real_final_amount:,.2f}")
            else:
                st.metric("Real Final Value", f"₹{final_amount:,.2f}")
        with col4:
            if total_withdrawn > 0:
                st.metric("Total Withdrawn", f"₹{total_withdrawn:,.2f}")
            else:
                st.metric("Nominal Returns", f"₹{final_amount - total_invested:,.2f}")
        with col5:
            net_benefit = final_amount + total_withdrawn - total_invested
            st.metric("Net Benefit", f"₹{net_benefit:,.2f}")
        
        # Additional portfolio breakdown if inflation is applied
        if inflation_rate > 0:
            st.info(f"💡 **Inflation Impact**: At {inflation_rate}% annual inflation, your purchasing power is reduced. "
                   f"The real value represents what your money can actually buy in today's terms.")
        
        # Investment type breakdown
        if not df.empty:
            st.subheader("💼 Investment Breakdown")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'Total_SIP_Invested' in df.columns:
                    sip_invested = df['Total_SIP_Invested'].iloc[-1] if not df.empty else 0
                    sip_value = df['Total_SIP_Value'].iloc[-1] if 'Total_SIP_Value' in df.columns else 0
                    st.metric("SIP Investment", f"₹{sip_invested:,.2f}")
                    if sip_value > 0:
                        st.metric("SIP Current Value", f"₹{sip_value:,.2f}")
            
            with col2:
                if 'Rollover_Lumpsum_Invested' in df.columns and 'Additional_Lumpsum_Invested' in df.columns:
                    rollover_invested = df['Rollover_Lumpsum_Invested'].iloc[-1] if not df.empty else 0
                    additional_invested = df['Additional_Lumpsum_Invested'].iloc[-1] if not df.empty else 0
                    lumpsum_value = df['Total_Lumpsum_Value'].iloc[-1] if 'Total_Lumpsum_Value' in df.columns else 0
                    
                    st.metric("Rollover Lumpsum", f"₹{rollover_invested:,.2f}")
                    st.metric("Additional Lumpsum", f"₹{additional_invested:,.2f}")
                    if lumpsum_value > 0:
                        st.metric("Total Lumpsum Value", f"₹{lumpsum_value:,.2f}")
                elif 'Total_Lumpsum_Invested' in df.columns:
                    lumpsum_invested = df['Total_Lumpsum_Invested'].iloc[-1] if not df.empty else 0
                    lumpsum_value = df['Total_Lumpsum_Value'].iloc[-1] if 'Total_Lumpsum_Value' in df.columns else 0
                    st.metric("Lumpsum Investment", f"₹{lumpsum_invested:,.2f}")
                    if lumpsum_value > 0:
                        st.metric("Lumpsum Current Value", f"₹{lumpsum_value:,.2f}")
            
            with col3:
                if total_withdrawn > 0:
                    st.metric("Total Withdrawals", f"₹{total_withdrawn:,.2f}")
                    avg_withdrawal = total_withdrawn / len(df) / 12 if len(df) > 0 else 0
                    st.metric("Avg Monthly Withdrawal", f"₹{avg_withdrawal:,.2f}")
    
    elif chart_type == "Combined":
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
    st.subheader("📅 Year-wise Breakdown")
    st.dataframe(df, use_container_width=True)
    
    # Display chart
    st.subheader("📈 Growth Visualization")
    fig = create_growth_chart(df, chart_type)
    st.plotly_chart(fig, use_container_width=True)
    
def portfolio_investment_section(phase_num: int = 1, rollover_nominal: float = 0.0, cumulative_years_before_phase: int = 0):
    """Portfolio investment section UI with multiple parallel investments."""
    st.subheader(f"🎯 Portfolio Calculator - Phase {phase_num}")
    
    if rollover_nominal > 0:
        st.info(f"💰 **Rollover from Previous Phase**: ₹{rollover_nominal:,.2f} (will be treated as Lumpsum investment)")
    
    if cumulative_years_before_phase > 0:
        st.info(f"📅 **Cumulative Timeline**: {cumulative_years_before_phase} years have elapsed since start of investment plan")
    
    # Initialize session state for multiple investments
    if f'sips_{phase_num}' not in st.session_state:
        st.session_state[f'sips_{phase_num}'] = []
    if f'lumpsums_{phase_num}' not in st.session_state:
        st.session_state[f'lumpsums_{phase_num}'] = []
    if f'swps_{phase_num}' not in st.session_state:
        st.session_state[f'swps_{phase_num}'] = []
    
    # Common parameters
    st.markdown("### 📊 Common Parameters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        years = st.number_input(
            "Investment Duration (Years)", 
            min_value=1, 
            value=10,
            key=f"portfolio_years_{phase_num}"
        )
    
    with col2:
        inflation_rate = st.number_input(
            "Annual Inflation Rate (%)", 
            min_value=0.0, 
            value=6.0,
            key=f"inflation_rate_{phase_num}",
            help="Used to calculate real (inflation-adjusted) values for reporting"
        )
    
    with col3:
        st.markdown("**Portfolio Actions**")
        if st.button("🔄 Clear All Investments", key=f"clear_all_{phase_num}"):
            st.session_state[f'sips_{phase_num}'] = []
            st.session_state[f'lumpsums_{phase_num}'] = []
            st.session_state[f'swps_{phase_num}'] = []
            st.success("All investments cleared!")
    
    # Rollover + Additional Lumpsum Section
    st.markdown("### 💰 Lumpsum Investment (Rollover + Additional)")
    col1, col2 = st.columns(2)
    
    with col1:
        additional_lumpsum = st.number_input(
            "Additional Lumpsum Amount (₹)", 
            min_value=0.0, 
            value=0.0,
            key=f"additional_lumpsum_{phase_num}",
            help="Additional lumpsum to add to rollover amount"
        )
        
        total_lumpsum = rollover_nominal + additional_lumpsum
        st.info(f"**Total Lumpsum**: ₹{rollover_nominal:,.2f} (rollover) + ₹{additional_lumpsum:,.2f} (additional) = ₹{total_lumpsum:,.2f}")
    
    with col2:
        lumpsum_roi = st.number_input(
            "Lumpsum ROI (%)", 
            min_value=0.0, 
            value=12.0,
            key=f"lumpsum_roi_{phase_num}",
            help="ROI for combined lumpsum (rollover + additional)"
        )
        
        if total_lumpsum > 0:
            projected_value = total_lumpsum * ((1 + lumpsum_roi / 100) ** years)
            st.metric("Projected Lumpsum Value", f"₹{projected_value:,.2f}")
    
    # SIP Section
    st.markdown("### 📈 SIP Investments")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("*Add multiple SIP investments with different amounts and returns*")
    with col2:
        if st.button("➕ Add SIP", key=f"add_sip_{phase_num}"):
            st.session_state[f'sips_{phase_num}'].append({
                'amount': 5000, 'rate': 12, 'step_up': 10
            })
    
    # Display existing SIPs
    sips_to_remove = []
    for i, sip in enumerate(st.session_state[f'sips_{phase_num}']):
        with st.expander(f"SIP {i+1}: ₹{sip['amount']:,}/month @ {sip['rate']}%", expanded=True):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                sip['amount'] = st.number_input(
                    "Monthly Amount (₹)", 
                    min_value=0.0, 
                    value=float(sip['amount']),
                    key=f"sip_amount_{phase_num}_{i}"
                )
            
            with col2:
                sip['rate'] = st.number_input(
                    "Annual Return (%)", 
                    min_value=0.0, 
                    value=float(sip['rate']),
                    key=f"sip_rate_{phase_num}_{i}"
                )
            
            with col3:
                sip['step_up'] = st.number_input(
                    "Annual Step-up (%)", 
                    min_value=0.0, 
                    value=float(sip['step_up']),
                    key=f"sip_stepup_{phase_num}_{i}"
                )
            
            with col4:
                if st.button("🗑️", key=f"remove_sip_{phase_num}_{i}", help="Remove this SIP"):
                    sips_to_remove.append(i)
    
    # Remove SIPs marked for deletion
    for i in reversed(sips_to_remove):
        st.session_state[f'sips_{phase_num}'].pop(i)
        st.rerun()
    
    # Other Lumpsum Section (separate from rollover)
    st.markdown("### � Other Lumpsum Investments")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("*Add other lumpsum investments separate from rollover amount*")
    with col2:
        if st.button("➕ Add Other Lumpsum", key=f"add_other_lumpsum_{phase_num}"):
            st.session_state[f'lumpsums_{phase_num}'].append({
                'amount': 100000, 'rate': 12
            })
    
    # Display existing Other Lumpsums
    lumpsums_to_remove = []
    for i, lumpsum in enumerate(st.session_state[f'lumpsums_{phase_num}']):
        with st.expander(f"Other Lumpsum {i+1}: ₹{lumpsum['amount']:,} @ {lumpsum['rate']}%", expanded=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                lumpsum['amount'] = st.number_input(
                    "Lumpsum Amount (₹)", 
                    min_value=0.0, 
                    value=float(lumpsum['amount']),
                    key=f"other_lumpsum_amount_{phase_num}_{i}"
                )
            
            with col2:
                lumpsum['rate'] = st.number_input(
                    "Annual Return (%)", 
                    min_value=0.0, 
                    value=float(lumpsum['rate']),
                    key=f"other_lumpsum_rate_{phase_num}_{i}"
                )
            
            with col3:
                if st.button("🗑️", key=f"remove_other_lumpsum_{phase_num}_{i}", help="Remove this Lumpsum"):
                    lumpsums_to_remove.append(i)
    
    # Remove Other Lumpsums marked for deletion
    for i in reversed(lumpsums_to_remove):
        st.session_state[f'lumpsums_{phase_num}'].pop(i)
        st.rerun()
    
    # SWP Section
    st.markdown("### 🏦 SWP (Withdrawal) Plans")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("*Add withdrawal plans from your portfolio*")
    with col2:
        if st.button("➕ Add SWP", key=f"add_swp_{phase_num}"):
            st.session_state[f'swps_{phase_num}'].append({
                'amount': 10000, 'rate': 8, 'start_year': 1
            })
    
    # Display existing SWPs
    swps_to_remove = []
    for i, swp in enumerate(st.session_state[f'swps_{phase_num}']):
        with st.expander(f"SWP {i+1}: ₹{swp['amount']:,}/month from Year {swp['start_year']}", expanded=True):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                swp['amount'] = st.number_input(
                    "Monthly Withdrawal (₹)", 
                    min_value=0.0, 
                    value=float(swp['amount']),
                    key=f"swp_amount_{phase_num}_{i}"
                )
            
            with col2:
                swp['rate'] = st.number_input(
                    "Return Rate During SWP (%)", 
                    min_value=0.0, 
                    value=float(swp['rate']),
                    key=f"swp_rate_{phase_num}_{i}"
                )
            
            with col3:
                swp['start_year'] = st.number_input(
                    "Start Year", 
                    min_value=1, 
                    max_value=years,
                    value=int(swp['start_year']),
                    key=f"swp_start_{phase_num}_{i}"
                )
            
            with col4:
                if st.button("🗑️", key=f"remove_swp_{phase_num}_{i}", help="Remove this SWP"):
                    swps_to_remove.append(i)
    
    # Remove SWPs marked for deletion
    for i in reversed(swps_to_remove):
        st.session_state[f'swps_{phase_num}'].pop(i)
        st.rerun()
    
    # Portfolio summary
    if st.session_state[f'sips_{phase_num}'] or st.session_state[f'lumpsums_{phase_num}'] or st.session_state[f'swps_{phase_num}'] or total_lumpsum > 0:
        st.markdown("### 📋 Portfolio Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("SIP Investments", len(st.session_state[f'sips_{phase_num}']))
        with col2:
            st.metric("Other Lumpsum Investments", len(st.session_state[f'lumpsums_{phase_num}']))
        with col3:
            st.metric("SWP Plans", len(st.session_state[f'swps_{phase_num}']))
        with col4:
            st.metric("Total Lumpsum", f"₹{total_lumpsum:,.0f}")
    
    # Calculate button
    has_investments = (st.session_state[f'sips_{phase_num}'] or 
                      st.session_state[f'lumpsums_{phase_num}'] or 
                      total_lumpsum > 0)
    
    if st.button(f"🧮 Calculate Portfolio - Phase {phase_num}", 
                key=f"calc_portfolio_{phase_num}", 
                type="primary",
                disabled=not has_investments):
        
        if has_investments and years > 0:
            # Perform portfolio calculation with updated parameters
            nominal_final, real_final, total_invested, total_withdrawn, net_benefit, portfolio_df = calculate_combined_portfolio_parallel(
                sips_list=st.session_state[f'sips_{phase_num}'],
                lumpsums_list=st.session_state[f'lumpsums_{phase_num}'],
                swps_list=st.session_state[f'swps_{phase_num}'],
                years=years,
                rollover_nominal=rollover_nominal,
                additional_lumpsum=additional_lumpsum,
                lumpsum_roi=lumpsum_roi,
                inflation_rate=inflation_rate,
                phase_start_year=cumulative_years_before_phase
            )
            
            st.session_state[f'portfolio_result_{phase_num}'] = {
                'nominal_final': nominal_final,
                'real_final': real_final,
                'total_invested': total_invested,
                'total_withdrawn': total_withdrawn,
                'net_benefit': net_benefit,
                'portfolio_df': portfolio_df,
                'inflation_rate': inflation_rate,
                'rollover_nominal': rollover_nominal,
                'additional_lumpsum': additional_lumpsum,
                'lumpsum_roi': lumpsum_roi
            }
        else:
            st.error("Please add at least one investment or ensure you have a rollover amount.")
    
    # Display results if available
    if f'portfolio_result_{phase_num}' in st.session_state:
        result = st.session_state[f'portfolio_result_{phase_num}']
        display_results(
            final_amount=result['nominal_final'],
            total_invested=result['total_invested'],
            df=result['portfolio_df'],
            chart_type="Portfolio",
            total_withdrawn=result['total_withdrawn'],
            real_final_amount=result['real_final'],
            inflation_rate=result['inflation_rate']
        )
        return result['nominal_final']  # Return nominal value for rollover
    
    return None

def old_combined_investment_section(phase_num: int = 1, initial_amount: float = 0.0):
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
    st.title("🏦 Advanced Portfolio Financial Calculator")
    st.markdown("*Multi-phase portfolio planning with parallel investments & inflation adjustment*")
    st.markdown("---")
    
    # Initialize session state for phases
    if 'num_phases' not in st.session_state:
        st.session_state.num_phases = 1
    
    # Phase management
    st.sidebar.header("📊 Investment Phases")
    st.sidebar.markdown("*Build sophisticated multi-phase investment strategies*")
    
    if st.sidebar.button("➕ Add Next Phase"):
        st.session_state.num_phases += 1
        st.sidebar.success(f"Phase {st.session_state.num_phases} added!")
    
    if st.sidebar.button("🗑️ Reset All Phases"):
        st.session_state.num_phases = 1
        # Clear all results
        keys_to_remove = [key for key in st.session_state.keys() if 'result_' in key or 'sips_' in key or 'lumpsums_' in key or 'swps_' in key]
        for key in keys_to_remove:
            del st.session_state[key]
        st.sidebar.success("All phases reset!")
    
    st.sidebar.write(f"**Current Phases:** {st.session_state.num_phases}")
    
    # Instructions
    with st.expander("📋 Portfolio Calculator Features", expanded=False):
        st.markdown("""
        **🎯 Multiple Parallel Investments:**
        - **Multiple SIPs**: Add different SIP amounts with varying return rates
        - **Multiple Lumpsums**: Invest different amounts across various instruments
        - **Multiple SWPs**: Set up multiple withdrawal streams with different rates
        
        **💰 Advanced Features:**
        - **Inflation Adjustment**: See both nominal and real (inflation-adjusted) values
        - **Portfolio Diversification**: Mix investments with different risk-return profiles
        - **Multi-Phase Planning**: Chain strategies across different life phases
        
        **🔄 Real-World Scenarios:**
        1. **Diversified SIP Portfolio**: ₹10K in equity funds (15% return) + ₹5K in debt funds (8% return)
        2. **Mixed Investment Strategy**: Lumpsum in real estate (12% return) + SIP in equity (18% return)
        3. **Retirement Planning**: Growth phase → Income generation phase with multiple SWPs
        4. **Goal-Based Investing**: Different investments for different financial goals
        """)
    
    # Display phases
    rollover_amount = 0.0
    cumulative_years = 0  # Track total years elapsed since start
    
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
        
        # Portfolio investment section (passing rollover as nominal amount and cumulative years)
        phase_result = portfolio_investment_section(phase, rollover_amount, cumulative_years)
        
        # Update rollover amount and cumulative years for next phase (using nominal value only)
        if phase_result is not None:
            rollover_amount = phase_result  # This is the nominal final amount
            
            # Get the duration of the current phase to update cumulative years
            if f'portfolio_result_{phase}' in st.session_state:
                result = st.session_state[f'portfolio_result_{phase}']
                if 'portfolio_df' in result and not result['portfolio_df'].empty:
                    phase_years = len(result['portfolio_df'])
                    cumulative_years += phase_years
            
            if phase < st.session_state.num_phases:
                st.success(f"✅ Phase {phase} completed! **Nominal amount** ₹{rollover_amount:,.2f} will roll over to Phase {phase + 1} as Lumpsum investment")
                st.info(f"📅 **Cumulative Years**: {cumulative_years} years have elapsed since start of investment plan")
        
        st.markdown("---")
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with ❤️ using Streamlit | Advanced Portfolio Calculator v3.0*")
    st.markdown("*Features: Multi-parallel investments, Inflation adjustment, Multi-phase planning*")

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
    import math
    
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
    print(f'\n🎯 All tests passed! Cumulative inflation logic is correct.')
    
if __name__ == "__main__":
    import sys
    
    # Run test if --test argument is provided
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_cumulative_inflation_logic()
    else:
        main()
