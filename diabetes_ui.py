import streamlit as st
import numpy as np
import joblib
import pandas as pd


def run():
    model = joblib.load("diabetes_model.pkl")

    # ─── PAGE HEADER ───
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-title">Diabetes <span>Risk Analyzer</span></div>
            <div class="page-subtitle">AI-powered clinical risk assessment · Pima Indians Dataset · Random Forest Classifier</div>
        </div>
        <div class="page-badge">🩺 Diagnostic Tool</div>
    </div>
    """, unsafe_allow_html=True)

    # ─── TWO COLUMN LAYOUT ───
    col_left, col_right = st.columns([1, 1.55], gap="large")

    # ════════════════════════════════
    # LEFT — INPUT PANEL
    # ════════════════════════════════
    with col_left:
        st.markdown("""
        <div class="glass-card">
            <div class="section-header">Patient Parameters</div>
        """, unsafe_allow_html=True)

        pregnancies = st.slider("Pregnancies", 0, 20, 1,
                                help="Number of times pregnant")
        glucose = st.slider("Glucose Level (mg/dL)", 0, 300, 120,
                            help="Plasma glucose concentration (2h oral glucose tolerance test)")
        bp = st.slider("Blood Pressure (mmHg)", 0, 200, 70,
                       help="Diastolic blood pressure")
        skin = st.slider("Skin Thickness (mm)", 0, 100, 20,
                         help="Triceps skinfold thickness")
        insulin = st.slider("Insulin (μU/mL)", 0, 900, 80,
                            help="2-hour serum insulin")
        bmi = st.slider("BMI (kg/m²)", 0.0, 70.0, 25.0, step=0.1,
                        help="Body mass index")
        dpf = st.slider("Diabetes Pedigree Function", 0.0, 3.0, 0.47, step=0.01,
                        help="Likelihood of diabetes based on family history")
        age = st.slider("Age (years)", 1, 120, 30,
                        help="Patient age")

        st.markdown("</div>", unsafe_allow_html=True)

        predict = st.button("⚡ Run AI Analysis", use_container_width=True)

    # ════════════════════════════════
    # RIGHT — RESULTS PANEL
    # ════════════════════════════════
    with col_right:
        if not predict:
            # ─── IDLE STATE ───
            st.markdown("""
            <div class="glass-card" style="height:100%; min-height: 460px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; gap: 1rem;">
                <div style="font-size: 3.5rem; filter: drop-shadow(0 0 16px rgba(56,189,248,0.4));">🧬</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #94a3b8;">Ready for Analysis</div>
                <div style="font-size: 0.82rem; color: #475569; max-width: 240px; line-height: 1.6;">
                    Configure patient parameters on the left and click <strong style="color:#38bdf8">Run AI Analysis</strong> to get your results.
                </div>
                <div style="margin-top: 0.5rem; display:flex; gap: 1rem; flex-wrap:wrap; justify-content:center;">
                    <span style="font-size:0.72rem; padding:0.3rem 0.8rem; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.2); border-radius:20px; color:#7dd3fc;">Random Forest</span>
                    <span style="font-size:0.72rem; padding:0.3rem 0.8rem; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.2); border-radius:20px; color:#7dd3fc;">Real-time Inference</span>
                    <span style="font-size:0.72rem; padding:0.3rem 0.8rem; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.2); border-radius:20px; color:#7dd3fc;">Probabilistic Score</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # ─── RUN PREDICTION ───
            data = pd.DataFrame([[pregnancies, glucose, bp, skin,
                              insulin, bmi, dpf, age]])
            pred = model.predict(data)[0]
            prob = model.predict_proba(data)[0][1]
            risk_pct = int(prob * 100)

            # Risk tier
            if risk_pct < 30:
                risk_tier = "Low Risk"
                risk_color = "#10b981"
                risk_bg = "rgba(16,185,129,0.08)"
                risk_border = "rgba(16,185,129,0.3)"
                risk_icon = "✅"
            elif risk_pct < 65:
                risk_tier = "Moderate Risk"
                risk_color = "#f59e0b"
                risk_bg = "rgba(245,158,11,0.08)"
                risk_border = "rgba(245,158,11,0.3)"
                risk_icon = "⚠️"
            else:
                risk_tier = "High Risk"
                risk_color = "#f43f5e"
                risk_bg = "rgba(244,63,94,0.08)"
                risk_border = "rgba(244,63,94,0.3)"
                risk_icon = "🚨"

            # ─── MAIN RESULT CARD ───
            st.markdown(f"""
            <div class="glass-card" style="
                background: {risk_bg};
                border-color: {risk_border};
                text-align: center;
                margin-bottom: 1.2rem;
                padding: 2rem;
            ">
                <div style="font-size:2.8rem; margin-bottom:0.5rem;">{risk_icon}</div>
                <div style="
                    font-size: 0.72rem;
                    font-weight: 700;
                    letter-spacing: 0.2em;
                    text-transform: uppercase;
                    color: {risk_color};
                    margin-bottom: 0.4rem;
                    opacity: 0.8;
                ">Diagnosis Result</div>
                <div style="
                    font-size: 1.9rem;
                    font-weight: 700;
                    color: {risk_color};
                    letter-spacing: -0.02em;
                ">{risk_tier}</div>
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.85rem;
                    color: {risk_color};
                    opacity: 0.75;
                    margin-top: 0.3rem;
                ">Confidence: {prob:.1%}</div>
            </div>
            """, unsafe_allow_html=True)

            # ─── RISK SCORE BAR ───
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
                    <div style="font-size:0.75rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#64748b;">Risk Score</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:1.3rem; font-weight:700; color:{risk_color};">{risk_pct}<span style="font-size:0.75rem; opacity:0.6;"> / 100</span></div>
                </div>
                <div style="background:rgba(255,255,255,0.05); border-radius:999px; height:8px; overflow:hidden;">
                    <div style="
                        width:{risk_pct}%;
                        height:100%;
                        background:linear-gradient(90deg, {risk_color}88, {risk_color});
                        border-radius:999px;
                        box-shadow: 0 0 12px {risk_color}66;
                        transition: width 0.8s ease;
                    "></div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-top:0.4rem;">
                    <span style="font-size:0.65rem; color:#334155;">Low (0–30)</span>
                    <span style="font-size:0.65rem; color:#334155;">Moderate (30–65)</span>
                    <span style="font-size:0.65rem; color:#334155;">High (65+)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ─── KPI CARDS ───
            st.markdown('<div class="section-header">Key Biomarkers</div>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)

            def bmi_label(b):
                if b < 18.5: return "Underweight"
                if b < 25: return "Normal"
                if b < 30: return "Overweight"
                return "Obese"

            def glucose_label(g):
                if g < 100: return "Normal"
                if g < 126: return "Pre-diabetic"
                return "Diabetic range"

            c1.metric("Glucose", f"{glucose}", glucose_label(glucose))
            c2.metric("BMI", f"{bmi:.1f}", bmi_label(bmi))
            c3.metric("Age", f"{age}", "yrs")
            c4.metric("Insulin", f"{insulin}", "μU/mL")

            # ─── RISK FACTORS ───
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Risk Factor Analysis</div>', unsafe_allow_html=True)

            factors = []
            if glucose >= 126: factors.append(("Glucose in Diabetic Range", "high", f"{glucose} mg/dL"))
            elif glucose >= 100: factors.append(("Glucose Pre-diabetic Range", "medium", f"{glucose} mg/dL"))
            if bmi >= 30: factors.append(("Obesity (BMI ≥ 30)", "high", f"{bmi:.1f}"))
            elif bmi >= 25: factors.append(("Overweight (BMI 25–30)", "medium", f"{bmi:.1f}"))
            if age >= 45: factors.append(("Age Risk Factor (≥45)", "medium", f"{age} yrs"))
            if dpf > 1.0: factors.append(("High Diabetes Pedigree", "high", f"{dpf:.2f}"))
            if insulin > 200: factors.append(("Elevated Insulin", "medium", f"{insulin} μU/mL"))
            if bp > 90: factors.append(("Elevated Blood Pressure", "medium", f"{bp} mmHg"))

            if not factors:
                factors.append(("No major risk factors detected", "low", "—"))

            colors = {"high": "#f43f5e", "medium": "#f59e0b", "low": "#10b981"}
            for name, level, val in factors:
                color = colors[level]
                st.markdown(f"""
                <div style="
                    display:flex; align-items:center; justify-content:space-between;
                    padding: 0.7rem 1rem;
                    background: rgba(255,255,255,0.02);
                    border: 1px solid rgba(255,255,255,0.05);
                    border-left: 3px solid {color};
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                ">
                    <div style="font-size:0.82rem; color:#cbd5e1;">{name}</div>
                    <div style="display:flex; align-items:center; gap:0.6rem;">
                        <span style="font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:{color}; font-weight:600;">{val}</span>
                        <span style="
                            font-size:0.62rem; font-weight:700; letter-spacing:0.1em;
                            text-transform:uppercase; padding:0.2rem 0.6rem;
                            background:{color}18; color:{color};
                            border-radius:4px;
                        ">{level}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ─── DISCLAIMER ───
            st.markdown("""
            <div style="
                margin-top: 1.5rem;
                padding: 0.8rem 1rem;
                background: rgba(56,189,248,0.04);
                border: 1px solid rgba(56,189,248,0.1);
                border-radius: 8px;
                font-size: 0.72rem;
                color: #475569;
                line-height: 1.6;
            ">
                ⚠️ <strong style="color:#64748b;">Medical Disclaimer:</strong> This AI tool is for informational purposes only and does not constitute medical advice. Consult a licensed healthcare professional for diagnosis and treatment.
            </div>
            """, unsafe_allow_html=True)