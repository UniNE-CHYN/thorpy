from ._base import MessageWithData, MessageWithoutData
import struct

##### Generic System Control Messages #####

class MGMSG_MOD_IDENTIFY(MessageWithoutData):
    """Instruct hardware unit to identify itself (by flashing its front panel
    LEDs)."""
    message_id = 0x0223
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_MOD_SET_CHANENABLESTATE(MessageWithoutData):
    """Sent to enable or disable the specified drive channel.
    
    Fields:
    - chan_ident (0x01, 0x02)
    - chan_enable_state (0x01: enable, 0x02: disable)"""
    
    message_id = 0x0210
    _params_names = ['message_id'] + ['chan_ident', 'chan_enable_state'] + ['dest', 'source']

class MGMSG_MOD_REQ_CHANENABLESTATE(MessageWithoutData):
    """See MGMSG_MOD_SET_CHANENABLESTATE
    
    Fields:
    - chan_ident"""
    message_id = 0x0211
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOD_GET_CHANENABLESTATE(MessageWithoutData):
    """See MGMSG_MOD_SET_CHANENABLESTATE
    
    Fields:
    - chan_ident
    - chan_enable_state"""
    message_id = 0x0212
    _params_names = ['message_id'] + ['chan_ident', 'chan_enable_state'] + ['dest', 'source']

class MGMSG_HW_DISCONNECT(MessageWithoutData):
    """Sent by the hardware unit or host when either wants to disconnect
    from the Ethernet/USB bus."""
    message_id = 0x0002
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_HW_RESPONSE(MessageWithoutData):
    """Sent by the controllers to notify APT Server of some event that
    requires user intervention, usually some fault or error condition that
    needs to be handled before normal operation can resume. The
    message transmits the fault code as a numerical value – see Return
    Codes."""
    message_id = 0x0080
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_HW_RICHRESPONSE(MessageWithData):
    """Similarly to HW_RESPONSE, this message is s ent by the
    controllers to notify APT Server of some event that requires user
    intervention, usually some fault or error condition that needs to be
    handled before normal operation can resume. However unlike
    HW_RESPONSE, this message also transmits a printable text string.
    Upon receiving the message, APT Server displays both the numerical
    value and the text information, which is useful in finding the cause
    of the problem.
    
    Fields:
    - msg_ident
    - code
    - notes"""
    
    message_id = 0x0081
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', '64s']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['msg_ident', 'code', 'notes']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_HW_START_UPDATEMSGS(MessageWithoutData):
    """Sent to start status updates from the embedded controller. Status
    update messages contain information about the position and status
    of the controller (for example limit switch status, motion indication,
    etc). The messages will be sent by the controller periodically until it
    receives a STOP STATUS UPDATE MESSAGES command. In
    applications where spontaneous messages (i.e. messages which are
    not received as a response to a specific command) must be avoided
    the same information can also be obtained by using the relevant
    GET_STATUTSUPDATES function."""
    message_id = 0x0011
    _params_names = ['message_id'] + ['update_rate', None] + ['dest', 'source']

class MGMSG_HW_STOP_UPDATEMSGS(MessageWithoutData):
    """Sent to stop status updates from the controller – usually called by a
    client application when it is shutting down, to instruct the controller
    to turn off status updates to prevent USB buffer overflows on the
    PC."""
    message_id = 0x0012
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_HW_REQ_INFO(MessageWithoutData):
    """Sent to request hardware information from the controller."""
    message_id = 0x0005
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_HW_GET_INFO(MessageWithData):
    """See MGMSG_HW_REQ_INFO.
    
    Fields:
    - serial_number
    - model_number
    - type
    - firmware_version
    - notes
    - hw_version
    - mod_state
    - nchs
    """
    message_id = 0x0006
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['I', '8s', 'H', '4s', '48s', '12s', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['serial_number', 'model_number', 'type', 'firmware_version', 'notes', 'empty_space', 'hw_version', 'mod_state', 'nchs']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))

class MGMSG_RACK_REQ_BAYUSED(MessageWithoutData):
    """Sent to determine whether the specified bay in the controller is
    occupied.
    
    Fields:
    - bay_ident"""
    message_id = 0x0060
    _params_names = ['message_id'] + ['bay_ident', None] + ['dest', 'source']

class MGMSG_RACK_GET_BAYUSED(MessageWithoutData):
    """See MGMSG_RACK_REQ_BAYUSED
    
    Fields:
    - bay_ident
    - bay_state"""
    
    message_id = 0x0061
    _params_names = ['message_id'] + ['bay_ident', 'bay_state'] + ['dest', 'source']

class MGMSG_HUB_REQ_BAYUSED(MessageWithoutData):
    """Sent to determine which bay a specific T-Cube is fitted."""
    message_id = 0x0065
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_HUB_GET_BAYUSED(MessageWithoutData):
    """See MGMSG_HUB_REQ_BAYUSED.
    
    Fields:
    - bay_ident
    """
    message_id = 0x0066
    _params_names = ['message_id'] + ['bay_ident', None] + ['dest', 'source']

class MGMSG_RACK_REQ_STATUSBITS(MessageWithoutData):
    """This method is applicable only to the MMR modular rack, and 2- and 3-channel card slot
    type controllers such as the BSC103 and BPC202.
    
    The USER IO connector on the rear panel of these units exposes a
    number of digital inputs. This function returns a number of status
    flags pertaining to the status of the inputs on the rack modules, or
    the motherboard of the controller unit hosting the single channel
    controller card.
    These flags are returned in a single 32 bit integer parameter and can
    provide additional useful status information for client application
    development. The individual bits (flags) of the 32 bit integer value
    correspond to digital output state.
    
    Fields:
    - status_bits"""
    message_id = 0x0226
    _params_names = ['message_id'] + ['status_bits', None] + ['dest', 'source']

class MGMSG_RACK_GET_STATUSBITS(MessageWithData):
    """See MGMSG_RACK_REQ_STATUSBITS"""
    message_id = 0x0227
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['sstatus_bits']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))
    
class MGMSG_RACK_SET_DIGOUTPUTS(MessageWithoutData):
    """This method is applicable only to the MMR rack modules, and 2- and 3-channel card slot
    type controllers such as the BSC103 and BPC202.
    
    The USER IO connector on the rear panel of these units exposes a
    number of digital outputs. These functions set and return the status
    of the outputs on the rack modules, or the motherboard of the
    controller unit hosting the single channel controller card.
    These flags are returned in a single 32 bit integer parameter and can
    provide additional useful status information for client application
    development. The individual bits (flags) of the 32 bit integer value
    are described below.
    
    Fields:
    - dig_op"""
    
    #FIXME: Doc is likely to be WRONG. Fix this definition!
    message_id = 0x0228
    _params_names = ['message_id'] + ['dig_op', None] + ['dest', 'source']

class MGMSG_RACK_REQ_DIGOUTPUTS(MessageWithoutData):
    """See MGMSG_RACK_SET_DIGOUTPUTS"""
    message_id = 0x0229
    #FIXME: Doc is likely to be WRONG. Fix this definition!
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_RACK_GET_DIGOUTPUTS:
    """See MGMSG_RACK_SET_DIGOUTPUTS"""
    message_id = 0x0230
    #FIXME: Doc is likely to be WRONG. Fix this definition!
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_MOD_SET_DIGOUTPUTS(MessageWithoutData):
    """The CONTROL IO connector on the rear panel of the unit exposes a
    number of digital outputs. The number of outputs available depends
    on the type of unit. This message is used to configure these digital
    outputs.
    
    Fields:
    - bits"""
    message_id = 0x0213
    _params_names = ['message_id'] + ['bits', None] + ['dest', 'source']

class MGMSG_MOD_REQ_DIGOUTPUTS(MessageWithoutData):
    """See MGMSG_MOD_SET_DIGOUTPUTS"""
    message_id = 0x0214
    #FIXME: Fix this definition, is bits really required here?
    _params_names = ['message_id'] + ['bits', None] + ['dest', 'source']

class MGMSG_MOD_GET_DIGOUTPUTS:
    """See MGMSG_MOD_SET_DIGOUTPUTS"""
    message_id = 0x0215
    _params_names = ['message_id'] + ['bits', None] + ['dest', 'source']
