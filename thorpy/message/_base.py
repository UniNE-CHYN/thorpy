import struct
from ..helpers import classproperty


class IncompleteMessageException(Exception):
    """IncompleteMessageException is thrown when a message could not be parsed,
    because some of the bytes are missing."""
    pass


class Message:
    """Base class for messages.
    
    Subclasses should override:
    - id (int)
    - is_long_cmd (bool)
    - parameters (list of tubles like (name, struct encoding))
    """
    
    #This will be overrided by subclasses
    id = 0x0
    is_long_cmd = False
    parameters = [(None, 'B'), (None, 'B')]

    # class wide caches
    _struct_description = None

    def __init__(self, *args, source=0x01, dest=None, **kwargs):
        self.dest, self.source = dest, source

        parameter_values = [None, ] * len(self.parameters)

        # Set parameters by position
        for i, value in enumerate(args):
            parameter_values[i] = value

        # Set parameter by name
        parameter_mapping = {name: position for position, (name, encoding)
                             in enumerate(self.parameters)}
        for name, value in kwargs.items():
            try:
                position = parameter_mapping[name]
            except KeyError:
                raise KeyError('{0} not a valid parameter. Must be one of {1}'.format(name, self.parameter_names))

            if parameter_values[position] is not None:
                raise ValueError('Parameter {0} "{1}" was already set by positional argument.'.format(position, name))
            parameter_values[position] = value

        # Check that all parameters of the message are set. A message may not miss any parameters on creation.
        for position, ((name, encoding), value) in enumerate(zip(self.parameters, parameter_values)):
            if name is not None and value is None:
                raise ValueError('Parameter {0} "{1}" ({2}) was not set.'.format(position, name, encoding))
        self._parameter_values = parameter_values

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, destination_id):
        if destination_id is not None:
            assert isinstance(destination_id, int)
            assert 0 <= destination_id <= 0x80
        self._dest = destination_id

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source_id):
        if source_id is not None:
            assert isinstance(source_id, int)
            assert 0 <= source_id <= 0x80
        self._source = source_id

    @classproperty
    def name(self):
        return self.__name__

    @classproperty
    def category(cls):
        split_name = cls.__name__.split('_')
        assert split_name[0] == 'MGMSG', 'Class name has to start with MGMSG_'
        return split_name[1].lower()

    @classproperty
    def is_property(cls):
        split_name = cls.__name__.split('_')
        return split_name[2] in ('REQ', 'SET', 'GET')

    @classproperty
    def parameter_names(cls):
        return [name for name, encoding in cls.parameters if name is not None]

    @classproperty
    def struct_description(cls):
        # On the first call the class wide message Struct is not yet built,
        # after that we may rely on the class wide cache of the Struct.
        if cls._struct_description is None:
            if not cls.is_long_cmd:
                full_struct_desc = [('message_id', 'H'), ] + cls.parameters + [('dest', 'B'), ('source', 'B')]
            else:
                full_struct_desc = ([('message_id', 'H'), ('length', 'H'), ('dest', 'B'), ('source', 'B')]
                                    + cls.parameters)
            names, encodings = zip(*full_struct_desc)
            message_struct = struct.Struct('<' + ''.join(encodings))
            cls._struct_description = names, message_struct
        else:
            names, message_struct = cls._struct_description
        return names, message_struct

    @property
    def parameter_items(self):
        return ((name, value) for ((name, encoding), value)
                in zip(self.parameters, self._parameter_values) if name is not None)

    @classproperty
    def binary_length(cls):
        return cls.struct_description[1].size

    def __len__(self):
        return self.binary_length
    
    def __getitem__(self, k):
        if isinstance(k, int):
            return self._parameter_values[k]
        else:
            # FIXME: This is a bit inefficient since we create dictioneries on the fly.
            #        However, I doubt this will ever become a bottle neck.
            return dict(self.parameter_items)[k]
        
    def __contains__(self, k):
        return k in self.parameter_names

    @classmethod
    def get_message_class_by_id(cls, message_id):
        message_classes = list(filter(lambda x: x.id == message_id, Message.__subclasses__()))
        assert len(message_classes) < 2, 'Multiple classes with id {0} defined'.format(message_id)
        if len(message_classes) < 1:
            raise KeyError('Unknown message id {0}'.format(message_id))
        return message_classes[0]

    @classmethod
    def parse(cls, buffer):
        base_package = struct.Struct('<HHBB')
        base_package_length = base_package.size

        # Messages less than 6 bytes cannot be complete according to the spec, ignore them
        if len(buffer) < base_package_length:
            raise IncompleteMessageException()

        # Assuming a long message, get its id and length
        message_id, length, dest, source = base_package.unpack(buffer[:base_package_length])
        long_message = (dest & 0x80) == 0x80    # Is it really a long message?

        # In case of a long message, we might not have all bytes yet
        if len(buffer) < base_package_length + (length if long_message else 0):
            raise IncompleteMessageException()

        msg_cls = Message.get_message_class_by_id(message_id)
        # TODO: Add checks if long message is really a long message
        fields, msg_struct = msg_cls.struct_description
        descr = dict(zip(fields, msg_struct.unpack(buffer)))

        if msg_cls.is_long_cmd:
            assert descr['dest'] & 0x80, 'Long message expected, but message binary does not mark it as long.'
            descr['dest'] &= 0x7f

            assert descr['length'] == len(buffer) - 6
            del descr['length']

        assert descr['message_id'] == msg_cls.id
        del descr['message_id']

        if None in descr:
            del descr[None]

        return msg_cls(**descr)

    def __bytes__(self):
        fields, msg_struct = self.struct_description

        if self.dest is None:
            raise RuntimeError('Cannot convert message without destination '
                               'to byte representation')

        if self.source is None:
            raise RuntimeError('Cannot convert message without source to '
                               'to byte representation')

        descr = dict(self.parameter_items)
        descr['message_id'] = self.id
        descr['length'] = self.binary_length - 6
        descr['source'] = self.source
        descr['dest'] = self.dest | (0x80 if self.is_long_cmd else 0)
        descr[None] = 0

        values = map(lambda x: descr[x], fields)

        type_mapping = {
            str: lambda x: x.encode('ascii')
        }
        encoded_values = map(lambda x: type_mapping.get(type(x), type(x))(x), values)
        return msg_struct.pack(*encoded_values)

    def __repr__(self):
        return "<%s>(dest=0x%x, src=0x%x, %s)" % (self.__class__.__name__,
                                                self.dest, self.source,
                                                ', '.join('{0}={1}'.format(name, repr(value)) for name, value in
                                                          self.parameter_items))
