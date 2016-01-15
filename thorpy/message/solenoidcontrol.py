from ._base import Message


##### Solenoid Control Messages #####
class MGMSG_MOT_GET_SOL_CYCLEPARAMS(Message):
    id = 0x4c5
    is_long_cmd = True
    parameters = [('chan_ident', 'H'), ('on_time', 'I'), ('off_time', 'I'), ('num_cycles', 'I')]


class MGMSG_MOT_GET_SOL_INTERLOCKMODE(Message):
    id = 0x4c8
    parameters = [('chan_ident', 'B'), ('mode', 'B')]


class MGMSG_MOT_GET_SOL_OPERATINGMODE(Message):
    id = 0x4c2
    parameters = [('chan_ident', 'B'), ('mode', 'B')]


class MGMSG_MOT_GET_SOL_STATE(Message):
    id = 0x4c8
    parameters = [('chan_ident', 'B'), ('state', 'B')]


class MGMSG_MOT_REQ_SOL_CYCLEPARAMS(Message):
    id = 0x4c4
    parameters = [('chan_ident', 'B'), (None, 'B')]


class MGMSG_MOT_REQ_SOL_INTERLOCKMODE(Message):
    id = 0x4c7
    parameters = [('chan_ident', 'B'), (None, 'B')]


class MGMSG_MOT_REQ_SOL_OPERATINGMODE(Message):
    id = 0x4c1
    parameters = [('chan_ident', 'B'), (None, 'B')]


class MGMSG_MOT_REQ_SOL_STATE(Message):
    id = 0x4c7
    parameters = [('chan_ident', 'B'), (None, 'B')]


class MGMSG_MOT_SET_SOL_CYCLEPARAMS(Message):
    id = 0x4c3
    is_long_cmd = True
    parameters = [('chan_ident', 'H'), ('on_time', 'I'), ('off_time', 'I'), ('num_cycles', 'I')]


class MGMSG_MOT_SET_SOL_INTERLOCKMODE(Message):
    id = 0x4c6
    parameters = [('chan_ident', 'B'), ('mode', 'B')]


class MGMSG_MOT_SET_SOL_OPERATINGMODE(Message):
    id = 0x4c0
    parameters = [('chan_ident', 'B'), ('mode', 'B')]


class MGMSG_MOT_SET_SOL_STATE(Message):
    id = 0x4c6
    parameters = [('chan_ident', 'B'), ('state', 'B')]
