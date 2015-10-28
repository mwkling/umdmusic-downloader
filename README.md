# umdmusic-downloader
Python script to download top billboard singles from www.umdmusic.com

I used this to get the data I needed for a data visualization project on my blog at http://www.modestinsights.com/analyzing-the-billboard-hot-100/.  Great website for historical music chart data (was not able to find anything elsewhere, except possibly paying billboard.com).

One note - using the default python html parser did not work, but BeautifulSoup docs suggested using html5lib, which fixed the problem.
