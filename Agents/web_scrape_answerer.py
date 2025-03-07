from langchain_groq import ChatGroq
import os

def get_answers(queries, results, query):
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant"
    )

    # Ensure correct pairing of queries with results
    query_result_pairs = "\n".join([f"- **Query:** {q}\n  **Result:** {r}" for q, r in zip(queries, results)])

    prompt = f"""
### Goal:
You are an AI assistant with deep expertise in cryptocurrencies, blockchain technology, tokenomics, and financial markets. Your task is to analyze the retrieved search results and synthesize a **concise, coherent, and precise** response to the user's query.

### Context:
- **User Query:** "{query}"
- **Search Query & Results:**
{query_result_pairs}

### Instructions:
1. **Format the response in clear bullet points.**  
2. **Ensure coherence**—avoid redundancy, conflicting statements, or multiple interpretations. Provide a **single, well-defined** answer per query.  
3. **Concise but valuable answers are preferred.** If exceeding the word limit (100-150 words) improves clarity and usefulness, prioritize helpfulness over brevity.  
4. **Use only the provided results.** If data is missing, **explicitly state the gap.**  
5. **If no relevant results exist, return "Insufficient data available to provide an accurate response."**  
6. **If the query is unrelated to finance, crypto, or blockchain, return "Query is outside my expertise."**  

Now, generate a structured response that follows these rules.
"""

    response = llm.invoke(prompt)
    print(response.content)
    return response.content
