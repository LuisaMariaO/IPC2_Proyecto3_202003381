class Fechagrafica():
    def __init__(self,fecha):
        self.fecha=fecha
        self.vtotal=0
        self.vsiniva=0
    
    def sumTotal(self,total):
        self.vtotal+=total

    def sumSIva(self,siva):
        self.vsiniva+=siva