import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Fiktive Privatjet-Flugdaten – Tommy Hilfiger
# -----------------------------
data = {
    "flight_id": [1, 2, 3, 4, 5],
    "date": ["2025-01-05", "2025-01-08", "2025-01-10", "2025-01-14", "2025-01-18"],
    "from": ["Los Angeles", "San Francisco", "Austin", "Miami", "New York"],
    "to": ["San Francisco", "Austin", "Miami", "New York", "Los Angeles"],
    "lat_from": [34.0522, 37.7749, 30.2672, 25.7617, 40.7128],
    "lon_from": [-118.2437, -122.4194, -97.7431, -80.1918, -74.0060],
    "lat_to": [37.7749, 30.2672, 25.7617, 40.7128, 34.0522],
    "lon_to": [-122.4194, -97.7431, -80.1918, -74.0060, -118.2437],
    "distance_km": [543, 2420, 1800, 1750, 3950]
}

df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["date"])

# -----------------------------
# Statistik berechnen
# -----------------------------
total_distance = df["distance_km"].sum()
total_emission = total_distance * 2.5 / 1000  # CO₂ in Tonnen
avg_distance = df["distance_km"].mean()
city_emission = 20000 * 8
percent = total_emission / city_emission * 100

# -----------------------------
# Streamlit Oberfläche
# -----------------------------
st.set_page_config(page_title="Privatjet Tracker Tommy Hilfiger", layout="wide")

st.title("🛩️ Privatjet-Tracker – Tommy Hilfiger")
st.markdown("""
Diese Web-App zeigt fiktive Privatjet-Flüge von **Tommy Hilfiger**
auf einer Weltkarte, berechnet statistische Kennzahlen und vergleicht
die CO₂-Emissionen mit einer deutschen Kleinstadt.
""")

# Kennzahlen anzeigen
col1, col2, col3 = st.columns(3)
col1.metric("✈️ Anzahl Flüge", len(df))
col2.metric("📏 Gesamtdistanz (km)", f"{total_distance:,.0f}")
col3.metric("🌍 CO₂-Emissionen (t)", f"{total_emission:.2f}")
st.caption(f"Das entspricht {percent:.4f}% der jährlichen Emissionen einer Kleinstadt mit 20.000 Einwohnern.")

# -----------------------------
# Schieberegler für Datum
# -----------------------------
st.subheader("📅 Flüge nach Datum anzeigen")
min_date, max_date = df["date"].min(), df["date"].max()

selected_date = st.slider(
    "Bis zu welchem Datum anzeigen?",
    min_value=min_date.date(),
    max_value=max_date.date(),
    value=max_date.date()
)

filtered = df[df["date"].dt.date <= selected_date]

# -----------------------------
# GROSSE Weltkarte
# -----------------------------
st.subheader("🌍 Flugroutenkarte von Tommy Hilfiger (vergrößert)")

fig = px.line_geo(
    filtered,
    lat="lat_from",
    lon="lon_from",
    color="flight_id",
    hover_name="to",
    projection="natural earth",
)

# Linien hinzufügen
for _, row in filtered.iterrows():
    fig.add_trace(px.line_geo(
        lat=[row["lat_from"], row["lat_to"]],
        lon=[row["lon_from"], row["lon_to"]],
    ).data[0])

# **WICHTIG: Karte größer machen**
fig.update_layout(
    height=650,     # <--- Hier stellst du die Kartengröße ein
    margin=dict(l=0, r=0, t=30, b=0),
    title_text="Flugrouten von Tommy Hilfiger"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Balkendiagramm
# -----------------------------
st.subheader("📊 Flugdistanz je Flug")

bar_chart = px.bar(
    filtered,
    x="to",
    y="distance_km",
    text="distance_km",
    color="distance_km",
    labels={"to": "Zielort", "distance_km": "Distanz (km)"},
    title="Distanz pro Flug von Tommy Hilfiger"
)
st.plotly_chart(bar_chart, use_container_width=True)

# -----------------------------
# Datentabelle
# -----------------------------
st.subheader("📋 Flugdaten")
st.dataframe(filtered[["date", "from", "to", "distance_km"]])

st.info("💡 Hinweis: Alle Daten sind fiktiv und dienen nur zur Demonstration der App.")
