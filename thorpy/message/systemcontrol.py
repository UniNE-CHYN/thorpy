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
    
    :param chan_ident: channel number (0x01, 0x02)
    :type chan_ident: int 
    :param chan_enable_state: is channel enabled (0x01: enable, 0x02: disable)
    :type chan_enable_state: int"""
    
    message_id = 0x0210
    _params_names = ['message_id'] + ['chan_ident', 'chan_enable_state'] + ['dest', 'source']

class MGMSG_MOD_REQ_CHANENABLESTATE(MessageWithoutData):
    """See :class:`MGMSG_MOD_SET_CHANENABLESTATE`.
    
    :param chan_ident: channel number (0x01, 0x02)
    :type chan_ident: int"""
    message_id = 0x0211
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOD_GET_CHANENABLESTATE(MessageWithoutData):
    """See :class:`MGMSG_MOD_SET_CHANENABLESTATE`.
    
    :param chan_ident: channel number (0x01, 0x02)
    :type chan_ident: int
    :param chan_enable_state: is channel enabled (0x01: enable, 0x02: disable)
    :type chan_enable_state: int"""
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
    """Similarly to :class:`MGMSG_HW_RESPONSE`, this message is sent by the
    controllers to notify APT Server of some event that requires user
    intervention, usually some fault or error condition that needs to be
    handled before normal operation can resume. However unlike
    :class:`MGMSG_HW_RESPONSE`, this message also transmits a printable text string.
    Upon receiving the message, APT Server displays both the numerical
    value and the text information, which is useful in finding the cause
    of the problem.
    
    :param msg_ident: If the message is sent in response to an APT message, these
        bytes show the APT message number that evoked the
        message. Most often though the message is transmitted as
        a result of some unexpected fault condition, in which case
        these bytes are 0x00, 0x00
    :type msg_ident: int
    :param code: This is an internal Thorlabs specific code that specifies the
        condition that has caused the message (see Return Codes).
    :type code: int
    :param notes: This is a zero-terminated printable (ascii) text string that
        contains the textual information about the condition that
        has occurred. For example: “Hardware Time Out Error”.
    :type notes: string"""
    
    message_id = 0x0081
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', '64s']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['msg_ident', 'code', 'notes']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_HW_START_UPDATEMSGS(MessageWithoutData):
    """Sent to start status updates from the embedded controller. Status
    update messages contain information about the position and status
    of the controller (for example limit switch status, motion indication,
    etc). The messages will be sent by the controller periodically until it
    receives a :class:`MGMSG_HW_STOP_UPDATEMSGS` command. In
    applications where spontaneous messages (i.e. messages which are
    not received as a response to a specific command) must be avoided
    the same information can also be obtained by using the relevant
    :class:`~thorpy.message.motorcontrol.MGMSG_MOT_GET_STATUSUPDATE` or
    :class:`~thorpy.message.motorcontrol.MGMSG_MOT_GET_DCSTATUSUPDATE` message."""
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
    """See :class:`MGMSG_HW_REQ_INFO`.
    
    :param serial_number: unique 8-digit serial number
    :type serial_number: int
    :param model_number: alphanumeric model number
    :type: model_number: string
    :param type: hardware type (not really documented)
    :type type: int
    :param firmware_version: firmware version
        
        - byte 0 = minor revision number
        - byte 1 = interim revision number
        - byte 2 = major revision number
        - byte 3 = unused

    :type firmware_version: bytes
    :param notes: arbitrary alphanumeric information string (48 bytes)
    :type notes: string
    :param empty_space: ironically, not an empty space. Contain undocumented
        information which helps identifying the connected stage. See
        :func:`~thorpy.stages.stage_name_from_get_hw_info` for the reversed
        engineered algorithm.
    :type empty_space: bytes
    :param hw_version: the hardware version number
    :type hw_version: int
    :param mod_state: the modification state of the hardware
    :type mod_state: int
    :param nchs: number of channels
    :type nchs: int
    """
    message_id = 0x0006
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['I', '8s', 'H', '4s', '48s', '12s', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['serial_number', 'model_number', 'type', 'firmware_version', 'notes', 'empty_space', 'hw_version', 'mod_state', 'nchs']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))

class MGMSG_RACK_REQ_BAYUSED(MessageWithoutData):
    """Sent to determine whether the specified bay in the controller is
    occupied.
    
    :param bay_ident: bay identifier (0x01 to 0x09, for bay 1 to bay 9)
    :type bay_ident: int
    """
    message_id = 0x0060
    _params_names = ['message_id'] + ['bay_ident', None] + ['dest', 'source']

class MGMSG_RACK_GET_BAYUSED(MessageWithoutData):
    """See :class:`MGMSG_RACK_REQ_BAYUSED`.
    
    :param bay_ident: bay identifier (0x01 to 0x09, for bay 1 to bay 9)
    :type bay_ident: int
    :param bay_state: bay state (0x01: occopied, 0x02: empty, unused)
    :type bay_state: int"""
    
    message_id = 0x0061
    _params_names = ['message_id'] + ['bay_ident', 'bay_state'] + ['dest', 'source']

class MGMSG_HUB_REQ_BAYUSED(MessageWithoutData):
    """Sent to determine which bay a specific T-Cube is fitted."""
    message_id = 0x0065
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_HUB_GET_BAYUSED(MessageWithoutData):
    """See :class:`MGMSG_HUB_REQ_BAYUSED`.
    
    :param bay_ident: bay identifier (0x01 to 0x06, for bay 1 to bay 6)
    :type bay_ident: int
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
    
    :param status_bits: The status bits for the associated controller channel.
        
        - bit 1: Digital output 1 state (1 - logic high, 0 - logic low).
        - bit 2: Digital output 1 state (1 - logic high, 0 - logic low).
        - bit 3: Digital output 1 state (1 - logic high, 0 - logic low).
        - bit 4: Digital output 1 state (1 - logic high, 0 - logic low).

    :type status_bits: int"""
    message_id = 0x0226
    _params_names = ['message_id'] + ['status_bits', None] + ['dest', 'source']

class MGMSG_RACK_GET_STATUSBITS(MessageWithData):
    """See :class:`MGMSG_RACK_REQ_STATUSBITS`."""
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
    
    .. todo::
        Not sure exactly how it behaves. Fix if we have access to the hardware!
    
    :param dig_op:
    :type dig_op: int"""
    
    message_id = 0x0228
    _params_names = ['message_id'] + ['dig_op', None] + ['dest', 'source']

class MGMSG_RACK_REQ_DIGOUTPUTS(MessageWithoutData):
    """See :class:`MGMSG_RACK_SET_DIGOUTPUTS`."""
    message_id = 0x0229
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_RACK_GET_DIGOUTPUTS:
    """See :class:`MGMSG_RACK_SET_DIGOUTPUTS`."""
    message_id = 0x0230
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_MOD_SET_DIGOUTPUTS(MessageWithoutData):
    """The CONTROL IO connector on the rear panel of the unit exposes a
    number of digital outputs. The number of outputs available depends
    on the type of unit. This message is used to configure these digital
    outputs.
    
    :param bits:
    :type bits: int"""
    message_id = 0x0213
    _params_names = ['message_id'] + ['bits', None] + ['dest', 'source']

class MGMSG_MOD_REQ_DIGOUTPUTS(MessageWithoutData):
    """See :class:`MGMSG_MOD_SET_DIGOUTPUTS`.
    
    :param bits:
    :type bits: int"""
    message_id = 0x0214
    #FIXME: Fix this definition, is bits really required here?
    _params_names = ['message_id'] + ['bits', None] + ['dest', 'source']

class MGMSG_MOD_GET_DIGOUTPUTS:
    """See :class:`MGMSG_MOD_SET_DIGOUTPUTS`.
    
    :param bits:
    :type bits: int"""
    message_id = 0x0215
    _params_names = ['message_id'] + ['bits', None] + ['dest', 'source']
