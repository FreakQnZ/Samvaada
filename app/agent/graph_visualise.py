import sys
import os

project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(project_root)

from agent.graph import build_agent_app
from IPython.display import Image, display

app = build_agent_app()
png_bytes = app.get_graph().draw_mermaid_png()

# Step 3: Display inline in Jupyter
display(Image(data=png_bytes))

# Step 4: Save the image to disk
with open("agent_graph_mermaid.png", "wb") as f:
    f.write(png_bytes)

print("Graph saved to agent_graph_mermaid.png")
