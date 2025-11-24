
import streamlit as st
from app.DTN_LTP_Simulator import SimulationConfig, DTNSimulator

st.set_page_config(page_title="DTN-LTP Simulator", layout="centered")
st.title("🚀 DTN-LTP Cognitive Routing Simulator")

st.sidebar.header("🛠 Configuration")
num_nodes = st.sidebar.slider("Number of Nodes", 3, 20, 8)
sim_time = st.sidebar.slider("Simulation Time (sec)", 100, 1000, 500)
buffer_size = st.sidebar.slider("Max Buffer Size", 10, 200, 50)
ltp_seg_size = st.sidebar.slider("LTP Segment Size (bytes)", 256, 4096, 1024)

if st.button("Run Simulation"):
    with st.spinner("Running DTN Simulation..."):
        config = SimulationConfig(
            num_nodes=num_nodes,
            simulation_time=sim_time,
            max_buffer_size=buffer_size,
            ltp_segment_size=ltp_seg_size,
        )
        simulator = DTNSimulator(config)
        simulator.run()
        report = simulator.generate_report("results/dtn_ui_results.json")

    st.success("Simulation Completed!")
    st.subheader("📊 Final Metrics")
    final_metrics = simulator.metrics_log[-1]
    st.json(final_metrics)

    with open("results/dtn_ui_results.json", "rb") as f:
        st.download_button(
            label="📥 Download Report",
            data=f,
            file_name="dtn_simulation_results.json",
            mime="application/json"
        )
