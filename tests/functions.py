def get_new_price(oldPrice, deduction, deductionPrecision=3):
    # deductionPrecision is 3
    length = len(str(oldPrice))-2
    toAdd = length - deductionPrecision
    toAdd = "8"*toAdd
    power = pow(10, deductionPrecision)
    intPart = int((oldPrice-deduction)*power)
    floatPart = intPart / power
    return float(str(floatPart)+toAdd)
print(get_new_price(0.27442,0.0008,5))
#$0.2732