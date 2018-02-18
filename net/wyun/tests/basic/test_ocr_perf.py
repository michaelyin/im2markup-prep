import numpy as np

from scipy import stats



def print_stats(time_list):
    lst = map(int, time_list)
    np_a = np.asarray(lst)
    print 'max:', max(lst), ', mean: ', sum(lst)/len(lst), ', min: ', min(lst), ', 98%: ', np.percentile(np_a, 98), ', 50%: ', \
        np.percentile(np_a, 50), ', 2 sec. percentile: ', stats.percentileofscore(np_a, 2000)

#dir = "/home/michael/git/OCRCloud/WyunOcrClient/"
dir = 'data/ocr_search/'
#batch_20180217080157.txt, the worst case
file = open(dir + "batch_20180218134018.txt", 'r')
file = open(dir + "batch_20180217080157.txt", 'r')

total_list = []
ocr_list = []
search_list = []

for line in file.readlines():
    cols = line.rstrip().split(',') #using rstrip to remove the \n
    #print cols
    total_list.append(cols[2])
    ocr_list.append(cols[3])
    search_list.append(cols[4])

print_stats(total_list)
print_stats(ocr_list)
print_stats(search_list)

