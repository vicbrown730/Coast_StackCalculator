from . import instuctions as oins

class CoastStackCalcculator():
    def __init__(self):
        self.ins_dict = {
            "+": self.add
        }
    
    def run(self, ins: str):
        self.stack = []
        ins_list = ins.split()
        for i in range(len(ins_list)):
            this_token:str = ins_list[i]
            try:
                self.ins_dict[this_token]()
            except KeyError:
                self.stack.append(this_token)
            except IndexError:
                print("栈上越界")

    def add(self):
        
        self.stack.append(oins.add(self.stack.pop(), self.stack.pop()))
        return
        


