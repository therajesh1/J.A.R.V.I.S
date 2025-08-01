
from tinydb import TinyDB, Query

db = TinyDB("memory.json")

def save_to_memory(question, answer):
    db.insert({"question": question, "answer": answer})

def retrieve_memory(query_text):
    Q = Query()
    results = db.search(Q.question.matches(query_text, flags=0))
    return results[0]["answer"] if results else None
