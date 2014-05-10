from os.path import join

import utilities as util

data_path = join(util.module_path(), "..\\analysis")
f = open(join(data_path, 'logsimpGAN=128.txt'), 'r')
f2 = open(join(data_path, 'ResultlogsimpGAN=128.txt'), 'w')

count = 0
flg = False
print "Process Started ..."
for j in f.readlines():
    if "Final Members" in j:
        count += 1
        flg = True
        f2.write("Generation %d\n" % count)
        continue
    if "Undergoing" in j:
        f2.write("\n")
        flg = False
    if flg:
        f2.write(j)

f2.close()

print "Done"
