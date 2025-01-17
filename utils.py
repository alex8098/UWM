import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from copy import deepcopy

DEFAULT_STEPS = [
    {
        "Schritt": "Materialeingang",
        "Zykluszeit (Minuten)": 3.0,
        "Maschinen": 1,
        "Anschaffungskosten (€)": 50.0,
        "Stillstandskostenrate (€/Min)": 0.10,
        "Fehlerquote (%)": 3.0,
        "Kosten pro fehlerhafte Einheit (€)": 2.0
    },
    {
        "Schritt": "Schneiden",
        "Zykluszeit (Minuten)": 6.0,
        "Maschinen": 1,
        "Anschaffungskosten (€)": 100.0,
        "Stillstandskostenrate (€/Min)": 1.20,
        "Fehlerquote (%)": 2.0,
        "Kosten pro fehlerhafte Einheit (€)": 5.0
    },
    {
        "Schritt": "Montage",
        "Zykluszeit (Minuten)": 10.0,
        "Maschinen": 1,
        "Anschaffungskosten (€)": 200.0,
        "Stillstandskostenrate (€/Min)": 2,
        "Fehlerquote (%)": 3.0,
        "Kosten pro fehlerhafte Einheit (€)": 10.0
    },
    {
        "Schritt": "Bemalen",
        "Zykluszeit (Minuten)": 4.0,
        "Maschinen": 1,
        "Anschaffungskosten (€)": 800.0,
        "Stillstandskostenrate (€/Min)": 4,
        "Fehlerquote (%)": 4.5,
        "Kosten pro fehlerhafte Einheit (€)": 15.0
    },
    {
        "Schritt": "Qualitätsprüfung",
        "Zykluszeit (Minuten)": 5.0,
        "Maschinen": 1,
        "Anschaffungskosten (€)": 120.0,
        "Stillstandskostenrate (€/Min)": 2.25,
        "Fehlerquote (%)": 12.0,
        "Kosten pro fehlerhafte Einheit (€)": 25.0
    },
    {
        "Schritt": "Versand",
        "Zykluszeit (Minuten)": 3.0,
        "Maschinen": 1,
        "Anschaffungskosten (€)": 70.0,
        "Stillstandskostenrate (€/Min)": 1.5,
        "Fehlerquote (%)": 0.5,
        "Kosten pro fehlerhafte Einheit (€)": 2.0
    }
]


def add_new_step(steps, new_step):
    steps.append(new_step)
    return steps

def remove_steps(steps, steps_to_remove):
    return [step for step in steps if step["Schritt"] not in steps_to_remove]

def move_step(steps, index, direction):
    if direction == "up" and index > 0:
        steps[index], steps[index-1] = steps[index-1], steps[index]
    elif direction == "down" and index < len(steps)-1:
        steps[index], steps[index+1] = steps[index+1], steps[index]
    return steps


def adjust_process():
    """
    Ensures the sidebar is shown on every page.
    Returns (steps, runtime, sale_price, material_cost).
    """
    #If not in session, load default steps
    if "steps" not in st.session_state:
        st.session_state.steps = deepcopy(DEFAULT_STEPS)

    steps = st.session_state.steps  # current steps

    st.sidebar.header("Produktionsprozess anpassen")

    runtime = st.sidebar.number_input(
        "Laufzeit (Minuten)",
        min_value=1,
        max_value=10000,
        value=480,
        step=1,
        key="sidebar_runtime"
    )

    sale_price = st.sidebar.number_input(
        "Verkaufspreis pro Einheit (Endprodukt) (€)",
        min_value=0.0,
        max_value=10000.0,
        value=300.0,
        step=1.0,
        key="sidebar_sale_price"
    )
    material_cost = st.sidebar.number_input(
        "Materialkosten pro Einheit (€)",
        min_value=0.0,
        max_value=10000.0,
        value=25.0,
        step=1.0,
        key="sidebar_mat_cost"
    )

    st.sidebar.subheader("Bestehende Schritte bearbeiten")
    for index, step in enumerate(steps):
        with st.sidebar.expander(f"{step['Schritt']} bearbeiten"):
            step['Zykluszeit (Minuten)'] = st.number_input(
                f"Zykluszeit für {step['Schritt']} (Min)",
                min_value=0.1,
                max_value=10000.0,
                value=float(step['Zykluszeit (Minuten)']),
                step=0.1,
                key=f"zykluszeit_{index}"
            )
            step['Maschinen'] = st.number_input(
                f"Anzahl Maschinen für {step['Schritt']}",
                min_value=1,
                max_value=10,
                value=int(step['Maschinen']),
                step=1,
                key=f"maschinen_{index}"
            )
            step['Anschaffungskosten (€)'] = st.number_input(
                f"Anschaffungskosten pro Maschine für {step['Schritt']} (€)",
                min_value=0.0,
                max_value=100000.0,
                value=float(step['Anschaffungskosten (€)']),
                step=100.0,
                key=f"anschaffung_{index}"
            )
            step['Stillstandskostenrate (€/Min)'] = st.number_input(
                f"Stillstandskostenrate pro Maschine für {step['Schritt']} (€/Min)",
                min_value=0.0,
                max_value=10000.0,
                value=float(step['Stillstandskostenrate (€/Min)']),
                step=0.1,
                key=f"idle_cost_{index}"
            )
            step['Fehlerquote (%)'] = st.number_input(
                f"Fehlerquote für {step['Schritt']} (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(step['Fehlerquote (%)']),
                step=0.1,
                key=f"fail_rate_{index}"
            )
            step['Kosten pro fehlerhafte Einheit (€)'] = st.number_input(
                f"Kosten pro fehlerhafte Einheit für {step['Schritt']} (€)",
                min_value=0.0,
                max_value=10000.0,
                value=float(step['Kosten pro fehlerhafte Einheit (€)']),
                step=1.0,
                key=f"fail_cost_{index}"
            )
            col_move1, col_move2 = st.columns(2)
            with col_move1:
                if st.button("Nach oben verschieben", key=f"move_up_{index}"):
                    st.session_state.steps = move_step(st.session_state.steps, index, "up")
            with col_move2:
                if st.button("Nach unten verschieben", key=f"move_down_{index}"):
                    st.session_state.steps = move_step(st.session_state.steps, index, "down")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Neuen Schritt hinzufügen")
    new_step_name = st.sidebar.text_input("Name des neuen Schritts")
    if new_step_name:
        with st.sidebar.expander(f"{new_step_name} konfigurieren"):
            new_cycle_time = st.number_input(
                f"Zykluszeit für {new_step_name} (Min)",
                min_value=0.1,
                max_value=10000.0,
                value=5.0,
                step=0.1,
                key="new_cycle_time"
            )
            new_stations = st.number_input(
                f"Anzahl Maschinen für {new_step_name}",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                key="new_stations"
            )
            new_capital_cost = st.number_input(
                f"Anschaffungskosten pro Maschine für {new_step_name} (€)",
                min_value=0.0,
                max_value=100000.0,
                value=1000.0,
                step=100.0,
                key="new_capital_cost"
            )
            new_idle_cost = st.number_input(
                f"Stillstandskostenrate pro Maschine für {new_step_name} (€/Min)",
                min_value=0.0,
                max_value=10000.0,
                value=0.5,
                step=0.1,
                key="new_idle_cost"
            )
            new_fail_rate = st.number_input(
                f"Fehlerquote für {new_step_name} (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="new_fail_rate"
            )
            new_fail_cost = st.number_input(
                f"Kosten pro fehlerhafte Einheit für {new_step_name} (€)",
                min_value=0.0,
                max_value=10000.0,
                value=0.0,
                step=1.0,
                key="new_fail_cost"
            )
            if st.button("Schritt hinzufügen"):
                s = {
                    "Schritt": new_step_name,
                    "Zykluszeit (Minuten)": new_cycle_time,
                    "Maschinen": new_stations,
                    "Anschaffungskosten (€)": new_capital_cost,
                    "Stillstandskostenrate (€/Min)": new_idle_cost,
                    "Fehlerquote (%)": new_fail_rate,
                    "Kosten pro fehlerhafte Einheit (€)": new_fail_cost
                }
                st.session_state.steps = add_new_step(st.session_state.steps, s)
                st.sidebar.success(f"Schritt '{new_step_name}' hinzugefügt!")
                #st.sidebar.experimental_rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("Schritte entfernen")
    steps_to_remove = st.sidebar.multiselect(
        "Zu entfernende Schritte auswählen", 
        options=[step["Schritt"] for step in st.session_state.steps]
    )
    if steps_to_remove:
        if st.sidebar.button("Ausgewählte Schritte entfernen"):
            st.session_state.steps = remove_steps(st.session_state.steps, steps_to_remove)
            st.sidebar.success(f"Entfernte Schritte: {', '.join(steps_to_remove)}")
           # st.sidebar.experimental_rerun()
    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Eine Demo App zur Veranschaulichung von Lean Prinzipen von Lars Mertens, "
        "Chaerim Kim, Leon Strauch und Alexander Johae"
    )

    return st.session_state.steps, runtime, sale_price, material_cost


def calculate_line_performance(steps, runtime, sale_price, material_cost):
    df = pd.DataFrame(steps)
    df['Effektive Zykluszeit (Minuten)'] = df['Zykluszeit (Minuten)'] / df['Maschinen']
    df['fail_rate'] = df['Fehlerquote (%)'] / 100.0

    T_ideal = (runtime / df['Effektive Zykluszeit (Minuten)']).min()

    df['Idle_Time (Min)'] = runtime - (T_ideal * df['Effektive Zykluszeit (Minuten)'])
    df['Idle_Time (Min)'] = df['Idle_Time (Min)'].apply(lambda x: x if x > 0 else 0.0)
    df['Gemeinkosten (€)'] = df['Idle_Time (Min)'] * df['Stillstandskostenrate (€/Min)'] * df['Maschinen']

    units_in = T_ideal
    total_fail_cost = 0.0
    for i, row in df.iterrows():
        step_fail = units_in * row['fail_rate']
        step_out = units_in * (1 - row['fail_rate'])
        step_fail_cost = step_fail * row['Kosten pro fehlerhafte Einheit (€)']
        total_fail_cost += step_fail_cost
        units_in = step_out

    final_good_units = units_in
    total_capital_cost = (df['Anschaffungskosten (€)'] * df['Maschinen']).sum()
    total_overhead_cost = df['Gemeinkosten (€)'].sum()
    total_material_cost = T_ideal * material_cost
    total_revenue = final_good_units * sale_price
    total_costs = total_capital_cost + total_overhead_cost + total_fail_cost + total_material_cost
    profit = total_revenue - total_costs

    results = {
        "df": df,
        "Final_Good_Units": final_good_units,
        "T_ideal": T_ideal,
        "Total_Capital_Cost": total_capital_cost,
        "Total_Overhead_Cost": total_overhead_cost,
        "Total_Fail_Cost": total_fail_cost,
        "Total_Material_Cost": total_material_cost,
        "Total_Revenue": total_revenue,
        "Profit": profit,
        "Runtime": runtime
    }
    return results

#Display the top summary

def display_summary(results):
    """
    Shows the same table + metrics the main page uses,
    so that ALL pages (Gewinnanalyse, Fehleranalyse) 
    can have the identical top half.
    """
    df_display = results["df"].copy()
    df_display = df_display[[
        "Schritt",
        "Zykluszeit (Minuten)",
        "Maschinen",
        "Anschaffungskosten (€)",
        "Stillstandskostenrate (€/Min)",
        "Fehlerquote (%)",
        "Kosten pro fehlerhafte Einheit (€)",
        "Idle_Time (Min)",
        "Gemeinkosten (€)"
    ]]

    st.markdown("## Produktionsprozess")
    st.dataframe(df_display.style.format({
        "Zykluszeit (Minuten)": "{:.2f}",
        "Maschinen": "{:.0f}",
        "Anschaffungskosten (€)": "€{:,.2f}",
        "Stillstandskostenrate (€/Min)": "€{:,.2f}",
        "Fehlerquote (%)": "{:.1f}%",
        "Kosten pro fehlerhafte Einheit (€)": "€{:,.2f}",
        "Idle_Time (Min)": "{:.2f}",
        "Gemeinkosten (€)": "€{:,.2f}"
    }))

    col1, col2 = st.columns(2)
    col1.metric("Produzierte Einheiten (in Laufzeit)", f"{results['Final_Good_Units']:.2f} Einheiten")
    col2.metric("Gesamte Anschaffungskosten (€)", f"€{results['Total_Capital_Cost']:.2f}")

    col3, col4 = st.columns(2)
    col3.metric("Gesamte Gemeinkosten (€)", f"€{results['Total_Overhead_Cost']:.2f}")
    col4.metric("Gesamte Fehlerkosten (€)", f"€{results['Total_Fail_Cost']:.2f}")

    col5, col6 = st.columns(2)
    col5.metric("Gesamte Materialkosten (€)", f"€{results['Total_Material_Cost']:.2f}")
    col6.metric("Gesamtumsatz (€)", f"€{results['Total_Revenue']:.2f}")

    col7, _ = st.columns(2)
    col7.metric("Gewinn (€)", f"€{results['Profit']:.2f}")


def plot_cost_profit_analysis_line(results):
    runtime = int(results["Runtime"])
    df = results["df"]
    lead_time = df['Effektive Zykluszeit (Minuten)'].sum()
    time_range = range(runtime + 1)

    total_capital = results["Total_Capital_Cost"]
    total_overhead = results["Total_Overhead_Cost"]
    total_fail = results["Total_Fail_Cost"]
    total_material = results["Total_Material_Cost"]
    total_revenue = results["Total_Revenue"]

    capital_line = [total_capital]*(runtime+1)
    overhead_line = []
    for t in time_range:
        fraction = t / runtime if runtime>0 else 1
        overhead_line.append(total_overhead * fraction)

    material_line, fail_line, revenue_line = [], [], []
    for t in time_range:
        if t < lead_time or runtime == lead_time:
            material_line.append(0.0)
            fail_line.append(0.0)
            revenue_line.append(0.0)
        else:
            fraction = (t - lead_time)/(runtime - lead_time) if (runtime - lead_time)>0 else 1
            material_line.append(total_material * fraction)
            fail_line.append(total_fail * fraction)
            revenue_line.append(total_revenue * fraction)

    profit_line = []
    for i, _ in enumerate(time_range):
        current_cost = capital_line[i] + overhead_line[i] + material_line[i] + fail_line[i]
        current_revenue = revenue_line[i]
        profit_line.append(current_revenue - current_cost)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(time_range), y=revenue_line, name='Umsatz', mode='lines', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=list(time_range), y=material_line, name='Materialkosten', mode='lines', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=list(time_range), y=overhead_line, name='Gemeinkosten', mode='lines', line=dict(color='red', dash='dot')))
    fig.add_trace(go.Scatter(x=list(time_range), y=fail_line, name='Fehlerkosten', mode='lines', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=list(time_range), y=capital_line, name='Anschaffungskosten', mode='lines', line=dict(color='red', dash='longdash')))
    fig.add_trace(go.Scatter(x=list(time_range), y=profit_line, name='Gewinn', mode='lines', line=dict(color='gold', width=3)))

    fig.update_layout(
        title='Kosten- und Gewinnanalyse über die Laufzeit',
        xaxis_title='Zeit (Min)',
        yaxis_title='Wert (€)',
        template="plotly_white",
        legend_title="Kategorie"
    )
    return fig
