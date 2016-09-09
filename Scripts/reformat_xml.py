# import modules
import codecs
import re
import string
import xml.etree.ElementTree as ET
import os
import os.path

# KS 20160825: modified to add test for cases when the number of conductors, works, and composers in the input XML is unequal; in that case, it skips the worksInfo section. Will need to consider chamber works
# os.chdir('C:/Users/schlottmannk/Desktop/pythonDebug/xml') used for debug 
# KS 20160909: used re.split instead of str.plit for soloists, as non-ascii characters were not hitting on semincolons for some reason

# create xml element
os.chdir('i:/Archives Digitization Project/PerformanceHistoryRepo/PerformanceHistory/Programs/xml')

files = [g for g in os.listdir('.') if os.path.isfile(g)]
for g in files:
    tree = ET.parse(g)
    root = tree.getroot()

    #create list of lines for new file (kludge to solve ampersand escaping
    lines = []

    # separate composer and work into two elements
    def separateComposerWork(composerAndWork):
        composer = re.sub(r'(.*?) /.*',r'\1',composerAndWork)
        work = re.sub(r'.*?/ (.*)',r'\1',composerAndWork)
        return composer, work

    # remove extra spaces at front of soloist info
    def fixSpaces(text):
        if re.match(r'  ',text):
            fixed_text = re.sub(r'  (\w.*)',r'\1',text)
        elif re.match(r' ',text):
            fixed_text = re.sub(r' (\w.*)',r'\1',text)
        else:
            fixed_text = text
        return fixed_text

    # separate soloist lists into separate individuals (and instruments and roles)
    def sortSoloistInfo(soloists,soloist_instruments,soloist_roles):
        if re.search(r';',soloists):
            try:
                soloists_list = re.split('; ', soloists)
                soloist_instruments_list = str.split(soloist_instruments,";")
                soloist_roles_list = str.split(soloist_roles,";")
                for x in range(0,len(soloists_list)):
                    lines.append("                    <soloist>\n")
                    lines.append("                        <soloistName>%s</soloistName>\n"%fixSpaces(soloists_list[x]))
                    lines.append("                        <soloistInstrument>%s</soloistInstrument>\n"%fixSpaces(soloist_instruments_list[x]))
                    lines.append("                        <soloistRoles>%s</soloistRoles>\n"%fixSpaces(soloist_roles_list[x]))
                    lines.append("                    </soloist>\n")
            except:
                lines.append("                    <soloist>\n")
                lines.append("                        <soloistName>%s</soloistName>\n"%soloists)
                lines.append("                        <soloistInstrument>%s</soloistInstrument>\n"%soloist_instruments)
                lines.append("                        <soloistRoles>%s</soloistRoles>\n"%soloist_roles)
                lines.append("                    </soloist>\n")
        else:
            lines.append("                    <soloist>\n")
            lines.append("                        <soloistName>%s</soloistName>\n"%soloists)
            lines.append("                        <soloistInstrument>%s</soloistInstrument>\n"%soloist_instruments)
            lines.append("                        <soloistRoles>%s</soloistRoles>\n"%soloist_roles)
            lines.append("                    </soloist>\n")

    # reprint the unchanged entities
    def standardItems(p):
        lines.append("        <id>%s</id>\n"%p.find('id').text)
        lines.append("        <programID>%s</programID>\n"%p.find('programID').text)
        lines.append("        <orchestra>%s</orchestra>\n"%p.find('orchestra').text)
        lines.append("        <season>%s</season>\n"%p.find('season').text)

    # reprint unchanged concert info entities
    def concertInfo(c):
        lines.append("            <eventType>%s</eventType>\n"%c.find('eventType').text)
        lines.append("            <Location>%s</Location>\n"%c.find('Location').text)
        lines.append("            <Venue>%s</Venue>\n"%c.find('Venue').text)
        lines.append("            <Date>%s</Date>\n"%c.find('Date').text)
        lines.append("            <Time>%s</Time>\n"%c.find('Time').text)

    # reorder worksInfo children into works, each with conductor, composer, title, and soloists (if applicable)
    def sortWorksInfo(works):
        conductors = works.findall('worksConductorName')
        composerAndWork = works.findall('worksComposerTitle')
        movement = works.findall('worksMovement')
        soloists = works.findall('worksSoloistName')
        soloist_instruments = works.findall('worksSoloistInstrument')
        soloist_roles = works.findall('worksSoloistRole')
        work_id = works.findall('workID')
        movement_id = works.findall('movementID')
        #insert test to skip if conductors, composerAndWork, and movement do not add up
        try:
            if ((len(conductors) == len(composerAndWork)) and (len(composerAndWork) == len(movement))):
                for x in range(0,len(conductors)):
                    composer_work_separated = separateComposerWork(composerAndWork[x].text)
                    lines.append("            <work ID=\"%s\">\n"%work_id[x].text)
                    if re.match(r'Intermission',composer_work_separated[0]):
                        lines.append("                <interval>%s</interval>\n"%composer_work_separated[0][:-1])
                    else:
                        if composer_work_separated[0]:
                            lines.append("                <composerName>%s</composerName>\n"%composer_work_separated[0])
                        if composer_work_separated[1]:
                            lines.append("                <workTitle>%s</workTitle>\n"%composer_work_separated[1])
                        if movement[x].text:
                            lines.append("                <movement>%s</movement>\n"%movement[x].text)
                        if conductors[x].text:
                            lines.append("                <conductorName>%s</conductorName>\n"%conductors[x].text)
                        try:
                            if soloists[x].text:
                                lines.append("                <soloists>\n")
                                sortSoloistInfo(soloists[x].text, soloist_instruments[x].text,soloist_roles[x].text)
                                lines.append("                </soloists>\n")
                        except:
                            pass
                    lines.append("            </work>\n")
                #insert except pass here - output blank worksInfo if test above fails
        except:
                pass

    # parse xml file and write new output, per functions above
    programs = root.findall('doc')

    lines.append("<programs>\n")

    for p in programs:
        lines.append("    <program>\n")
        standardItems(p)
        for c in p.findall('concertInfo'):
            lines.append("        <concertInfo>\n")
            concertInfo(c)
            lines.append("        </concertInfo>\n")
        lines.append("        <worksInfo>\n")
        sortWorksInfo(p.find('worksInfo'))
        lines.append("        </worksInfo>\n")
        lines.append("    </program>\n")

    lines.append("</programs>")

    # create new xml file
    f = codecs.open(g, 'w','utf-8')
    f.write('<?xml version="1.0" encoding="utf-8"?>\n\n')
    for l in lines:
        l = re.sub(r'&', r'&amp;', l)
        f.write(l)
    f.close()
