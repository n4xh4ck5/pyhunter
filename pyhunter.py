#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script will return emails gathered from hunter.io given a target domain
"""

import json
import requests
import sys
import xlsxwriter

def export_results (emails):
	"""
	Exports the results into a XLSX file
	"""
	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0
	i = 0
	try:
		print "Exporting the results in an excel"
		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook('hunter.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write(row, col, "email")
		row += 1
		# Iterate over the data and write it out row by row.
		for email in emails:
				col = 0
				worksheet.write(row, col, email)
				row += 1
				i += 1

		#Close the excel
		workbook.close()

	except Exception as e:
		print "Error in export_results" + str(e)

def manage_response (data):
	"""
	Treats the response obtained from the API
	"""
	emails = []
	try:
		for email in data['data']['emails']:
			print "\n[*]Email: " + str(email['value'])
			emails.append(str(email['value']))
	except:
		print "Not found information of the domain"
		emails = "-"

	finally:
		return emails
		
def send_request (url):
	"""
	Sends custom request to the API
	"""
	response = None

	try:

		response = requests.get(url,timeout=5,allow_redirects =True)
	except Exception as e:
		print e

	finally:
		return response.json()

def banner():
	"""
	Prints cool custom banner
	"""
	print"\n"
	print """
	                                                                                                              
	                     /$$                             /$$                        
	                    | $$                            | $$                        
	  /$$$$$$  /$$   /$$| $$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ 
	 /$$__  $$| $$  | $$| $$__  $$| $$  | $$| $$__  $$|_  $$_/   /$$__  $$ /$$__  $$
	| $$  \\ $$| $$  | $$| $$  \\ $$| $$  | $$| $$  \\ $$  | $$    | $$$$$$$$| $$  \\__/
	| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$  | $$ /$$| $$_____/| $$      
	| $$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$/| $$  | $$  |  $$$$/|  $$$$$$$| $$      
	| $$____/  \\____  $$|__/  |__/ \\______/ |__/  |__/   \\___/   \\_______/|__/      
	| $$       /$$  | $$                                                            
	| $$      |  $$$$$$/                                                            
	|__/       \\______/                                                                                                        
	"""
	print """
	** Tool to search possible emails indexed throught API's Hunter.io (https://hunter.io)
    	** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
    	** DISCLAMER This tool was developed for educational goals. 
    	** The author is not responsible for using to others goals.
    	** A high power, carries a high responsibility!
    	** Version 1.0"""

def main(argv):
	"""
	Main function of this tool
	"""
	banner()
	target = str(sys.argv[1])
	API=""
	r = None
	emails = []
	try:

		url = "https://api.hunter.io/v2/domain-search?domain="+target+"&api_key="+API
		#Sent request
		r = send_request(url)
		# Manage the response
		emails = manage_response(r)

		#Export results		
		export_results(emails)

	except Exception as e:
		print "Error in main function" + str(e)


if __name__ == "__main__":
    main(sys.argv[1:])
