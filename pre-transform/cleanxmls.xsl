<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<!-- KS 20160825: added tests to add null values for various fields, based on messy or weird input data, so that the python script works properly -->
<!-- KS 20160825: Someday, consider making this a purely XSLT solution, as the needs of the Python script muddy the waters. -->
<!-- KS 20160907: added patch to remove soloists from 13715  -->

<!-- output XML indended for readability -->
<xsl:output method="xml" indent="yes" />

<!-- Within this template, call "StringSplit" templates for any fields that repeat. -->
<xsl:template name="WritePropertyNodeTemplate" match="/response/result">

<programs>

<!-- Sort by folder ID for easier debugging -->
<xsl:for-each select="doc">
<!-- Start listing fields.  For fields that never repeat, just list the field with mapping.  Otherwise, call "StringSplit" template -->
<doc>

<id><xsl:value-of select="str[@name='id']" /></id>
<programID><xsl:value-of select="str[@name='npp:ProgramID']" /></programID>
<orchestra><xsl:value-of select="arr[@name='npp:OrchestraName']/str" /></orchestra>
<season><xsl:value-of select="str[@name='npp:Season']" /></season>

<xsl:for-each select="arr[@name='npp:Date']/date">
<xsl:variable name="index" select="position()"></xsl:variable>
<concertInfo>
	<eventType><xsl:value-of select="../../arr[@name='npp:SubEventName']/str[$index]" /></eventType>
	<Location><xsl:value-of select="../../arr[@name='npp:LocationName']/str[$index]" /></Location>
	<Venue><xsl:value-of select="../../arr[@name='npp:VenueName']/str[$index]" /></Venue>
	<Date><xsl:value-of select="../../arr[@name='npp:Date']/date[$index]" /></Date>
	<Time><xsl:value-of select="../../arr[@name='npp:Time']/str[$index]" /></Time>
</concertInfo>
</xsl:for-each>

<worksInfo>

<xsl:for-each select="arr[@name='npp:WorksMovIDs']/str">
<workID>
 	<xsl:value-of select="." />
</workID>
</xsl:for-each>

<!-- added test to provide null worksConductorName if no worksConductor in data, to fix the ~130 Carlos items where this happens, whether correctly or not KS 20160825 -->

<xsl:choose>

<xsl:when test="arr[@name='npp:WorksConductorNames']/str">
	<xsl:for-each select="arr[@name='npp:WorksConductorNames']/str">
		<worksConductorName>
 			<xsl:value-of select="." />
 		</worksConductorName>
	</xsl:for-each>
</xsl:when>

<xsl:otherwise>
	<worksConductorName/>
</xsl:otherwise>

</xsl:choose>

<xsl:for-each select="arr[@name='npp:ComposerWorksTitle_facet']/str">
<worksComposerTitle>
	<xsl:value-of select="." />
</worksComposerTitle>
</xsl:for-each>

<xsl:for-each select="arr[@name='npp:ProgramWorksIDs']/str">
<movementID>
		<xsl:if test="substring(., string-length(.)) != '*'">
			<xsl:value-of select="substring(., string-length(.))" /> 
		</xsl:if>
</movementID>
</xsl:for-each>

<!-- added test for WorksTitle; if none, use short workstitle and add blank worksmovement for each, if none at all, add one blank works movement KS 20160825 -->

<xsl:choose>
<xsl:when test="arr[@name='npp:WorksTitle']/str">
<xsl:for-each select="arr[@name='npp:WorksTitle']/str">
<!-- Insert if test for | ; if there is a |, do it, otherwise put in a blank worksMovement KS 20160824 -->
	<xsl:choose>
		<xsl:when test="contains(., '|')">
<worksMovement>
	<xsl:value-of select="substring-after(.,' | ')" />
</worksMovement>
		</xsl:when>
		<xsl:otherwise>
			<worksMovement></worksMovement>			
		</xsl:otherwise>
	</xsl:choose>
</xsl:for-each>
</xsl:when>

<xsl:otherwise>
	<xsl:choose>
	<xsl:when test="arr[@name='npp:WorksShortTitle']/str">
	<xsl:for-each select="arr[@name='npp:WorksShortTitle']/str">
		<worksMovement></worksMovement>		
	</xsl:for-each>	
	</xsl:when>
<xsl:otherwise>
<!-- 2nd test inserted to add blank worksMovement for chamber concerts and talks when there is legit no works -->
	<worksMovement></worksMovement>		
</xsl:otherwise>

	</xsl:choose>
</xsl:otherwise>

</xsl:choose>

<xsl:choose>
<xsl:when test="str[@name='id']='73800337-b5e9-42a1-be41-22b4f9108115'">
<!-- DO NOTHING -->
</xsl:when>
<xsl:otherwise>

<xsl:for-each select="arr[@name='npp:WorksSoloistNames']/str">
<worksSoloistName>
	<xsl:value-of select="." />
</worksSoloistName>
</xsl:for-each>

<xsl:for-each select="arr[@name='npp:WorksSoloistInstrumentNames']/str">
<worksSoloistInstrument>
	<xsl:value-of select="." />
</worksSoloistInstrument>
</xsl:for-each>

<xsl:for-each select="arr[@name='npp:WorksSoloistFunction']/str">
<worksSoloistRole>
	<xsl:value-of select="." />
</worksSoloistRole>
</xsl:for-each>

</xsl:otherwise>
</xsl:choose>

</worksInfo>
</doc>
</xsl:for-each>
</programs>

</xsl:template>


</xsl:stylesheet>
