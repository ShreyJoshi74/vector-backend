
from collections import deque
from typing import List, Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Pipeline(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


@app.get("/")
def read_root():
    return {"Ping": "Pong"}


def is_dag(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> bool:
    
    node_ids = [n.get("id") for n in nodes]
    indegree = {nid: 0 for nid in node_ids}
    adj = {nid: [] for nid in node_ids}

    for e in edges:
        src = e.get("source")
        tgt = e.get("target")
        if src is None or tgt is None:
            continue

        if src not in adj:
            adj[src] = []
            indegree.setdefault(src, 0)

        if tgt not in adj:
            adj[tgt] = []
        indegree[tgt] = indegree.get(tgt, 0) + 1
        adj[src].append(tgt)

    q = deque([nid for nid, deg in indegree.items() if deg == 0])
    visited = 0

    while q:
        v = q.popleft()
        visited += 1
        for neighbor in adj.get(v, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                q.append(neighbor)

    total_nodes = len(indegree)
    return visited == total_nodes


@app.post("/pipelines/parse")
def parse_pipeline(pipeline: Pipeline):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    dag = is_dag(pipeline.nodes, pipeline.edges)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": dag,
    }
