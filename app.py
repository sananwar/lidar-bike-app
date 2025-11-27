import streamlit as st
import pandas as pd

# ---------------------------------------------------
# Pagina-instellingen
# ---------------------------------------------------
st.set_page_config(
    page_title="LiDAR Bike Safety",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS (iOS look + grotere UI + mobiel)
# ---------------------------------------------------
st.markdown(
    """
    <style>

    /* Basis typografie */
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
        font-size: 18px;
        background-color: #F2F2F7;
    }

    /* Verberg Streamlit header & footer voor app-gevoel */
    header[data-testid="stHeader"] {
        display: none;
    }
    footer {
        visibility: hidden;
    }

    /* Content-breedte en padding */
    main.block-container {
        padding-top: 1rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 1200px;
    }

    /* Titels */
    h1 {
        font-size: 2.2rem;
        font-weight: 700;
    }
    h2, h3 {
        font-weight: 600;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        min-width: 260px;
        background: #F5F5F7;
        border-right: 1px solid #E5E5EA;
        color: #111111;
    }
    [data-testid="stSidebar"] * {
        font-size: 17px !important;
        color: #111111 !important;
    }

    /* Buttons (bv. in Systeemstatus / Logboek) */
    .stButton > button {
        border-radius: 14px;
        padding: 0.9rem 1.5rem;
        font-size: 18px;
        font-weight: 500;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        cursor: pointer;
        transition: 0.2s;
    }
    .stButton > button:hover {
        filter: brightness(0.97);
        transform: translateY(1px);
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }

    /* Slider-labels */
    .row-widget.stSlider label {
        font-size: 18px !important;
        margin-bottom: 0.4rem;
    }

    /* Checkboxes & radios */
    .stCheckbox label, .stRadio label {
        font-size: 18px !important;
    }

    /* Toggle switches groter (voor vingers) */
    [data-testid="stToggle"] {
        margin-bottom: 0.8rem;
    }
    [data-testid="stToggle"] label {
        font-size: 18px !important;
    }
    [data-testid="stToggle"] div[role="switch"] {
        transform: scale(1.3);
        margin-right: 0.6rem;
    }

    /* Progressbars */
    .stProgress > div > div {
        height: 12px;
        border-radius: 999px;
    }

    /* Kaart / kaartje (optioneel) */
    .route-card {
        padding: 1rem 1.2rem;
        border-radius: 18px;
        background: #FFFFFF;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        border: 1px solid #E5E5EA;
    }

    /* --- MOBIELE LAYOUT AANPASSINGEN --- */
    @media (max-width: 900px) {
        main.block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            padding-top: 0.5rem;
            max-width: 100%;
        }

        h1 {
            font-size: 1.6rem;
        }

        /* Kolommen onder elkaar i.p.v. naast elkaar */
        [data-testid="column"] {
            width: 100% !important;
            flex: none !important;
            margin-bottom: 1.2rem;
        }

        /* Toggles iets kleiner op hele smalle schermen */
        [data-testid="stToggle"] div[role="switch"] {
            transform: scale(1.1);
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("🚲 LiDAR Bike Safety")

pagina = st.sidebar.radio(
    "Navigatie",
    ["Hoofdscherm", "Systeemstatus", "Instellingen", "Logboek"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Systeemstatus (globaal)")
st.sidebar.write("🔶 LiDAR-unit: **Actief**")
st.sidebar.write("🛰️ Lantaarnpalen: **Verbonden**")
st.sidebar.write("⚡ Trapondersteuning: **Normaal**")
st.sidebar.write("🛞 Bandenspanning: **OK**")

# ---------------------------------------------------
# PAGINA: Hoofdscherm
# ---------------------------------------------------
if pagina == "Hoofdscherm":
    st.title("Hoofdscherm – Live weergave")

    col1, col2, col3 = st.columns(3)

    # -------- Waarschuwingen --------
    with col1:
        st.subheader("🚨 Waarschuwingen")

        st.toggle("Simuleer obstakel dichtbij", key="obstakel_dichtbij")
        st.toggle("Simuleer obstakel verderop", key="obstakel_verderop")
        st.toggle("Simuleer gevaar achter bocht", key="gevaar_bocht")

    # -------- LiDAR & omgeving --------
    with col2:
        st.subheader("📡 LiDAR & omgeving")
        st.write("• Scanhoek: 0–25°")
        st.write("• Scanmodus: Continu")
        st.write("• Laatste update: 0,2 s geleden")
        st.slider("Simuleer afstand tot obstakel (m)", 0, 100, 35)

    # -------- Trapondersteuning --------
    with col3:
        st.subheader("⚡ Trapondersteuning (e-bike)")

        st.toggle("Verminder ondersteuning (gevaar)", key="ondersteuning_verminderd")
        st.toggle("Schakel ondersteuning uit", key="ondersteuning_uit")
        st.toggle("Herstel naar normaal", key="ondersteuning_normaal")

    st.markdown("---")

    # -------- Bandenspanning --------
    st.subheader("🛞 Bandenspanning")
    band_col1, band_col2 = st.columns(2)

    with band_col1:
        st.write("Voorband: **OK**")
        st.progress(80)

    with band_col2:
        st.write("Achterband: **OK**")
        st.progress(75)

    st.markdown("---")

    # -------- Route met adres + kaart --------
    st.subheader("📍 Route")

    bestemming = st.text_input(
        "Voer je bestemming in (adres of plaats)",
        key="bestemming",
        placeholder="Bijv. Hogeschool Windesheim, Zwolle"
    )

    col_route_map, col_route_info = st.columns([2, 1])

    with col_route_map:
        st.write("Kaartweergave (mock):")
        # Mock-locatie – eventueel aanpassen aan jouw scenario
        locatie_data = pd.DataFrame(
            [
                {
                    "lat": 52.5180,   # voorbeeldcoördinaten
                    "lon": 5.4714,
                }
            ]
        )
        st.map(locatie_data)

    with col_route_info:
        st.write("Huidige bestemming:")
        if bestemming:
            st.success(bestemming)
        else:
            st.info("Nog geen bestemming ingevoerd.")

# ---------------------------------------------------
# PAGINA: Systeemstatus
# ---------------------------------------------------
elif pagina == "Systeemstatus":
    st.title("Systeemstatus & Diagnose")

    st.header("LiDAR-unit")
    st.write("• Hardware status: **OK**")
    st.write("• Temperatuur: 42°C (mock)")
    st.write("• Firmware-versie: v0.1-demo")

    st.header("Communicatie met lantaarnpalen")
    st.write("• Verbonden: **Ja (demo)**")
    st.write("• Laatste contact: 2 s geleden")
    st.write("• Dekking: Stadspark – Zone A")

    st.header("Bandenspanning-sensoren")
    st.write("• Sensor voorband: verbonden")
    st.write("• Sensor achterband: verbonden")
    st.write("• Batterijstatus sensoren: 80%")

    st.markdown("---")
    st.subheader("Testknoppen (UI-only)")
    st.button("Herlaad systeemstatus")
    st.button("Simuleer fout in LiDAR-unit")
    st.button("Simuleer verlies verbinding lantaarnpalen")

# ---------------------------------------------------
# PAGINA: Instellingen
# ---------------------------------------------------
elif pagina == "Instellingen":
    st.title("Instellingen")

    st.subheader("Waarschuwingsinstellingen")
    st.radio(
        "Wanneer wil je waarschuwingen?",
        ["Alleen bij direct gevaar", "Normaal", "Vroegtijdig waarschuwen"],
        key="waarschuwingsniveau"
    )

    st.checkbox("Geluid bij waarschuwingen inschakelen", value=True, key="geluid")
    st.checkbox("Trillen bij waarschuwingen inschakelen", value=True, key="trillen")

    st.markdown("---")
    st.subheader("Bandenspanning-profielen")
    st.selectbox("Kies fietsprofiel", ["Stadsfiets", "E-bike", "Racefiets"], key="profiel")
    st.slider("Gewenste bandenspanning (bar)", 2.0, 6.0, 3.5, 0.1, key="bandenspanning_doel")

    st.markdown("---")
    st.subheader("Taal & interface")
    st.selectbox("Taal", ["Nederlands", "Engels"], key="taal")
    st.checkbox("Donkere modus", value=True, key="darkmode_mock")

    st.markdown("---")
    st.subheader("Privacy (mock)")
    st.checkbox("Deel geanonimiseerde gegevens met gemeente", value=False, key="privacy")

# ---------------------------------------------------
# PAGINA: Logboek
# ---------------------------------------------------
elif pagina == "Logboek":
    st.title("Logboek – Recente waarschuwingen (demo)")
    st.write("Hier kun je later een tabel of overzicht tonen met recente obstakels en waarschuwingen.")

    st.table(
        {
            "Tijd": ["08:15", "08:17", "08:25"],
            "Type": ["Obstakel dichtbij", "Drukte na bocht", "Lage bandenspanning"],
            "Status": ["Afgehandeld", "Afgehandeld", "Nog actief"]
        }
    )

    st.button("Vernieuw logboek")
