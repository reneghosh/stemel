var number = /^\d+$/;
var float = /^\d+?\.*?\d*?$/;
var upoctave = /^>+$/;
var downoctave = /^<+$/;
var rest = /^\*+$/;
var carry = /^\-+$/;
var carry = /^\-+$/;
var repeat = /^r\d+$/;
var ampValue = /^a\d+\.*\d*$/;

function parseNotes(pattern) {
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
                scoreLine[counter]={note:parseFloat(word)+octave*12,duration:1,amplitude:amplitude};
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


function makeScore(program){
    var score = {};
    for (var instrument in program){
        pattern_holder = {};
        score[instrument]= pattern_holder;
        for (var pattern in program[instrument]){
            var parsedLine = parseNotes(program[instrument][pattern]);
            pattern_holder[pattern]=parsedLine;
        }
    }
    return score;
}

function parsePatterns(pattern){
    var sequence = [];
    var counter = 0;
    var words = pattern.split(" ");
    for (var i=0;i<words.length;i++){
        sequence[counter]=words[i].trim();
        counter++;
    }
    return sequence;
}
function makeSequence(plan){
    sequence={};
    for (var instrument in plan){
        pattern_sequence = plan[instrument];
        sequence[instrument]=parsePatterns(pattern_sequence);
    }
    return sequence;
}

var patterns = {
    base: {
        p1: "0 0 5 0",
        p2: "0 5 7 0 0 0 -- - a0.5 5 a1.0 > 0 / 0 5 >> 8 << * **"
    },
    lead: {
        p1: "0 5 7 8 9",
        p2: "0 6 * * 9"
    }
};
var plan = {
    base: "p1 p1 p2 p1",
    lead: "p1 *"
};
function playScore(instrument,pattern){
    console.log("playing "+pattern+" on "+instrument);
}

function playSequence(sequence, score){
    var cursor = 0;
    var ended = false;
    while(!ended){
        ended=true;
        for(var instrument in sequence){
            if (cursor<sequence[instrument].length-1){
                ended = false;
            }
            var patternName = sequence[instrument][cursor % sequence[instrument].length];
            if (patternName != "*"){
                console.log("play "+patternName+" from "+instrument);
                pattern = score[instrument][patternName];
                console.log("pattern "+pattern);
                var playThread = function(){
                    playScore(instrument,pattern);
                }();
                //setTimeout(playThread,500);
            }
        }
        cursor ++;
    }
}
var score = makeScore(patterns);
var sequence = makeSequence(plan);
playSequence(sequence, score);