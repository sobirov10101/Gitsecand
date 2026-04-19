
toam = True
osh = True
shashlik = True
cola = True
choy = True
shorva = True
salot = True
print('OSH MARKAZ\n Assalomu Aleykum\n Bizning osh markaziga hush kelibsiz\n Bizning Menu\n Osh - 35000\n Shorva - 15000 \n Shashlik - 12000\n salat - 10000\n  Ichimliklar: cola, choy\n cola - 10000\n choy - 5000\n OSH MARKAZI Kamchilik\n Siz bizga ha yoki yoq deb aytolmaysiz shuning uchun buni yodda tuting!\n HA: ovqatdan qancha buyurtma qilmoqchi bolsanggiz yozing 1 yoki 2\n YOQ: 0')
d = int(input("necha porsi osh buyurasiz: "))
if osh:
    toam += 35000 * d
    if d == 0:
        print("siz choy buyurtma bermadinggiz")
    else:
        print("siz choy buyurtma berdinggiz") 
e = int(input("necha dona shashlik buyurma berasiz: "))
if shashlik:
    toam += 12000 * e
    if e == 0:
        print("siz choy buyurtma bermadinggiz")
    else:
        print("siz choy buyurtma berdinggiz")
a = int(input("necha cola buyurasaiz: "))
if cola:
    toam += 10000 * a
    if a == 0:
        print("siz choy buyurtma bermadinggiz")
    else:
        print("siz choy buyurtma berdinggiz")
b = int(input("nechta choynak choy buyurtma berasiz: "))
if choy:
    toam += 5000 * b
    if b == 0:
        print("siz choy buyurtma bermadinggiz")
    else:
        print("siz choy buyurtma berdinggiz")
r = int(input("necha tarelka salot buyurma berasiz: "))
if salot:
    toam += 10000 * r
    if r == 0:
        print("siz choy buyurtma bermadinggiz")
    else:
        print("siz choy buyurtma berdinggiz")
q = int(input("qancha kosa shorva buyurtma berasiz: "))
if shorva:
    toam += 15000 * q
    if q == 0:
        print("siz choy buyurtma bermadinggiz")
    else:
        print("siz choy buyurtma berdinggiz")
v = toam -1
if v == 0:
    print("siz ovqat zaqas bemadinggiz:")
print("sizning buyurmalaringgiz: ")
if d > 0:
    print("osh")
if e > 0:
    print("shashlik")
if b > 0:
    print("choy")
if r > 0:
    print("salot")
if q > 0:
    print("shorva")
if a > 0:
    print("cola")
print(f"sizning hisobinggiz {toam - 1} som boldi")
print("Tolovni amalga oshirish uchun Kassaga boring va shu kodni ayting")