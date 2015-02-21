#import modules
import codecs
import re
import string
import xml.etree.ElementTree as ET

#create xml element
tree = ET.parse('complete.xml')
root = tree.getroot()

#create new xml file
f = codecs.open('complete_with_works_subdivided.xml','w','utf-8')
f.write("<?xml version="1.0" encoding="utf-8"?>\n\n")

#separate composer and work into two elements
def separateComposerWork(composerAndWork):
    composer = re.sub(r'(.*?) /.*',r'\1',composerAndWork)
    work = re.sub(r'.*?/ (.*)',r'\1',composerAndWork)
    return composer, work

#separate soloist lists into separate individuals (and instruments and roles)
def sortSoloistInfo(soloists,soloist_instruments,soloist_roles):
    if re.search(r';',soloists):
        try:
            soloists_list = string.split(soloists,";")
            soloist_instruments_list = string.split(soloist_instruments,";")
            soloist_roles_list = string.split(soloist_roles,";")
            for x in range(0,len(soloists_list)):
                f.write("\t\t\t\t<soloist>\n")
                f.write("\t\t\t\t\t<soloistName>%s</soloistName>\n"%soloists_list[x])
                f.write("\t\t\t\t\t<soloistInstrument>%s</soloistInstrument>\n"%soloist_instruments_list[x])
                f.write("\t\t\t\t\t<soloistRoles>%s</soloistRoles>\n"%soloist_roles_list[x])
                f.write("\t\t\t\t</soloist>\n")
        except:
            f.write("\t\t\t\t<soloist>\n")
            f.write("\t\t\t\t\t<soloistName>%s</soloistName>\n"%soloists)
            f.write("\t\t\t\t\t<soloistInstrument>%s</soloistInstrument>\n"%soloist_instruments)
            f.write("\t\t\t\t\t<soloistRoles>%s</soloistRoles>\n"%soloist_roles)
            f.write("\t\t\t\t</soloist>\n")
    else:
        f.write("\t\t\t\t<soloist>\n")
        f.write("\t\t\t\t\t<soloistName>%s</soloistName>\n"%soloists)
        f.write("\t\t\t\t\t<soloistInstrument>%s</soloistInstrument>\n"%soloist_instruments)
        f.write("\t\t\t\t\t<soloistRoles>%s</soloistRoles>\n"%soloist_roles)
        f.write("\t\t\t\t</soloist>\n")
        
#reprint the unchanged entities
def standardItems(p):
    f.write("\t<id>%s<\id>\n"%p.find('id').text)
    f.write("\t<programID>%s<\programID>\n"%p.find('programID').text)
    f.write("\t<orchestra>%s</orchestra>\n"%p.find('orchestra').text)
    f.write("\t<season>%s</season>\n"%p.find('season').text)
    
#reprint unchanged concert info entities
def concertInfo(c):
    f.write("\t\t<eventType>%s</eventType>\n"%c.find('eventType').text)
    f.write("\t\t<Location>%s</Location>\n"%c.find('Location').text)
    f.write("\t\t<Venue>%s</Venue>\n"%c.find('Venue').text)
    f.write("\t\t<Date>%s</Date>\n"%c.find('Date').text)
    f.write("\t\t<Time>%s</Time>\n"%c.find('Time').text)
    
#reorder worksInfo children into works, each with conductor, composer, title, and soloists (if applicable)
def sortWorksInfo(works):
    conductors = works.findall('worksConductorName')
    composerAndWork = works.findall('worksComposerTitle')
    soloists = works.findall('worksSoloistName')
    soloist_instruments = works.findall('worksSoloistInstrument')
    soloist_roles = works.findall('worksSoloistRole')
    for x in range(0,len(conductors)):
        composer_work_separated = separateComposerWork(composerAndWork[x].text)
        f.write("\t\t<work>\n")
        if re.match(r'Intermission',composer_work_separated[0]):
            f.write("\t\t\t<interval>%s</interval>\n"%composer_work_separated[0][:-1])
        else:
            if composer_work_separated[0]:
                f.write("\t\t\t<composerName>%s</composerName>\n"%composer_work_separated[0])
            if composer_work_separated[1]:
                f.write("\t\t\t<workTitle>%s</workTitle>\n"%composer_work_separated[1])
            if conductors[x].text:
                f.write("\t\t\t<conductorName>%s</conductorName>\n"%conductors[x].text)
            try:
                if soloists[x].text:
                    f.write("\t\t\t<soloists>\n")
                    sortSoloistInfo(soloists[x].text,soloist_instruments[x].text,soloist_roles[x].text)
                    f.write("\t\t\t</soloists>\n")
            except:
                pass
        f.write("\t\t</work>\n")
        
        
#parse xml file and write new output, per functions above
programs = root.findall('doc')

f.write("<programs>\n")

for p in programs:
    f.write("<program>\n")
    standardItems(p)
    for c in p.findall('concertInfo'):
        f.write("\t<concertInfo>\n")
        concertInfo(c)
        f.write("\t</concertInfo>\n")
    f.write("\t<worksInfo>\n")
    sortWorksInfo(p.find('worksInfo'))
    f.write("\t</worksInfo>\n")
    f.write("</program>\n")

f.write("</programs>")
f.close()
