#import cgi
import sys
#form = cgi.FieldStorage()
#searchterm =  form.getvalue('searchbox')
searchterm = sys.argv[1];
print(searchterm)
file = open("test.txt", "w+")
file.write(searchterm)
file.close()