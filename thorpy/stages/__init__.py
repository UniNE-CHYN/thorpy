from thorpy.message import *
import weakref
import time
import pkgutil

def _print_stage_detection_improve_message(m):
    import sys
    print('If you see this message, please send a mail with the following information: \n' + \
          '- controller type\n' + \
          '- stage type\n' + \
          '- this data: {0}'.format(m), file = sys.stderr)

def stage_name_from_get_hw_info(m):
    controller_type = m['serial_number'] // 1000000  #v7
    stage_type = m['empty_space'][-2]  #Reverse engineered
    hw_version = m['hw_version']
    model_number = m['model_number'].decode('ascii').strip('\x00')
    if controller_type in (60, 80):
        if hw_version == 3:
            return 'HS ZST6(B)'
        else:
            return 'ZST6(B)'
    elif controller_type in (27, 63, 83, 2197):
        #Info obtained from thorlabs technical support
        if stage_type == 0x01:
            _print_stage_detection_improve_message(m)
            return None  #Open circuit - no motor connected.
        elif stage_type == 0x02:
            return 'Z706'
        elif stage_type == 0x03:
            return 'Z712'
        elif stage_type == 0x04:
            return 'Z725'
        elif stage_type == 0x05:
            return 'CR1-Z7'
        elif stage_type == 0x06:
            return 'PRM1-Z8'
        elif stage_type == 0x07:
            return 'MTS25-Z8'
        elif stage_type == 0x08:
            return 'MTS50-Z8'
        elif stage_type == 0x09:
            return 'Z825'
        elif stage_type == 0x0A:
            return 'Z812'
        elif stage_type == 0x0B:
            return 'Z806'
        elif stage_type == 0x0C:
            _print_stage_detection_improve_message(m)
            return None  #Non Thorlabs motor.
        else:
            #This is reverse engineered...
            _print_stage_detection_improve_message(m)
            return 'Z606(B)'
    elif controller_type in (43, 93):
        return 'DRV414'
    elif controller_type in (94, ):
        if stage_type == 16:
            return 'MLS203 X'
        elif stage_type == 17:
            return 'MLS203 Y'
        _print_stage_detection_improve_message(m)
        return None
    elif controller_type in (45, ):
        if model_number == 'LTS150':
            return 'HS LTS150 150mm Stage'
        elif model_number == 'LTS300':
            return 'HS LTS300 300mm Stage'
        _print_stage_detection_improve_message(m)
        return None

    elif controller_type in (46, ):
        return "L490MZ Labjack"
    elif controller_type in (47, ):
        return "FW105 Filter Wheel"
    elif controller_type in (55, ):
        return "K100CR1 Rotation Stage"
    elif controller_type in (49, ):
        return "MLJ050 Labjack"
    elif controller_type in (37, ):
        return "MFF Filter Flipper"
    elif controller_type in (67, ):
        if stage_type == 20:
            return 'MVS005MZ'
        else:
            _print_stage_detection_improve_message(m)
            return 'DDSM100'
    else:
        _print_stage_detection_improve_message(m)
        return None

class GenericStage:
    def __init__(self, port, chan_ident, ini_section):
        import os, configparser
        self._port = port
        self._chan_ident = chan_ident
        self._config = configparser.ConfigParser()
        self._config.read_string(pkgutil.get_data('thorpy.stages','MG17APTServer.ini').decode('ascii'))
        
        self._name = ini_section
        
        self._conf_stage_id = self._config.getint(ini_section, 'Stage ID')
        self._conf_axis_id = self._config.getint(ini_section, 'Axis ID')
        self._conf_units = self._config.getint(ini_section, 'Units')
        self._conf_pitch = self._config.getfloat(ini_section, 'Pitch')
        self._conf_dir_sense = self._config.getint(ini_section, 'Dir Sense')
        self._conf_min_pos = self._config.getfloat(ini_section, 'Min Pos')
        self._conf_max_pos = self._config.getfloat(ini_section, 'Max Pos')
        self._conf_def_min_vel = self._config.getfloat(ini_section, 'Def Min Vel')
        self._conf_def_accn = self._config.getfloat(ini_section, 'Def Accn')
        self._conf_def_max_vel = self._config.getfloat(ini_section, 'Def Max Vel')
        self._conf_max_accn = self._config.getfloat(ini_section, 'Max Accn')
        self._conf_def_accn = self._config.getfloat(ini_section, 'Def Accn')
        self._conf_max_vel = self._config.getfloat(ini_section, 'Max Vel')
        self._conf_backlash_dist = self._config.getfloat(ini_section, 'Backlash Dist')
        self._conf_move_factor = self._config.getint(ini_section, 'Move Factor')
        self._conf_rest_factor = self._config.getint(ini_section, 'Rest Factor')
        self._conf_cw_hard_limit = self._config.getint(ini_section, 'CW Hard Limit')
        self._conf_ccw_hard_limit = self._config.getint(ini_section, 'CCW Hard Limit')
        self._conf_cw_soft_limit = self._config.getfloat(ini_section, 'CW Soft Limit')
        self._conf_ccw_soft_limit = self._config.getfloat(ini_section, 'CCW Soft Limit')        
        self._conf_soft_limit_mode = self._config.getint(ini_section, 'Soft Limit Mode')
        self._conf_home_dir = self._config.getint(ini_section, 'Home Dir')
        self._conf_home_limit_switch = self._config.getint(ini_section, 'Home Limit Switch')
        self._conf_home_vel = self._config.getfloat(ini_section, 'Home Vel')
        self._conf_home_zero_offset = self._config.getfloat(ini_section, 'Home Zero Offset')
        self._conf_jog_mode = self._config.getint(ini_section, 'Jog Mode')
        self._conf_jog_step_size = self._config.getfloat(ini_section, 'Jog Step Size')
        self._conf_jog_min_vel = self._config.getfloat(ini_section, 'Jog Min Vel')
        self._conf_jog_accn = self._config.getfloat(ini_section, 'Jog Accn')
        self._conf_jog_max_vel = self._config.getfloat(ini_section, 'Jog Max Vel')
        self._conf_jog_stop_mode = self._config.getint(ini_section, 'Jog Stop Mode')
        self._conf_steps_per_rev = self._config.getint(ini_section, 'Steps Per Rev')
        self._conf_gearbox_ratio = self._config.getint(ini_section, 'Gearbox Ratio')
        self._conf_dc_servo = self._config.getboolean(ini_section, 'DC Servo', fallback = False)
        
        if self._conf_dc_servo:
            self._conf_dc_prop = self._config.getint(ini_section, 'DC Prop')
            self._conf_dc_int = self._config.getint(ini_section, 'DC Int')
            self._conf_dc_diff = self._config.getint(ini_section, 'DC Diff')
            self._conf_dc_intlim = self._config.getint(ini_section, 'DC IntLim')
        
        self._conf_fp_controls = self._config.getboolean(ini_section, 'FP Controls', fallback = False)
        if self._conf_fp_controls:
            self._conf_pot_zero_wnd = self._config.getint(ini_section, 'Pot Zero Wnd')
            self._conf_pot_vel_1 = self._config.getfloat(ini_section, 'Pot Vel 1')
            self._conf_pot_wnd_1 = self._config.getint(ini_section, 'Pot Wnd 1')
            self._conf_pot_vel_2 = self._config.getfloat(ini_section, 'Pot Vel 2')
            self._conf_pot_wnd_2 = self._config.getint(ini_section, 'Pot Wnd 2')
            self._conf_pot_vel_3 = self._config.getfloat(ini_section, 'Pot Vel 3')
            self._conf_pot_wnd_3 = self._config.getint(ini_section, 'Pot Wnd 3')
            self._conf_pot_vel_4 = self._config.getfloat(ini_section, 'Pot Vel 4')
            self._conf_button_mode = self._config.getint(ini_section, 'Button Mode')
            self._conf_button_pos_1 = self._config.getfloat(ini_section, 'Button Pos 1')
            self._conf_button_pos_2 = self._config.getfloat(ini_section, 'Button Pos 2')
            
        self._conf_js_params = self._config.getboolean(ini_section, 'JS Params', fallback = False)
        if self._conf_js_params:
            self._conf_js_gearlow_maxvel = self._config.getfloat(ini_section, 'JS GearLow MaxVel')
            self._conf_js_gearlow_accn = self._config.getfloat(ini_section, 'JS GearLow Accn')
            self._conf_js_dir_sense = self._config.getfloat(ini_section, 'JS Dir Sense')
            
        self._last_ack_sent = time.time()
        
        self._port.send_message(MGMSG_MOD_SET_CHANENABLESTATE(chan_ident = self._chan_ident, chan_enable_state = 0x01))
        
        print("Constructed: {0!r}".format(self))
        
        #STATUSUPDATE
        self._state_position = None
        self._state_velocity = None
        self._state_status_bits = None
        #VELPARAMS
        self._state_min_velocity = None
        self._state_max_velocity = None
        self._state_acceleration = None
        #HOMEPARAMS
        self._state_home_velocity = None
        self._state_home_direction = None
        self._state_home_limit_switch = None
        self._state_home_offset_distance = None
        
        
    def __del__(self):
        print("Destructed: {0!r}".format(self))
        
    def _handle_message(self, msg):
        if self._last_ack_sent < time.time() - 0.5:
            self._port.send_message(MGMSG_MOT_ACK_DCSTATUSUPDATE())
            self._last_ack_sent = time.time()
            
        if isinstance(msg, MGMSG_MOT_GET_DCSTATUSUPDATE) or \
           isinstance(msg, MGMSG_MOT_GET_STATUSUPDATE) or \
           isinstance(msg, MGMSG_MOT_MOVE_COMPLETED):
            
            self._state_position = msg['position']
            if isinstance(msg, MGMSG_MOT_GET_DCSTATUSUPDATE):
                self._state_velocity = msg['velocity']
            self._state_status_bits = msg['status_bits']
            return True
        
        if isinstance(msg, MGMSG_MOT_MOVE_HOMED):
            return True
        
        if isinstance(msg, MGMSG_MOT_GET_VELPARAMS):
            self._state_min_velocity = msg['min_velocity']
            self._state_max_velocity = msg['max_velocity']
            self._state_acceleration = msg['acceleration']
            return True
        
        if isinstance(msg, MGMSG_MOT_GET_HOMEPARAMS):
            self._state_home_direction = msg['home_direction']
            self._state_home_limit_switch = msg['limit_switch']
            self._state_home_velocity = msg['home_velocity']
            self._state_home_offset_distance = msg['offset_distance']
            return True
            
        
        return False
    
    #STATUSUPDATE
    
    @property
    def position(self):
        self._wait_for_properties(('_state_position', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return self._state_position / self._EncCnt

    @position.setter
    def position(self, new_value):
        assert type(new_value) in (float, int)
        absolute_distance = int(new_value * self._EncCnt)
        self._port.send_message(MGMSG_MOT_MOVE_ABSOLUTE_long(chan_ident = self._chan_ident, absolute_distance = absolute_distance))

    @property
    def velocity(self):
        self._wait_for_properties(('_state_velocity', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return self._state_velocity / (self._EncCnt * self._T)  #Dropped the 65536 factor, which resulted in false results

    @property
    def status_forward_hardware_limit_switch_active(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00000001) != 0

    @property
    def status_reverse_hardware_limit_switch_active(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00000002) != 0

    @property
    def status_in_motion_forward(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00000010) != 0

    @property
    def status_in_motion_reverse(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00000020) != 0

    @property
    def status_in_motion_jogging_forward(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00000040) != 0

    @property
    def status_in_motion_jogging_reverse(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00000080) != 0

    @property
    def status_in_motion_homing(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00000200) != 0

    @property
    def status_homed(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00000400) != 0

    @property
    def status_tracking(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00001000) != 0

    @property
    def status_settled(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00002000) != 0

    @property
    def status_motion_error(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x00004000) != 0

    @property
    def status_motor_current_limit_reached(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x01000000) != 0

    @property
    def status_channel_enabled(self):
        self._wait_for_properties(('_state_status_bits', ), timeout = 3, message = MGMSG_MOT_REQ_DCSTATUSUPDATE(chan_ident = self._chan_ident))
        return (self._state_status_bits & 0x80000000) != 0
    
    #VELPARAMS
    
    @property
    def min_velocity(self):
        self._wait_for_properties(('_state_min_velocity', ), timeout = 3, message = MGMSG_MOT_REQ_VELPARAMS(chan_ident = self._chan_ident))
        return self._state_min_velocity / (self._EncCnt * self._T * 65536)
    
    @property
    def max_velocity(self):
        self._wait_for_properties(('_state_max_velocity', ), timeout = 3, message = MGMSG_MOT_REQ_VELPARAMS(chan_ident = self._chan_ident))
        return self._state_max_velocity / (self._EncCnt * self._T * 65536)
    
    @property
    def acceleration(self):
        self._wait_for_properties(('_state_acceleration', ), timeout = 3, message = MGMSG_MOT_REQ_VELPARAMS(chan_ident = self._chan_ident))
        return self._state_acceleration / (self._EncCnt * (self._T ** 2) * 65536)
    
    @min_velocity.setter
    def min_velocity(self, new_value):
        self._set_velparams(float(new_value), self.max_velocity, self.acceleration)

    @max_velocity.setter
    def max_velocity(self, new_value):
        self._set_velparams(self.min_velocity, float(new_value), self.acceleration)

    @acceleration.setter
    def acceleration(self, new_value):
        self._set_velparams(self.min_velocity, self.max_velocity, float(new_value))

    def _set_velparams(self, min_velocity, max_velocity, acceleration):
        msg = MGMSG_MOT_SET_VELPARAMS(
            chan_ident = self._chan_ident,
            min_velocity = int(min_velocity *(self._EncCnt * self._T * 65536)),
            max_velocity = int(max_velocity *(self._EncCnt * self._T * 65536)),
            acceleration = int(acceleration *(self._EncCnt * (self._T ** 2) * 65536)),
        )
        self._port.send_message(msg)
        #Invalidate current values
        self._state_min_velocity = None
        self._state_max_velocity = None
        self._state_acceleration = None
        
        
    #HOMEPARAMS
    
    @property
    def home_velocity(self):
        self._wait_for_properties(('_state_home_velocity', ), timeout = 3, message = MGMSG_MOT_REQ_HOMEPARAMS(chan_ident = self._chan_ident))
        return self._state_home_velocity / (self._EncCnt * self._T * 65536)
    
    @home_velocity.setter
    def home_velocity(self, new_value):
        self._set_homeparams(float(new_value), self.home_direction, self.home_limit_switch, self.home_offset_distance)

    @property
    def home_direction(self):
        self._wait_for_properties(('_state_home_direction', ), timeout = 3, message = MGMSG_MOT_REQ_HOMEPARAMS(chan_ident = self._chan_ident))
        return self._state_home_direction
    
    @property
    def home_limit_switch(self):
        self._wait_for_properties(('_state_home_limit_switch', ), timeout = 3, message = MGMSG_MOT_REQ_HOMEPARAMS(chan_ident = self._chan_ident))
        return self._state_home_limit_switch
    
    @property
    def home_offset_distance(self):
        self._wait_for_properties(('_state_home_offset_distance', ), timeout = 3, message = MGMSG_MOT_REQ_HOMEPARAMS(chan_ident = self._chan_ident))
        return self._state_home_offset_distance / self._EncCnt
    
    def _set_homeparams(self, home_velocity, home_direction, home_limit_switch, home_offset_distance):
        msg = MGMSG_MOT_SET_HOMEPARAMS( 
            chan_ident = self._chan_ident,
            home_velocity = int(home_velocity *(self._EncCnt * self._T * 65536)),
            home_direction = home_direction,
            limit_switch = home_limit_switch,
            offset_distance = int(home_offset_distance*self._EncCnt)
        )
        self._port.send_message(msg)
        #Invalidate current values
        self._state_home_velocity = None
        self._state_home_direction = None
        self._state_home_limit_switch = None
        self._state_home_offset_distance = None

    
    #Conversion factors
    @property
    def _EncCnt(self):
        return self._conf_steps_per_rev * self._conf_gearbox_ratio / self._conf_pitch
    
    @property
    def _T(self):
        return 2048 / 6e6
    
    @property
    def units(self):
        return {1: 'mm', 2: '°'}[self._conf_units]
    
    def print_state(self):
        print("Stage: {0}".format(self._name))
        print("Position: {0:0.03f}{1}".format(self.position, self.units))
        # Velocity information not available with some stages, e.g. LTS300
        #print("Velocity: {0:0.03f}{1}/s".format(self.velocity, self.units))
        
        flags = []
        if self.status_forward_hardware_limit_switch_active:
            flags.append("forward hardware limit switch is active")
        if self.status_reverse_hardware_limit_switch_active:
            flags.append("reverse hardware limit switch is active")
        if self.status_in_motion_forward or self.status_in_motion_reverse or self.status_in_motion_jogging_forward or self.status_in_motion_jogging_reverse or self.status_in_motion_homing:
            flags.append('in motion')
        if self.status_in_motion_forward:
            flags.append('moving forward')
        if self.status_in_motion_reverse:
            flags.append('moving reverse')
        if self.status_in_motion_jogging_forward:
            flags.append('jogging forward')
        if self.status_in_motion_jogging_reverse:
            flags.append('jogging reverse')
        if self.status_in_motion_homing:
            flags.append('homing')
        if self.status_homed:
            flags.append('homed')
        if self.status_tracking:
            flags.append('tracking')
        if self.status_settled:
            flags.append('settled')
        if self.status_motion_error:
            flags.append('motion error')
        if self.status_motor_current_limit_reached:
            flags.append('motor current limit reached')
        if self.status_channel_enabled:
            flags.append('channel enabled')
            
        print("Status: {0}".format(', '.join(flags)))
        
        print("")
        print("Velocity parameters: velocity: {0.min_velocity:0.3f}-{0.max_velocity:0.3f}{0.units}/s, acceleration: {0.acceleration:0.3f}{0.units}/s²".format(self))
        print("Homing parameters: velocity: {0.home_velocity:0.3f}{0.units}/s, direction: {0.home_direction}, limit_switch: {0.home_limit_switch}, offset_distance: {0.home_offset_distance:0.3f}{0.units}".format(self))
        
    def home(self, force = False):
        if self.status_homed and not force:
            return True
        
        while not self.status_homed:
            if not self.status_in_motion_forward and not self.status_in_motion_reverse:
                self._port.send_message(MGMSG_MOT_MOVE_HOME(chan_ident = self._chan_ident))
            time.sleep(1)

        return True

    def home_non_blocking(self, force = True ):
        if self.status_homed and not force:
            return True
        
        self._port.send_message(MGMSG_MOT_MOVE_HOME(chan_ident = self._chan_ident))     
        return True

    def _wait_for_properties(self, properties, timeout = None, message = None, message_repeat_timeout = None):
        start_time = time.time()
        last_message_time = 0
        while any(getattr(self, prop) is None for prop in properties):
            if message is not None:
                if last_message_time == 0 or (message_repeat_timeout is not None and time.time() - last_message_time > message_repeat_timeout):
                    self._port.send_message(message)
                    last_message_time = time.time()
            time.sleep(0.1)
            if timeout is not None and time.time() - start_time >= timeout:
                return False
        return True
        
    def __repr__(self):
        return '<{0} on {1!r} channel {2}>'.format(self._name, self._port, self._chan_ident)
        

#Message which should maybe be implemented?
#Should be in port: MGMSG_HUB_REQ_BAYUSED, MGMSG_HUB_GET_BAYUSED,
#Really useful? MGMSG_MOT_SET_POSCOUNTER, MGMSG_MOT_REQ_POSCOUNTER, MGMSG_MOT_GET_POSCOUNTER, MGMSG_MOT_SET_ENCCOUNTER, MGMSG_MOT_REQ_ENCCOUNTER, MGMSG_MOT_GET_ENCCOUNTER, 
#MGMSG_MOT_SET_JOGPARAMS, MGMSG_MOT_REQ_JOGPARAMS, MGMSG_MOT_GET_JOGPARAMS, MGMSG_MOT_SET_GENMOVEPARAMS, MGMSG_MOT_REQ_GENMOVEPARAMS, MGMSG_MOT_GET_GENMOVEPARAMS, MGMSG_MOT_SET_MOVERELPARAMS, MGMSG_MOT_REQ_MOVERELPARAMS, MGMSG_MOT_GET_MOVERELPARAMS, MGMSG_MOT_SET_MOVEABSPARAMS, MGMSG_MOT_REQ_MOVEABSPARAMS, MGMSG_MOT_GET_MOVEABSPARAMS, MGMSG_MOT_SET_HOMEPARAMS, MGMSG_MOT_REQ_HOMEPARAMS, MGMSG_MOT_GET_HOMEPARAMS, MGMSG_MOT_SET_LIMSWITCHPARAMS, MGMSG_MOT_REQ_LIMSWITCHPARAMS, MGMSG_MOT_GET_LIMSWITCHPARAMS, MGMSG_MOT_MOVE_HOME, MGMSG_MOT_MOVE_HOMED, MGMSG_MOT_MOVE_RELATIVE_short,MGMSG_MOT_MOVE_RELATIVE_long, MGMSG_MOT_MOVE_COMPLETED, MGMSG_MOT_MOVE_ABSOLUTE_short,MGMSG_MOT_MOVE_ABSOLUTE_long, MGMSG_MOT_MOVE_JOG, MGMSG_MOT_MOVE_VELOCITY, MGMSG_MOT_MOVE_STOP, MGMSG_MOT_MOVE_STOPPED, MGMSG_MOT_SET_DCPIDPARAMS, MGMSG_MOT_REQ_DCPIDPARAMS, MGMSG_MOT_GET_DCPIDPARAMS, MGMSG_MOT_SET_AVMODES, MGMSG_MOT_REQ_AVMODES, MGMSG_MOT_GET_AVMODES, MGMSG_MOT_SET_POTPARAMS, MGMSG_MOT_REQ_POTPARAMS, MGMSG_MOT_GET_POTPARAMS, MGMSG_MOT_SET_BUTTONPARAMS, MGMSG_MOT_REQ_BUTTONPARAMS, MGMSG_MOT_GET_BUTTONPARAMS, MGMSG_MOT_SET_EEPROMPARAMS, MGMSG_MOT_REQ_DCSTATUSUPDATE, MGMSG_MOT_GET_DCSTATUSUPDATE, MGMSG_MOT_ACK_DCSTATUSUPDATE, MGMSG_MOT_REQ_STATUSBITS, MGMSG_MOT_GET_STATUSBITS, MGMSG_MOT_SUSPEND_ENDOFMOVEMSGS, MGMSG_MOT_RESUME_ENDOFMOVEMSGS
