def build_prompt(summary, question):

    return f"""
You are a supply chain analytics assistant.

The dataset contains logistics information including:
- order preparation time
- order processing time
- shipping duration
- fulfillment time
- shipping delays
- warehouse performance
- product performance

Use the dataset insights below to answer the user's question.

Dataset insights:
{summary}

User Question:
{question}

Answer clearly using the dataset insights.
"""