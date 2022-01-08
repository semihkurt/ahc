from enum import Enum

class AODVMessageTypes(Enum):
    RREQ = "RREQ"
    RREP = "RREP"
    PROPOSE = "PROPOSE"
    ACCEPT = "ACCEPT"