"""301
n=input()
is_valid=True
for digit in n:
    if int(digit)%2!=0:
        is_valid=False
        break
if is_valid:
    print("Valid")
else:
    print("Not valid")"""

"""302
def isUsual(num):
    if num<=0:
        return False
    for divisor in [2,3,5]:
        while num%divisor==0:
            num//=divisor
    return num==1
n=int(input())
if isUsual(n):
    print("Yes")
else:
    print("No")"""

"""303
def decode_number(s):
    codes={
    "ZER":"0","ONE":"1","TWO":"2", "THR":"3",
    "FOU":"4","FIV":"5","SIX":"6"
    "SEV":"7","EIG":"8", "NIN":"9"
    }
    numder=""
    for i in range(0,len(s),3):
    """
