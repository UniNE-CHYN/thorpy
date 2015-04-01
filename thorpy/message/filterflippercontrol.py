from ._base import MessageWithData, MessageWithoutData
import struct

##### Filter Flipper Control Messages #####
class MGMSG_MOT_SET_MFF_OPERPARAMS(MessageWithData):
    """Used to set various operating parameters that dictate the function of the
    MFF series flipper unit.
    
    Fields:
    - chan_ident
    - i_transit_time
    - i_transit_time_adc
    - oper_mode_1
    - sig_mode_1
    - pulse_width_1
    - oper_mode_2
    - sig_mode_2
    - pulse_width_2
    """
    message_id = 0x0510
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'H', 'H', 'I', 'H', 'H', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'i_transit_time', 'i_transit_time_adc', 'oper_mode_1', 'sig_mode_1', 'pulse_width_1', 'oper_mode_2', 'sig_mode_2', 'pulse_width_2', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))        

class MGMSG_MOT_REQ_MFF_OPERPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_MFF_OPERPARAMS.
    
    Fields:
    - chan_ident"""
    
    message_id = 0x0511
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_MFF_OPERPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_MFF_OPERPARAMS.

    Fields:
    - chan_ident
    - i_transit_time
    - i_transit_time_adc
    - oper_mode_1
    - sig_mode_1
    - pulse_width_1
    - oper_mode_2
    - sig_mode_2
    - pulse_width_2
    """    
    message_id = 0x0512
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'H', 'H', 'I', 'H', 'H', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'i_transit_time', 'i_transit_time_adc', 'oper_mode_1', 'sig_mode_1', 'pulse_width_1', 'oper_mode_2', 'sig_mode_2', 'pulse_width_2', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))      
