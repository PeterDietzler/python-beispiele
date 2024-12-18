
std_1= 7
min_1= 2

std_2 =15
min_2=5

pause = 45

delta = ((std_2*60) + min_2) - ((std_1*60) + min_1)


print("Kommen = {%2d}:{%2d}", (std_1, min_1))
print(delta/60)
print(delta/60)

print("%2d:%2d" % ( (int(delta/60), delta%60)))

