// Run this code in supercollider to create synths and a trigger function
// that will be called from the supercollider.py example.
//
// These synthdefs were copied from the supercollider example folder,
// taken from the Steal This Sound! book.
// the folder is at: https://github.com/supercollider/supercollider/tree/develop/examples/demonstrations.
//The recipes are from:
//Mitchell Sigman (2011) Steal this Sound. Milwaukee, WI: Hal Leonard Books
//adapted for SuperCollider and elaborated by Nick Collins (http://www.sussex.ac.uk/Users/nc81/index.html)
//under GNU GPL 3 as per SuperCollider license
SynthDef(\moogbasstone,{|out= 0 freq = 440 amp = 0.1 gate=1 cutoff= 1000 gain=2.0 lagamount = 0.01 pan=0.0|
	var osc, filter, env, filterenv;
	osc = Mix(VarSaw.ar(freq.lag(lagamount)*[1.0,1.001,2.0],Rand(0.0,1.0)!3,Rand(0.5,0.75)!3,0.33));
	filterenv = EnvGen.ar(Env.adsr(0.2,0.0,1.0,0.2),gate,doneAction:2);
	filter =  MoogFF.ar(osc,cutoff*(1.0+(0.5*filterenv)),gain);
	env = EnvGen.ar(Env.adsr(0.001,0.3,0.9,0.2),gate,doneAction:2);
	Out.ar(out,Pan2.ar((0.7*filter+(0.3*filter.distort))*env*amp*1.5,pan));
}).add;
SynthDef(\bassfoundation,{|out= 0 freq = 440 amp = 0.1 gate=1 cutoff= 1000 rq=0.5 pan=0.0|
	var osc, filter, env, filterenv;
	osc = Saw.ar(freq);
	filterenv = EnvGen.ar(Env.adsr(0.0,0.5,0.2,0.2),gate,doneAction:2);
	filter =  RLPF.ar(osc,cutoff*filterenv+100,rq);
	env = EnvGen.ar(Env.adsr(0.01,0.0,0.9,0.05),gate,doneAction:2);
	Out.ar(out,Pan2.ar(filter*env*amp*2,pan));
}).add;
SynthDef(\spookystrings,{|out= 0 freq = 440 amp = 0.1 gate=1 cutoff=8000 rq=0.2 lfowidth=0.01 lforate=3.8 pan=0.0|

	var pulse, filter, env, lfo;

	lfo = LFTri.kr(lforate,Rand(0,2.0)!2);

	//LFO only on second oscillator
	pulse = Mix(Saw.ar(freq*[1,1.001]*[1.0,1.0+(lfowidth*lfo)]))*0.5;

	filter = BHiPass.ar(pulse,cutoff,rq);
	amp = amp * 2;

	env = EnvGen.ar(Env.adsr(0.1,0.0,1.0,3),gate,doneAction:2);

	Out.ar(out,Pan2.ar(filter*env*amp,pan));

}).add;
SynthDef(\situationsynth,{|out= 0 freq = 440 amp = 0.1 gate=1 cutoff=8000 rq=0.8 lfowidth=0.001 lforate= 3.3 pan=(-0.1)|

	var pulse, filter, env, filterenv, lfo;

	lfo = LFTri.kr(lforate,Rand(0,2.0)!2);

	pulse = Mix(Pulse.ar((((freq.cpsmidi)+[0,0.14])+(lfo*lfowidth)).midicps,[0.5,0.51]+(lfowidth*lfo)))*0.5;

	filterenv = EnvGen.ar(Env([0.0,1.0,0.3,0.0],[0.005,0.57,0.1],-3));

	filter =  RLPF.ar(pulse,100+(filterenv*cutoff),rq);

	env = EnvGen.ar(Env.adsr(0.002,0.57,1.0,0.3),gate,doneAction:2);

	Out.ar(out,Pan2.ar(filter*env*amp,pan));

}).add;
SynthDef(\tonewheeltwo,{|out= 0 freq = 440 amp = 0.1 gate=1 lforate = 4.85 lfowidth= 0.1 cutoff= 5000 rq=0.25 pan = 0.0|

	var lfo, pulse, filter, env;

	lfo = LFTri.kr(lforate*[1,1.01],Rand(0,2.0)!2);

	pulse = Pulse.ar( (((freq*[1,3]).cpsmidi) + (lfo*lfowidth)).midicps,[0.5,0.51],[0.4,0.6]);

	env = EnvGen.ar(Env.adsr(0.0,0.0,1.0,0.1),gate,doneAction:2);

	filter = BLowPass4.ar(pulse,cutoff,rq);

	filter= BPeakEQ.ar(filter,500,1.0,3);

	Out.ar(out,Pan2.ar(Mix(filter)*env*amp,pan));

}).add;
SynthDef(\fatvelocitybass,{|out= 0 freq = 440 amp = 0.1 gate=1 cutoff= 12000 rq=0.25 lagTime=0.01 pan = 0.0|
	var lfo, osc, filter, env;
	var basefreq =  ((freq.lag(lagTime).cpsmidi)+[0,11.95,31.03]).midicps;
	amp = amp * 2;
	osc = Saw.ar(basefreq,[0.5,0.4,0.1]); //+PinkNoise.ar(Line.kr(1.0,0,0.03));
	env = EnvGen.ar(Env.adsr(0.01,1.0,1.0,0.25),gate,doneAction:2);
	filter = BLowPass4.ar(osc,100+((amp.squared)*(freq+cutoff)),rq);
	Out.ar(out,Pan2.ar(Mix(filter)*env*amp*0.8,pan));
}).add;
OSCFunc( { | msg, time, addr, port |
	var myFreq;
	var myDur;
	var ins;
	ins = msg[1];
	myFreq = msg[2].asFloat();
	myDur = msg[3].asFloat();
	//Pbind(\midinote, myFreqs, \dur, 0.5).play;
	Pbind(\instrument,ins,\midinote, Pseq([myFreq]), \dur, myDur).play;
}, '/stemel' )
