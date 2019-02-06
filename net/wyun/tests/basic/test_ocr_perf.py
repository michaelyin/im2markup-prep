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

#handwriting test with aws tokyo ecs/autoscale
file = open(dir + "batch_20180924070030.txt", 'r')

file_num_list = []
total_list = []
ocr_list = []
search_list = []

for line in file.readlines():
    cols = line.rstrip().split(',') #using rstrip to remove the \n
    #print cols
    file_num_list.append(cols[0])
    total_list.append(cols[2])
    ocr_list.append(cols[3])
    search_list.append(cols[4])

print_stats(total_list)
print_stats(ocr_list)
print_stats(search_list)

# find top 10 in ocr_list
lst = map(int, ocr_list)
np_a = np.asarray(lst)
top_10_idx = np.argsort(np_a)[-20:]
top_10_filenum = [file_num_list[i] for i in top_10_idx]
print top_10_filenum
print [ocr_list[i] for i in top_10_idx]

print 'total in the list: ', len(ocr_list), 'percent: ', len(ocr_list)/36017.0