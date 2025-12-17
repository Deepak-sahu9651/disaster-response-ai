from fastapi import FastAPI
from pydantic import BaseModel
import networkx as nx
from shapely.geometry import LineString, Polygon

app = FastAPI(title="Disaster Response AI System")

# Dummy flood zone
flood_zone = Polygon([
    (77.19, 28.60),
    (77.21, 28.60),
    (77.21, 28.62),
    (77.19, 28.62)
])

def create_graph():
    G = nx.Graph()
    G.add_node(1, pos=(77.18, 28.60))
    G.add_node(2, pos=(77.20, 28.61))
    G.add_node(3, pos=(77.22, 28.60))

    G.add_edge(1, 2)
    G.add_edge(2, 3)
    return G

class Route(BaseModel):
    start: int
    end: int

@app.get("/")
def home():
    return {"message": "Disaster Response AI is running"}

@app.get("/predict-flood")
def predict_flood():
    return {
        "flood_zone": list(flood_zone.exterior.coords),
        "risk": "HIGH"
    }

@app.post("/route")
def safe_route(data: Route):
    G = create_graph()
    safe_edges = []

    for u, v in G.edges():
        line = LineString([G.nodes[u]['pos'], G.nodes[v]['pos']])
        if not line.intersects(flood_zone):
            safe_edges.append((u, v))

    if (data.start, data.end) in safe_edges or (data.end, data.start) in safe_edges:
        return {"route": [data.start, data.end], "status": "SAFE"}
    else:
        return {"status": "NO SAFE ROUTE FOUND"}

@app.get("/emergency-message")
def message(area: str):
    return {
        "message": f"⚠️ ALERT: {area} mein flood risk HIGH hai. Kripya safe jagah par shift karein. Helpline: 112"
    }
