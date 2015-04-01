from ._base import MessageWithData, MessageWithoutData
import struct

###### MOTOR CONTROL MESSAGES ######

class MGMSG_HW_YES_FLASH_PROGRAMMING(MessageWithoutData):
    """This message is sent by the server on start up, however, it is a
    deprecated message (i.e. has no function) and can be ignored."""
    message_id = 0x0017
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_HW_NO_FLASH_PROGRAMMING(MessageWithoutData):
    """This message is sent on start up to notify the controller of the
    source and destination addresses. A client application must send
    this message as part of its initialization process."""
    message_id = 0x0018
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_MOT_SET_POSCOUNTER(MessageWithData):
    """Used to set the ‘live’ position count in the controller. In general, this
    command is not normally used. Instead, the stage is homed
    immediately after power-up (at this stage the position is unknown
    as the stage is free to move when the power is off); and after the
    homing process is completed the position counter is automatically
    updated to show the actual position. From this point onwards the
    position counter always shows the actual absolute position.
    
    Fields:
    - chan_ident
    - position"""
    message_id = 0x0410
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'position']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_MOT_REQ_POSCOUNTER(MessageWithoutData):
    """See MGMSG_MOT_SET_POSCOUNTER

    Fields:
    - chan_ident"""
    
    message_id = 0x0411
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_POSCOUNTER(MessageWithData):
    """See MGMSG_MOT_SET_POSCOUNTER

    Fields:
    - chan_ident
    - position"""
    message_id = 0x0412
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'position']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    
    

class MGMSG_MOT_SET_ENCCOUNTER(MessageWithData):
    """Similarly to the MGMSG_MOT_SET_POSCOUNTER message described previously,
    this message is used to set the encoder count in the controller and is
    only applicable to stages and actuators fitted with an encoder. In
    general, this command is not normally used. Instead, the stage is
    homed immediately after power-up (at this stage the position is
    unknown as the stage is free to move when the power is off); and
    after the homing process is completed the position counter is
    automatically updated to show the actual position. From this point
    onwards the encoder counter always shows the actual absolute
    position.
    
    Fields:
    - chan_ident
    - encoder_count
    """
    message_id = 0x0409
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'encoder_count']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    
    

class MGMSG_MOT_REQ_ENCCOUNTER(MessageWithoutData):
    """See MGMSG_MOT_SET_ENCCOUNTER

    Fields:
    - chan_ident"""
    
    message_id = 0x040A
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_ENCCOUNTER(MessageWithData):
    """See MGMSG_MOT_SET_ENCCOUNTER
    
    Fields:
    - chan_ident
    - enc_counter
    """
    
    message_id = 0x040B
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'encoder_count']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

    

class MGMSG_MOT_SET_VELPARAMS(MessageWithData):
    """Used to set the trapezoidal velocity parameters for the specified
    motor channel. For DC servo controllers, the velocity is set in
    encoder counts/sec and acceleration is set in encoder counts/sec/sec.
    
    For stepper motor controllers the velocity is set in microsteps/sec
    and acceleration is set in microsteps/sec/sec.
    
    Fields:
    - chan_ident
    - min_velocity
    - acceleration
    - max_velocity
    """
    message_id = 0x0413
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'min_velocity', 'acceleration', 'max_velocity']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    
    

class MGMSG_MOT_REQ_VELPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_VELPARAMS
    
    Fields:
    - chan_ident
    """
    
    message_id = 0x0414
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_VELPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_VELPARAMS

    Fields:
    - chan_ident
    - min_velocity
    - acceleration
    - max_velocity
    """    
    message_id = 0x0415
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'min_velocity', 'acceleration', 'max_velocity']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    


class MGMSG_MOT_SET_JOGPARAMS(MessageWithData):
    """Used to set the velocity jog parameters for the specified motor
    channel, For DC servo controllers, values set in encoder counts.
    For stepper motor controllers the values is set in microsteps.
    
    Fields:
    - chan_ident
    - jog_mode
    - jog_step_size
    - jog_min_velocity
    - jog_acceleration
    - job_max_velocity
    - stop_mode
    """
    message_id = 0x0416
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'I', 'I', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'jog_mode', 'jog_step_size', 'jog_min_velocity', 'jog_acceleration', 'job_max_velocity', 'stop_mode']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields)) 

class MGMSG_MOT_REQ_JOGPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_JOGPARAMS
    
    Fields:
    - chan_ident
    """
    message_id = 0x0417
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_JOGPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_JOGPARAMS

    Fields:
    - chan_ident
    - jog_mode
    - jog_step_size
    - jog_min_velocity
    - jog_acceleration
    - job_max_velocity
    - stop_mode
    """    
    message_id = 0x0418
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'I', 'I', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'jog_mode', 'jog_step_size', 'jog_min_velocity', 'jog_acceleration', 'job_max_velocity', 'stop_mode']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields)) 

class MGMSG_MOT_REQ_ADCINPUTS(MessageWithoutData):
    """This message reads the voltage applied to the analog input on the
    rear panel CONTROL IO connector, and returns a value in the
    ADCInput1 parameter. The returned value is in the range 0 to
    32768, which corresponds to zero to 5 V.
    Note. The ADCInput2 parameter is not used at this time.
    In this way, a 0 to 5V signal generated by a client system could be
    read in by calling this method and monitored by a custom client
    application. When the signal reaches a specified value, the
    application could instigate further actions, such as a motor move.
    
    Fields:
    - chan_ident"""
    message_id = 0x042B
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_ADCINPUTS(MessageWithData):
    """See MGMSG_MOT_REQ_ADCINPUTS

    Fields:
    - chan_ident
    - adc_input1
    - adc_input2"""    
    message_id = 0x042C
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['adc_input1', 'adc_input2']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))     

class MGMSG_MOT_SET_POWERPARAMS(MessageWithData):
    """The power needed to hold a motor in a fixed position is much
    smaller than that required for a move. It is good practice to
    decrease the power in a stationary motor in order to reduce
    heating, and thereby minimize thermal movements caused by
    expansion. This message sets a reduction factor for the rest power
    and the move power values as a percentage of full power. Typically,
    move power should be set to 100% and rest power to a value
    significantly less than this.
    
    Note for BSC20x, MST602 and TST101 controller users:
    If the controllers listed above are used with APTServer, the ini file will typically have values
    set of 5 for the rest power and 30 for the move power. Although these values are loaded
    when the server boots only the rest power value is used. This allows the user to set the rest
    current as normal. The move power however is not used. The move power is set within the
    controller as a function of velocity. This command can be used only to set the rest power.
    The command MGMSG_MOT_REQ_POWERPARAMS will return the default values or the
    values that were set.
    
    Fields:
    - chan_ident
    - rest_factor
    - move_factor
    """
    message_id = 0x0426
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'rest_factor', 'move_factor']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))     

class MGMSG_MOT_REQ_POWERPARAMS(MessageWithoutData):
    """See MGMSG_MOT_GET_POWERPARAMS.
    
    Fields:
    - chan_ident"""
    message_id = 0x0427
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_POWERPARAMS(MessageWithData):
    """See MGMSG_MOT_GET_POWERPARAMS.

    Fields:
    - chan_ident
    - rest_factor
    - move_factor"""
    message_id = 0x0428
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'rest_factor', 'move_factor']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))


class MGMSG_MOT_SET_GENMOVEPARAMS(MessageWithData):
    """Used to set the general move parameters for the specified motor
    channel. At this time this refers specifically to the backlash settings.
    
    Fields:
    - chan_ident
    - backlash_distance
    """
    message_id = 0x043A
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'backlash_distance']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))

class MGMSG_MOT_REQ_GENMOVEPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_GENMOVEPARAMS
    
    Fields:
    - chan_ident"""
    message_id = 0x043B
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']
    
class MGMSG_MOT_GET_GENMOVEPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_GENMOVEPARAMS

    Fields:
    - chan_ident
    - backlash_distance"""    
    message_id = 0x043C
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'backlash_distance']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    
    

class MGMSG_MOT_SET_MOVERELPARAMS(MessageWithData):
    """Used to set the relative move parameters for the specified motor
    channel. The only significant parameter at this time is the relative
    move distance itself. This gets stored by the controller and is used
    the next time a relative move is initiated.
    
    Fields:
    - chan_ident
    - relative_distance"""
    
    message_id = 0x0445
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'relative_distance']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))        

class MGMSG_MOT_REQ_MOVERELPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_MOVERELPARAMS

    Fields:
    - chan_ident"""
    
    message_id = 0x0446
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_MOVERELPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_MOVERELPARAMS

    Fields:
    - chan_ident
    - relative_distance"""
    message_id = 0x0447
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'relative_distance']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))            

class MGMSG_MOT_SET_MOVEABSPARAMS(MessageWithData):
    """Used to set the absolute move parameters for the specified motor
    channel. The only significant parameter at this time is the absolute
    move position itself. This gets stored by the controller and is used
    the next time an absolute move is initiated.
    
    Fields:
    - chan_ident
    - absolute_position"""
    message_id = 0x0450
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'absolute_position']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))                

class MGMSG_MOT_REQ_MOVEABSPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_MOVEABSPARAMS.

    Fields:
    - chan_ident"""
    message_id = 0x0451
    
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_MOVEABSPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_MOVEABSPARAMS.

    Fields:
    - chan_ident
    - absolute_position"""
    message_id = 0x0452
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'absolute_position']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))
    

class MGMSG_MOT_SET_HOMEPARAMS(MessageWithData):
    """Used to set the home parameters for the specified motor channel.
    These parameters are stage specific and for the MLS203 stage
    implementation the only parameter that can be changed is the
    homing velocity.
    
    Fields:
    - chan_ident
    - home_direction
    - limit_switch
    - home_velocity
    - offset_distance
    """
    message_id = 0x0440
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'home_direction', 'limit_switch', 'home_velocity', 'offset_distance']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_MOT_REQ_HOMEPARAMS(MessageWithoutData):
    """See MGMSG_MOT_GET_HOMEPARAMS.
    
    Fields:
    - chan_ident"""
    
    message_id = 0x0441
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_HOMEPARAMS(MessageWithData):
    """See MGMSG_MOT_GET_HOMEPARAMS.

    Fields:
    - chan_ident
    - home_direction
    - limit_switch
    - home_velocity
    - offset_distance
    """
    
    message_id = 0x0442
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'home_direction', 'limit_switch', 'home_velocity', 'offset_distance']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))        

class MGMSG_MOT_SET_LIMSWITCHPARAMS(MessageWithData):
    """Used to set the limit switch parameters for the specified motor
    channel.
    
    These functions are not applicable to BBD10x units
    
    Fields:
    - chan_ident
    - cw_hard_limit
    - ccw_hard_limit
    - cw_soft_limit
    - ccw_soft_limit
    - software_limit_mode
    """
    message_id = 0x0423
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'cw_hard_limit', 'ccw_hard_limit', 'cw_soft_limit', 'ccw_soft_limit', 'software_limit_mode']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))            

class MGMSG_MOT_REQ_LIMSWITCHPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_LIMSWITCHPARAMS.

    Fields:
    - chan_ident"""
    
    message_id = 0x0424
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_LIMSWITCHPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_LIMSWITCHPARAMS.
    
    Fields:
    - chan_ident
    - cw_hard_limit
    - ccw_hard_limit
    - cw_soft_limit
    - ccw_soft_limit
    - software_limit_mode"""
    message_id = 0x0425
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'cw_hard_limit', 'ccw_hard_limit', 'cw_soft_limit', 'ccw_soft_limit', 'software_limit_mode']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))                

class MGMSG_MOT_MOVE_HOME(MessageWithoutData):
    """Sent to start a home move sequence on the specified motor channel
    (in accordance with the home parameters above).
    
    Fields:
    - chan_ident"""
    message_id = 0x0443
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_MOVE_HOMED(MessageWithoutData):
    """Message sent upon completion of the MGMSG_MOT_MOVE_HOME command.

    Fields:
    - chan_ident"""
    message_id = 0x0444
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_MOVE_RELATIVE_short(MessageWithoutData):
    """This command can be used to start a relative move on the specified
    motor channel (using the relative move distance parameter above).
    The relative distance parameter used for the move will be the parameter sent
    previously by a MGMSG_MOT_SET_MOVERELPARAMS command.
    
    Fields:
    - chan_ident"""
    message_id = 0x0448
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_MOVE_RELATIVE_long(MessageWithData):
    """This command can be used to start a relative move on the specified
    motor channel using the parameter relative_distance parameter.

    Fields:
    - chan_ident
    - relative_distance"""
    
    message_id = 0x0448
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'relative_distance']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))     
    

class MGMSG_MOT_MOVE_COMPLETED(MessageWithData):
    """Upon completion of a relative or absolute move sequence, the controller
    sends a MGMSG_MOT_MOVE_COMPLETED message.
    
    Fields:
    - chan_ident
    - position
    - status_bits"""
    message_id = 0x0464
    #3rd datafield is either EncCount or Velocity + Reserved, depending on the stage type. It's better to ignore it.
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'position', None, 'status_bits']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    


class MGMSG_MOT_MOVE_ABSOLUTE_short(MessageWithoutData):
    """This command can be used to start a absolute move on the specified
    motor channel.
    The absolute move position used for the move will be the parameter sent
    previously by a MGMSG_MOT_SET_MOVEABSPARAMS command.

    Fields:
    - chan_ident"""    
    message_id = 0x0453
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_MOVE_ABSOLUTE_long(MessageWithData):
    """This command can be used to start a absolute move on the specified
    motor channel using the parameter absolute_distance parameter.

    Fields:
    - chan_ident
    - absolute_distance"""    
    message_id = 0x0453
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'absolute_distance']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))      
    

class MGMSG_MOT_MOVE_JOG(MessageWithoutData):
    """Sent to start a jog move on the specified motor channel.
    
    Fields:
    - chan_ident
    - direction (0x01=forward, 0x02=reverse)"""
    message_id = 0x046A
    _params_names = ['message_id'] + ['chan_ident', 'direction'] + ['dest', 'source']

class MGMSG_MOT_MOVE_VELOCITY(MessageWithoutData):
    """This command can be used to start a move on the specified motor channel.
    When this method is called, the motor will move continuously in the
    specified direction, using the velocity parameters set in the
    MGMSG_MOT_SET_MOVEVELPARAMS command until either a stop command
    (either StopImmediate or StopProfiled) is called, or a limit switch is
    reached.
    
    Fields:
    - chan_ident
    - direction
    """

    message_id = 0x0457
    _params_names = ['message_id'] + ['chan_ident', 'direction'] + ['dest', 'source']

class MGMSG_MOT_MOVE_STOP(MessageWithoutData):
    """Sent to stop any type of motor move (relative, absolute, homing or move
    at velocity) on the specified motor channel.
    
    Fields:
    - chan_ident
    - stop_mode (0x01: immediately, 0x02: controlled (profiled) manner)"""
    message_id = 0x0465
    _params_names = ['message_id'] + ['chan_ident', 'stop_mode'] + ['dest', 'source']

class MGMSG_MOT_MOVE_STOPPED(MessageWithData):
    """Upon completion of the stop move, the controller sends this message.
    
    Fields:
    - chan_ident
    - position
    - status_bits"""
    
    message_id = 0x0466
    #3rd datafield is either EncCount or Velocity + Reserved, depending on the stage type. It's better to ignore it.
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'position', None, 'status_bits']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))        

class MGMSG_MOT_SET_BOWINDEX(MessageWithData):
    """Set bow index (see page 63 of the specs).
    
    Fields:
    - chan_ident
    - bow_index"""
    message_id = 0x04F4
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'bow_index']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))            

class MGMSG_MOT_REQ_BOWINDEX(MessageWithoutData):
    """See MGMSG_MOT_SET_BOWINDEX.
    
    Fields:
    - chan_ident"""
    message_id = 0x04F5
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_BOWINDEX(MessageWithData):
    """See MGMSG_MOT_SET_BOWINDEX.

    Fields:
    - chan_ident
    - bow_index"""
    
    message_id = 0x04F6
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'bow_index']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))

class MGMSG_MOT_SET_DCPIDPARAMS(MessageWithData):
    """Used to set the position control loop parameters for the specified
    motor channel. See page 66 of the spec.
    
    Fields:
    - chan_ident
    - proportional
    - integral
    - differential
    - integral_limit
    - filter_control
    """
    message_id = 0x04A0
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'proportional', 'integral', 'differential', 'integral_limit', 'filter_control']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_MOT_REQ_DCPIDPARAMS(MessageWithoutData):
    """See MGMSG_MOT_GET_DCPIDPARAMS.
    
    Fields:
    - chan_ident
    """
    message_id = 0x04A1
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_DCPIDPARAMS(MessageWithData):
    """See MGMSG_MOT_GET_DCPIDPARAMS.

    Fields:
    - chan_ident
    - proportional
    - integral
    - differential
    - integral_limit
    - filter_control
    """    
    message_id = 0x04A2
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'proportional', 'integral', 'differential', 'integral_limit', 'filter_control']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    
    

class MGMSG_MOT_SET_AVMODES(MessageWithData):
    """The LED on the control keypad can be configured to indicate certain
    driver states.
    All modes are enabled by default. However, it is recognised that in a light
    sensitive environment, stray light from the LED could be undesirable.
    Therefore it is possible to enable selectively, one or all of the LED
    indicator modes described below by setting the appropriate value in the
    Mode Bits parameter.
    
    Fields:
    - chan_ident
    - mode_bits"""
    message_id = 0x04B3
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'mode_bits']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_MOT_REQ_AVMODES(MessageWithoutData):
    """See MGMSG_MOT_SET_AVMODES

    Fields:
    - chan_ident
    """
    message_id = 0x04B4
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_AVMODES(MessageWithData):
    """See MGMSG_MOT_SET_AVMODES
    
    Fields:
    - chan_ident
    - mode_bits"""
    
    message_id = 0x04B5
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'mode_bits']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))     

class MGMSG_MOT_SET_POTPARAMS(MessageWithData):
    """The potentiometer slider on the control panel panel is sprung, such that when released it returns to it’s central position. In this central position the motor is stationary. As the slider is moved away from the center, the motor begins to move; the speed of this movement increases as the slider deflection is increased. Bidirectional control of motor moves is possible by moving the slider in both directions.
    The speed of the motor increases by discrete amounts rather than continuously, as a function of slider deflection. These speed settings are defined by 4 pairs of parameters. Each pair specifies a pot deflection value (in the range 0 to 127) together with an associated velocity (set in encoder counts/sec) to be applied at or beyond that deflection. As each successive deflection is reached by moving the pot slider, the next velocity value is applied. These settings are applicable in either direction of pot deflection, i.e. 4 possible velocity settings in the forward or reverse motion directions.
    Note. The scaling factor between encoder counts and mm/sec depends on the specific stage/actuator being driven.

    Fields:
    - chan_ident
    - zero_wnd
    - vel1
    - wnd1
    - vel2
    - wnd2
    - vel3
    - wnd3
    - vel4"""
    message_id = 0x04B0
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'I', 'H', 'I', 'H', 'I', 'H', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'zero_wnd', 'vel1', 'wnd1', 'vel2', 'wnd2', 'vel3', 'wnd3', 'vel4']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))

class MGMSG_MOT_REQ_POTPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_POTPARAMS.

    Fields:
    - chan_ident"""
    message_id = 0x04B1
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_POTPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_POTPARAMS.

    Fields:
    - chan_ident
    - zero_wnd
    - vel1
    - wnd1
    - vel2
    - wnd2
    - vel3
    - wnd3
    - vel4"""    
    message_id = 0x04B2
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'I', 'H', 'I', 'H', 'I', 'H', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'zero_wnd', 'vel1', 'wnd1', 'vel2', 'wnd2', 'vel3', 'wnd3', 'vel4']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))

class MGMSG_MOT_SET_BUTTONPARAMS(MessageWithData):
    """The control keypad can be used either to jog the motor, or to perform moves to absolute positions. This function is used to set the front panel button functionality.
    
    Fields:
    - chan_ident
    - mode
    - position1
    - position2
    - timeout"""
    message_id = 0x04B6
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'i', 'i', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'mode', 'position1', 'position2', 'timeout', None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_MOT_REQ_BUTTONPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_BUTTONPARAMS.
    
    Fields:
    - chan_ident"""
    
    message_id = 0x04B7
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_BUTTONPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_BUTTONPARAMS.
    
    Fields:
    - chan_ident
    - mode
    - position1
    - position2
    - timeout"""
    message_id = 0x04B8
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'i', 'i', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'mode', 'position1', 'position2', 'timeout', None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))        

class MGMSG_MOT_SET_EEPROMPARAMS(MessageWithData):
    """Used to save the parameter settings for the specified message.
    These settings may have been altered either through the various method calls
    or through user interaction with the GUI (specifically, by clicking on the
    ‘Settings’ button found in the lower right hand corner of the user
    interface).
    
    Fields:
    - chan_ident
    - msg_id"""
    
    message_id = 0x04B9
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'msg_id']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))

class MGMSG_MOT_SET_PMDPOSITIONLOOPPARAMS(MessageWithData):
    """Used to set the position control loop parameters for the specified
    motor channel.
    The motion processors within the BBD series controllers use a
    position control loop to determine the motor command output. The
    purpose of the position loop is to match the actual motor position
    and the demanded position. This is achieved by comparing the
    demanded position with the actual encoder position to create a
    position error, which is then passed through a digital PID-type filter.
    The filtered value is the motor command output.
    
    Fields:
    - chan_ident
    - kp_pos
    - integral
    - i_lim_pos
    - differential
    - kd_time_pos
    - k_out_pos
    - k_vff_pos
    - k_aff_pos
    - pos_err_limit"""
    message_id = 0x04D7
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'I', 'H', 'H', 'H', 'H', 'H', 'I', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'kp_pos', 'integral', 'i_lim_pos', 'differential', 'kd_time_pos', 'k_out_pos', 'k_vff_pos', 'k_aff_pos', 'pos_err_limit', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_MOT_REQ_PMDPOSITIONLOOPPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_PMDPOSITIONLOOPPARAMS.

    Fields:
    - chan_ident"""
    message_id = 0x04D8
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_PMDPOSITIONLOOPPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_PMDPOSITIONLOOPPARAMS.

    Fields:
    - chan_ident
    - kp_pos
    - integral
    - i_lim_pos
    - differential
    - kd_time_pos
    - k_out_pos
    - k_vff_pos
    - k_aff_pos
    - pos_err_limit"""    
    message_id = 0x04D9
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'I', 'H', 'H', 'H', 'H', 'H', 'I', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'kp_pos', 'integral', 'i_lim_pos', 'differential', 'kd_time_pos', 'k_out_pos', 'k_vff_pos', 'k_aff_pos', 'pos_err_limit', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    
    

class MGMSG_MOT_SET_PMDMOTOROUTPUTPARAMS(MessageWithData):
    """Used to set certain limits that can be applied to the motor drive signal.
    
    Fields:
    - chan_ident
    - cont_current_lim
    - energy_lim
    - motor_lim
    - motor_bias"""
    message_id = 0x04DA
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'H', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'cont_current_lim', 'energy_lim', 'motor_lim', 'motor_bias', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))        

class MGMSG_MOT_REQ_PMDMOTOROUTPUTPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_PMDMOTOROUTPUTPARAMS.

    Fields:
    - chan_ident"""
    message_id = 0x04DB
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_PMDMOTOROUTPUTPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_PMDMOTOROUTPUTPARAMS.

    Fields:
    - chan_ident
    - cont_current_lim
    - energy_lim
    - motor_lim
    - motor_bias"""    
    message_id = 0x04DC
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'H', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'cont_current_lim', 'energy_lim', 'motor_lim', 'motor_bias', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))

class MGMSG_MOT_SET_PMDTRACKSETTLEPARAMS(MessageWithData):
    """Moves are generated by an internal profile generator, and are based
    on either a trapezoidal or S-curve trajectory. A move is considered
    complete when the profile generator has completed the calculated
    move and the axis has 'settled' at the demanded position. This
    command contains parameters which specify when the system is
    settled.
    
    See page 81 for details.
    
    Fields:
    - chan_ident
    - time
    - settle_window
    - track_window"""
    message_id = 0x04E0
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'time', 'settle_window', 'track_window', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_MOT_REQ_PMDTRACKSETTLEPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_PMDTRACKSETTLEPARAMS.

    Fields:
    - chan_ident"""
    message_id = 0x04E1
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_PMDTRACKSETTLEPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_PMDTRACKSETTLEPARAMS.

    Fields:
    - chan_ident
    - time
    - settle_window
    - track_window"""
    
    message_id = 0x04E2
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'time', 'settle_window', 'track_window', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))        


class MGMSG_MOT_SET_PMDPROFILEMODEPARAMS(MessageWithData):
    """The system incorporates a trajectory generator, which performs
    calculations to determine the instantaneous position, velocity and
    acceleration of each axis at any given moment. During a motion
    profile, these values will change continuously. Once the move is
    complete, these parameters will then remain unchanged until the
    next move begins.
    The specific move profile created by the system depends on several
    factors, such as the profile mode and profile parameters presently
    selected, and other conditions such as whether a motion stop has
    been requested. This method is used to set the profile mode to
    either ‘Trapezoidal’ or ‘S-curve’.
    
    Fields:
    - chan_ident
    - mode
    - jerk"""
    message_id = 0x04E3
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'I', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'mode', 'jerk', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))            

class MGMSG_MOT_REQ_PMDPROFILEMODEPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_PMDPROFILEMODEPARAMS.

    Fields:
    - chan_ident"""
    message_id = 0x04E4
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_PMDPROFILEMODEPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_PMDPROFILEMODEPARAMS.

    Fields:
    - chan_ident
    - mode
    - jerk"""
    message_id = 0x04E5
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'I', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'mode', 'jerk', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))                


class MGMSG_MOT_SET_PMDJOYSTICKPARAMS(MessageWithData):
    """The MJC001 joystick console has been designed for use by
    microscopists to provide intuitive, tactile, manual positioning of the
    stage. The console consists of a two axis joystick for XY control
    which features both low and high gear modes. This message is used
    to set max velocity and acceleration values for these modes.
    
    Fields:
    - chan_ident
    - js_gear_low_max_vel
    - js_gear_high_max_vel
    - js_gear_low_accn
    - js_gear_high_accn
    - dir_sense
    """
    message_id = 0x04E6
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'js_gear_low_max_vel', 'js_gear_high_max_vel', 'js_gear_low_accn', 'js_gear_high_accn', 'dir_sense']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))                    

class MGMSG_MOT_REQ_PMDJOYSTICKPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_PMDJOYSTICKPARAMS.

    Fields:
    - chan_ident"""
    message_id = 0x04E7
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_PMDJOYSTICKPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_PMDJOYSTICKPARAMS.
    
    Fields:
    - chan_ident
    - js_gear_low_max_vel
    - js_gear_high_max_vel
    - js_gear_low_accn
    - js_gear_high_accn
    - dir_sense
    """
    message_id = 0x04E8
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I', 'I', 'I', 'I', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'js_gear_low_max_vel', 'js_gear_high_max_vel', 'js_gear_low_accn', 'js_gear_high_accn', 'dir_sense']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))


class MGMSG_MOT_SET_PMDCURRENTLOOPPARAMS(MessageWithData):
    """Used to set the current control loop parameters for the specified
    motor channel.
    The motion processors within the BBD series controllers use digital
    current control as a technique to control the current through each
    phase winding of the motors. In this way, response times are
    improved and motor efficiency is increased. This is achieved by
    comparing the required (demanded) current with the actual current
    to create a current error, which is then passed through a digital PI-
    type filter. The filtered current value is used to develop an output
    voltage for each motor coil.
    This method sets various constants and limits for the current
    feedback loop.

    Fields:
    - chan_ident
    - phase
    - kp_current
    - ki_current
    - i_lim_current
    - i_dead_band
    - kff"""
    
    message_id = 0x04D4
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'phase', 'kp_current', 'ki_current', 'i_lim_current', 'i_dead_band', 'kff', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_MOT_REQ_PMDCURRENTLOOPPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_PMDCURRENTLOOPPARAMS.
    
    Fields:
    - chan_ident"""
    
    message_id = 0x04D5
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_PMDCURRENTLOOPPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_PMDCURRENTLOOPPARAMS.

    Fields:
    - chan_ident
    - phase
    - kp_current
    - ki_current
    - i_lim_current
    - i_dead_band
    - kff"""    
    message_id = 0x04D6
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'phase', 'kp_current', 'ki_current', 'i_lim_current', 'i_dead_band', 'kff', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))        


class MGMSG_MOT_SET_PMDSETTLEDCURRENTLOOPPARAMS(MessageWithData):
    """These commands assist in maintaining stable operation and
    reducing noise at the demanded position. They allow the system to
    be tuned such that errors caused by external vibration and manual
    handling (e.g. loading of samples) are minimized, and are applicable
    only when the stage is settled, i.e. the Axis Settled status bit (bit 14)
    is set.
    
    Fields:
    - chan_ident
    - phase
    - kp_settled
    - ki_settled
    - i_lim_settled
    - dead_band_set
    - kff_settled"""
    message_id = 0x04E9
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'phase', 'kp_settled', 'ki_settled', 'i_lim_settled', 'dead_band_set', 'kff_settled', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))            

class MGMSG_MOT_REQ_PMDSETTLEDCURRENTLOOPPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_PMDSETTLEDCURRENTLOOPPARAMS.

    Fields:
    - chan_ident"""
    message_id = 0x04EA
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_PMDSETTLEDCURRENTLOOPPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_PMDSETTLEDCURRENTLOOPPARAMS.

    Fields:
    - chan_ident
    - phase
    - kp_settled
    - ki_settled
    - i_lim_settled
    - dead_band_set
    - kff_settled"""    
    message_id = 0x04EB
    
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'phase', 'kp_settled', 'ki_settled', 'i_lim_settled', 'dead_band_set', 'kff_settled', None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))                



class MGMSG_MOT_SET_PMDSTAGEAXISPARAMS(MessageWithData):
    """The REQ and GET commands are used to obtain various parameters
    pertaining to the particular stage being driven. Most of these
    parameters are inherent in the design of the stage and cannot be
    altered. The SET command can only be used to increase the
    Minimum position value and decrease the Maximum position value,
    thereby reducing the overall travel of the stage.

    Fields:
    - chan_ident
    - stage_id
    - axis_id
    - part_no_axis
    - serial_num
    - cnts_per_unit
    - min_pos
    - max_pos
    - max_accn
    - max_dec
    - max_vel"""
    message_id = 0x04F0
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', '16s', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'H', 'H', 'H', 'H', 'I', 'I', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'stage_id', 'axis_id', 'part_no_axis', 'serial_num', 'cnts_per_unit', 'min_pos', 'max_pos', 'max_accn', 'max_dec', 'max_vel', None, None, None, None, None, None, None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))                    

class MGMSG_MOT_REQ_PMDSTAGEAXISPARAMS(MessageWithoutData):
    """See MGMSG_MOT_SET_PMDSTAGEAXISPARAMS.
    
    Fields:
    - chan_ident"""
    message_id = 0x04F1
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_PMDSTAGEAXISPARAMS(MessageWithData):
    """See MGMSG_MOT_SET_PMDSTAGEAXISPARAMS.

    Fields:
    - chan_ident
    - stage_id
    - axis_id
    - part_no_axis
    - serial_num
    - cnts_per_unit
    - min_pos
    - max_pos
    - max_accn
    - max_dec
    - max_vel"""    
    message_id = 0x04F2
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'H', 'H', '16s', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'H', 'H', 'H', 'H', 'I', 'I', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'stage_id', 'axis_id', 'part_no_axis', 'serial_num', 'cnts_per_unit', 'min_pos', 'max_pos', 'max_accn', 'max_dec', 'max_vel', None, None, None, None, None, None, None, None]
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))                        


class MGMSG_MOT_SET_TSTACTUATORTYPE(MessageWithoutData):
    """This command is for use only with the TST101 driver, and is used to
    define an actuator type so that the TST driver knows the effective
    length of the stage. This information is used if a user wishes to home
    the stage to the far travel end. In this case, once the stage is homed
    the APT GUI count will be set to the far travel value. For example, in
    the case of a ZFS25 the user will see 25mm once homed. The TST
    holds this value as a number of Trinamic microsteps, which will be a
    function of the gearbox ratio, the lead screw pitch, and the motor
    type. So for example the number stored in the TST for the ZFS25 is
    54613333.
    
    Fields:
    - actuator_ident"""
    message_id = 0x04FE
    _params_names = ['message_id'] + ['actuator_ident', None] + ['dest', 'source']

class MGMSG_MOT_REQ_STATUSUPDATE(MessageWithoutData):
    """Used to request a status update for the specified motor channel.
    This request can be used instead of enabling regular updates as
    described above.
    
    Fields:
    - chan_ident"""
    message_id = 0x0480
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_STATUSUPDATE(MessageWithData):
    """This message is returned when a status update is requested for the
    specified motor channel. This request can be used instead of
    enabling regular updates as described above.
    
    - chan_ident
    - position
    - enc_count
    - status_bits"""
    
    message_id = 0x0481
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i', 'I', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'position', 'enc_count', 'status_bits']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))
    

class MGMSG_MOT_REQ_DCSTATUSUPDATE(MessageWithoutData):
    """Used to request a status update for the specified motor channel.
    This request can be used instead of enabling regular updates as
    described above.
    
    Fields:
    - chan_ident"""
    message_id = 0x0490
    _params_names = ['message_id'] +['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_DCSTATUSUPDATE(MessageWithData):
    """This message is returned when a status update is requested for the
    specified motor channel. This request can be used instead of
    enabling regular updates as described above.
    
    Fields:
    - chan_ident
    - position
    - velocity
    - status_bits"""
    
    message_id = 0x0491
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'i', 'h', 'H', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'position', 'velocity', None, 'status_bits']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))

class MGMSG_MOT_ACK_DCSTATUSUPDATE(MessageWithoutData):
    """Only Applicable If Using USB COMMS. Does not apply to RS-232 COMMS
    
    If using the USB port, this message called “server alive” must be sent
    by the server to the controller at least once a second or the
    controller will stop responding after ~50 commands.
    The controller keeps track of the number of "status update" type of
    messages (e.g.move complete message) and it if has sent 50 of
    these without the server sending a "server alive" message, it will
    stop sending any more "status update" messages.
    This function is used by the controller to check that the PC/Server
    has not crashed or switched off. There is no response."""
    
    message_id = 0x0492
    _params_names = ['message_id'] +[None, None] + ['dest', 'source']


class MGMSG_MOT_REQ_STATUSBITS(MessageWithoutData):
    """Used to request a “cut down” version of the status update message,
    only containing the status bits, without data about position and velocity.
    
    Fields:
    - chan_ident"""
    message_id = 0x0429
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_STATUSBITS(MessageWithData):
    """See MGMSG_MOT_REQ_STATUSBITS.

    Fields:
    - chan_ident
    - status_bits"""
    
    message_id = 0x042A
    _message_struct_fields = ['H', 'H', 'B', 'B'] + ['H', 'I']
    _params_names = ['message_id', 'data_packet_length', 'dest', 'source'] + ['chan_ident', 'status_bits']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))    

class MGMSG_MOT_SUSPEND_ENDOFMOVEMSGS(MessageWithoutData):
    """Sent to disable all unsolicited end of move messages and error
    messages returned by the controller, i.e.
    
    MGMSG_MOT_MOVE_STOPPED
    MGMSG_MOT_MOVE_COMPLETED
    MGMSG_MOT_MOVE_HOMED
    
    The command also disables the error messages that the controller
    sends when an error conditions is detected:
    
    MGMSG_HW_RESPONSE
    MGMSG_HW_RICHRESPONSE"""
    message_id = 0x046B
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']

class MGMSG_MOT_RESUME_ENDOFMOVEMSGS(MessageWithoutData):
    """Sent to resume all unsolicited end of move messages and error
    messages returned by the controller, i.e.
    
    MGMSG_MOT_MOVE_STOPPED
    MGMSG_MOT_MOVE_COMPLETED
    MGMSG_MOT_MOVE_HOMED
    
    This is the default state when the controller is powered up."""
    message_id = 0x046C
    _params_names = ['message_id'] + [None, None] + ['dest', 'source']


class MGMSG_MOT_SET_TRIGGER(MessageWithoutData):
    """This message is used to configure the Motor controller for triggered
    move operation. It is possible to configure a particular controller to
    respond to trigger inputs, generate trigger outputs or both respond
    to and generate a trigger output. When a trigger input is received,
    the unit can be set to initiate a move (relative, absolute or home).
    Similarly the unit can be set to generate a trigger output signal when
    a specified event (e.g move initiated) occurs. For those units
    configured for both input and output triggering, a move can be
    initiated via a trigger input while at the same time, a trigger output
    can be generated to initiate a move on another unit.
    The trigger settings can be used to configure multiple units in a
    master – slave set up, thereby allowing multiple channels of motion
    to be synchronized. Multiple moves can then be initiated via a single
    software or hardware trigger command.

    Fields:
    - chan_ident
    - mode"""
    message_id = 0x0500
    _params_names = ['message_id'] + ['chan_ident', 'mode'] + ['dest', 'source']

class MGMSG_MOT_REQ_TRIGGER(MessageWithoutData):
    """See MGMSG_MOT_SET_TRIGGER.
    
    Fields:
    - chan_ident"""
    message_id = 0x0501
    _params_names = ['message_id'] + ['chan_ident', None] + ['dest', 'source']

class MGMSG_MOT_GET_TRIGGER(MessageWithoutData):
    """See MGMSG_MOT_SET_TRIGGER.
    
    Fields:
    - chan_ident
    - mode"""
    message_id = 0x0502
    _params_names = ['message_id'] + ['chan_ident', 'mode'] + ['dest', 'source']

