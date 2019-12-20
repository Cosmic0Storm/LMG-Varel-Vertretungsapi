class Data:
    def __init__(self,Stand,Table,Name):
        self.Time=Stand.split(" ")[1]
        self.Table=Table
        Namespli=Name.split(" ")[0].split(".")
        self.Name="{0}-{1}-{2}".format(Namespli[-1],Namespli[-2] if len(Namespli[-2])>1 else "0"+Namespli[-2],Namespli[-3] if len(Namespli[-3])>1 else "0"+Namespli[-3])
        Daspli=Stand.split(" ")[0].split(".")
        self.Date="{0}-{1}-{2}".format(Daspli[-1],Daspli[-2],Daspli[-3])

    
    def __eq__(self,other):
        if not isinstance(other,self.__class__):
            return NotImplemented
        if len(self.Table)>1:
            for a in range(len(self.Table)):
                for b in range(len(self.Table[a])):
                    try:
                        if self.Table[a][b]!=other.Table[a][b]: 
                            return False
                    except IndexError:
                        return False
            return True
        else:
            return False

    def __ne__(self,other):
        return not self.__eq__(other)
                
    def clear(self):
        self.Date=""
        self.Time=""
        self.Table=[[]]
