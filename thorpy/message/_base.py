from abc import abstractmethod, abstractclassmethod
import struct

class IncompleteMessageException(Exception):
    """IncompleteMessageException is thrown when a message could not be parsed,
    because some of the bytes are missing."""
    pass

class Message:
    """Base class for messages.
    
    Subclasses should override:
    - message_id (int)
    - _message_struct_fields (list)
    - _params_names (list)
    - _message_struct (struct)
    """
    
    #This will be overrided by subclasses
    
    message_id = None
    
    _message_struct_fields = None
    _params_names = None
    _message_struct = None
    
    #Final class attributes (Message parsing)
    #Unpack message_id and dest
    _message_base_unpack_struct = struct.Struct('<HxxBx')
    #List of all final subclasses of Message (cache)
    _all_final_subclasses = None
    
    #Object attributes: parameters
    _params = None
    
    

    def __init__(self, **kw):
        self._params = {}
        
        for k, v in kw.items():
            self[k] = v
            
        self['message_id'] = self.message_id
        if 'data_packet_length' in self:
            self['data_packet_length'] = len(self) - 6
        
    def _validate_class_invariants(self):
        assert self._params_names is not None, "Invalid class {0} (no _params_names)".format(self.__class__)
        assert len(self._params_names) == len(self._message_struct_fields), "Invalid class {0} (length of _params_names and length of _message_struct_fields mismatch)".format(self.__class__)
        assert self._message_struct.format.decode('ascii') == '<' + ''.join(self._message_struct_fields), "Invalid class {0} (structure _message_struct doesn't match _message_struct_fields)\nHint: add _message_struct = struct.Struct('<' + ''.join(_message_struct_fields)) at the end of the message definition".format(self.__class__)
        return True
        
            
    def __len__(self):
        assert self._validate_class_invariants()
        return self._message_struct.size
    
    def __getitem__(self, k):
        assert self._validate_class_invariants()
        return self._params[k]
    
    def __setitem__(self, k, v):
        assert self._validate_class_invariants()
        if k not in self._params_names:
            raise KeyError("Unknown key {0}".format(k))
        
        ki = self._params_names.index(k)
        
        value_type = self._message_struct_fields[ki]
        if value_type == 'c':
            value_valid = type(v) == bytes and len(v) == 1
        elif value_type == '?':
            value_valid = type(v) == bool
        elif value_type in ('b', 'B', 'h', 'H', 'i', 'I', 'l', 'L', 'q', 'Q'):
            value_unsigned = value_type == value_type.upper()
            value_size = 8 * {'B': 1, 'H': 2, 'I': 4, 'Q': 8}[value_type.upper()]
            if type(v) == int:
                if value_unsigned:
                    value_valid = v >= 0 and v < (2 ** value_size)
                else:
                    value_valid = v >= -(2 ** (value_size - 1)) and v < (2 ** (value_size - 1))
            else:
                value_valid = False
        elif value_type in ('f', 'd'):
            value_valid = type(v) == float
        elif value_type.endswith('s'):
            value_valid = type(v) == bytes and len(v) <= int(value_type[:-1])
        else:
            value_valid = False
            
        if not value_valid:
            raise ValueError("Value {1!r} is not suitable for field {0} (type {2})".format(k, v, value_type))
        
        #Pad bytes
        if value_type.endswith('s'):
            value_length = int(value_type[:-1])
            v += (value_length - len(v)) * b'\x00'
            
        if hasattr(self, '_f_{0}_validate'.format(k)):
            if not getattr(self, '_f_{0}_validate'.format(k))(v):
                raise ValueError("Failed to validate field {0} with value {1!r}".format(k, v))
        self._params[k] = v
        
    def __contains__(self, k):
        return k in self._params_names
    
    def keys(self):
        return self._params_names
        
    def _f_message_id_validate(self, v):
        #Cannot change message id
        return v == self.message_id
    
    def _f_data_packet_length_validate(self, v):
        #Cannot change length of the data packet
        return v == len(self) - 6
    
    def _f_source_validate(self, v):
        return v < 0x80

    def _f_dest_validate(self, v):
        return v < 0x80
    
    def _f_chan_ident_validate(self, v):
        #Thorlabs APT Controllers, Issue 14, Page 21
        return v in (0x01, 0x02)
    
    def _f_chan_enable_state_validate(self, v):
        #Thorlabs APT Controllers, Issue 14, Page 21
        return v in (0x01, 0x02)

    @classmethod
    def parse(cls, message):
        #If the class is NOT a generic class, create an object and assign the bits
        if cls.message_id is not None:
            obj = cls()
            obj.bytes = message
            return obj
        
        #If instead we have a generic class, than we need to extract the message ID
        #We also extract the dest to determine if it's a long message or not
        #(some messages have two variants)
        
        #Messages less than 6 bytes cannot be complete according to the spec, ignore them
        if len(message) < cls._message_base_unpack_struct.size:
            raise IncompleteMessageException()
        
        #Get message id and destination
        message_id, dest = cls._message_base_unpack_struct.unpack(message[:cls._message_base_unpack_struct.size])
        
        #Is this a long message?
        long_message = (dest & 0x80) == 0x80

        #We cache for performance reasons the list of all Message subclasses
        if cls._all_final_subclasses is None:
            #Generic parse, we need to find the class
            subclasses = [Message]
            while any([len(x.__subclasses__()) > 0 for x in subclasses]):
                subclasses = [x for x in subclasses if len(x.__subclasses__()) == 0] + sum([x.__subclasses__() for x in subclasses if len(x.__subclasses__()) > 0], [])
                
            #Useful to debug problems fast
            for c in subclasses:
                assert c()._validate_class_invariants()
                
            Message._all_final_subclasses = subclasses

        #Find the correct class for the message
        for c in Message._all_final_subclasses:
            if c.message_id == message_id and long_message == (c._message_struct.size > 6):
                return c.parse(message)
            
        #Unable to find the message
        raise ValueError("Unknown message ID 0x{0:04X} {1!r}".format(message_id, message))
    
    def __len__(self):
        return self._message_struct.size    
    
    @property
    def bytes(self):
        assert self._validate_class_invariants()
        p = []
        for f in self._params_names:
            if f is None:
                p.append(0)
            else:
                if hasattr(self, '_f_{0}_to_bytes'.format(f)):
                    p.append(getattr(self, '_f_{0}_to_bytes'.format(f))(self[f]))
                else:
                    p.append(self[f])

        return self._message_struct.pack(*p)
    
    @bytes.setter
    def bytes(self, message):
        assert self._validate_class_invariants()
        try:
            params = self._message_struct.unpack(message[:self._message_struct.size])
        except struct.error:
            raise IncompleteMessageException()
        
        for f, p in zip(self._params_names, params):
            if f is None:
                continue
            if hasattr(self, '_f_{0}_from_bytes'.format(f)):
                self[f] = getattr(self, '_f_{0}_from_bytes'.format(f))(p)
            else:
                self[f] = p
                
    def __repr__(self):
        assert self._validate_class_invariants()
        params = []
        for f in self._params_names:
            #Ignore unknown field or message_id (which is already specified by the class name)
            if f is not None and f not in ('message_id', 'data_packet_length'):
                params.append('{0}={1!r}'.format(f, self[f]))

        return '{0}({1})'.format(self.__class__.__name__, ','.join(params))
        
        

class MessageWithData(Message):
    def _f_dest_to_bytes(self, v):
        return v ^ 0x80
    
    def _f_dest_from_bytes(self, v):
        return v ^ 0x80
    pass

class MessageWithoutData(Message):
    _message_struct_fields = ['H', 'B', 'B', 'B', 'B']
    _params_names = ['message_id', 'param1', 'param2', 'dest', 'source']
    _message_struct = struct.Struct('<' + ''.join(_message_struct_fields))
    
