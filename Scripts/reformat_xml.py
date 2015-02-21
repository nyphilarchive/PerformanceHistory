#import modules
import codecs
import re
import string
import xml.etree.ElementTree as ET

#create xml element
tree = ET.parse('../Programs/complete.xml')
root = tree.getroot()

#create new xml file
f = codecs.open('../Programs/complete_with_works_subdivided.xml','w','utf-8')
f.write('<?xml version="1.0" encoding="utf-8"?>\n\n')

#separate composer and work into two elements
def separateComposerWork(composerAndWork):
    composer = re.sub(r'(.*?) /.*',r'\1',composerAndWork)
    work = re.sub(r'.*?/ (.*)',r'\1',composerAndWork)
    return composer, work

#remove extra spaces at front of soloist info
def fixSpaces(text):
    if re.match(r'  ',text):
        fixed_text = re.sub(r'  (\w.*)',r'\1',text)
    elif re.match(r' ',text):
        fixed_text = re.sub(r' (\w.*)',r'\1',text)
    else:
        fixed_text = text
    return fixed_text

#separate soloist lists into separate individuals (and instruments and roles)
def sortSoloistInfo(soloists,soloist_instruments,soloist_roles):
    if re.search(r';',soloists):
        try:
            soloists_list = string.split(soloists,";")
            soloist_instruments_list = string.split(soloist_instruments,";")
            soloist_roles_list = string.split(soloist_roles,";")
            for x in range(0,len(soloists_list)):
                f.write("                    <soloist>\n")
                f.write("                        <soloistName>%s</soloistName>\n"%fixSpaces(soloists_list[x]))
                f.write("                        <soloistInstrument>%s</soloistInstrument>\n"%fixSpaces(soloist_instruments_list[x]))
                f.write("                        <soloistRoles>%s</soloistRoles>\n"%fixSpaces(soloist_roles_list[x]))
                f.write("                    </soloist>\n")
        except:
            f.write("                    <soloist>\n")
            f.write("                        <soloistName>%s</soloistName>\n"%soloists)
            f.write("                        <soloistInstrument>%s</soloistInstrument>\n"%soloist_instruments)
            f.write("                        <soloistRoles>%s</soloistRoles>\n"%soloist_roles)
            f.write("                    </soloist>\n")
    else:
        f.write("                    <soloist>\n")
        f.write("                        <soloistName>%s</soloistName>\n"%soloists)
        f.write("                        <soloistInstrument>%s</soloistInstrument>\n"%soloist_instruments)
        f.write("                        <soloistRoles>%s</soloistRoles>\n"%soloist_roles)
        f.write("                    </soloist>\n")
        
#reprint the unchanged entities
def standardItems(p):
    f.write("        <id>%s<\id>\n"%p.find('id').text)
    f.write("        <programID>%s<\programID>\n"%p.find('programID').text)
    f.write("        <orchestra>%s</orchestra>\n"%p.find('orchestra').text)
    f.write("        <season>%s</season>\n"%p.find('season').text)
    
#reprint unchanged concert info entities
def concertInfo(c):
    f.write("            <eventType>%s</eventType>\n"%c.find('eventType').text)
    f.write("            <Location>%s</Location>\n"%c.find('Location').text)
    f.write("            <Venue>%s</Venue>\n"%c.find('Venue').text)
    f.write("            <Date>%s</Date>\n"%c.find('Date').text)
    f.write("            <Time>%s</Time>\n"%c.find('Time').text)
    
#reorder worksInfo children into works, each with conductor, composer, title, and soloists (if applicable)
def sortWorksInfo(works):
    conductors = works.findall('worksConductorName')
    composerAndWork = works.findall('worksComposerTitle')
    soloists = works.findall('worksSoloistName')
    soloist_instruments = works.findall('worksSoloistInstrument')
    soloist_roles = works.findall('worksSoloistRole')
    for x in range(0,len(conductors)):
        composer_work_separated = separateComposerWork(composerAndWork[x].text)
        f.write("            <work>\n")
        if re.match(r'Intermission',composer_work_separated[0]):
            f.write("                <interval>%s</interval>\n"%composer_work_separated[0][:-1])
        else:
            if composer_work_separated[0]:
                f.write("                <composerName>%s</composerName>\n"%composer_work_separated[0])
            if composer_work_separated[1]:
                f.write("                <workTitle>%s</workTitle>\n"%composer_work_separated[1])
            if conductors[x].text:
                f.write("                <conductorName>%s</conductorName>\n"%conductors[x].text)
            try:
                if soloists[x].text:
                    f.write("                <soloists>\n")
                    sortSoloistInfo(soloists[x].text,soloist_instruments[x].text,soloist_roles[x].text)
                    f.write("                </soloists>\n")
            except:
                pass
        f.write("            </work>\n")
        
        
#parse xml file and write new output, per functions above
programs = root.findall('doc')

f.write("<programs>\n")

for p in programs:
    f.write("    <program>\n")
    standardItems(p)
    for c in p.findall('concertInfo'):
        f.write("        <concertInfo>\n")
        concertInfo(c)
        f.write("        </concertInfo>\n")
    f.write("        <worksInfo>\n")
    sortWorksInfo(p.find('worksInfo'))
    f.write("        </worksInfo>\n")
    f.write("    </program>\n")

f.write("</programs>")
f.close()
