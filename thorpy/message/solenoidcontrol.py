from ._base import MessageWithData, MessageWithoutData
import struct

##### Solenoid Control Messages #####

class MGMSG_MOT_SET_SOL_OPERATINGMODE(MessageWithoutData):
    message_id = 0x04C0
    _params_names = ['message_id'] + ['chan_ident', 'mode'] + ['dest', 'source']

class MGMSG_MOT_REQ_SOL_OPERATINGMODE(MessageWithoutData):
    message_id = 0x04C1
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_SOL_OPERATINGMODE(MessageWithoutData):
    message_id = 0x04C2
    _params_names = ['message_id'] + ['chan_ident', 'mode'] + ['dest', 'source']

class MGMSG_MOT_SET_SOL_CYCLEPARAMS(MessageWithData):
    message_id = 0x04C3
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'on_time', 'off_time', 'num_cycles']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))        
    

class MGMSG_MOT_REQ_SOL_CYCLEPARAMS(MessageWithoutData):
    message_id = 0x04C4
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_SOL_CYCLEPARAMS(MessageWithData):
    message_id = 0x04C5
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'on_time', 'off_time', 'num_cycles']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))
    

class MGMSG_MOT_SET_SOL_INTERLOCKMODE(MessageWithoutData):
    message_id = 0x04C6
    _params_names = ['message_id'] + ['chan_ident', 'mode'] + ['dest', 'source']

class MGMSG_MOT_REQ_SOL_INTERLOCKMODE(MessageWithoutData):
    message_id = 0x04C7
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_SOL_INTERLOCKMODE(MessageWithoutData):
    message_id = 0x04C8
    _params_names = ['message_id'] + ['chan_ident', 'mode'] + ['dest', 'source']

class MGMSG_MOT_SET_SOL_STATE(MessageWithoutData):
    message_id = 0x04C6
    _params_names = ['message_id'] + ['chan_ident', 'state'] + ['dest', 'source']

class MGMSG_MOT_REQ_SOL_STATE(MessageWithoutData):
    message_id = 0x04C7
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_SOL_STATE(MessageWithoutData):
    message_id = 0x04C8
    _params_names = ['message_id'] + ['chan_ident', 'state'] + ['dest', 'source']
