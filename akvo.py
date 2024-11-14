import streamlit as st

# Conversion factors
# 1 ppm Ca = 2.5 ppm CaCO3
# 1 ppm Mg = 4.1 ppm CaCO3

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

def calculate_buffer_requirements(target_gh, target_kh, water_volume, ca_ratio, mg_ratio, k_ratio):
    target_ca_caco3 = target_gh * (ca_ratio / 100)
    target_mg_caco3 = target_gh * (mg_ratio / 100)
    target_k_caco3 = target_kh * k_ratio

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

st.title("Water Hardness Buffer Calculator for AKVO")
st.write("Calculate the buffer quantities needed to achieve target GH and KH levels in water.")

target_gh = st.number_input("Target GH (in ppm CaCO₃)", min_value=0.0, value=45.0)
target_kh = st.number_input("Target KH (in ppm CaCO₃)", min_value=0.0, value=20.0)
water_volume = st.number_input("Water Volume (in ml)", min_value=0.0, value=500.0)

st.write("Specify the desired proportions for GH components (Calcium and Magnesium):")
ca_ratio = st.number_input("Calcium proportion (as % of GH)", min_value=0.0, max_value=100.0, value=66.7)
mg_ratio = st.number_input("Magnesium proportion (as % of GH)", min_value=0.0, max_value=100.0, value=33.3)
k_ratio = st.number_input("Potassium proportion (as % of KH)", min_value=0.0, max_value=100.0, value=100.0)

ca_buffer, mg_buffer, k_buffer = calculate_buffer_requirements(target_gh, target_kh, water_volume, ca_ratio, mg_ratio, k_ratio)

st.subheader("Buffer Additions Required:")
st.write(f"Calcium Buffer: {ca_buffer:.2f} grams")
st.write(f"Magnesium Buffer: {mg_buffer:.2f} grams")
st.write(f"Potassium Buffer: {k_buffer:.2f} grams")