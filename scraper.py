from lxml import html
import requests
import csv


# probably didn't need to use objects here (could do list of lists or list of dictionaries) but wanted to try objects
class ContractAnnouncement(object):

    def __init__(self, url_id, announcement, date):
        self.url_id = url_id
        self.announcement = announcement
        self.date = date

# globally track press releases
press_releases = []

# put the numbers in the url range you want to get here
for i in range(391, 5606):

    # open page and make html tree
    page = requests.get('http://archive.defense.gov/Contracts/Contract.aspx?ContractID=' + str(i))

    # if error returned, try next site on list
    if page.status_code != 200:
        print(str(page.status_code) + " for Contract ID " + str(i) + '. Could not open page.')
        continue

    else:
        tree = html.fromstring(page.content)

        # get date
        dateOfRelease = tree.xpath('//*[@id="ctl00_cphBody_ContentContents_PressOpsItemContentPreTitle"]/div/text()'
                                   '[preceding-sibling::br]')[0]

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

with open('contract_announcements.csv', 'w', encoding='utf8', newline='') as csvfile:
    print('Logging scraped items to CSV.')
    contractAnnouncementsWriter = csv.writer(csvfile)
    contractAnnouncementsWriter.writerow(['url_id', 'announcement', 'date'])
    for item in press_releases:
        contractAnnouncementsWriter.writerow([item.url_id, item.announcement, item.date])
