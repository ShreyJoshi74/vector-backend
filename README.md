# 🧠 DAG Validator Backend (Python)

This backend API validates automation workflows by checking whether the given graph forms a **Directed Acyclic Graph (DAG)** using **Kahn’s Algorithm**.  
It is designed to work with visual automation builders (like n8n, Zapier, or VectorShift-like UIs).

The service receives a list of **nodes** and **edges**, performs DAG validation, and returns:

- Total number of **nodes**
- Total number of **edges**
- Whether the structure is a **valid DAG**
- (Optional) Any cycles or invalid links

---

## 🚀 Why Kahn’s Algorithm?

Kahn’s Algorithm is chosen because it is:

### ✅ **Optimal for DAG detection**
It performs a linear-time topological sort in **O(V + E)**, making it extremely efficient even for large graphs.

### ✅ **Reliable cycle detection**
If Kahn’s algorithm cannot process all nodes, a cycle exists — making the graph **not a DAG**.

### ✅ **Easy to integrate**
Works perfectly with graphs coming from UI automation builders where edges are dynamic.

### ⚡ Perfect fit for workflow engines
Workflow automation systems **must be DAGs** to ensure:
- No infinite loops  
- No circular dependencies  
- Repeatable, deterministic execution order  

Kahn’s algorithm guarantees this.

---

## 🛠️ Tech Stack

| Component | Description |
|----------|-------------|
| **Python 3.x** | Backend language |
| **FastAPI** | (Depending on your implementation) REST API |
| **Kahn’s Algorithm** | DAG validation / topological sort |
| **Pydantic / JSON** | Request validation |

---

## 📥 Input Format

The backend expects a JSON payload like:

```json
{
  "nodes": ["A", "B", "C", "D"],
  "edges": [
    ["A", "B"],
    ["B", "C"],
    ["A", "D"]
  ]
}
