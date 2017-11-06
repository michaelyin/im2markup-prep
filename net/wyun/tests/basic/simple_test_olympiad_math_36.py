# for a given ind, generate number with 'ind' 1s
#  ind = 1, return 1
#  ind = 2, return 11
#
def generate(ind):
    sum = 0
    for i in range(0, ind):
        sum += 10 ** i
    return sum

# generate all the numbers and put them inside a list
num_list  = []
for i in range(1, 31):
    current = generate(i)
    num_list.append(current)


total = 0
for num in num_list:
    print '\n', num
    total += num

print '\n total: ', total

# get last 2 digits
num_2digits = total % 100  # get remainder when divide 100
num_1digits = total % 10   # get remainder when divide 10

# get the digit of 10s
print 'digit at 10s: ', (num_2digits - num_1digits) / 10

