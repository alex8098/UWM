# 01_Main.py
import streamlit as st
from utils import (
    adjust_process,
    calculate_line_performance,
    display_summary,
    plot_cost_profit_analysis_line
)

def main():
    st.title("📈 Umwelt & Wertschöpfungsmanagement: Papierflugzeugproduktion")

    steps, runtime, sale_price, material_cost = adjust_process()  # Sidebar
    results = calculate_line_performance(steps, runtime, sale_price, material_cost)

    # Show the top half (table + metrics)
    display_summary(results)

    st.markdown("## Kosten- und Gewinnanalyse über die Laufzeit")
    line_fig = plot_cost_profit_analysis_line(results)
    st.plotly_chart(line_fig, use_container_width=True)


if __name__ == "__main__":
    main()
