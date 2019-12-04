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
    Exportando los resultados a Excel (XLSX file) con el nombre emails.xlsx en carpeta del lenguaje
    """
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    count = 0
    try:
        print("Exporting the results in an excel")
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook('emails.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0,0,30)
        worksheet.set_column(1,1,40)
        worksheet.set_column(2,2,100)
        formato=workbook.add_format({'bold': True})
        worksheet.write(row, 0, "Correo Electrónico", formato)
        worksheet.write(row, 1, "Dominio", formato)
        worksheet.write(row, 2, "URL", formato)
        row = 1
        fil=0
        for cada in emails:
            for j in range(0,3):
                worksheet.write(row, j, emails[fil][j])
            row += 1
            fil += 1

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
            print("\n[*]Email: " + str(email['value']+ str(email['sources'][0]['uri'])))
            #emails.append(str(email['value']))
            emails.append([str(email['value']),str(email['sources'][0]['domain']),str(email['sources'][0]['uri'])])
        
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

    ** Herramienta para buscar emails con api Hunter)
        ** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5-
        ***Agregados 03/12/2019: @Saltaseg con mejora en la interfases y recolecta mas informacion
        ** DISCLAMER: Esta herramienta está desarrollada con fines educativos. 
        ** El autor no se responsabiliza por otros usos
        ** Version 1.0""")


def main():
    """
    Main function of this tool
    """
    banner()
    #target = str(sys.argv[1])
    print("INGRESE UN DOMINIO PARA BUSCAR CORREOS ELECTRONICOS:..(. sin http ni www)...")
    print ("Dominio:")
    target = input()
    ##colocar aquí la api de hunter
    api = ""
    ##
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
        if emails != "-" and emails:
            export_results(emails)
        else:
            print("Sin Datos!!!!")
       
    except Exception as exception:
        print("Error in main function" + str(exception))


if __name__ == "__main__":
    main()
