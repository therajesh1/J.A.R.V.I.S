# fallback_llm.py
from llama_cpp import Llama
import time

# Initialize the LLM model (loads once)
llm = Llama(
    model_path="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",  # adjust path if needed
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=20,
    use_mlock=True,
    use_mmap=True,
    verbose=False
)

def query_llm(prompt):
    system_prompt = (
        "You are a helpful AI assistant. Answer the following user query in simple English.\n\n"
        f"User: {prompt}\nAI:"
    )

    start = time.time()
    response = llm(
        system_prompt,
        max_tokens=200,
        temperature=0.7,
        stop=["User:", "AI:"]
    )["choices"][0]["text"].strip()

    print("📄 LLM Response:", response)
    print("⏱️ Response Time:", round(time.time() - start, 2), "sec")
    return response
