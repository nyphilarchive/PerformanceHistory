# New York Philharmonic Performance History
Since its first concert on December 7, 1842, the New York Philharmonic has been keeping records of all its performances which now add up to almost 16,000. Each concert has been cataloged in the Philharmonic's [Performance History database](http://archives.nyphil.org/performancehistory) in great detail. The [Leon Levy Digital Archives](http://archives.nyphil.org), provides an additional interface for searching performances alongside other digitized items such as marked music scores, marked orchestral parts, business records, and photos.

In an effort to make this data available for study, analysis, and reuse, the Philharmonic joins organizations like the [Tate](https://github.com/tategallery/collection) and the <a href="http://www.cooperhewitt.org/">Cooper Hewitt</a> in making its own contribution to the Open Data movement.

The metadata here is released under the Creative Commons Public Domain [CC0](http://creativecommons.org/publicdomain/zero/1.0/) licence. Please see the enclosed LICENCE file for more detail.

##Considerations
* A **program** is one or more performances close together in which the same **repertoire**, **conductors**, and **soloists** are EXACTLY the same.
* At this time, movement names are not included (we're working on it). In cases where several specific movements are performed rather than the complete work, the work title will be repeated in the data.
* To see detailed information about our internal descriptive standards, please go to http://nyphil.org/history/performance-history/help.

##Repository Contents
The data is currently available as XML only, though we hope to provide JSON in the future.
In the *Programs* directory, you will find a series of XML files. The file called complete.xml contains every program from December 7, 1842 to the present (it's possible that it could take up to a week for the latest program to be included). The other files are named with document ranges, for no other reason than to make it easier to work with the data. Each file contains 1,000 records and is sorted by date ascending.

The XML is structured in the following way:

```
<programs>
   <doc>
      <id/> // GUID
      <programID/> // NYP Local ID
      <orchestra/>
      <season/>  
      <concertInfo> // A program can have multiple concerts
         <eventType/>
         <Location/>
         <Venue/>
         <Date/>
         <Time/>
      </concertInfo>
      <worksInfo> // each field below is repeated for each work
         <worksConductorName/>     
         <worksComposerTitle/>
         <worksSoloistName/>
         <worksSoloistInstrument/>         
      </worksInfo>
   </doc>
</programs>
```
<table>
	<tr>
		<th>Field</th><th>Description</th>
	</tr>
	<tr>
		<td colspan=2>General Info: Info that applies to entire program</td>
	</tr>
	<tr>
		<td>id</td><td>GUID (`To view program: http://archives.nyphil.org/index.php/artifact/**[GUID]**/fullview`)</td>
	</tr>
	<tr>
		<td>ProgramID</td><td>Local NYP ID</td>
	</tr>
	<tr>
		<td>Orchestra</td><td>Full orchestra name <a href="http://nyphil.org/history/performance-history/help">Learn more...</a></td>
	</tr>
	<tr>
		<td>Season</td><td>Defined as Sep 1 - Aug 31, displayed "1842-43"</td>
	</tr>
	<tr>
		<td colspan=2>Concert Info: Repeated for each individual performance within a program</td>
	</tr>
	<tr>
		<td>eventType</td><td><a href="http://nyphil.org/history/performance-history/help">See term definitions</a></td>
	</tr>
	<tr>
		<td>Location</td><td>Geographic location of concert</td>
	</tr>
	<tr>
		<td>Venue</td><td>Name of hall, theater, or building where the concert took place</td>
	</tr>
	<tr>
		<td>Date</td><td>Full ISO date used, but ignore TIME part (1842-12-07T05:00:00Z = Dec. 7, 1842)</td>
	</tr>
	<tr>
		<td>Time</td><td>Actual time of concert, e.g. "8:00PM"</td>
	</tr>
	<tr>
		<td colspan=2>Works Info: the fields below are repeated for each work performed on a program. By matching the index number of each field, you can tell who the soloist(s) and conductor(s) performed a specific work on each of the concerts listed above.</td>
	</tr>
	<tr>
		<td>WorksConductorName</td><td>Last name, first name</td>
	</tr>
	<tr>
		<td>worksComposerTitle</td><td>Composer Last name, first / TITLE (NYP works titles used)</td>
	</tr>
	<tr>
		<td>worksSoloistName</td><td>Last name, first name (if multiple soloists on a single work, delimited by semicolon)</td>
	</tr>
	<tr>
		<td>worksSoloistInstrument</td><td>Last name, first name (if multiple soloists on a single work, delimited by semicolon)</td>

</table>


##Usage Guidelines

These usage guidelines are based on goodwill, they are not a legal contract but the New York Philharmonic requests that you follow these guidelines if you use Metadata from our Performance History dataset.

The Metadata published by the New York Philharmonic is available free of restrictions under the Creative Commons Zero Public Domain Dedication http://creativecommons.org/publicdomain/zero/1.0/

This means that you can use it for any purpose without having to give attribution. However, the New York Philharmonic requests that you actively acknowledge and give attribution to the New York Philharmonic. Attribution supports future efforts to release other data.

**Give credit where credit is due.**

**Give attribution to the New York Philharmonic.**

Make sure that others are aware of the rights status of the the New York Philharmonic Metadata and are aware of these guidelines by keeping intact links to the CC0 Public Domain Dedication.

If for technical or other reasons you cannot include all the links to all sources of the Metadata and rights information directly with the Metadata, you should consider including them separately, for example in a separate document that is distributed with the Metadata or dataset.

If for technical or other reasons you cannot include all the links to all sources of the Metadata and rights information, you may consider linking only to the Metadata source on the New York Philharmonic GitHub page, where all available sources and rights information can be found, including in machine readable formats.

**Metadata is dynamic**

When working with Metadata obtained from the New York Philharmonic be aware that this Metadata is not static, it changes. the New York Philharmonic continuously updates its Metadata in order to correct mistakes and include new and additional information. As performances take place, the New York Philharmonic will aim to update its Performance History Metadata at regular intervals.

**Mention your modifications of the Metadata and contribute your modified Metadata back.**

Whenever you transform, translate or otherwise modify the Metadata, make it clear that the resulting Metadata has been modified by you. If you enrich or otherwise modify Metadata, consider publishing the derived Metadata without reuse restrictions, preferably via the Creative Commons Zero Public Domain Dedication.

**Be responsible.**

Ensure that you do not use the Metadata in a way that suggests any official status or that the New York Philharmonic endorses you or your use of the Metadata, unless you have prior permission to do so.

**Ensure that you do not mislead others or misrepresent the Metadata or its sources.**

Ensure that your use of the Metadata does not breach any national legislation based thereon, notably concerning (but not limited to) data protection, defamation or copyright.

**Please note that you use the Metadata at your own risk.**

the New York Philharmonic offers the Metadata as-is and makes no representations or warranties of any kind concerning any Metadata published by the New York Philharmonic.

The writers of these guidelines are deeply indebted to the [Tate](http://www.tate.org.uk), the [Smithsonian Cooper-Hewitt, National Design Museum](http://www.cooperhewitt.org/), and [Europeana](http://europeana.eu/).
