import streamlit as st

# ---------------------------------------------------
# Pagina-instellingen
# ---------------------------------------------------
st.set_page_config(
    page_title="LiDAR Bike Safety",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS (iOS look + grotere UI + toggles)
# ---------------------------------------------------
st.markdown(
    """
    <style>

    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
        font-size: 18px;
    }

    main.block-container {
        padding-top: 1rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 1200px;
    }

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

    /* Buttons (zoals in logboek, systeemstatus) */
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

    /* Sliders */
    .row-widget.stSlider label {
        font-size: 18px !important;
        margin-bottom: 0.4rem;
    }

    /* Checkboxes & radios */
    .stCheckbox label, .stRadio label {
        font-size: 18px !important;
    }

    /* Toggle switches groter maken (voor vingers) */
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

    /* Route / situatieschets kaartje */
    .route-card {
        padding: 1rem 1.2rem;
        border-radius: 18px;
        background: #FFFFFF;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        border: 1px solid #E5E5EA;
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

    st.subheader("📍 Route / situatieschets")
    st.markdown(
        """
        <div class="route-card">
          Hier zou je later een kaart, radarview of abstracte visualisatie kunnen tonen.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# PAGINA: Systeemstatus
# ---------------------------------------------------
elif pagina == "Systeemstatus":
    st.title("Systeemstatus & Diagnose")

    st.header("LiDAR-unit")
    st.write("• Hardware status: **OK**")
    st.write("• Temperatuur: 42°C")
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
    st.checkbox("Donkere modus", value=True, key="darkmode")

    st.markdown("---")
    st.subheader("Privacy")
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
