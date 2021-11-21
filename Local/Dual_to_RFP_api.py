
"""API

Generates floorplamns for given graph data as input.
Current support only for rectangular floorplans.
A running example is available.

"""
import source.inputgraph as inputgraph

normalize_const = 50

def graph_to_rfp(input_data):
    """Generates a rfp for given graph data

    Args:
        input_data: A dictionary containing keys:
            nodes: Node data of the graph.
            edges: Edge data of the graph.
            command: GPLAN command to try (single and multiple support right now)

    Returns:
        output_data: A list containing multiple or single floorplan.
            Each floorplan is a list of dictionary where each dictionary denotes a room.
    """
    nodecnt = len(input_data['nodes'])
    edgecnt = len(input_data['edges'])
    edgedata = []
    for edge in input_data['edges']:
        edgedata.append([edge['source'],edge['target']])
    node_coordinates = []
    for node in input_data['nodes']:
        node_coordinates.append([node['x'],node['y']])
    graph = inputgraph.InputGraph(nodecnt, edgecnt, edgedata, node_coordinates)
    output_data  = []
    if(input_data['command'] == 'single'):
        graph.single_dual()
        output_fp = []
        for node in input_data['nodes']:
            output_fp.append({"id": node["id"]
                                ,"label": node["id"]
                                ,"color": node["color"]
                                ,"topLeft": [int(graph.room_x[node["id"]] *normalize_const), int(graph.room_y[node["id"]] *normalize_const)]
                                ,"width": int(graph.room_width[node["id"]] *normalize_const)
                                ,"height": int(graph.room_height[node["id"]] *normalize_const)})
        output_data.append(output_fp)
    elif(input_data['command'] == 'multiple'):
        graph.multiple_dual()
        for idx in range(graph.fpcnt):
            output_fp = []
            for node in input_data['nodes']:
                output_fp.append({"id": node["id"]
                                    ,"label": node["id"]
                                    ,"color": node["color"]
                                    ,"topLeft": [int(graph.room_x[idx][node["id"]] *normalize_const), int(graph.room_y[idx][node["id"]] *normalize_const)]
                                    ,"width": int(graph.room_width[idx][node["id"]] *normalize_const)
                                    ,"height": int(graph.room_height[idx][node["id"]] *normalize_const)})
            output_data.append(output_fp)
    return output_data
    



if __name__ == "__main__":
    input_data = {
        "nodes": [
            {"id": 0, "label": "kitchen", "x":14, "y":20, "color" :  "#e7e7e7" },
            {"id": 1, "label": "living room", "x":25, "y":20, "color" :  "#e7e7e7" },
            {"id": 2, "label": "rotunda", "x":20, "y":30 , "color" :  "#e7e7e7" }],
        "edges": [
            {"source": 0, "target": 1},
            {"source": 1, "target": 2},
            {"source": 2, "target": 0}],
        "command": "single"
    }
    dual_to_rfp(input_data)

    input_data = {
        "nodes": [
            {"id": 0, "label": "kitchen", "x":14, "y":20, "color" :  "#e7e7e7" },
            {"id": 1, "label": "living room", "x":25, "y":20, "color" :  "#e7e7e7" },
            {"id": 2, "label": "rotunda", "x":20, "y":30 , "color" :  "#e7e7e7" }],
        "edges": [
            {"source": 0, "target": 1},
            {"source": 1, "target": 2},
            {"source": 2, "target": 0}],
        "command": "multiple"
    }
    dual_to_rfp(input_data)