class student:
    
    def __init__(self,name,roll_no,marks):
        self.marks=marks
        self.name=name
        self.roll_no=roll_no
        self._protected = "Protected"
    
    def avg(self):
        print(sum(self.marks.values()) / len(self.marks))

s1=student("sudhanshu",11,{"Math": 50, "Science": 60})
s2=student("me",12,{"Math": 100, "Science": 60})
s1.avg()
s2.avg()
print(s1._protected)
