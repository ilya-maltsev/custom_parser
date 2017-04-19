import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import lxml.html as html
import codecs
import re
import time
import MySQLdb

main_domain = 'http://domain.ru'
page = '/Web.aspx?node=currentorders&tso=1&tsl=1&sbflag=0&pubdates=20160101&pubdatef=20161231&pform=e&page='
pages = []
db = MySQLdb.connect(host="localhost", user="root", passwd="passwd", db="proc", charset='utf8')
cursor = db.cursor()
for i in range(1,79):
    s_page = html.parse('%s%s' % (main_domain, page + str(i)))
    e = s_page.getroot().find_class('table-lots-list').pop()
    desc = e.xpath("//td[@class=\'description\']//p//a")
    ids = []
    for href in desc:
        m = re.search('href="(.+?)"', html.tostring(href))
        if m:
            found = m.group(1)
            ids.append(found)
    for id in ids:
        p_page = html.parse('%s%s' % (main_domain, id))
        p_table = p_page.xpath("//table[@id=\'table_01\']//text()")
        date = p_page.xpath("//div[@class=\'printed\']//text()")
        if len(date) > 0:
            p = re.search(' (\d+.\d+.\d+?)\.', date[0].encode('utf8'))
        p_date = '0'
        p_index = '0'
        p_name =  '0'
        p_e =  '0'
        p_link = '0'
        p_o_index = '0'
        if p:
            p_date = p.group(1)
        if len(p_table) > 2:
            p_index = p_table[2]
        if len(p_table) > 4:
            p_name = p_table[5]
        if len(p_table) > 28:
            p_e = p_table[29]
        if len(p_table) > 31:
            p_link = p_table[32]
        if len(p_table) > 35:
          p_o_index = p_table[35]
        sql = """INSERT INTO 2016 (p_index,p_date,p_e,p_link,p_o_index) VALUES ('%(p_index)s', '%(p_date)s','%(p_e)s', '%(p_link)s', '%(p_o_index)s') """%{"p_index":p_index,"p_date":p_date, "p_e":p_e, "p_link":p_link, "p_o_index":p_o_index}
        cursor.execute(sql)
        db.commit()
        time.sleep(1)

db.close()
