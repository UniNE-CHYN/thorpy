def discover_stages():
    import usb
    import os
    from .port import Port
    
    for dev in usb.core.find(find_all=True, custom_match= lambda x: x.bDeviceClass != 9):
        if dev.manufacturer != 'Thorlabs':
            continue
        
        #FIXME: this is linux specific...
        port_candidates = [x for x in os.listdir('/sys/bus/usb/devices/{0.bus}-{0.bus}.{0.port_number}:1.0/'.format(dev)) if x.startswith('ttyUSB')]
        assert len(port_candidates) == 1
        port = '/dev/'+port_candidates[0]
        #End of linux specific part
        

        p = Port.create(port, dev.serial_number)
        for stage in p.get_stages().values():
            yield stage
        
if __name__ == '__main__':
    print(list(discover()))
    

#iManufacturer           1 Thorlabs
#    iProduct                2 APT DC Motor Controller
#    iSerial                 3 83856536
