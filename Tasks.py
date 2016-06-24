class Task :
    """
    calss for cearting new tasks
    """
    def __init__(self,T=[]):
        if len(T)==11:
            self.taskclass = str(T[0])
            self.title = str(T[1])
            self.shortcut = str(T[2])
            self.isurg = bool(T[3])
            self.isimp = bool(T[4])
            self.isinst = bool(T[5])
            self.period = int(T[6])
            self.starttime = int(T[7][:2])*60 + int(T[7][3:5])
            self.endtime = int(T[8][:2])*60 + int(T[8][3:5])
            self.hardness = int(T[9])
            self.notes = str(T[10])
            if T[5]:
                self.s_task = int(T[7][:2])*60 + int(T[7][3:5])
        else:
            pass


