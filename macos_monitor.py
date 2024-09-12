# __author__ = 'Eric Jiang'
# -*- coding: utf-8 -*-

import requests
import sqlite3
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


def wiki_macos():
    # init sqlite
    conn = sqlite3.connect('macos_version.db')
    cursor = conn.cursor()
    cursor.execute("create table if not exists macos_wiki (version TEXT, build TEXT, release_time TEXT)")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }
    release_url = [
        'https://en.wikipedia.org/wiki/MacOS_Big_Sur',
        'https://en.wikipedia.org/wiki/MacOS_Monterey',
        'https://en.wikipedia.org/wiki/MacOS_Ventura',
        'https://en.wikipedia.org/wiki/MacOS_Sonoma',
        'https://en.wikipedia.org/wiki/MacOS_Sequoia'
    ]
    for url in release_url:
        result = requests.get(url, headers=headers)
        html = BeautifulSoup(result.text, 'html.parser')
        # Version Table in this wiki page is the fourth table now, may be changed in the future
        if url == 'https://en.wikipedia.org/wiki/MacOS_Big_Sur':
            version_table = html.find_all('table')[4]
        elif url == 'https://en.wikipedia.org/wiki/MacOS_Sequoia':
            version_table = html.find_all('table')[2]
        else:
            version_table = html.find_all('table')[3]
        # list the rows in Version Table, exclude first header row
        rows = version_table.findChildren('tr')[1:]
        for row in rows:
            # list the first 3 columns in Version Table
            cells = row.findChildren(['th', 'td'])[:3]
            version_list = []
            if len(cells) == 3:
                version_list.append(cells[0].text.strip())
                version_list.append(cells[1].text.strip())
                version_list.append(cells[2].text.strip())
                cursor.execute("select count(*) from macos_wiki where version=?", (version_list[0],))
                print(version_list)
                count = cursor.fetchone()[0]
                if count == 0:
                    cursor.execute("insert into macos_wiki (version, build, release_time) values (?, ?, ?)", (version_list[0], version_list[1], version_list[2]))
                    send_mail(version_list)
    cursor.close()
    conn.commit()
    conn.close()


def send_mail(version_list):
    mail_body = "Dears,\n\n" \
                "There is a new version of MacOS, kindly check it from following page.\n" \
                "    > [Wiki macOS15] https://en.wikipedia.org/wiki/MacOS_Sequoia\n" \
                "    > [Wiki macOS14] https://en.wikipedia.org/wiki/MacOS_Sonoma\n" \
                "    > [Wiki macOS13] https://en.wikipedia.org/wiki/MacOS_Ventura\n" \
                "    > [Wiki macOS12] https://en.wikipedia.org/wiki/MacOS_Monterey\n" \
                "    > [Wiki macOS11] https://en.wikipedia.org/wiki/MacOS_Big_Sur\n" \
                "    > [Apple] https://developer.apple.com/documentation/macos-release-notes#topics\n" \
                "You can try to download install package from  https://mrmacintosh.com\n\n" \
                "Have a good one."
    # Configuration1
    mailFrom = ''
    # Configuration2
    mailTo = []
    msg = MIMEText(mail_body)
    msg['From'] = mailFrom
    msg['To'] = ','.join(mailTo)
    msg['Subject'] = '⏰ MacOS New Version [%s][%s] Release' % (version_list[0], version_list[1])
    # Configuration3
    s = smtplib.SMTP('')
    s.sendmail(mailFrom, mailTo, msg.as_string())
    s.close()


if __name__ == '__main__':
    wiki_macos()
