import streamlit as st
import requests
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="Hotel Package Suggester", layout="centered")

st.markdown("""
<style>
.glow-text {
  font-size: 1.8em;
  font-weight: bold;
  color: #eab308;
  text-shadow: 0 0 10px #facc15, 0 0 20px #facc15;
  text-align: center;
}
.package-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  padding: 1.5em;
  transition: transform 0.2s;
}
.package-card:hover {
  transform: scale(1.02);
}
.activity-pill {
  background-color: #f0f4f8;
  border-radius: 9999px;
  padding: 0.4em 0.8em;
  display: inline-block;
  margin: 4px 6px 0 0;
  font-size: 0.9em;
  color: #334155;
}
.discount {
  font-size: 2em;
  font-weight: bold;
  color: #dc2626;
  text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🏨 Smart Hotel Package Suggester")

with st.form("input_form"):
    customer_id = st.text_input("Enter Customer ID", placeholder="e.g., C1001")
    email = st.text_input("Enter Email (for verification)", placeholder="john@example.com")
    submitted = st.form_submit_button("Suggest Packages 💡")

if submitted:
    if not customer_id.strip() or not email.strip():
        st.warning("Please enter both customer ID and email.")
    else:
        with st.spinner("Fetching personalized packages from Gemini..."):
            try:
                url = f"http://localhost:5000/suggest-package/{customer_id}"
                response = requests.get(url)
                data = response.json()

                if response.status_code != 200:
                    st.error(data.get("error", "Something went wrong."))
                else:
                    packages = data.get("suggestions", [])
                    st.success(f"🎉 {len(packages)} package(s) found for {customer_id}")

                    for i, pkg in enumerate(packages):
                        with stylable_container(
                            key=f"pkg_{i}",
                            css_styles="margin: 2em 0; padding: 1.5em; border-radius: 1em; background-color: #fff; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"):

                            st.markdown(f"<div class='glow-text'>{pkg['package_name']}</div>", unsafe_allow_html=True)

                            if "discount_percent" in pkg:
                                st.markdown(f"<div class='discount'>{pkg['discount_percent']}% OFF</div>", unsafe_allow_html=True)

                            st.markdown("<div style='margin-top:1em;'><strong>Activities Included:</strong></div>", unsafe_allow_html=True)
                            activity_html = "".join([f"<span class='activity-pill'>{act}</span>" for act in pkg['activities']])
                            st.markdown(f"<div>{activity_html}</div>", unsafe_allow_html=True)

                            with st.expander("📜 Why this package?"):
                                st.markdown(pkg['reason'])

            except Exception as e:
                st.error(f"❌ Error fetching data: {e}")
