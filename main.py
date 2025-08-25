from graph.workflow import build_graph



if __name__ == "__main__":
    graph =  build_graph()
    result = graph.invoke({})
    print("✅ Report generated at:", result["pdf_path"])
