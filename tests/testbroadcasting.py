import os
import sys
import random
from enum import Enum

sys.path.insert(0, os.getcwd())

import networkx as nx
import matplotlib.pyplot as plt

from Ahc import ComponentModel, Event, ConnectorTypes, Topology, EventTypes
from Ahc import ComponentRegistry, GenericMessage, GenericMessageHeader, GenericMessagePayload
from Broadcasting.Broadcasting import ControlledFlooding
from Channels.Channels import P2PFIFOFairLossChannel, P2PFIFOPerfectChannel
from LinkLayers.GenericLinkLayer import LinkLayer

registry = ComponentRegistry()


# define your own message types
class ApplicationLayerMessageTypes(Enum):
    PROPOSE = "PROPOSE"
    ACCEPT = "ACCEPT"


# define your own message header structure
class ApplicationLayerMessageHeader(GenericMessageHeader):
    pass


# define your own message payload structure
class ApplicationLayerMessagePayload(GenericMessagePayload):
    pass

class ApplicationLayerComponent(ComponentModel):
    def on_init(self, eventobj: Event):
        print(f"Initializing {self.componentname}.{self.componentinstancenumber}")

        if self.componentinstancenumber == 0:
            # destination = random.randint(len(Topology.G.nodes))
            destination = 1
            hdr = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.PROPOSE, self.componentinstancenumber,
                                                destination)
            payload = ApplicationLayerMessagePayload("23")
            proposalmessage = GenericMessage(hdr, payload)
            self.send_self(Event(self, "propose", proposalmessage))
        else:
            pass

    def on_message_from_bottom(self, eventobj: Event):
        try:
            applmessage = eventobj.eventcontent
            hdr = applmessage.header
            if hdr.messagetype == ApplicationLayerMessageTypes.ACCEPT:
                print(
                    f"Node-{self.componentinstancenumber} says Node-{hdr.messagefrom} has sent {hdr.messagetype} message")
            elif hdr.messagetype == ApplicationLayerMessageTypes.PROPOSE:
                print(
                    f"Node-{self.componentinstancenumber} says Node-{hdr.messagefrom} has sent {hdr.messagetype} message")
        except AttributeError:
            print("Attribute Error")

    # print(f"{self.componentname}.{self.componentinstancenumber}: Gotton message {eventobj.content} ")
    # value = eventobj.content.value
    # value += 1
    # newmsg = MessageContent( value )
    # myevent = Event( self, "agree", newmsg )
    # self.trigger_event(myevent)

    def on_propose(self, eventobj: Event):
        destination = 1
        hdr = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.ACCEPT, self.componentinstancenumber,
                                            destination)
        payload = ApplicationLayerMessagePayload("23")
        proposalmessage = GenericMessage(hdr, payload)
        self.send_down(Event(self, EventTypes.MFRT, proposalmessage))

    def on_agree(self, eventobj: Event):
        print(f"Agreed on {eventobj.eventcontent}")

    def on_timer_expired(self, eventobj: Event):
        pass

    def __init__(self, componentname, componentinstancenumber):
        super().__init__(componentname, componentinstancenumber)



class AdHocNode(ComponentModel):
  def on_message_from_top(self, eventobj: Event):
    self.send_down(Event(self, EventTypes.MFRT, eventobj.eventcontent))

  def on_message_from_bottom(self, eventobj: Event):
    self.send_up(Event(self, EventTypes.MFRB, eventobj.eventcontent))

  def __init__(self, componentname, componentid):
    # SUBCOMPONENTS
    self.applayer = ApplicationLayerComponent("ApplicationLayer", componentid)
    self.broadcastservice = ControlledFlooding("SimpleFlooding", componentid)
    self.linklayer = LinkLayer("LinkLayer", componentid)

    # CONNECTIONS AMONG SUBCOMPONENTS
    self.applayer.connect_me_to_component(ConnectorTypes.DOWN,self.broadcastservice)
    self.broadcastservice.connect_me_to_component(ConnectorTypes.UP,self.applayer)
    self.broadcastservice.connect_me_to_component(ConnectorTypes.DOWN, self.linklayer)
    self.linklayer.connect_me_to_component(ConnectorTypes.UP, self.broadcastservice)

    # Connect the bottom component to the composite component....
    self.linklayer.connect_me_to_component(ConnectorTypes.DOWN, self)
    self.connect_me_to_component(ConnectorTypes.UP, self.linklayer)

    super().__init__(componentname, componentid)

#    self.eventhandlers[EventTypes.MFRT] = self.onMessageFromTop
#    self.eventhandlers["messagefromchannel"] = self.onMessageFromChannel

def main():
  # G = nx.Graph()
  # G.add_nodes_from([1, 2])
  # G.add_edges_from([(1, 2)])
  
  
  G = nx.random_geometric_graph(5, 0.5)
  topo = Topology()
  topo.construct_from_graph(G, AdHocNode, P2PFIFOPerfectChannel)
  #for ch in topo.channels:
  #  topo.channels[ch].setPacketLossProbability(random.random())
  #  topo.channels[ch].setAverageNumberOfDuplicates(0)

  ComponentRegistry().print_components()

  topo.start()
  topo.plot()

  nx.draw(G, with_labels=True, font_weight='bold')
  plt.draw()
  plt.show()  # while (True): pass

  print(topo.nodecolors)

  #node = topo.get_random_node()
  #node.broadcastservice.senddownbroadcast(1,1)


if __name__ == "__main__":
  main()
