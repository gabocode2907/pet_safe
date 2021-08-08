def ci_validator(ci):
    print(ci)
    suma = 0
    for i in range(len(ci)-2,-1,-1):
        x = int(ci[i])
        print(x)
        if i%2 == 0:
            x = x * 2
            if x > 9:
                x = x - 9
        suma = suma + x
    print(suma)
    if suma%10 != 0:
        result = 10 - (suma%10)
    if result == int(ci[9]):
        isvalid = 1
        return isvalid
    else:
        isvalid = 0
        return isvalid