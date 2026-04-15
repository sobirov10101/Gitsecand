import math
x = float(input("x ni kiriting"))
y = float(input("y ni kiriting"))
c1 = x + y / (y ** 2) + (((y **2) + 2 ) / ((x) + math.fabs((x ** 3)/5))) + math.e ** (y + 2)
print(f"misol javobi={c1}")