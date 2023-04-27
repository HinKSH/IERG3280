# SIR model
#   0: susceptible
#   1: infectious
#   2: recovered

import snap
import random 
filename = "text.txt"

net = snap.LoadEdgeList(snap.PNEANet, filename, 0, 1)


# nodes with high page rank
# initial_node = [107, 1684, 1352, 1800, 483, 1589, 3437, 2543, 2602,2324]

# nodes with low page rank
initial_node = [379, 1534, 257, 2784, 3260, 2480, 2797, 451, 617, 738] 

# max step of infection
time_step = 2 

#initial the node state
for Node in net.Nodes():
    nid = Node.GetId()
    state = 0
    if nid in initial_node: 
        #initial the node in list as infected node
        state = 1
    else:
        #initial the other node as susceptible
        state = 0

    setState = net.AddIntAttrDatN(nid, state, "state")
    setState = net.AddIntAttrDatN(nid, 0, "step")

#infectious Process
infectiousPeriod = 0
numberOfNode = net.GetNodes()
number_recovNode = numberOfNode - len(initial_node)


while number_recovNode != numberOfNode:
    for Node in net.Nodes():
        nid = Node.GetId()
        #check if the connected node is infected or not
        # yes
        if net.GetIntAttrDatN(nid, "state") == 1:
            for connectedNode in Node.GetOutEdges():
                if (random.randint(0, 10) == 0) and (net.GetIntAttrDatN(connectedNode, "state") == 0): 
                    setState = net.AddIntAttrDatN(connectedNode, 1, "state")
                    # print("Test",setState)
            timeStamp = net.GetIntAttrDatN(nid, "step") + 1
            setState = net.AddIntAttrDatN(nid, timeStamp, "step")
            
            #if time step is up, the node get recovered
            if timeStamp == time_step:
                setState = net.AddIntAttrDatN(nid, 2, "state")
                # print("Test",setState)
    temp = 0
    
    #count the infected node in each process
    for Node in net.Nodes():
        nid = Node.GetId()
        if (net.GetIntAttrDatN(nid, "state") == 1):
            break
        elif (net.GetIntAttrDatN(nid, "state") == 0) or (net.GetIntAttrDatN(nid, "state") == 2):
            temp += 1    
    number_recovNode = temp

    print ("Infectious Period %4d\t Infected Node = %5d" % (infectiousPeriod, numberOfNode-number_recovNode))
    infectiousPeriod += 1

print ("End of spreading rumors")

#Graph plotting , set the color of each node
#   0: susceptible : Green
#   2: recovered : Red

color = snap.TIntStrH()
for Node in net.Nodes():
    nid = Node.GetId()
    if net.GetIntAttrDatN(nid, "state") == 0:
        color[nid] = "green"
    elif net.GetIntAttrDatN(nid, "state") == 2:
        color[nid] = "red"
    else:
        print ("Error! There is infectious node in the network!")


Graph = snap.TIntV()
graph_node = []
for i in initial_node:
    for connectedNode in net.GetNI(i).GetOutEdges():
        graph_node = list(set(graph_node) | set([connectedNode])) 
    graph_node = list(set(graph_node) | set([i])) 

for nid in graph_node:
    Graph.Add(nid)
sub = snap.ConvertSubGraph(snap.PNEANet, net, Graph)

snap.SaveGViz(sub, "SIRsub.dot", "SIR simulation subnet", True, color)
