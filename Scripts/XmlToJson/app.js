'use strict';

let glob = require('glob');
let fs = require('fs');
let xml2js = require('xml2js');
let jsonfile = require('jsonfile');

let parser = new xml2js.Parser({
  explicitArray: false,
  mergeAttrs: true,
  trim: true
});

/**
 *  This is the function that takes a standard conversion from
 *  XML and restructures it to be a little more friendly.
 *
 *  Most notably, it ensures that certain fields are always arrays,
 *  which is problematic to determine in the XML conversion when a
 *  parent only has one child.
 *
 *  It also does the following renaming:
 *  worksInfo -> works
 *  concertsInfo -> concerts
 *
 *  This also mutates the result in place. It my be better to build up
 *  a separate data structure instead.
 */
function restructureNestedLists(result) {
  result.programs = result.programs.program;

  for(var i = 0, l1 = result.programs.length; i < l1; i++) {
    // Fix concerts
    if(result.programs[i].concertInfo) {
      result.programs[i].concerts = [].concat(result.programs[i].concertInfo);
      delete result.programs[i].concertInfo;
    } else {
      result.programs[i].concerts = [];
      delete result.programs[i].concertInfo;
    }

    // Fix works
    if(result.programs[i].worksInfo.work) {
      result.programs[i].works = [].concat(result.programs[i].worksInfo.work);
      delete result.programs[i].worksInfo;

      if(result.programs[i].works) {
        for(var j = 0, l2 = result.programs[i].works.length; j < l2; j++) {
          if(result.programs[i].works[j].soloists) {
            result.programs[i].works[j].soloists = [].concat(result.programs[i].works[j].soloists.soloist);
          } else {
            result.programs[i].works[j].soloists = [];
          }
        }
      }
    } else {
      result.programs[i].works = [];
      delete result.programs[i].worksInfo;
    }
  }
  return result;
}

const RELATIVE_PROGRAM_ROOT = '../../Programs';

glob('*.xml', {cwd: `${RELATIVE_PROGRAM_ROOT}/xml`}, function(err, data) {
  data.forEach(function(filename, idx, arr) {
    const startTime = Date.now();
    const xmlPath = `${__dirname}/${RELATIVE_PROGRAM_ROOT}/xml/${filename}`
    const jsonPath = `${__dirname}/${RELATIVE_PROGRAM_ROOT}/json/${filename.split('.')[0]}.json`;

    fs.readFile(xmlPath, function(err, data) {
      if(err) {
        throw new Error(err);
      }
      parser.parseString(data, function (err, result) {
        let json = restructureNestedLists(result);
        jsonfile.writeFile(jsonPath, json, {spaces: 2}, function(err) {
          if(err) {
            throw new Error(err);
          }
          console.log(`Took ${Date.now() - startTime}ms to process ${filename}`);
        });
      });
    });
  });
});

