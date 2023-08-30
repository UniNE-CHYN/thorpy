import thorpy.comm.discovery as thc

class flipMount:

    def __init__(self, sn):
        self.__stage = thc.discover_stages(sn)

    def identify(self):
        self.__stage.identify()

    def open(self):
        self.__stage.move_jog_forward()

    def close(self):
        self.__stage.move_jog_backward()

    def is_open(self):
        return self.__stage.status_forward_hardware_limit_switch_active

    def is_close(self):
        return self.__stage.status_reverse_hardware_limit_switch_active

    def is_moving(self):
        return self.__stage.status_in_motion_forward

    def flip(self):
        if self.is_open():
            self.close()
        else:
            self.open()
