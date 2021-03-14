class user:
    """
    Class for convenient consolidation of a user's name, client and IP address
    """

    def __init__(self, name, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def setName(self, name):
        self.name = name