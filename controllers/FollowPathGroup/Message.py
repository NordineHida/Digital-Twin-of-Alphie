import struct

class Message:
    # Définition des types de message
    class Type_Message:
        OK = 0
        REPORT_STATUS = 1
        STATUS = 2
        REPORT_ERRORS = 3
        ERROR = 4
        REPORT_POSITION = 5
        POSITION = 6
        ABORT = 7
        FORWARD = 8
        BACKWARD = 9
        TURN_LEFT = 10
        TURN_RIGHT = 11
        FORWARD_TURN = 12
        BACKWARD_TURN = 13
        STOP = 14
        TURN_TOWARDS = 15
        GO_TO_COORDINATES = 16
        RAW = 17
        INVALID = 18

    def __init__(self):
        """
        Constructeur de la classe Message.
        """
        self._type = Message.Type.INVALID
        self._size = 0
        self._payload = bytearray()

    def __eq__(self, other):
        """
        Méthode de comparaison pour les opérateurs d'égalité (==).
        """
        return (self._type == other._type) and (self._size == other._size) and (self._payload == other._payload)

    def __ne__(self, other):
        """
        Méthode de comparaison pour les opérateurs de différence (!=).
        """
        return not self.__eq__(other)

    def size(self):
        """
        Renvoie la taille de la charge utile du message.
        """
        return self._size

    def type(self):
        """
        Renvoie le type du message.
        """
        return self._type

    def raw_payload(self):
        """
        Renvoie la charge utile brute du message.
        """
        return bytes(self._payload)

    def write_raw_payload(self, type_, data):
        """
        Écrit une charge utile brute dans le message.
        """
        self._type = type_
        self._payload = bytearray(data)
        self._size = len(data)

    def write(self, type_):
        """
        Écrit un message sans charge utile.
        """
        self._type = type_
        self._payload = bytearray()
        self._size = 0

    def write_byte(self, type_, data):
        """
        Écrit un message avec un octet.
        """
        self._type = type_
        self._payload = bytearray([data])
        self._size = 1

    def write_bytes(self, type_, data1, data2):
        """
        Écrit un message avec deux octets.
        """
        self._type = type_
        self._payload = bytearray([data1, data2])
        self._size = 2

    def write_float(self, type_, data):
        """
        Écrit un message avec un nombre flottant.
        """
        self._type = type_
        self._payload = bytearray(struct.pack('f', data))
        self._size = 4

    def write_coordinates(self, type_, latitude, longitude):
        """
        Écrit un message avec des coordonnées.
        """
        self._type = type_
        self._payload = bytearray(struct.pack('ff', latitude, longitude))
        self._size = 8

    def read(self, type_):
        """
        Vérifie si le message correspond au type attendu sans charge utile.
        """
        return self._type == type_ and self._size == 0

    def read_byte(self, type_):
        """
        Vérifie si le message correspond au type attendu avec un octet.
        """
        return self._type == type_ and self._size == 1

    def read_bytes(self, type_):
        """
        Vérifie si le message correspond au type attendu avec deux octets.
        """
        return self._type == type_ and self._size == 2

    def read_float(self, type_):
        """
        Vérifie si le message correspond au type attendu avec un nombre flottant.
        """
        return self._type == type_ and self._size == 4

    def read_coordinates(self, type_):
        """
        Vérifie si le message correspond au type attendu avec des coordonnées.
        """
        return self._type == type_ and self._size == 8
