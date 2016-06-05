from lxml import html
import requests
import csv


# probably didn't need to use objects here (could do list of lists or list of dictionaries) but wanted to try objects
class ContractAnnouncement(object):

    def __init__(self, url_id, announcement, date):
        self.url_id = url_id
        self.announcement = announcement
        self.date = date

# globally track urls for actual scraping
urls = []

# globally track press releases
press_releases = []

# put the numbers in the url range you want to get here
for i in range(1, 7):

    # open page and make html tree to get hyperlinks needed for actual scrape
    page = requests.get('http://www.defense.gov/News/Contracts?Page=' + str(i))

    # if error returned, try next site on list
    if page.status_code != 200:
        print(str(page.status_code) + " for Page " + str(i) + '. Could not open page.')
        continue
    else:
        tree = html.fromstring(page.content)
        # get elements corresponding to links to press release pages for each day
        hrefs = tree.xpath('//div/div/div/div[2]/div/div/div/a')
        for href in hrefs:
            urls.append(href.attrib['href'])
            print(href.attrib['href'] + '   Scraped Successfully')

# put the numbers in the url range you want to get here
for url in urls:

    # open page and make html tree
    page = requests.get(url)

    # if error returned, try next site on list
    if page.status_code != 200:
        print(str(page.status_code) + " for Contract ID " + str(i) + '. Could not open page.')
        continue
    else:
        tree = html.fromstring(page.content)
        # get date
        dateOfRelease = tree.xpath('//*[@id="dnn_ctr761_ViewArticle_UpdatePanel1"]/div/span[1]/text()'
                                   '[preceding-sibling::br]')[0]
        # get rid of extra whitespace and unicode characters
        dateOfRelease = " ".join(dateOfRelease.split())
        # select nodes
        paragraphs = tree.xpath('//p')
        # loop and filter out short (and unwanted) titles, etc.
        for paragraph in paragraphs:
            paragraph = paragraph.text_content()
            if len(paragraph) > 50:
                    # get rid of extra whitespace and unicode characters
                    paragraph = " ".join(paragraph.split())
                    press_releases.append(ContractAnnouncement(i, paragraph, dateOfRelease))
                    print('Successfully downloaded item from ' + dateOfRelease)

with open('contract_announcements_recent_items.csv', 'w', encoding='utf8', newline='') as csvfile:
    print('Logging scraped items to CSV.')
    contractAnnouncementsWriter = csv.writer(csvfile)
    contractAnnouncementsWriter.writerow(['url_id', 'announcement', 'date'])
    for item in press_releases:
        contractAnnouncementsWriter.writerow([item.url_id, item.announcement, item.date])
