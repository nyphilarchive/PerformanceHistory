# New York Philharmonic Performance History
The New York Philharmonic played its first concert on December 7, 1842. Since then, it has merged with the New York Symphony, the New/National Symphony, and had a long-running summer season at New York's Lewisohn Stadium. This Performance History dataset documents all known concerts of all of these organizations, amounting to more than 23,000 performances. You can also search it in the [Data Explorer](https://data.nyphil.org/performance-history/). The [New York Philharmonic Leon Levy Digital Archives](https://archives.nyphil.org) provides an additional interface for searching printed programs alongside other digitized items such as marked music scores, marked orchestral parts, business records, and photos.

In an effort to make this data available for study, analysis, and reuse, the New York Philharmonic joins organizations like [The Tate](https://github.com/tategallery/collection) and the [Cooper-Hewitt Smithsonian National Design Museum](https://www.cooperhewitt.org/) in making its own contribution to the Open Data movement.

The metadata here is released under the Creative Commons Public Domain [CC0](https://creativecommons.org/publicdomain/zero/1.0/) license. Please see the enclosed LICENSE file for more detail.

## Updates

The data is generated from the Archives' catalog every night, and any changes are committed here. Each commit message summarizes how many programs were added, removed, or changed. To follow updates, watch this repository or check its commit history.

## Considerations

* A **program** is one or more performances or presentations in which the **repertoire**, **conductors**, and **soloists** are EXACTLY the same (dates, times, and locations may vary). For example, if a soloist plays an encore one night but not another, the concert with the encore becomes a different program.
* Movements are included as cataloged by the New York Philharmonic. We don't necessarily catalog every movement of a work, only movements that we have performed.
* Recording sessions are not included.
* Definitions of the orchestras and event types are on the Data Explorer's [About the data](https://data.nyphil.org/performance-history/about/) page.

## Files

The data is available as both XML and JSON, with the same content in each:

- `Programs/xml/complete.xml` and `Programs/json/complete.json`: every program.
- The same data split by season, for example `1842-43_TO_1910-11.json`. The last file, `2024-25_TO_NOW`, includes the current season.

Programs are sorted by the date and time of their first concert.

## Structure

### XML

```
<programs>
    <program>
        <id/>                  // legacy Digital Archives ID (see Identifiers)
        <programID/>           // New York Philharmonic program ID
        <damRecordID/>         // Digital Archives record ID (see Identifiers)
        <orchestra/>
        <season/>
        <concertInfo>          // repeated for each concert of the program
            <eventType/>
            <Location/>
            <Venue/>
            <Date/>
            <Time/>
        </concertInfo>
        <worksInfo>            // a program usually has several works
            <work ID="">       // e.g. "8834*4": work ID, then movement ID
                <composerName/>
                <workTitle/>
                <movement/>
                <conductorName/>
                <soloists>     // only if the work has soloists
                    <soloist>
                        <soloistName/>
                        <soloistInstrument/>
                        <soloistRoles/>
                    </soloist>
                </soloists>
                <interval/>    // intermissions appear among the works, with an interval element instead
            </work>
        </worksInfo>
    </program>
</programs>
```

Elements with no value are left out of a work. A program with no works cataloged has an empty `<worksInfo>`.

### JSON

The JSON has the same fields, with `concertInfo` as a `concerts` array and `worksInfo` as a `works` array. `soloists` is always an array, empty when a work has no soloists. Here is the first program, shortened to two of its works:

```json
{
  "programs": [
    {
      "id": "00646b9f-fec7-4ffb-9fb1-faae410bd9dc-0.1",
      "programID": "3853",
      "damRecordID": "2TTUGPLIOHA2",
      "orchestra": "New York Philharmonic",
      "season": "1842-43",
      "concerts": [
        {
          "eventType": "Subscription Season",
          "Location": "Manhattan, NY",
          "Venue": "Apollo Rooms",
          "Date": "1842-12-07T05:00:00Z",
          "Time": "8:00PM"
        }
      ],
      "works": [
        {
          "ID": "8834*4",
          "composerName": "Weber,  Carl  Maria von",
          "workTitle": "OBERON",
          "movement": "\"Ozean, du Ungeheuer\" (Ocean, thou mighty monster), Reiza (Scene and Aria), Act II",
          "conductorName": "Timm, Henry C.",
          "soloists": [
            {
              "soloistName": "Otto, Antoinette",
              "soloistInstrument": "Soprano",
              "soloistRoles": "S"
            }
          ]
        },
        {
          "ID": "0*",
          "interval": "Intermission",
          "soloists": []
        }
      ]
    }
  ]
}
```

## Fields

| Field | Description |
|---|---|
| **Program** | Applies to the entire program |
| `id` | Legacy Digital Archives ID. See [Identifiers](#identifiers). |
| `programID` | New York Philharmonic program ID. Use this to identify programs. |
| `damRecordID` | Digital Archives record ID. See [Identifiers](#identifiers). |
| `orchestra` | Full orchestra name. See [About the data](https://data.nyphil.org/performance-history/about/). |
| `season` | September 1 to August 31, written "1842-43" |
| **Concerts** | Repeated for each performance of the program |
| `eventType` | See [About the data](https://data.nyphil.org/performance-history/about/) for definitions |
| `Location` | Geographic location of the concert. Countries are given by their current name: concerts in Czechoslovakia, for example, are listed under the Czech Republic. |
| `Venue` | Hall, theater, or building where the concert took place |
| `Date` | Date of the concert, written as midnight in New York expressed in UTC: `1842-12-07T05:00:00Z` is December 7, 1842 (`T04:00:00Z` during daylight saving time). Ignore the time part. |
| `Time` | Start time of the concert, for example "8:00PM". Empty if unknown. |
| **Works** | Repeated for each work on the program |
| `ID` | Work ID and movement ID, separated by `*`: "8834*4" is movement 4 of work 8834, and "52446*" is the complete work 52446. Intermissions are "0*". |
| `composerName` | Last name, first name. Works by more than one composer list them separated by ` / `. |
| `workTitle` | Short title as cataloged by the New York Philharmonic, including the arranger when there is one, for example "REQUIEM, K.626 (ARR. Sussmayr)" |
| `movement` | Movement or excerpt, as cataloged. Titles of larger works appear in angle brackets, for example "Overture To &lt;Tannhäuser&gt;". |
| `conductorName` | Last name, first name. More than one conductor is separated by `;`. |
| `soloists` | One entry per soloist, with `soloistName` (last name, first name), `soloistInstrument`, and `soloistRoles`: "S" for soloist, "A" for assisting artist |
| `interval` | "Intermission", in place of the fields above |

## Identifiers

- **`programID`** is the New York Philharmonic's own ID for each program. It's always present and never changes, so use it to identify and join programs.
- **`damRecordID`** is the program's record in the Digital Archives: `https://archives.nyphil.org/asset-management/<damRecordID>`. A newly added program may have none for a day or two.
- **`id`** is the ID the earlier Digital Archives assigned to each program. It's kept unchanged for programs that have one, and links using it continue to redirect to the Digital Archives. New programs are no longer given one, so it's empty for them.

## Changes in October 2026

The dataset is now generated directly from the Archives' catalog instead of from the Digital Archives' search index. Along with the usual catalog updates, this release:

- adds `damRecordID` to every program;
- leaves values empty when they are unknown, instead of the text "None" (most often in `Time`);
- puts every composer of a co-written work in `composerName`, where previously the second composer appeared in `workTitle`;
- removes repeated spaces in work titles: "SYMPHONY NO.  4" is now "SYMPHONY NO. 4";
- writes titles inside movement and work titles in angle brackets, for example "Overture To &lt;Tannhäuser&gt;". Previously these were `<em>` elements in the XML, which made the JSON value an object instead of a string;
- removes empty soloist entries;
- orders programs that start on the same day by the time of their first concert.

## Usage Guidelines

These usage guidelines are based on goodwill, they are not a legal contract but the New York Philharmonic requests that you follow these guidelines if you use Metadata from our Performance History dataset.

The Metadata published by the New York Philharmonic is available free of restrictions under the Creative Commons Zero Public Domain Dedication https://creativecommons.org/publicdomain/zero/1.0/

This means that you can use it for any purpose without having to give attribution. However, the New York Philharmonic requests that you actively acknowledge and give attribution to the New York Philharmonic. Attribution supports future efforts to release other data.

**Give credit where credit is due.**

**Give attribution to the New York Philharmonic.**

Make sure that others are aware of the rights status of the New York Philharmonic Metadata and are aware of these guidelines by keeping intact links to the CC0 Public Domain Dedication.

If for technical or other reasons you cannot include all the links to all sources of the Metadata and rights information directly with the Metadata, you should consider including them separately, for example in a separate document that is distributed with the Metadata or dataset.

If for technical or other reasons you cannot include all the links to all sources of the Metadata and rights information, you may consider linking only to the Metadata source on the New York Philharmonic GitHub page, where all available sources and rights information can be found, including in machine readable formats.

**Metadata is dynamic**

When working with Metadata obtained from the New York Philharmonic be aware that this Metadata is not static, it changes. The New York Philharmonic continuously updates its Metadata in order to correct mistakes and include new and additional information. As performances take place, the New York Philharmonic will aim to update its Performance History Metadata at regular intervals.

**Mention your modifications of the Metadata and contribute your modified Metadata back.**

Whenever you transform, translate or otherwise modify the Metadata, make it clear that the resulting Metadata has been modified by you. If you enrich or otherwise modify Metadata, consider publishing the derived Metadata without reuse restrictions, preferably via the Creative Commons Zero Public Domain Dedication.

**Be responsible.**

Ensure that you do not use the Metadata in a way that suggests any official status or that the New York Philharmonic endorses you or your use of the Metadata, unless you have prior permission to do so.

**Ensure that you do not mislead others or misrepresent the Metadata or its sources.**

Ensure that your use of the Metadata does not breach any national legislation based thereon, notably concerning (but not limited to) data protection, defamation or copyright.

**Please note that you use the Metadata at your own risk.**

The New York Philharmonic offers the Metadata as-is and makes no representations or warranties of any kind concerning any Metadata published by the New York Philharmonic.

The writers of these guidelines are deeply indebted to the [Tate](https://www.tate.org.uk), the [Cooper-Hewitt Smithsonian National Design Museum](https://www.cooperhewitt.org/), and [Europeana](https://www.europeana.eu/).
