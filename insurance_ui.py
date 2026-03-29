import streamlit as st
import pandas as pd
import joblib
import time


def run():
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    columns = joblib.load("columns.pkl")

    # ─── PAGE HEADER ───
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-title">Insurance Cost <span>Predictor</span></div>
            <div class="page-subtitle">ML-powered premium estimation · Gradient Boost Model · Real-time inference</div>
        </div>
        <div class="page-badge">💰 Financial Tool</div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.55], gap="large")

    # ════════════════════════════════
    # LEFT — INPUT PANEL
    # ════════════════════════════════
    with col_left:
        st.markdown("""
        <div class="glass-card">
            <div class="section-header">Profile Parameters</div>
        """, unsafe_allow_html=True)

        age = st.slider("Age (years)", 18, 100, 30,
                        help="Your current age")
        bmi = st.slider("BMI (kg/m²)", 10.0, 50.0, 26.5, step=0.1,
                        help="Body mass index (weight in kg / height² in m)")
        children = st.slider("Dependents / Children", 0, 5, 1,
                             help="Number of children covered by insurance")

        st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            sex = st.selectbox("Biological Sex", ["male", "female"],
                               help="Biological sex for actuarial purposes")
        with col_b:
            smoker = st.selectbox("Smoking Status", ["no", "yes"],
                                  help="Current tobacco/smoking status")

        region = st.selectbox(
            "US Region",
            ["northeast", "northwest", "southeast", "southwest"],
            help="Geographic region within the United States"
        )

        st.markdown("</div>", unsafe_allow_html=True)

        predict = st.button("⚡ Predict Insurance Cost", use_container_width=True)

    # ════════════════════════════════
    # RIGHT — RESULTS PANEL
    # ════════════════════════════════
    with col_right:
        if not predict:
            # ─── IDLE STATE ───
            st.markdown("""
            <div class="glass-card" style="height:100%; min-height: 460px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; gap: 1rem;">
                <div style="font-size: 3.5rem; filter: drop-shadow(0 0 16px rgba(56,189,248,0.4));">📋</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #94a3b8;">Awaiting Profile Data</div>
                <div style="font-size: 0.82rem; color: #475569; max-width: 240px; line-height: 1.6;">
                    Fill in your profile details on the left and click <strong style="color:#38bdf8">Predict Insurance Cost</strong> to receive your estimate.
                </div>
                <div style="margin-top: 0.5rem; display:flex; gap: 1rem; flex-wrap:wrap; justify-content:center;">
                    <span style="font-size:0.72rem; padding:0.3rem 0.8rem; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.2); border-radius:20px; color:#7dd3fc;">Gradient Boost</span>
                    <span style="font-size:0.72rem; padding:0.3rem 0.8rem; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.2); border-radius:20px; color:#7dd3fc;">Scaled Features</span>
                    <span style="font-size:0.72rem; padding:0.3rem 0.8rem; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.2); border-radius:20px; color:#7dd3fc;">Actuarial Model</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Running AI model..."):
                time.sleep(0.9)

                # ─── FEATURE ENGINEERING ───
                data = pd.DataFrame([{
                    "age": age,
                    "bmi": bmi,
                    "children": children
                }])
                data["sex_male"] = 1 if sex == "male" else 0
                data["smoker_yes"] = 1 if smoker == "yes" else 0
                data["region_northwest"] = 1 if region == "northwest" else 0
                data["region_southeast"] = 1 if region == "southeast" else 0
                data["region_southwest"] = 1 if region == "southwest" else 0
                data = data.reindex(columns=columns, fill_value=0)
                data_scaled = scaler.transform(data)
                pred = model.predict(data_scaled)[0]

            # ─── RISK TIER ───
            if pred < 10000:
                tier = "Low Premium"
                tier_desc = "You fall in the lowest cost bracket"
                tier_color = "#10b981"
                tier_bg = "rgba(16,185,129,0.08)"
                tier_border = "rgba(16,185,129,0.3)"
                tier_icon = "🟢"
            elif pred < 20000:
                tier = "Standard Premium"
                tier_desc = "Average market rate for your profile"
                tier_color = "#38bdf8"
                tier_bg = "rgba(56,189,248,0.08)"
                tier_border = "rgba(56,189,248,0.3)"
                tier_icon = "🔵"
            elif pred < 35000:
                tier = "Elevated Premium"
                tier_desc = "Above-average cost due to risk factors"
                tier_color = "#f59e0b"
                tier_bg = "rgba(245,158,11,0.08)"
                tier_border = "rgba(245,158,11,0.3)"
                tier_icon = "🟡"
            else:
                tier = "High Premium"
                tier_desc = "Significant risk factors detected"
                tier_color = "#f43f5e"
                tier_bg = "rgba(244,63,94,0.08)"
                tier_border = "rgba(244,63,94,0.3)"
                tier_icon = "🔴"

            monthly = pred / 12

            # ─── MAIN COST CARD ───
            st.markdown(f"""
            <div class="glass-card" style="
                background: {tier_bg};
                border-color: {tier_border};
                text-align: center;
                margin-bottom: 1.2rem;
                padding: 2rem;
            ">
                <div style="font-size: 0.72rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:{tier_color}; opacity:0.8; margin-bottom:0.4rem;">
                    Estimated Annual Premium
                </div>
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 2.6rem;
                    font-weight: 700;
                    color: {tier_color};
                    letter-spacing: -0.02em;
                    line-height:1;
                ">₹ {pred:,.0f}</div>
                <div style="font-size:0.82rem; color:{tier_color}; opacity:0.65; margin-top:0.5rem;">
                    ≈ ₹ {monthly:,.0f} / month
                </div>
                <div style="
                    display:inline-flex; align-items:center; gap:0.5rem;
                    margin-top:1rem;
                    padding: 0.4rem 1rem;
                    background: rgba(255,255,255,0.04);
                    border: 1px solid {tier_border};
                    border-radius: 20px;
                    font-size: 0.8rem; font-weight: 600; color: {tier_color};
                ">{tier_icon} {tier}</div>
                <div style="font-size:0.75rem; color:#475569; margin-top:0.4rem;">{tier_desc}</div>
            </div>
            """, unsafe_allow_html=True)

            # ─── KPI ROW ───
            st.markdown('<div class="section-header">Profile Summary</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)

            def bmi_label(b):
                if b < 18.5: return "Underweight"
                if b < 25: return "Normal"
                if b < 30: return "Overweight"
                return "Obese"

            c1.metric("Age", f"{age} yrs")
            c2.metric("BMI", f"{bmi:.1f}", bmi_label(bmi))
            c3.metric("Dependents", f"{children}")

            # ─── COST DRIVERS ───
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Cost Driver Analysis</div>', unsafe_allow_html=True)

            drivers = []
            if smoker == "yes":
                drivers.append(("Smoking Status", "critical", "Smokers pay 3–4× more on average", "yes"))
            if bmi >= 30:
                drivers.append(("BMI — Obesity", "high", f"BMI {bmi:.1f} significantly raises premiums", f"{bmi:.1f}"))
            elif bmi >= 25:
                drivers.append(("BMI — Overweight", "medium", f"BMI {bmi:.1f} moderately increases cost", f"{bmi:.1f}"))
            if age >= 55:
                drivers.append(("Senior Age Bracket", "high", f"Age {age} is in high-premium range", f"{age} yrs"))
            elif age >= 40:
                drivers.append(("Mid-age Factor", "medium", f"Age {age} carries moderate risk weighting", f"{age} yrs"))
            if children >= 3:
                drivers.append(("Large Family Coverage", "medium", f"{children} dependents increase premium", f"{children} deps"))
            if region in ["southeast"]:
                drivers.append(("Southeast Region", "medium", "SE has higher average claim rates", region))
            if smoker == "no" and bmi < 25 and age < 40:
                drivers.append(("Healthy Profile Discount", "low", "Non-smoker + healthy BMI + young age", "eligible"))

            if not drivers:
                drivers.append(("Standard risk profile", "low", "No major cost drivers detected", "—"))

            colors = {"critical": "#f43f5e", "high": "#fb923c", "medium": "#f59e0b", "low": "#10b981"}
            labels = {"critical": "Critical", "high": "High Impact", "medium": "Medium", "low": "Low"}
            for name, level, desc, val in drivers:
                color = colors[level]
                label = labels[level]
                st.markdown(f"""
                <div style="
                    padding: 0.75rem 1rem;
                    background: rgba(255,255,255,0.02);
                    border: 1px solid rgba(255,255,255,0.05);
                    border-left: 3px solid {color};
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                ">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <div style="font-size:0.83rem; font-weight:600; color:#cbd5e1;">{name}</div>
                            <div style="font-size:0.73rem; color:#475569; margin-top:0.2rem;">{desc}</div>
                        </div>
                        <span style="
                            font-size:0.62rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
                            padding:0.2rem 0.6rem; background:{color}18; color:{color}; border-radius:4px;
                            white-space:nowrap; margin-left:0.8rem; flex-shrink:0;
                        ">{label}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ─── COST BREAKDOWN VISUAL ───
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Annual Cost Breakdown</div>', unsafe_allow_html=True)

            q_pred = pred / 4
            m_pred = pred / 12
            d_pred = pred / 365

            st.markdown(f"""
            <div class="glass-card" style="padding:1.2rem;">
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem;">
                    <div style="text-align:center; padding:0.8rem; background:rgba(255,255,255,0.02); border-radius:10px;">
                        <div style="font-size:0.65rem; color:#475569; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.3rem;">Quarterly</div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:1rem; font-weight:700; color:#94a3b8;">₹{q_pred:,.0f}</div>
                    </div>
                    <div style="text-align:center; padding:0.8rem; background:rgba(56,189,248,0.05); border:1px solid rgba(56,189,248,0.1); border-radius:10px;">
                        <div style="font-size:0.65rem; color:#38bdf8; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.3rem;">Monthly</div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:1rem; font-weight:700; color:#38bdf8;">₹{m_pred:,.0f}</div>
                    </div>
                    <div style="text-align:center; padding:0.8rem; background:rgba(255,255,255,0.02); border-radius:10px;">
                        <div style="font-size:0.65rem; color:#475569; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.3rem;">Daily</div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:1rem; font-weight:700; color:#94a3b8;">₹{d_pred:,.0f}</div>
                    </div>
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
                ⚠️ <strong style="color:#64748b;">Disclaimer:</strong> Estimates are generated by an ML model trained on public datasets. Actual insurance premiums vary by insurer, policy terms, and local regulations. Consult a licensed insurance advisor for accurate quotes.
            </div>
            """, unsafe_allow_html=True)