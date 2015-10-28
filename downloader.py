from bs4 import BeautifulSoup
import urllib.request
import re

def main():
    request_path="http://www.umdmusic.com/default.asp?Lang=English&Chart=D"
    out_file = "us_billboard.psv"
    f=open(out_file, 'a')

    while request_path != "":
        print("Downloading data from: " + request_path)
        response = urllib.request.urlopen(request_path)
        html = response.read()
        soup = BeautifulSoup(html, "html5lib")
        chart_date=""

        #first find the link for the previous chart (since the date for the current chart is embedded in it)
        previous_link=soup.find_all(href=re.compile("ChDate=\d+&ChMode=P"))
        if len(previous_link) > 0:
            request_path=previous_link[0]['href']
            request_path="http://www.umdmusic.com/" + request_path
            m=re.match(".*ChDate=(\d+).*",request_path)
            chart_date=m.group(1)
        else:
            request_path=""

        #use this comment text that appears in the html to guide us towards the main table body
        main_table=soup.find_all(text=re.compile("Display Chart Table"))[0]
        while main_table.name != "table":
            main_table = main_table.next_element

        for row in main_table.tbody.children:
            if row.name == "tr":
                past_first_cell=False
                for cell in row.children:
                    if cell.name == "td":
                        if len(cell.contents) == 1:
                            f.write(cell.string.strip()+"|")
                            past_first_cell=True
                        elif len(cell.contents) == 3:
                            #fix that lets us skip header rows
                            if not(past_first_cell):
                                break
                            f.write(cell.contents[0].string.strip() + "|")
                            f.write(cell.contents[2].string.strip() + "|")
                if past_first_cell:
                    f.write(chart_date + "\n")

    f.close()

if __name__=="__main__":
    main()
