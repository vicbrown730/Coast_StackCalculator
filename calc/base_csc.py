import operator as op

from .exceptions import StackManagement, MathError, SyntaxFault, BaseCSCException

class CoastStackCalculator():
    def __init__(self):
        self.ins_dict = {
            "+": self.add,
            "-": self.sub,
            "*": self.mul,
            "/": self.true_div
        }
    
    def run(self, ins: str):
        self.stack = []
        ins_list = ins.split()
        for i in range(len(ins_list)):
            this_token:str = ins_list[i]
            if this_token in self.ins_dict.keys():
                try:
                    self.ins_dict[this_token]()
                except IndexError:
                    raise StackManagement("栈上越界", 0) from None
                except ValueError:
                    raise SyntaxFault("token无法参与运算", 0) from None
                except Exception:
                    raise BaseCSCException("未知错误", 0)
            
            else:
                self.stack.append(this_token)
            

    def add(self):
        self.stack.append(op.add(float(self.stack.pop()), float(self.stack.pop())))
        return
    
    def sub(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(op.sub(float(b), float(a)))
        return
    
    def mul(self):
        self.stack.append(op.mul(float(self.stack.pop()), float(self.stack.pop())))
        return
    
    def true_div(self):
        a = float(self.stack.pop())
        b = float(self.stack.pop())
        if a == 0:
            raise MathError("除数为零", 0) from None
        self.stack.append(op.truediv(b, a))
        return
        


