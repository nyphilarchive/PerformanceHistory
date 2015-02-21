#import modules
import re
from collections import Counter
import xml.etree.ElementTree as ET

#create xml collection of "docs" (i.e., programs in NYPhil's definition)
tree = ET.parse('../Programs/complete.xml')
root = tree.getroot()
concerts = root.findall('doc')

#gather info from XML file
pre = []
post = []


for c in concerts:
    works = c.findall('.//worksComposerTitle')
    for n, work in enumerate(works):
        if re.match('Intermission',work.text):
            try:
                pre.append(works[n-1].text)
            except:
                pass
            try:
                post.append(works[n+1].text)
            except:
                pass
        else:
            pass

collected_pre = Counter(pre)
collected_post = Counter(post)

print collected_pre.most_common()[0:5]
print collected_post.most_common()[0:5]

