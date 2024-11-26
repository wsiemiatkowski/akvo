import streamlit as st

CA_CACO3_CONVERSION = 2.497
MG_CACO3_CONVERSION = 4.118
HC03_CONVERSION = 0.8202

# Concentration in buffers (in mg of element per gram of buffer)

# mg K per gram of potassium buffer
POTASSIUM_BUFFER_CONCENTRATION = 2
# mg Mg per gram of magnesium buffer
MAGNESIUM_BUFFER_CONCENTRATION = 1
# mg Ca per gram of calcium buffer
CALCIUM_BUFFER_CONCENTRATION = 1

def calculate_buffer_requirements(target_gh, target_kh, water_volume, ca_ratio, mg_ratio):
    target_ca_caco3 = target_gh * (ca_ratio / 100)
    target_mg_caco3 = target_gh * (mg_ratio / 100)
    target_k_caco3 = target_kh

    target_ca_ppm = target_ca_caco3 / CA_CACO3_CONVERSION
    target_mg_ppm = target_mg_caco3 / MG_CACO3_CONVERSION
    target_k_ppm = target_k_caco3  / HC03_CONVERSION

    required_ca_mg = target_ca_ppm * (water_volume / 1000)
    required_mg_mg = target_mg_ppm * (water_volume / 1000)
    required_k_mg = target_k_ppm * (water_volume / 1000)

    ca_buffer = required_ca_mg / CALCIUM_BUFFER_CONCENTRATION
    mg_buffer = required_mg_mg / MAGNESIUM_BUFFER_CONCENTRATION
    k_buffer = required_k_mg / POTASSIUM_BUFFER_CONCENTRATION

    return ca_buffer, mg_buffer, k_buffer

st.title("Water Hardness Buffer Calculator for AkVo")
st.write("Calculate the buffer quantities needed to achieve target GH and KH levels in water.")

target_gh = st.number_input("Target GH (in ppm CaCO₃)", min_value=0.0, value=45.0)
target_kh = st.number_input("Target KH (in ppm CaCO₃)", min_value=0.0, value=20.0)
water_volume = st.number_input("Water Volume (in ml)", min_value=0.0, value=500.0)

st.write("Specify the desired proportions for GH components (Calcium and Magnesium):")

if "ca_ratio" not in st.session_state:
    st.session_state.ca_ratio = 66.7
if "mg_ratio" not in st.session_state:
    st.session_state.mg_ratio = 33.3

# Handle dynamic adjustment of calcium and magnesium ratios
ca_ratio = st.number_input(
    "Calcium proportion (%)",
    min_value=0.0,
    max_value=100.0,
    value=st.session_state.ca_ratio,
    step=0.1,
    key="calcium_input"
)

if ca_ratio != st.session_state.ca_ratio:
    st.session_state.ca_ratio = ca_ratio
    st.session_state.mg_ratio = 100 - ca_ratio

mg_ratio = st.number_input(
    "Magnesium proportion (%)",
    min_value=0.0,
    max_value=100.0,
    value=st.session_state.mg_ratio,
    step=0.1,
    key="magnesium_input"
)

if mg_ratio != st.session_state.mg_ratio:
    st.session_state.mg_ratio = mg_ratio
    st.session_state.ca_ratio = 100 - mg_ratio

st.write(f"Calcium: {st.session_state.ca_ratio:.2f}%")
st.write(f"Magnesium: {st.session_state.mg_ratio:.2f}%")

ca_buffer, mg_buffer, k_buffer = calculate_buffer_requirements(
    target_gh, target_kh, water_volume, st.session_state.ca_ratio, st.session_state.mg_ratio
)

st.write(f"Calcium: {st.session_state.ca_ratio:.2f}%")
st.write(f"Magnesium: {st.session_state.mg_ratio:.2f}%")

ca_buffer, mg_buffer, k_buffer = calculate_buffer_requirements(target_gh, target_kh, water_volume, ca_ratio, mg_ratio)

old_akvo = st.checkbox("Check if you are using the older iteration of AkVo where 1g of Akvo 1 = 1 mg of HC03-")
k_buffer = k_buffer * 2 if old_akvo else k_buffer

st.subheader("Your AkVo recipe:")
st.write(f"Akvo 1: {k_buffer:.2f} grams")
st.write(f"Akvo 2: {mg_buffer:.2f} grams")
st.write(f"Akvo 3: {ca_buffer:.2f} grams")

st.markdown("""
<hr style="margin-top: 3rem;">

<div style="text-align: center;">
    <p style="font-size: 14px; color: #555;">
        Created by <strong>Wojciech Siemiątkowski</strong> in collaboration with <strong>Michał Sitarek from AkVo.</strong><br>
        For inquiries or feedback, please contact Michał on <a href="https://www.instagram.com/michalmikkki/">Instagram</a>
    </p>
</div>
""", unsafe_allow_html=True)
