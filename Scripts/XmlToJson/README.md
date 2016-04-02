## Converting Programs to JSON

This is a node.js appication that converts the existing program
information from XML to JSON. It reads in all of the XML files from
`Programs/xml` in parallel and processes them at the same time, writing
their JSON 'equivalents' in `Programs/json`. Equivalents is quoted
because several changes are made for the sake of fitting the JSON
format. The most important change is that `worksInfo` and `concertInfo`
are mapped to `works` and `concerts`. Other changes are minor and should
be a problem. Here's an abridged example of what the output JSON will
look like:

```
{
  "programs": [
    {
      "id": "38e072a7-8fc9-4f9a-8eac-3957905c0002",
      "programID": "3853",
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
        /* more concerts, if applicable */
      ],
      "works": [
        {
          "ID": "8834*4",
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
            /* more soloists, if applicable */
          ]
        },
        /* more works, if applicable */
      ]
    },
    /* more programs */
  ]
}

```


### Running the script
If the XML is updated, the script will need to be rerun in order to
update the corresponding JSON. This can be as easy as running `node
app.js` from this directory, but will require some environment setup.

First you'll need node.js installed. I tested it with 5.5.0, but any
version after around 4 should work. I recommend downloading and
managing node versions with [nvm](https://github.com/creationix/nvm).

Once node is installed, you should have access to the command line tool,
`npm`. From this directory, run `npm install` in order to download
project dependencies.

Then, simply run `node app.js`. It will run for a while with no
feedback (~40 seconds) and will spit out some log messages when it's
done. You should then see that the json files in `Programs/json` have
all been changed. Stage and commit these files to complete the update
process.

### Known issues
If the shape of the XML changes significantly, this will certainly
break since the implementation of the converter is tightly coupled with the
format of the XML. When you run the converter and it can't handle the
change in shape, it will exit with an error, which should log to the
console.
