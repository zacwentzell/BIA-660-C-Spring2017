# == Python 2 Ipython window
infile = open('test_ascii_file')

infile.readline()

infile.read()

infile.read()

infile.seek(0)

infile.read()


infile = open('test_write_file', 'w')

infile.write('Hello World!')

infile.close()

infile = open('test_write_file', 'w')

infile.write('Different text')

infile.close()

infile = open('test_write_file', 'a')

infile.write('more text')

infile.close()

with open('test_write_file', 'a') as infile:
    infile.write('\n using a new line')


infile = open('../../SalesJan2009.csv')

infile.readline()

with open('../../SalesJan2009.csv') as infile:
    for line in infile.readlines()[:3]:
        print line.count(',')

infile = open('../../SalesJan2009.csv', 'rU')

header = infile.readline()


infile.readline()

infile = open('test_ascii_file')

infile = open('test_utf8_file')

infile.readline()

infile.readline()

l = infile.readline()

unicode(l)



unicode(l, 'ascii', 'ignore')

unicode(l, 'ascii', 'replace')

unicode(l, 'utf-8', 'replace')

print unicode(l, 'utf-8', 'replace')

infile = open('test_chinese_text')


l = infile.readline()


l.decode('utf-8')

print l.decode('utf-8')



infile = open('maxresdefault.jpg')

infile.readline()

# == Python 3 Ipython window
infile = open('test_chinese_text')

infile.readline()


infile.close()

infile = open('maxresdefault.jpg')

infile.readline()

infile = open('maxresdefault.jpg', 'rb')

infile.readline()
