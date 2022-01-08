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
from NetworkLayers.AllSeeingEyeNetworkLayer import AllSeingEyeNetworkLayer

# define your own message types
class MessageTypes(Enum):
    RREQ = "RREQ"
    RREP = "RREP"
    PROPOSE = "PROPOSE"
    ACCEPT = "ACCEPT"

# define your own message types
class ApplicationLayerMessageTypes(Enum):
    RREQ = "RREQ"
    RREP = "RREP"
    PROPOSE = "PROPOSE"
    ACCEPT = "ACCEPT"

class ApplicationLayerComponent(ComponentModel):
    def on_init(self, eventobj: Event):
        print(f"Initializing {self.componentname}.{self.componentinstancenumber}")

    def on_message_from_bottom(self, eventobj: Event):
        print(f"On MSFRB ApplicationLayerComponent {self.componentname}.{self.componentinstancenumber}")

    # print(f"{self.componentname}.{self.componentinstancenumber}: Gotton message {eventobj.content} ")
    # value = eventobj.content.value
    # value += 1
    # newmsg = MessageContent( value )
    # myevent = Event( self, "agree", newmsg )
    # self.trigger_event(myevent)

    def on_propose(self, eventobj: Event):
        pass

    def on_agree(self, eventobj: Event):
        print(f"Agreed on {eventobj.eventcontent} {self.componentname}.{self.componentinstancenumber}")

    def on_timer_expired(self, eventobj: Event):
        pass

    def __init__(self, componentname, componentinstancenumber):
        super().__init__(componentname, componentinstancenumber)
        self.eventhandlers["propose"] = self.on_propose
        self.eventhandlers["agree"] = self.on_agree
        self.eventhandlers["timerexpired"] = self.on_timer_expired

