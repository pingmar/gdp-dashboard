import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="SIR Epidemic Model", layout="wide")

# --- Sidebar parameters ---
st.sidebar.title("🔧 Parameters")
beta = st.sidebar.slider("β (infection rate)", 0.1, 0.8, 0.3, 0.05)
gamma = st.sidebar.slider("γ (recovery rate)", 0.05, 0.3, 0.1, 0.01)
population = st.sidebar.slider("Population", 500, 5000, 1000, 100)
initial_infected = st.sidebar.slider("Initially infected", 1, 50, 10, 1)
days = st.sidebar.slider("Simulation days", 50, 300, 160, 10)

# --- SIR simulation ---
S = [population - initial_infected]
I = [initial_infected]
R = [0]
data = []

for t in range(1, days + 1):
    dS = -beta * S[-1] * I[-1] / population
    dI = beta * S[-1] * I[-1] / population - gamma * I[-1]
    dR = gamma * I[-1]

    S.append(S[-1] + dS)
    I.append(I[-1] + dI)
    R.append(R[-1] + dR)

    data.append((t, S[-1], I[-1], R[-1]))

R0 = beta / gamma
max_infected = max(I)
day_of_peak = int(np.argmax(I))
total_infected = population - S[-1]
percent_infected = (total_infected / population) * 100

# --- Display results ---
st.title("📈 Epidemic Spread Model (SIR)")
st.markdown(f"""
**R₀:** {R0:.3f}  
**Peak Infected:** {max_infected:.0f} on day {day_of_peak}  
**Total Infected:** {total_infected:.0f} ({percent_infected:.1f}% of population)
""")

# --- Plot results ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(I, label="Infected (I)", color="r", linewidth=2)
ax.plot(S, label="Susceptible (S)", color="b", linewidth=2)
ax.plot(R, label="Recovered (R)", color="g", linewidth=2)
ax.set_xlabel("Days")
ax.set_ylabel("Number of people")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# --- Generate report ---
report = f"""
SIR MODEL REPORT
══════════════════════════════════════════════

Parameters:
  β (infection rate): {beta}
  γ (recovery rate): {gamma}
  Population: {population}
  Initial infected: {initial_infected}
  Duration: {days} days

Results:
  R₀ = {R0:.3f}
  Peak infected = {max_infected:.0f} (day {day_of_peak})
  Total infected = {total_infected:.0f} ({percent_infected:.1f}%)

Inductive Observations:
  • Higher β → faster spread, higher peak
  • Higher γ → faster recovery, lower peak
  • R₀ > 1 → epidemic grows
  • R₀ < 1 → epidemic fades

Report date: {datetime.now().strftime("%Y-%m-%d")}
"""

if st.button("📄 Download Report"):
    st.download_button(
        label="Save Report",
        data=report,
        file_name="sir_model_report.txt",
        mime="text/plain"
    )
