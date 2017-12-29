# New York Philharmonic Performance History
The New York Philharmonic played its first concert on December 7, 1842. Since then, it has merged with the New York Symphony, the New/National Symphony, and had a long-running summer season at New York's Lewisohn Stadium. This [Performance History database](http://archives.nyphil.org/performancehistory) documents all known concerts of all of these organizations, amounting to more than 20,000 performances. The [New York Philharmonic Leon Levy Digital Archives](http://archives.nyphil.org) provides an additional interface for searching printed programs alongside other digitized items such as marked music scores, marked orchestral parts, business records, and photos.

In an effort to make this data available for study, analysis, and reuse, the New York Philharmonic joins organizations like [The Tate](https://github.com/tategallery/collection) and the <a href="http://www.cooperhewitt.org/">Cooper-Hewitt Smithsonian National Design Museum</a> in making its own contribution to the Open Data movement.

The metadata here is released under the Creative Commons Public Domain [CC0](http://creativecommons.org/publicdomain/zero/1.0/) licence. Please see the enclosed LICENCE file for more detail.

##Considerations
* A **program** is defined as one or more performances or presentations in which the same **repertoire**, **conductors**, and **soloists** are EXACTLY the same (dates, times, locations may vary within). For example, if a soloist plays an encore one night but not another, the concert with the encore becomes a different program.
* ~~Only complete titles are included. If an excerpt or movement is performed, this will not be indicated in the database at this time. We are working to include this in the near future.~~ Movements are now included as cataloged by NYP. Keep in mind that we do not necessarily catalog every movement in the work, only movements that we have ever performed.
* To see detailed information about our internal descriptive standards, please go to http://archives.nyphil.org/index.php/help-performancehistory.

##Repository Contents
The data is currently available as both XML and JSON.  In the *Programs* directory, you will find two directories, `xml` and `json`, each with a series of XML. The file called complete.xml (and complete.json) contains every concert from December 7, 1842 to the present (it's possible that it could take up to a week for the latest program to be included). To allow for easier downloading and use, also available are segmented files determined by date ranges (each segment contains about 1,000 records).

The XML is structured in the following way:

```
<programs>
   <program>
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
      <worksInfo> // a program will usually have multiple works 
         <work ID=""> // e.g. "1234*1" - first part is the Work ID, second part is the NYP Movement ID
             <composerName/>
             <workTitle/>
             <movement/>
             <conductorName/>     
             <soloists> // included only if there are listed soloists
                <soloist>
                    <soloistName/>
                    <soloistInstrument/> 
                    <soloistRole/>   		 
                </soloist>
             </soloists>
             <interval/> // intermissions are listed among works, but with a distinct interval tag
         </work>
      </worksInfo>
   </program>
</programs>
```

The JSON is formatted almost the same, with a few small differences in
naming:

```
{
  "programs": [
    {
      "id": "38e072a7-8fc9-4f9a-8eac-3957905c0002", // GUID
      "programID": "3853", // NYP Local ID
      "orchestra": "New York Philharmonic",
      "season": "1842-43",
      "concerts": [
        {
           "eventType": "Subscription Season",
           "Location": "Manhattan, NY",
           "Venue": "Apollo Rooms",
           "Date": "1842-12-07T05:00:00Z",
           "Time": "8:00PM"
        },
        /* A program can have multiple concerts */
      ],
      "works": [
        {
          "ID": "8834*4", // e.g. "1234*1" - first part is the Work ID, second part is the NYP Movement ID
          "composerName": "Weber,  Carl  Maria Von",
          "workTitle": "OBERON",
          "movement": "\"Ozean, du Ungeheuer\" (Ocean, thou mighty monster), Reiza (Scene and Aria), Act II",
          "conductorName": "Timm, Henry C.",
          "soloists": [
            {
              "soloistName": "Otto, Antoinette",
              "soloistInstrument": "Soprano",
              "soloistRoles": "S"
            },
            /* more soloists, if applicable. If no soloists, this will be an empty array */
          ]
        },
        /* a program will usually have multiple works */
        {
          "ID": "0*",
          "interval": "Intermission",
          "soloists": []
        },
        /* Intermissions will also appear in the works array */
      ]
    },
    /* more programs */
  ]
}
```

<table>
	<tr>
		<th>Field</th><th>Description</th>
	</tr>
	<tr>
		<td colspan=2><strong>General Info: Info that applies to entire program</strong></td>
	</tr>
	<tr>
		<td>id</td><td>GUID (To view program: archives.nyphil.org/index.php/artifact/<strong>GUID</strong>/fullview)</td>
	</tr>
	<tr>
		<td>ProgramID</td><td>Local NYP ID</td>
	</tr>
	<tr>
		<td>Orchestra</td><td>Full orchestra name <a href="http://archives.nyphil.org/index.php/help-performancehistory">Learn more...</a></td>
	</tr>
	<tr>
		<td>Season</td><td>Defined as Sep 1 - Aug 31, displayed "1842-43"</td>
	</tr>
	<tr>
		<td colspan=2><strong>Concert Info: Repeated for each individual performance within a program</strong></td>
	</tr>
	<tr>
		<td>eventType</td><td><a href="http://archives.nyphil.org/index.php/help-performancehistory">See term definitions</a></td>
	</tr>
	<tr>
		<td>Location</td><td>Geographic location of concert (Countries are identified by their current name. For example, even though the orchestra played in Czechoslovakia, it is now identified in the data as the Czech Republic)</td>
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
		<td colspan=2><strong>Works Info: the fields below are repeated for each work performed on a program. By matching the index number of each field, you can tell which soloist(s) and conductor(s) performed a specific work on each of the concerts listed above.</strong></td>
	</tr>
	<tr>
		<td>worksConductorName</td><td>Last name, first name</td>
	</tr>
	<tr>
		<td>worksComposerTitle</td><td>Composer Last name, first / TITLE (NYP short titles used)</td>
	</tr>
	<tr>
		<td>movement</td><td>Movement title as cataloged by NYP</td>
	</tr>
	<tr>
		<td>worksSoloistName</td><td>Last name, first name (if multiple soloists on a single work, delimited by semicolon)</td>
	</tr>
	<tr>
		<td>worksSoloistInstrument</td><td>Last name, first name (if multiple soloists on a single work, delimited by semicolon)</td>
	</tr>
		<tr>
		<td>worksSoloistRole</td><td>"S" means "Soloist"; "A" means "Assisting Artist" (if multiple soloists on a single work, delimited by semicolon)</td>
	</tr>	
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

The New York Philharmonic offers the Metadata as-is and makes no representations or warranties of any kind concerning any Metadata published by the New York Philharmonic.

The writers of these guidelines are deeply indebted to the [Tate](http://www.tate.org.uk), the [Cooper-Hewitt Smithsonian National Design Museum](http://www.cooperhewitt.org/), and [Europeana](http://europeana.eu/).
