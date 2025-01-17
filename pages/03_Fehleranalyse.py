import streamlit as st
from utils import (
    adjust_process,
    calculate_line_performance,
    display_summary
)
import pandas as pd
import plotly.graph_objects as go

def plot_sankey(steps, input_units=100):
    df = pd.DataFrame(steps)
    df['fail_rate'] = df['Fehlerquote (%)'] / 100.0

    labels = df['Schritt'].tolist()
    source, target, value = [], [], []

    current_units = input_units
    for i in range(len(df)):
        fail_here = current_units * df.loc[i, 'fail_rate']
        good_out = current_units - fail_here

        if i < len(df) - 1:
            source.append(i)
            target.append(i+1)
            value.append(good_out)

        defect_label = f"Fehler_{df.loc[i, 'Schritt']}"
        labels.append(defect_label)
        defect_idx = len(labels) - 1
        source.append(i)
        target.append(defect_idx)
        value.append(fail_here)

        current_units = good_out

    colors = ["blue" if not lbl.startswith("Fehler_") else "red" for lbl in labels]

    fig = go.Figure(go.Sankey(
        node=dict(
            label=labels,
            color=colors,
            pad=20,
            thickness=30
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    ))
    fig.update_layout(
        title="Materialfluss & Fehleranalyse (Sankey)",
        template='plotly_white'
    )
    return fig

def main():
    st.title("Fehleranalyse")

    steps, runtime, sale_price, material_cost = adjust_process()
    results = calculate_line_performance(steps, runtime, sale_price, material_cost)

    display_summary(results)

    st.markdown("## Sankey-Diagramm")
    sankey_fig = plot_sankey(steps, input_units=100)
    st.plotly_chart(sankey_fig, use_container_width=True)

    st.markdown("## Übersicht über Fehlerkosten")
    df = results["df"].copy()
    fail_costs = []
    units_in = results["T_ideal"]
    for i, row in df.iterrows():
        step_fail = units_in * row['fail_rate']
        cost_step = step_fail * row['Kosten pro fehlerhafte Einheit (€)']
        fail_costs.append(cost_step)
        units_in = units_in - step_fail

    df['Fehlerkosten (geschätzt)'] = fail_costs
    st.dataframe(df[['Schritt','Fehlerquote (%)','Kosten pro fehlerhafte Einheit (€)','Fehlerkosten (geschätzt)']])
    st.write(f"**Gesamte Fehlerkosten (geschätzt)**: €{sum(fail_costs):.2f}")

if __name__ == "__main__":
    main()
