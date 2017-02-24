import sys
if len(sys.argv) == 2:
    file_name = sys.argv[1]
    try:
        with open(file_name) as file:
            content = file.readlines()

        content.reverse()
        for x in content:
            print x,
    except:
        print "No Such File!"
else:
    print "No File Specified!"
