import os
import sys
import time
import random
from enum import Enum

sys.path.insert(0, os.getcwd())

import networkx as nx
import matplotlib.pyplot as plt

from Ahc import ComponentModel, Event, ConnectorTypes, Topology
from Ahc import ComponentRegistry
from Ahc import GenericMessagePayload, GenericMessageHeader, GenericMessage, EventTypes
from Channels.Channels import P2PFIFOPerfectChannel
#from LinkLayers.GenericLinkLayer import LinkLayer
#from NetworkLayers.AllSeeingEyeNetworkLayer import AllSeingEyeNetworkLayer
from Routing.AODV.RoutingExample.GenericLinkLayer import LinkLayer
from Routing.AODV.RoutingExample.AODVNetworkLayerComponent import AODVNetworkLayerComponent
from Routing.AODV.RoutingExample.AODVApplicationLayerComponent import AODVApplicationLayerComponent

registry = ComponentRegistry()

class AODVNode(ComponentModel):
    def on_init(self, eventobj: Event):
        print(f"Initializing {self.componentname}.{self.componentinstancenumber}")

    def on_message_from_top(self, eventobj: Event):
        print(f"On MFRT {self.componentname}.{self.componentinstancenumber}")
        self.send_down(Event(self, EventTypes.MFRT, eventobj.eventcontent))

    def on_message_from_bottom(self, eventobj: Event):
        print(f"On MFRB {self.componentname}.{self.componentinstancenumber}")
        self.send_up(Event(self, EventTypes.MFRB, eventobj.eventcontent))

    def __init__(self, componentname, componentid):
        super(AODVNode,self).__init__(componentname, componentid)

        # SUBCOMPONENTS
        self.applayer = AODVApplicationLayerComponent(AODVApplicationLayerComponent.__name__, componentid) 
        self.netlayer = AODVNetworkLayerComponent(AODVNetworkLayerComponent.__name__, componentid)
        self.linklayer = LinkLayer(LinkLayer.__name__, componentid)
        
        # CONNECTIONS AMONG SUBCOMPONENTS
        self.applayer.connect_me_to_component(ConnectorTypes.DOWN, self.netlayer)
        self.netlayer.connect_me_to_component(ConnectorTypes.DOWN, self.linklayer)
        self.linklayer.connect_me_to_component(ConnectorTypes.DOWN, self)

        self.netlayer.connect_me_to_component(ConnectorTypes.UP, self.applayer)
        self.linklayer.connect_me_to_component(ConnectorTypes.UP, self.netlayer)
        self.connect_me_to_component(ConnectorTypes.UP, self.linklayer)
        

    def sendPackageToNode(self, nodeID, msg):
        print(f"On sendPackageToNode {self.componentname}.{self.componentinstancenumber}")
        self.applayer.sendPackageToNode(nodeID,msg)
        #message_header = GenericMessageHeader("SEND",str(self.componentinstancenumber),
        #                   str(nodeComponentID))                                          
        #message = GenericMessage(message_header, "Hello")
        #self.send_up(Event(self,EventTypes.MFRB,message))

        #message_payload = self.TOUEG(self.all_process_ids, neighbor_ids, self.neighbor_weights)
        #message_header = GenericMessageHeader("ROUTINGCOMPLETED", self.componentname+"-"+str(self.componentinstancenumber),
        #                                      "Coordinator-"+str(self.componentinstancenumber))
        #message = GenericMessage(message_header, message_payload)
        #event = Event(self, EventTypes.MFRP, message)
        #self.send_peer(event)


        #self.send_up(Event(self, EventTypes.MFRB, eventobj.eventcontent))


        
edges = [(0, 1, {"weight": 1}), (0, 2, {"weight": 1}), (1, 3, {"weight": 1}), (2, 4, {"weight": 1}), (4, 5, {"weight": 1}),
         (3, 5, {"weight": 1}), (1, 4, {"weight": 1}), (4, 6, {"weight": 1}), (4, 7, {"weight": 1}),
         (6, 8, {"weight": 1}), (8, 9, {"weight": 1}), (7, 10, {"weight": 1}), (7, 11, {"weight": 1}),
         (11, 13, {"weight": 1}), (2, 12, {"weight": 1}),
         (7, 9, {"weight": 1})]


def main():
    # G = nx.Graph()
    # G.add_nodes_from([1, 2])
    # G.add_edges_from([(1, 2)])
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.draw()
    
    #Toueg's edges fixed size determined example
    G = nx.Graph()
    G.add_edges_from(edges)
    nx.draw(G, with_labels=True, font_weight='bold')
    topo = Topology()
    topo.construct_from_graph(G, AODVNode, P2PFIFOPerfectChannel)

    #Random graph
    #G = nx.random_geometric_graph(5, 0.5)
    #nx.draw(G, with_labels=True, font_weight='bold')
    #plt.draw()

    #topo = Topology()
    #topo.construct_from_graph(G, AODVNode, P2PFIFOPerfectChannel)
    topo.start()
 
    
    nodeX = topo.get_random_node()
    nodeY = topo.get_random_node()
    print(nodeX.componentinstancenumber)
    print(nodeY.componentinstancenumber)

    nodeX.sendPackageToNode(5,"Hello")

    plt.show()  # while (True): pass


if __name__ == "__main__":
    main()
