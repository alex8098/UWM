import streamlit as st
from utils import (
    adjust_process,
    calculate_line_performance,
    display_summary,
    plot_cost_profit_analysis_line
)
import plotly.graph_objects as go
import pandas as pd

def plot_waterfall(results):
    rev = results["Total_Revenue"]
    cap = results["Total_Capital_Cost"]
    oh  = results["Total_Overhead_Cost"]
    fail= results["Total_Fail_Cost"]
    mat = results["Total_Material_Cost"]
    prof= results["Profit"]

    data = {
        'Label': ['Umsatz','Anschaffungskosten','Gemeinkosten','Fehlerkosten','Materialkosten','Gewinn'],
        'Value': [rev, -cap, -oh, -fail, -mat, prof],
        'Measure': ['relative','relative','relative','relative','relative','total']
    }
    df_wf = pd.DataFrame(data)

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=df_wf['Measure'],
        x=df_wf['Label'],
        y=df_wf['Value'],
        text=df_wf['Value'],
        textposition="outside",
        connector={"line":{"color":"gray"}},
        decreasing={"marker":{"color":"tomato"}},
        increasing={"marker":{"color":"mediumseagreen"}},
        totals={"marker":{"color":"lightskyblue"}}
    ))
    fig.update_layout(
        title="Waterfall: Umsatz - Kosten = Gewinn",
        template='plotly_white'
    )
    return fig

def plot_cost_breakdown_per_step(results):
    df = results["df"].copy()
    df['Kapitalkosten'] = df['Anschaffungskosten (€)'] * df['Maschinen']
    fail_costs = []
    units_in = results["T_ideal"]
    for _, row in df.iterrows():
        step_fail = units_in * row['fail_rate']
        cost = step_fail * row['Kosten pro fehlerhafte Einheit (€)']
        fail_costs.append(cost)
        units_in = units_in - step_fail
    df['Fehlerkosten (Schritt)'] = fail_costs

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Schritt'],
        y=df['Kapitalkosten'],
        name='Kapitalkosten',
        marker_color='lightsalmon'
    ))
    fig.add_trace(go.Bar(
        x=df['Schritt'],
        y=df['Gemeinkosten (€)'],
        name='Gemeinkosten',
        marker_color='lightblue'
    ))
    fig.add_trace(go.Bar(
        x=df['Schritt'],
        y=df['Fehlerkosten (Schritt)'],
        name='Fehlerkosten',
        marker_color='pink'
    ))
    fig.update_layout(
        title="Kostenaufteilung pro Schritt",
        xaxis_title='Schritt',
        yaxis_title='Kosten (€)',
        barmode='stack',
        template='plotly_white'
    )
    return fig

def main():
    st.title("Gewinnanalyse")

    steps, runtime, sale_price, material_cost = adjust_process()
    results = calculate_line_performance(steps, runtime, sale_price, material_cost)

    display_summary(results)

    st.markdown("## Kosten- und Gewinnanalyse über die Laufzeit")
    line_fig = plot_cost_profit_analysis_line(results)
    st.plotly_chart(line_fig, use_container_width=True)

    st.markdown("## Waterfall-Diagramm")
    wf_fig = plot_waterfall(results)
    st.plotly_chart(wf_fig, use_container_width=True)

    st.markdown("## Kostenaufteilung pro Schritt")
    breakdown_fig = plot_cost_breakdown_per_step(results)
    st.plotly_chart(breakdown_fig, use_container_width=True)

if __name__ == "__main__":
    main()
