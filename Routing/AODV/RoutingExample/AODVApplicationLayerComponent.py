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
from LinkLayers.GenericLinkLayer import LinkLayer
#from NetworkLayers.AllSeeingEyeNetworkLayer import AllSeingEyeNetworkLayer
from Routing.AODV.RoutingExample.AODVNetworkLayerComponent import AODVNetworkLayerComponent
from Routing.AODV.RoutingExample.AODVMessageTypes import AODVMessageTypes

registry = ComponentRegistry()

class AODVApplicationLayerComponent(ComponentModel):
    def on_init(self, eventobj: Event):
        print(f"Initializing {self.componentname}.{self.componentinstancenumber}")

    def on_message_from_bottom(self, eventobj: Event):
        print(f"On MSFRB {self.componentname}.{self.componentinstancenumber}")
        try:
            applmessage = eventobj.eventcontent
            hdr = applmessage.header
            print(f"Node-{self.componentinstancenumber} says Node-{hdr.messagefrom} has sent {hdr.messagetype} message")
            if hdr.messagetype == AODVMessageTypes.RREQ:
                print(f"{hdr.messagetype} has successfully delivered to {self.componentname}.{self.componentinstancenumber} from Node-{hdr.messagefrom}")
                if hdr.messageto == self.componentinstancenumber:  # RREQ received from destination
                    print(f"I received a message to {hdr.messageto} and I am {self.componentinstancenumber}")
                    #self.send_self(Event(self, "rrep",)) #TODO

            #Add to the Routing Table if the route doesn't exist
            #Otherwise, return the RREP msg because this node will know the rest of the route.
            elif hdr.messagetype == AODVMessageTypes.RREP:
                print(f"{hdr.messagetype} has successfully delivered to {self.componentname}.{self.componentinstancenumber} from Node-{hdr.messagefrom}")
        except AttributeError:
            print("Attribute Error")

    # print(f"{self.componentname}.{self.componentinstancenumber}: Gotton message {eventobj.content} ")
    # value = eventobj.content.value
    # value += 1
    # newmsg = MessageContent( value )
    # myevent = Event( self, "agree", newmsg )
    # self.trigger_event(myevent)

    def on_propose(self, eventobj: Event):
        print(f"On Propose AppLayerComponent {self.componentname}.{self.componentinstancenumber}")
        
        destination = 1
        hdr = GenericMessageHeader(AODVMessageTypes.ACCEPT, self.componentinstancenumber,
                                            destination)
        payload = GenericMessagePayload("23")
        proposalmessage = GenericMessage(hdr, payload)
        self.send_down(Event(self, EventTypes.MFRT, proposalmessage))

    def on_agree(self, eventobj: Event):
        print(f"Agreed on {eventobj.eventcontent} {self.componentname}.{self.componentinstancenumber}")

    def on_timer_expired(self, eventobj: Event):
        pass

    #On-demand behavior sustained with this.
    def sendPackageToNode(self, destNodeID,msgFromUser):
        print(f"On sendPackageToNode {self.componentname}.{self.componentinstancenumber}")
        destination = destNodeID
        #Checks whether destination node in the Routing Table of this Node.
        if destNodeID in self.RoutingTable:
            hdr = GenericMessageHeader(AODVMessageTypes.PROPOSE, self.componentinstancenumber,
                                                destination)
            payload = GenericMessagePayload(msgFromUser)
            message = GenericMessage(hdr, payload)
            print(f"Found {destNodeID}")

            self.send_down(Event(self, EventTypes.MFRT, message))
        else:
            print(f"Not found {destNodeID} in Routing Table of {self.componentname}.{self.componentinstancenumber}")
            hdr = GenericMessageHeader(AODVMessageTypes.RREQ, self.componentinstancenumber,
                                                destination)
            message = GenericMessage(hdr, None)
            self.send_self(Event(self, "rreq", message))

    #Route Disovery: route request
    def on_rreq(self, eventobj: Event):
        print(f"On rreq {eventobj.eventcontent} {self.componentname}.{self.componentinstancenumber}")
        self.send_down(Event(self,EventTypes.MFRT,eventobj.eventcontent))

    #Route Disovery: route response
    def on_rrep(self, eventobj: Event):
        print(f"On rrep {eventobj.eventcontent} {self.componentname}.{self.componentinstancenumber}")

    def __init__(self, componentname, componentinstancenumber):
        super().__init__(componentname, componentinstancenumber)
        
        #DestinationNode   NextNode    HopCount     SequenceNumber
        #self.RoutingTable = {}
        self.RoutingTable = { 7:[7,8,3,1] ,
                                6: [6,3,5,1]
                            }

        self.eventhandlers["rreq"] = self.on_rreq
        self.eventhandlers["rrep"] = self.on_rrep
        #self.eventhandlers["propose"] = self.on_propose
        
        #self.eventhandlers["agree"] = self.on_agree
        #self.eventhandlers["timerexpired"] = self.on_timer_expired

