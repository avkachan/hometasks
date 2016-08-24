word = input('Cлово: \n')
drow = word[::-1]
if word == drow:
    print ('Cлово - палиндром')
else:
    print('Cлово - не палиндром')
