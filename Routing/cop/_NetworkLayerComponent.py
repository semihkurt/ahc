from Ahc import ComponentModel, Event, GenericMessage, GenericMessageHeader, EventTypes

class NetworkLayerComponent(ComponentModel):
    def __init__(self, componentname, componentid):
        super(NetworkLayerComponent, self).__init__(componentname, componentid)
        self.RoutingTable = {}

    def on_message_from_top(self, eventobj: Event):
        pass

    def on_message_from_bottom(self, eventobj: Event):
        pass
   