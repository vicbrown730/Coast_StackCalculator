from calc import base_csc as cscal

rpn = cscal.CoastStackCalculator()

rpn.run("1 2 + 3 * 4 / 5 - 6")

print(rpn.stack)  

