import re

from bs4 import BeautifulSoup
from requests import session


def main():
    s = session()
    request_path = "http://www.umdmusic.com/default.asp?Lang=English&Chart=D"
    out_file = "us_billboard.psv"
    with open(out_file, 'a') as f:
        while True:
            print("Downloading data from: " + request_path)
            html = s.get(request_path).content
            soup = BeautifulSoup(html, "html5lib")

            # first find the link for the previous chart (since the date for the current chart is embedded in it)
            previous_link = soup.find_all(href=re.compile("ChDate=\d+&ChMode=P"))
            if len(previous_link) > 0:
                request_path = previous_link[0]['href']
                request_path = "http://www.umdmusic.com/" + request_path
                m = re.match(".*ChDate=(\d+).*", request_path)
                chart_date = m.group(1)
            else:
                break

            # use this comment text that appears in the html to guide us towards the main table body
            main_table = soup.find_all(text=re.compile("Display Chart Table"))[0]
            while main_table.name != "table":
                main_table = main_table.next_element

            for row in main_table.tbody.children:
                if row.name == "tr":
                    past_first_cell = False
                    for cell in row.children:
                        if cell.name == "td":
                            if len(cell.contents) == 1:
                                f.write(cell.string.strip() + "|")
                                past_first_cell = True
                            elif len(cell.contents) == 3:
                                # fix that lets us skip header rows
                                if not past_first_cell:
                                    break
                                f.write(cell.contents[0].string.strip() + "|")
                                f.write(cell.contents[2].string.strip() + "|")
                    if past_first_cell:
                        f.write(chart_date + "\n")


if __name__ == "__main__":
    main()
