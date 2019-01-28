#!/usr/bin/python3


import cgi, cgitb
import datetime
form = cgi.FieldStorage()

yearValue = int(form.getvalue("year"))
formatValue = form.getvalue("format")

def easter(y):
	a = y % 19
	b = y // 100
	c = y % 100
	d = b // 4
	e=b%4
	g = (8 * b + 13) // 25
	h = (19 * a + b - d - g + 15) % 30
	j = c // 4
	k=c%4
	m = (a + 11 * h) // 319
	r = (2 * e + 2 * j - k - h + m + 32) % 7
	n = (h - m + r + 90) // 25
	p = (h - m + r + n + 19) % 32
	formatOutput(y,n,p)
	
def getNumerical(year, month, day):
	return str(day)+"/"+str(month)+"/"+str(year)
	
def getVerbosely(year, month, day):
	monthString = datetime.date(year, month, 1).strftime('%B')
	suffix = ""
	if 4 <= day <= 20 or 24 <= day <= 30:
		suffix = "th"
	else:
		suffix = ["st", "nd", "rd"][day % 10 - 1]
	return str(day) + "<sup>" + suffix + "</sup>" + " of " + monthString + " " + str(year)
	
def formatOutput(year, month, day):
	if formatValue == "numerically":
		print("<h1>" + getNumerical(year, month, day) + "</h1>")
	elif formatValue == "verbosely":
		print("<h1>" + getVerbosely(year, month, day) + "</h1>")
	else:
		print("<h1>" + getNumerical(year, month, day) + "</h1>")
		print("<br />")
		print("<br />")
		print("<br />")
		print("<h1>" + getVerbosely(year, month, day) + "</h1>")
		
print("Content-Type: text/html")
print("")
print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("<meta charset=\"utf-8\">")
print("<title>The Date of Easter</title>")
print("<link rel=\"stylesheet\" type=\"text/css\" href=\"../styles.css\">")
print("</head>")
print("<body>")

print("<div class=\"header\">")
print("<h1>Finding Easter</h1>")
print("</div>")


print("<div class=\"output\">")
easter(yearValue)

print("<button type=\"button\" onclick=\"location.href=\'../index.html'\" id=\"backButton\">Go Back!</button>")

print("</div>")


print("</body>")
print("</html>")



