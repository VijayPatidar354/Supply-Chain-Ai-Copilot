def build_prompt(summary, question):

    return f"""
You are a supply chain analytics assistant.

Use ONLY the dataset insights below to answer the question.

Dataset insights:
{summary}

Question:
{question}
"""