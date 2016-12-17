""" 
Stored consants for
configuring the coretemp
module    
"""

''' Chip type '''
CHIP = "coretemp-isa-0000"

''' Feature subtypes '''
SUB_MAX_TYPE = 513
SUB_CRT_TYPE = 516

''' Threshold disposition constants '''
NORM = "NORMAL"
HIGH = "HIGH"
CRTC = "CRITICAL!"

''' Alert message constants '''
ARR_MSG = "Failure to Initialize Alert: %s" 
SND_MSG = "Failure to send Alert message: %s"
INV_MSG = "Error in 'coretemp.properties'. Interval value must be a number. Using default %s"
SMT_MSG = "Could not find mail server at %s:%s. Got response: %s"
HDR_MSG = "System Core Temperature Notification! The following CPU components on the host have registered above the configured threshold(s):"
