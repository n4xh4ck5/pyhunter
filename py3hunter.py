#!/usr/bin/python
# -*- coding: utf-8 -*-
#Colaboratorion of @Guille_Hartek to translate python2 to python3
"""
This script will return emails gathered from hunter.io given a target domain
"""
import sys
import requests
import xlsxwriter


def export_results(emails):
    """
    Exports the results into a XLSX file
    """
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    count = 0
    try:
        print("Exporting the results in an excel")
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
            count += 1

        #Close the excel
        workbook.close()

    except Exception as excp:
        print("Error in export_results" + str(excp))


def manage_response(data):
    """
    Treats the response obtained from the API
    """
    emails = []
    try:
        for email in data['data']['emails']:
            print("\n[*]Email: " + str(email['value']))
            emails.append(str(email['value']))
    except Exception:
        print("Could not find any information about that")
        emails = "-"
    return emails


def send_request(url):
    """
    Sends custom request to the API
    """
    response = None
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
    except Exception as excp:
        print(excp)
    return response.json()


def banner():
    """
    Prints cool custom banner
    """
    print("\n")
    print("""
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
        """)

    print("""

    ** Tool to search possible emails indexed throught API's Hunter.io (https://hunter.io)
        ** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
        ** DISCLAMER This tool was developed for educational goals. 
        ** The author is not responsible for using to others goals.
        ** A high power, carries a high responsibility!
        ** Version 1.0""")


def main():
    """
    Main function of this tool
    """
    banner()
    target = str(sys.argv[1])
    api = ""
    response = None
    emails = []
    limit = 100 # by default limit=10
    try:
        url = "https://api.hunter.io/v2/domain-search?domain="+target+"&api_key="+api+"&limit="+str(limit)
        #Sent request
        response = send_request(url)
        # Manage the response
        emails = manage_response(response)
        #Export results
        if emails != "-":
            export_results(emails)
    except Exception as exception:
        print("Error in main function" + str(exception))


if __name__ == "__main__":
    main()
