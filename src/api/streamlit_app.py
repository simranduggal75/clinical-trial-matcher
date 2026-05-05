import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Clinical Trial Matcher",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Clinical Trial Matcher")
st.markdown("Match patient medical records to relevant clinical trials using AI")

# ── Sidebar — Patient Input ──────────────────────────────────────────────────
st.sidebar.header("Patient Profile")

age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=45)
gender = st.sidebar.selectbox("Gender", ["female", "male"])
top_k = st.sidebar.slider("Number of trials to return", 1, 20, 5)

conditions_input = st.sidebar.text_area(
    "Medical Conditions (one per line)",
    value="diabetes\nhypertension"
)

medications_input = st.sidebar.text_area(
    "Current Medications (one per line)",
    value="metformin"
)

# ── Main — Results ───────────────────────────────────────────────────────────
if st.sidebar.button("Find Matching Trials", type="primary"):
    conditions  = [c.strip() for c in conditions_input.split("\n") if c.strip()]
    medications = [m.strip() for m in medications_input.split("\n") if m.strip()]

    if not conditions:
        st.error("Please enter at least one medical condition.")
    else:
        payload = {
            "age":         age,
            "gender":      gender,
            "conditions":  conditions,
            "medications": medications
        }

        with st.spinner("Searching trials..."):
            try:
                response = requests.post(
                    f"{API_URL}/match?top_k={top_k}",
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    trials = data["trials"]

                    st.success(f"Found {data['total_matches']} matching trials")

                    for i, trial in enumerate(trials, 1):
                        with st.expander(f"{i}. {trial['title']} — Score: {trial['match_score']}"):
                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown(f"**NCT ID:** {trial['nct_id']}")
                                st.markdown(f"**Conditions:** {', '.join(trial['conditions'])}")
                                st.markdown(f"**Sex:** {trial['sex']}")

                            with col2:
                                st.markdown(f"**Min Age:** {trial['min_age']}")
                                st.markdown(f"**Max Age:** {trial['max_age']}")
                                st.markdown(f"**Match Score:** {trial['match_score']}")

                            st.markdown(
                                f"[View on ClinicalTrials.gov](https://clinicaltrials.gov/study/{trial['nct_id']})"
                            )
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Make sure the FastAPI server is running on port 8000.")
            except Exception as e:
                st.error(f"Error: {e}")

# ── Health Check ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    if st.button("Check API Health"):
        try:
            r = requests.get(f"{API_URL}/health", timeout=5)
            if r.status_code == 200:
                data = r.json()
                st.success(f"API healthy — {data['trials']} trials indexed")
            else:
                st.error("API unhealthy")
        except:
            st.error("API not reachable")