var number = /^\d+$/;
var float = /^\d+?\.*?\d*?$/;
var upoctave = /^>+$/;
var downoctave = /^<+$/;
var rest = /^\*+$/;
var carry = /^\-+$/;
var carry = /^\-+$/;
var repeat = /^r\d+$/;
var ampValue = /^a\d+\.*\d*$/;

function s2notes(pattern) {
    var lines = pattern.split("/");
    var scoreLines = [];
    var lineCounter = 0;
    var octave = 3;
    var amplitude = 1.0
    for (var i=0;i<lines.length;i++){
        var line = lines[i].trim();
        var scoreLine = [];
        var counter = 0
        words = line.split(" ");
        for (var j=0;j<words.length;j++){
            var word = words[j];
            if (float.test(word)) {
                //number
                scoreLine[counter]={note:parseFloat(word)+(octave*12),duration:1,amplitude:amplitude};
                counter++;
            } else if (ampValue.test(word)) {
                amplitude = parseFloat(word.substring(1,word.length));
                //word is a float
            } else if (upoctave.test(word)) {
                //word is an upoctave
                octave+=word.length;
            } else if (downoctave.test(word)) {
                //word is a downoctave
                octave-=word.length;
                if (octave<0) {
                    octave=0;
                }
            } else if (rest.test(word)) {
                //word is a rest
                for (var k=0;k<word.length;k++){
                    scoreLine[counter]={note:-1,duration:1,amplitude:amplitude};
                    counter++;
                }
            } else if (carry.test(word)) {
                //word is a carry
                var lookBack = 1;
                while((lookBack<=counter)&&(scoreLine[counter-lookBack].note<0)){
                    lookBack++;
                }
                if (lookBack<=counter){
                    scoreLine[counter-lookBack].duration+=word.length
                    for (var k=0;k<word.length;k++){
                        scoreLine[counter]={note:-1,duration:1,amplitude:amplitude};
                        counter++;
                    }
                }
            } else if (repeat.test(word)) {
                //word is a repeat
            } else {
                console.log("don't understand " + word);
            }
        }
        if (scoreLine.length>0){
            scoreLines[lineCounter]=scoreLine;
            lineCounter++;
        }
    }
    return scoreLines;
}

function notes2buffer(notes){
  var no_voices = notes.length;
  var buffer_length = notes.map(a => a.length).reduce((a,b) => Math.max(a,b));
  buffer = [];
  for (var i=0;i<buffer_length;i++) {
    line = []
    for (var j=0;j<no_voices;j++){
      line.push(notes[j][i % notes[j].length]);
    }
    buffer.push(line);
  }
  return buffer;
}

function buffer2Sequencer(sequencer, instrument, buffer, numberTimes=1, clear=false){
  var track;
  if (clear || !(instrument in sequencer)) {
    track = [];
  } else {
    track = sequencer[instrument];
  }
  for (var i=0;i<numberTimes;i++){
    track = track.concat(buffer);
  }
  sequencer[instrument] = track;
  return sequencer;
}
function s2buffer(score){
  return notes2buffer(s2notes(score));
}
function example(){
  var notes = s2notes("0 -- * 3 / 12 12 ");
  var buffer = notes2buffer(notes)
  sequencer = {};
  buffer2Sequencer(sequencer, "bass", buffer);
}
