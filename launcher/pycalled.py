import sys
import os

# 将项目根目录加入 sys.path，支持直接运行
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_calc import coast_stackcalc as csc

rpn = csc.CoastStackCalcculator()

rpn.run("1 2 +")

print(rpn.stack)  

