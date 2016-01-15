from ._base import Message


##### Filter Flipper Control Messages #####
class MGMSG_MOT_GET_MFF_OPERPARAMS(Message):
    """
        See :class:`MGMSG_MOT_SET_MFF_OPERPARAMS`.

        :param chan_ident: channel number (0x01, 0x02)
        :type chan_ident: int
        - i_transit_time
        - i_transit_time_adc
        - oper_mode_1
        - sig_mode_1
        - pulse_width_1
        - oper_mode_2
        - sig_mode_2
        - pulse_width_2

    """
    id = 0x512
    is_long_cmd = True
    parameters = [('chan_ident', 'H'), ('i_transit_time', 'I'), ('i_transit_time_adc', 'I'), ('oper_mode_1', 'H'),
                  ('sig_mode_1', 'H'), ('pulse_width_1', 'I'), ('oper_mode_2', 'H'), ('sig_mode_2', 'H'),
                  ('pulse_width_2', 'I'), (None, 'I'), (None, 'H')]


class MGMSG_MOT_REQ_MFF_OPERPARAMS(Message):
    """
        See :class:`MGMSG_MOT_SET_MFF_OPERPARAMS`.

        :param chan_ident: channel number (0x01, 0x02)
        :type chan_ident: int
    """
    id = 0x511
    parameters = [('chan_ident', 'B'), (None, 'B')]


class MGMSG_MOT_SET_MFF_OPERPARAMS(Message):
    """
        Used to set various operating parameters that dictate the function of the
        MFF series flipper unit.

        :param chan_ident: channel number (0x01, 0x02)
        :type chan_ident: int
        - i_transit_time
        - i_transit_time_adc
        - oper_mode_1
        - sig_mode_1
        - pulse_width_1
        - oper_mode_2
        - sig_mode_2
        - pulse_width_2

    """
    id = 0x510
    is_long_cmd = True
    parameters = [('chan_ident', 'H'), ('i_transit_time', 'I'), ('i_transit_time_adc', 'I'), ('oper_mode_1', 'H'),
                  ('sig_mode_1', 'H'), ('pulse_width_1', 'I'), ('oper_mode_2', 'H'), ('sig_mode_2', 'H'),
                  ('pulse_width_2', 'I'), (None, 'I'), (None, 'H')]
