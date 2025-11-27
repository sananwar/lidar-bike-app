import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components

# ---------------------------------------------------
# ORS API KEY (VUL HIER JE EIGEN KEY IN!)
# ---------------------------------------------------
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImI2MWM1ZTFmYmQ3MTQ5NmRiZjY3OThlZmZmN2VjOTViIiwiaCI6Im11cm11cjY0In0="   # <----- vervang door je nieuwe key

# ---------------------------------------------------
# Pagina instellingen
# ---------------------------------------------------
st.set_page_config(
    page_title="LiDAR Bike Safety",
    layout="wide",
)

# ---------------------------------------------------
# Javascript voor haptics (alleen gevaar-knoppen)
# ---------------------------------------------------
def vibrate():
    components.html(
        """
        <script>
        if (navigator.vibrate) { navigator.vibrate(60); }
        </script>
        """,
        height=0,
        width=0
    )

# ---------------------------------------------------
# DARK MODE (iOS-style toggle via session state)
# ---------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ---------------------------------------------------
# CUSTOM CSS (iOS layout, smartphone fullscreen)
# ---------------------------------------------------
st.markdown(
    f"""
    <style>

    /* Globale iOS look */
    html, body, [class*="css"] {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
        font-size: 18px;
        background-color: {"#1C1C1E" if st.session_state.dark_mode else "#F2F2F7"};
        color: {"#FAFAFA" if st.session_state.dark_mode else "#1C1C1E"};
    }}

    /* Sidebar icons */
    [data-testid="stSidebar"] ul {{
        list-style-type: none;
        padding-left: 0;
    }}

    /* Verberg Streamlit footer & header */
    header[data-testid="stHeader"] {{ display: none; }}
    footer {{ visibility: hidden; }}

    /* Mobiel fullscreen: sidebar verbergen */
    @media (max-width: 900px) {{
        [data-testid="stSidebar"] {{
            display: none;
        }}
        main.block-container {{
            padding: 0.7rem;
            max-width: 100%;
        }}
    }}

    /* Big toggles */
    [data-testid="stToggle"] div[role="switch"] {{
        transform: scale(1.3);
        margin-right: .6rem;
    }}

    h1 {{
        font-size: 1.9rem;
        font-weight: 700;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SIDEBAR met ICONS
# ---------------------------------------------------
st.sidebar.title("🚲 LiDAR Safety")

pagina = st.sidebar.radio(
    "Navigatie",
    [
        "🏠 Hoofdscherm",
        "🗺️ Route",
        "📡 Systeemstatus",
        "⚙️ Instellingen",
        "📘 Logboek"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Systeemstatus")
st.sidebar.write("🔶 LiDAR: **Actief**")
st.sidebar.write("🛰️ Lantaarnpalen: **Verbonden**")
st.sidebar.write("⚡ Ondersteuning: **Normaal**")
st.sidebar.write("🛞 Banden: **OK**")

# ---------------------------------------------------
# ROUTE FUNCTIES: geocode + echte fietsroute ophalen
# ---------------------------------------------------
def geocode_address(address: str):
    """Adres → coördinaten met foutafhandeling (lat, lon) of None."""
    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": ORS_API_KEY,
        "text": address
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
    except Exception:
        return None

    # Check of er resultaten zijn
    if "features" not in data or len(data["features"]) == 0:
        return None

    try:
        coords = data["features"][0]["geometry"]["coordinates"]
        return coords[1], coords[0]  # lat, lon
    except Exception:
        return None


def get_route(start: tuple, end: tuple):
    """Lat/Lon → echte fietsroute polyline met foutcontrole. Geeft DataFrame of None."""
    url = "https://api.openrouteservice.org/v2/directions/cycling-regular"
    body = {
        "coordinates": [
            [start[1], start[0]],
            [end[1], end[0]]
        ]
    }
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json=body, headers=headers, timeout=10)
        data = r.json()
    except Exception:
        return None

    # Check of het resultaat OK is
    if "features" not in data:
        return None

    try:
        coords = data["features"][0]["geometry"]["coordinates"]
        df = pd.DataFrame([[lat, lon] for lon, lat in coords], columns=["lat", "lon"])
        return df
    except Exception:
        return None

# ---------------------------------------------------
# PAGINA: Hoofdscherm
# ---------------------------------------------------
if pagina.startswith("🏠"):
    st.title("Hoofdscherm – Live weergave")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🚨 Waarschuwingen")

        if st.toggle("⚠️ Obstakel dichtbij", key="obstakel_dichtbij"):
            vibrate()

        if st.toggle("⚠️ Obstakel verderop", key="obstakel_verderop"):
            vibrate()

        if st.toggle("❗ Gevaar achter bocht", key="gevaar_bocht"):
            vibrate()

    with col2:
        st.subheader("📡 LiDAR & omgeving")
        st.write("• Scanhoek: 0–25°")
        st.write("• Modus: Continu")
        st.write("• Laatste update: 0,2 s geleden")
        st.slider("Afstand obstakel (m)", 0, 100, 35)

    with col3:
        st.subheader("⚡ Trapondersteuning")

        if st.toggle("❗ Ondersteuning verminderen", key="limit_support"):
            vibrate()

        st.toggle("🔌 Ondersteuning uitschakelen", key="kill_support")
        st.toggle("🔄 Herstel normaal", key="restore_support")

    st.markdown("---")

    st.subheader("🛞 Bandenspanning")
    colb1, colb2 = st.columns(2)
    colb1.write("Voorband: **OK**")
    colb1.progress(80)
    colb2.write("Achterband: **OK**")
    colb2.progress(75)

# ---------------------------------------------------
# PAGINA: ROUTE (EIGEN)
# ---------------------------------------------------
elif pagina.startswith("🗺️"):
    st.title("📍 Route & Navigatie")

    bestemming = st.text_input(
        "Voer een bestemming in:",
        key="input_bestemming",
        placeholder="Bijv. Windesheim Zwolle"
    )

    if bestemming:
        st.write("🔄 Locatie zoeken…")
        dest_coords = geocode_address(bestemming)

        if dest_coords:
            st.success(f"Bestemming gevonden: {bestemming}")

            # Startpunt: Hogeschool van Amsterdam - Fraijlemaborg (Amsterdam Bijlmer)
            start_coords = (52.327343, 4.947332)


            route_df = get_route(start_coords, dest_coords)

            if route_df is None:
                st.warning(
                    "Kon geen route berekenen (mogelijk buiten fietsnetwerk of API-fout). "
                    "Toon een rechte lijn tussen start en bestemming als benadering."
                )
                # Fallback: rechte lijn tussen start en bestemming
                route_df = pd.DataFrame(
                    [
                        {"lat": start_coords[0], "lon": start_coords[1]},
                        {"lat": dest_coords[0], "lon": dest_coords[1]},
                    ]
                )

            st.write("🗺️ Routeweergave:")
            st.map(route_df)

        else:
            st.error("Kon bestemming niet vinden.")
    else:
        st.info("Voer een bestemming in om de route te berekenen.")

# ---------------------------------------------------
# PAGINA: Systeemstatus
# ---------------------------------------------------
elif pagina.startswith("📡"):
    st.title("Systeemstatus & Diagnose")
    st.write("• LiDAR hardware: OK")
    st.write("• Temperatuur: 42°C")
    st.write("• Firmware: v0.1-demo")
    st.write("• Lantaarnpalen: Verbonden")

# ---------------------------------------------------
# PAGINA: Instellingen
# ---------------------------------------------------
elif pagina.startswith("⚙️"):
    st.title("Instellingen")

    st.subheader("🌙 Dark mode")
    if st.toggle("Dark mode inschakelen", value=st.session_state.dark_mode):
        st.session_state.dark_mode = True
    else:
        st.session_state.dark_mode = False

    st.write("🔄 Herlaad de pagina om thema toe te passen.")

# ---------------------------------------------------
# PAGINA: Logboek
# ---------------------------------------------------
elif pagina.startswith("📘"):
    st.title("Logboek – Recente waarschuwingen")
    st.table(
        {
            "Tijd": ["08:15", "08:17", "08:25"],
            "Type": ["Obstakel dichtbij", "Gevaar na bocht", "Lage bandenspanning"],
            "Status": ["Afgehandeld", "Afgehandeld", "Actief"]
        }
    )
