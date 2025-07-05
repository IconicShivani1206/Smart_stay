from flask import Flask, jsonify
import json
import os
import google.generativeai as genai

app = Flask(__name__)

GOOGLE_API_KEY = "" # Your API key
genai.configure(api_key=GOOGLE_API_KEY)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

def load_data(filename):
    with open(os.path.join(DATA_PATH, filename)) as f:
        return json.load(f)

@app.route('/suggest-package/<customer_id>', methods=['GET'])
def suggest_package(customer_id):
    customers = load_data('customers.json')
    activities = load_data('activities.json')

    customer = next((c for c in customers if c['customer_id'] == customer_id), None)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    visit_summary = ""
    for visit in customer.get('past_visits', []):
        visit_summary += f"Hotel: {visit['hotel']}\nActivities: {', '.join(visit['activities'])}\nFeedback: {visit['feedback']}\n\n"

    activity_descriptions = "\n".join(
        [f"- {a['activity']}: {a['description']}" for a in activities]
    )

    prompt = f"""
You are a smart hotel assistant that creates personalized package deals.

Based on the customer's visit history and feedback below, suggest 2–4 themed packages. Each package should:

- Include a package_name
- Contain 2–5 activity names (from the list below only)
- Mention a discount_percent (optional)
- Explain briefly why the package is suitable

🚫 Do not include any activity not mentioned in the list.
🚫 Avoid activities the customer gave negative feedback on.

🎯 Valid Activities:
{activity_descriptions}

📄 Customer Visit History:
{visit_summary}

Respond strictly in JSON format like:
[
  {{
    "package_name": "...",
    "activities": ["...", "..."],
    "discount_percent": ...,
    "reason": "..."
  }},
  ...
]
"""
    try:
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        response = model.generate_content(prompt)

        print("\n🔍 Raw Gemini Response:")
        print(response.text)

        # ✅ Remove Markdown code fence if present
        cleaned = response.text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()

        # ✅ Try parsing cleaned JSON
        try:
            parsed = json.loads(cleaned)
            return jsonify({"suggestions": parsed})
        except json.JSONDecodeError:
            return jsonify({
                "error": "GenAI response was not valid JSON even after cleanup.",
                "raw_response": response.text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
