<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>KNN interactivo: ¿De qué grupo soy?</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&display=swap" rel="stylesheet">
<style>
:root{
  box-sizing:border-box;
  padding-top:env(safe-area-inset-top,0px);
  padding-bottom:env(safe-area-inset-bottom,0px);
  --bg:#F3F6FA; --surface:#FFFFFF; --ink:#141C2B; --muted:#586479; --line:#DAE1EB; --grid:#E9EEF5;
  --blue:#2F6FEB; --orange:#EE8A1E; --blue-tint:#DCE7FD; --orange-tint:#FCE6CB; --tie:#E4E8EF;
  --on-blue:#FFFFFF; --on-orange:#201200; --bad:#D6453D; --good:#17804F;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#0D131E; --surface:#151D2B; --ink:#E9EEF7; --muted:#9BA8BD; --line:#29344B; --grid:#202B3F;
    --blue:#5B93FF; --orange:#FFA043; --blue-tint:#1B2C50; --orange-tint:#40301A; --tie:#26314A;
    --on-blue:#06122B; --on-orange:#201200; --bad:#FF7A70; --good:#4CC790;
  }
}
:root[data-theme="dark"]{
  --bg:#0D131E; --surface:#151D2B; --ink:#E9EEF7; --muted:#9BA8BD; --line:#29344B; --grid:#202B3F;
  --blue:#5B93FF; --orange:#FFA043; --blue-tint:#1B2C50; --orange-tint:#40301A; --tie:#26314A;
  --on-blue:#06122B; --on-orange:#201200; --bad:#FF7A70; --good:#4CC790;
}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Bricolage Grotesque',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-size:15px;line-height:1.45}
.wrap{max-width:1180px;margin:0 auto;padding:22px 18px 48px}
h1{font-size:clamp(36px,6.4vw,60px);font-weight:800;letter-spacing:-.035em;line-height:1;margin:0 0 10px}
.lead{margin:0;max-width:62ch;color:var(--muted);font-size:16px}
.tabs{display:flex;gap:4px;margin:22px 0 20px;border-bottom:1px solid var(--line);overflow-x:auto}
.tab{background:none;border:0;padding:10px 14px;font:inherit;font-weight:600;color:var(--muted);border-bottom:3px solid transparent;margin-bottom:-1px;cursor:pointer;white-space:nowrap}
.tab[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--ink)}
.main{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(320px,.88fr);gap:32px;align-items:start}
@media (max-width:900px){.main{grid-template-columns:minmax(0,1fr)}}
@media (min-width:901px){.stage{position:sticky;top:calc(14px + env(safe-area-inset-top,0px))}}
.plane{background:var(--surface);border:1px solid var(--line);border-radius:6px;overflow:hidden;max-width:700px}
canvas{display:block;touch-action:none;cursor:crosshair;outline-offset:-3px}
canvas:focus-visible{outline:3px solid var(--blue)}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;margin:12px 0 0;font-size:13px;color:var(--muted)}
.lg{display:inline-flex;align-items:center;gap:6px}
.lg .q{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;border:3px solid var(--ink);font-size:10px;font-weight:800;color:var(--ink);line-height:1}
.lg .ring{width:16px;height:16px;border-radius:50%;border:2px dashed var(--bad)}
.note{min-height:1.5em;margin:10px 0 0;font-weight:600;max-width:64ch}
.dot{display:inline-block;width:11px;height:11px;border-radius:50%;flex:none}
.c0{background:var(--blue)} .c1{background:var(--orange)}
.block{padding:18px 0;border-top:1px solid var(--line)}
.block:first-child{border-top:0;padding-top:0}
.block h2{font-size:19px;font-weight:700;letter-spacing:-.01em;margin:0 0 12px}
.block h3{font-size:14px;font-weight:700;margin:18px 0 8px}
.hint{color:var(--muted);font-size:13px;margin:6px 0 0}
.empty{color:var(--muted);margin:0}
.field{margin:0 0 16px}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.row label,.lbl{font-weight:600;font-size:14px}
output{font-variant-numeric:tabular-nums;font-weight:700}
input[type=range]{width:100%;accent-color:var(--ink);margin:6px 0 0}
.seg-ctl{display:inline-flex;flex-wrap:wrap;border:1.5px solid var(--ink);border-radius:8px;overflow:hidden;margin-top:6px}
.seg-ctl label{position:relative;cursor:pointer}
.seg-ctl input{position:absolute;opacity:0;pointer-events:none}
.seg-ctl span{display:block;padding:8px 12px;font-size:14px;font-weight:600}
.seg-ctl input:checked+span{background:var(--ink);color:var(--bg)}
.seg-ctl input:focus-visible+span{outline:3px solid var(--blue);outline-offset:-3px}
.checks{display:flex;flex-direction:column;gap:8px;margin:4px 0 16px}
.chk{display:flex;align-items:center;gap:9px;font-weight:600;font-size:14px;cursor:pointer}
.chk input{width:18px;height:18px;accent-color:var(--ink);margin:0}
.btns{display:flex;flex-wrap:wrap;gap:8px}
.btn{font:inherit;font-weight:600;font-size:14px;padding:8px 12px;border-radius:8px;border:1.5px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer}
.btn:hover{background:var(--ink);color:var(--bg)}
.btn.primary{background:var(--ink);color:var(--bg)}
.btn.small{padding:4px 9px;font-size:13px}
button:focus-visible,input:focus-visible,summary:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.verdict{display:flex;align-items:center;gap:9px;font-size:21px;letter-spacing:-.01em;margin:0 0 12px;line-height:1.2}
.verdict .dot{width:17px;height:17px}
.verdict.tie{color:var(--bad)}
.sub{font-size:13px;color:var(--muted);font-weight:400;letter-spacing:0}
.prob{margin:0 0 14px;color:var(--muted)}
.prob .big{font-size:36px;font-weight:800;color:var(--ink);letter-spacing:-.03em;margin-right:8px;font-variant-numeric:tabular-nums}
.bar{display:flex;height:32px;border-radius:6px;overflow:hidden;background:var(--line)}
.seg{flex:0 1 0;min-width:0;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px}
.seg.c0{color:var(--on-blue)} .seg.c1{color:var(--on-orange)}
@media (prefers-reduced-motion:no-preference){.seg{transition:flex-grow .25s ease}}
.barlbl{display:flex;justify-content:space-between;font-size:12px;color:var(--muted);margin-top:4px}
.tiebox{border-left:4px solid var(--bad);padding:4px 0 4px 12px;margin:14px 0 4px}
.tiebox p{margin:0 0 10px;font-weight:600}
.rule{font-size:13px;color:var(--muted);margin:10px 0 0;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
ol.nbs{list-style:none;margin:0;padding:0}
.nb{display:flex;width:100%;gap:9px;align-items:center;text-align:left;background:none;border:0;border-bottom:1px solid var(--line);padding:7px 6px;font:inherit;font-size:14px;color:var(--ink);cursor:pointer;font-variant-numeric:tabular-nums}
.nb.on{background:var(--grid);font-weight:700}
.nbtxt{flex:1}
.nbtxt em{color:var(--bad);font-style:normal;font-weight:700;font-size:12px;margin-left:4px}
.nbd{color:var(--muted);font-size:13px;white-space:nowrap}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:6px;border:1.5px solid var(--line);background:none;border-radius:999px;padding:5px 11px;font:inherit;font-size:13px;color:var(--ink);cursor:pointer;font-variant-numeric:tabular-nums}
.chip.on{border-color:var(--ink);font-weight:700}
.calc .ln{padding:2px 0;font-variant-numeric:tabular-nums}
.calc .f{padding-left:1.4em}
.calc .res{font-weight:800;font-size:18px}
.score{margin:0 0 10px;font-size:15px}
ul.ret{list-style:none;margin:0 0 12px;padding:0}
ul.ret li{padding:9px 0;border-bottom:1px solid var(--line)}
ul.ret .t{font-weight:600}
ul.ret .st{font-size:13px;color:var(--muted)}
ul.ret li.ok .st{color:var(--good);font-weight:700}
details.block summary{font-weight:700;font-size:19px;cursor:pointer;letter-spacing:-.01em}
details.block ol{margin:12px 0 0;padding-left:1.3em}
details.block li{margin:0 0 6px}
body.mode-abstract .only-rain{display:none!important}
body.mode-rain .only-abstract{display:none!important}
</style>
</head>
<body class="mode-abstract">
<div class="wrap">
  <header>
    <h1 id="title">¿De qué grupo soy?</h1>
    <p class="lead" id="lead"></p>
  </header>

  <div class="tabs" role="tablist" aria-label="Elegir ejemplo">
    <button class="tab" role="tab" id="tab-abstract" aria-selected="true">Plano abstracto</button>
    <button class="tab" role="tab" id="tab-rain" aria-selected="false">Caso real: lluvia</button>
  </div>

  <div class="main">
    <section class="stage" aria-label="Plano interactivo">
      <div class="plane"><canvas id="cv" tabindex="0" aria-label="Plano de puntos. Haz clic para colocar el punto nuevo, arrástralo para moverlo o usa las flechas del teclado."></canvas></div>
      <div class="legend" id="legend"></div>
      <p class="note" id="note" aria-live="polite"></p>
    </section>

    <section class="side">
      <div class="block">
        <h2>Controles</h2>
        <div class="field">
          <div class="row"><label for="k">Vecinos que votan (K)</label><output id="kout">5</output></div>
          <input type="range" id="k" min="1" max="15" step="1" value="5">
          <p class="hint">Con K impar no hay empates.</p>
        </div>

        <div class="field only-abstract">
          <span class="lbl" id="placeLbl">Al hacer clic en el plano coloco</span>
          <div class="seg-ctl" role="radiogroup" aria-labelledby="placeLbl">
            <label><input type="radio" name="place" value="query" checked><span>❓ Punto nuevo</span></label>
            <label><input type="radio" name="place" value="0"><span>🔵 Dato azul</span></label>
            <label><input type="radio" name="place" value="1"><span>🟠 Dato naranja</span></label>
          </div>
        </div>

        <div class="only-rain">
          <div class="field">
            <div class="row"><label for="hum">Humedad de hoy</label><output id="humOut">68 %</output></div>
            <input type="range" id="hum" min="30" max="100" step="1" value="68">
          </div>
          <div class="field">
            <div class="row"><label for="tmp">Temperatura de hoy</label><output id="tmpOut">23.0 °C</output></div>
            <input type="range" id="tmp" min="10" max="35" step="0.1" value="23">
          </div>
        </div>

        <div class="checks">
          <label class="chk"><input type="checkbox" id="showDist"> Mostrar distancias</label>
          <label class="chk"><input type="checkbox" id="showBound"> Mostrar cómo piensa KNN</label>
          <label class="chk only-rain"><input type="checkbox" id="norm"> Normalizar variables</label>
          <p class="hint only-rain" id="normHint"></p>
        </div>

        <div class="btns only-abstract">
          <button class="btn primary" id="noise" type="button">Agregar dato erróneo</button>
          <button class="btn" id="mkTie" type="button">Crear empate</button>
          <button class="btn" id="clear" type="button">Quitar datos agregados</button>
          <button class="btn" id="reseed" type="button">Nuevo conjunto</button>
        </div>
      </div>

      <div class="block" id="result"></div>
      <div class="block calc" id="calc" hidden></div>
      <div class="block only-abstract" id="game"></div>

      <details class="block" id="guide">
        <summary>Guía para la clase</summary>
        <ol class="only-abstract">
          <li>Haz clic en el plano para colocar ❓ y arrástralo hacia un grupo.</li>
          <li>Cambia K de 1 a 9 y mira cuándo cambia la clasificación.</li>
          <li>Pulsa "Agregar dato erróneo": K=1 se equivoca y K=5 lo corrige.</li>
          <li>Activa "Mostrar distancias" y toca un vecino para ver el cálculo.</li>
          <li>Pulsa "Crear empate" y decide cómo resolverlo.</li>
          <li>Activa "Mostrar cómo piensa KNN" y compara K=1 con K=15.</li>
        </ol>
        <ol class="only-rain">
          <li>Mueve humedad y temperatura para describir el día de hoy.</li>
          <li>Revisa los días más parecidos y cuántos tuvieron lluvia.</li>
          <li>Cambia K y observa cómo cambia la probabilidad.</li>
          <li>Activa y desactiva "Normalizar variables". ¿Cambian los vecinos? ¿Por qué?</li>
        </ol>
      </details>
    </section>
  </div>
</div>

<script>
(function(){
'use strict';
var $=function(s){return document.querySelector(s);};
var MINUS='\u2212';
var r1=function(v){return Math.round(v*10)/10;};
var clamp=function(v,a,b){return Math.min(b,Math.max(a,v));};

function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}

var CFG={
  abstract:{xmin:0,xmax:10,ymin:0,ymax:10,xt:1,yt:1,xl:'x',yl:'y',
    names:['Azul','Naranja'],plural:['azules','naranjas'],
    verdict:['Azul (Clase A)','Naranja (Clase B)'],pre:'Clasificado como ',
    title:'¿De qué grupo soy?',
    lead:'Haz clic en el plano para colocar un punto nuevo ❓. KNN busca sus K vecinos más cercanos y decide por votación.'},
  rain:{xmin:30,xmax:100,ymin:10,ymax:35,xt:10,yt:5,xl:'Humedad (%)',yl:'Temperatura (°C)',
    names:['No llovió','Llovió'],plural:['días sin lluvia','días con lluvia'],
    verdict:['no va a llover','va a llover'],pre:'Predicción: ',
    title:'¿Va a llover?',
    lead:'Describe el clima de hoy con dos controles. KNN busca los días históricos más parecidos y vota.'}
};

function genAbstract(seed){
  var r=rng(seed*7919+11),pts=[],i;
  var cl=function(v){return clamp(v,0.4,9.6);};
  for(i=0;i<22;i++)pts.push({x:r1(cl(3.4+gauss(r)*1.5)),y:r1(cl(6.4+gauss(r)*1.5)),c:0});
  for(i=0;i<22;i++)pts.push({x:r1(cl(6.6+gauss(r)*1.5)),y:r1(cl(3.6+gauss(r)*1.5)),c:1});
  return pts;
}
function genRain(seed){
  var r=rng(seed*13+5),pts=[];
  for(var i=0;i<60;i++){
    var h=Math.round(38+r()*60);
    var t=r1(clamp(12+r()*20-(h-68)*0.06,10.5,34.5));
    var z=(h-66)/7-(t-22)/4.5;
    var c=r()<1/(1+Math.exp(-z))?1:0;
    pts.push({x:h,y:t,c:c,label:'Día '+(i+1)});
  }
  return pts;
}

var S={mode:'abstract',k:5,seed:7,tieRule:'none',place:'query',showDist:false,showBound:false,norm:false,
  A:{pts:[],q:null,sel:null},R:{pts:[],q:{x:68,y:23},sel:null},
  G:{on:false,d1:false,b1:false,d2:false,d3:false,score:0},msg:''};
S.A.pts=genAbstract(S.seed);
S.R.pts=genRain(S.seed);
var cur=function(){return S.mode==='abstract'?S.A:S.R;};
var say=function(t){S.msg=t;};
var lastRes=null;

function sc(){
  var C=CFG[S.mode];
  return (S.mode==='rain'&&S.norm)?[1/(C.xmax-C.xmin),1/(C.ymax-C.ymin)]:[1,1];
}
function dist(a,b){var s=sc();return Math.hypot((a.x-b.x)*s[0],(a.y-b.y)*s[1]);}
function knn(pts,q,k,rule){
  var arr=pts.map(function(p){return {p:p,d:dist(p,q)};}).sort(function(a,b){return a.d-b.d;});
  var nb=arr.slice(0,Math.min(k,arr.length));
  var votes=[0,0];nb.forEach(function(n){votes[n.p.c]++;});
  var pred=null,tie=false,how='';
  if(votes[0]!==votes[1]){pred=votes[1]>votes[0]?1:0;}
  else{
    tie=true;
    if(rule==='nearest'){pred=nb[0].p.c;how='nearest';}
    else if(rule==='weighted'){
      var w=[0,0];nb.forEach(function(n){w[n.p.c]+=1/(n.d+1e-6);});
      if(w[0]!==w[1]){pred=w[1]>w[0]?1:0;how='weighted';}
    }
  }
  return {nb:nb,votes:votes,pred:pred,tie:tie,how:how};
}
function effSel(res){
  if(!res)return null;
  var s=cur().sel;
  if(s&&res.nb.some(function(n){return n.p===s;}))return s;
  return res.nb[0].p;
}
function fmtD(d){return (S.mode==='rain'&&S.norm)?d.toFixed(3):d.toFixed(2);}
function fx(v){return S.mode==='rain'?String(Math.round(v)):v.toFixed(1);}
function fy(v){return v.toFixed(1);}

/* ---------- Canvas ---------- */
var cv=$('#cv'),ctx=cv.getContext('2d');
var W=600,H=594,dpr=1;
var PAD={l:46,r:14,t:14,b:40};
var geo={};
function setGeo(){geo={C:CFG[S.mode],pw:W-PAD.l-PAD.r,ph:H-PAD.t-PAD.b};}
function X(v){return PAD.l+(v-geo.C.xmin)/(geo.C.xmax-geo.C.xmin)*geo.pw;}
function Y(v){return PAD.t+geo.ph-(v-geo.C.ymin)/(geo.C.ymax-geo.C.ymin)*geo.ph;}
function IX(p){return geo.C.xmin+(p-PAD.l)/geo.pw*(geo.C.xmax-geo.C.xmin);}
function IY(p){return geo.C.ymin+(PAD.t+geo.ph-p)/geo.ph*(geo.C.ymax-geo.C.ymin);}
function colors(){
  var cs=getComputedStyle(document.documentElement);
  var g=function(n){return cs.getPropertyValue(n).trim();};
  return {surface:g('--surface'),ink:g('--ink'),muted:g('--muted'),line:g('--line'),grid:g('--grid'),
    blue:g('--blue'),orange:g('--orange'),blueT:g('--blue-tint'),orangeT:g('--orange-tint'),tie:g('--tie'),bad:g('--bad'),
    font:getComputedStyle(document.body).fontFamily};
}
function resize(){
  var w=Math.floor($('.plane').clientWidth);
  if(w<200)return;
  W=w;H=W-(PAD.l+PAD.r)+(PAD.t+PAD.b);
  dpr=window.devicePixelRatio||1;
  cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);
  cv.style.width=W+'px';cv.style.height=H+'px';
  draw();
}

function draw(){
  setGeo();
  var C=geo.C,col=colors(),A=cur(),pts=A.pts,q=A.q,v,i,j;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle=col.surface;ctx.fillRect(0,0,W,H);

  if(S.showBound){
    var n=56,cw=geo.pw/n,ch=geo.ph/n;
    for(i=0;i<n;i++)for(j=0;j<n;j++){
      var dx=C.xmin+(i+0.5)/n*(C.xmax-C.xmin),dy=C.ymin+(j+0.5)/n*(C.ymax-C.ymin);
      var rr=knn(pts,{x:dx,y:dy},S.k,S.tieRule);
      ctx.fillStyle=rr.pred===0?col.blueT:rr.pred===1?col.orangeT:col.tie;
      ctx.fillRect(PAD.l+i*cw,PAD.t+geo.ph-(j+1)*ch,cw+0.6,ch+0.6);
    }
  }

  ctx.lineWidth=1;ctx.strokeStyle=col.grid;ctx.fillStyle=col.muted;ctx.font='11px '+col.font;
  ctx.textAlign='center';ctx.textBaseline='top';
  for(v=C.xmin;v<=C.xmax+1e-9;v+=C.xt){
    var px=Math.round(X(v))+0.5;
    ctx.beginPath();ctx.moveTo(px,PAD.t);ctx.lineTo(px,PAD.t+geo.ph);ctx.stroke();
    ctx.fillText(String(v),X(v),PAD.t+geo.ph+7);
  }
  ctx.textAlign='right';ctx.textBaseline='middle';
  for(v=C.ymin;v<=C.ymax+1e-9;v+=C.yt){
    var py=Math.round(Y(v))+0.5;
    ctx.beginPath();ctx.moveTo(PAD.l,py);ctx.lineTo(PAD.l+geo.pw,py);ctx.stroke();
    ctx.fillText(String(v),PAD.l-8,Y(v));
  }
  ctx.strokeStyle=col.line;ctx.strokeRect(PAD.l+0.5,PAD.t+0.5,geo.pw,geo.ph);
  ctx.fillStyle=col.ink;ctx.font='600 12px '+col.font;ctx.textAlign='center';ctx.textBaseline='alphabetic';
  ctx.fillText(C.xl,PAD.l+geo.pw/2,H-8);
  ctx.save();ctx.translate(13,PAD.t+geo.ph/2);ctx.rotate(-Math.PI/2);ctx.fillText(C.yl,0,0);ctx.restore();

  var res=q?knn(pts,q,S.k,S.tieRule):null;
  var sel=effSel(res);

  if(res){
    var s=sc(),dk=res.nb[res.nb.length-1].d;
    var rx=dk/s[0]*geo.pw/(C.xmax-C.xmin),ry=dk/s[1]*geo.ph/(C.ymax-C.ymin);
    ctx.save();ctx.beginPath();ctx.ellipse(X(q.x),Y(q.y),rx,ry,0,0,Math.PI*2);
    ctx.setLineDash([5,5]);ctx.strokeStyle=col.muted;ctx.lineWidth=1.2;ctx.stroke();ctx.restore();
    res.nb.forEach(function(nn){
      ctx.beginPath();ctx.moveTo(X(q.x),Y(q.y));ctx.lineTo(X(nn.p.x),Y(nn.p.y));
      ctx.strokeStyle=nn.p.c?col.orange:col.blue;
      ctx.lineWidth=(nn.p===sel&&S.showDist)?3.5:1.8;ctx.stroke();
    });
  }

  var isNb=[];if(res)res.nb.forEach(function(nn){isNb.push(nn.p);});
  var rad=S.mode==='rain'?5:6;
  pts.forEach(function(p){
    var ax=X(p.x),ay=Y(p.y);
    ctx.beginPath();ctx.arc(ax,ay,rad,0,Math.PI*2);ctx.fillStyle=p.c?col.orange:col.blue;ctx.fill();
    ctx.lineWidth=2;ctx.strokeStyle=col.surface;ctx.stroke();
    if(isNb.indexOf(p)>=0){
      ctx.beginPath();ctx.arc(ax,ay,rad+4,0,Math.PI*2);ctx.lineWidth=(p===sel&&S.showDist)?3.5:2;ctx.strokeStyle=col.ink;ctx.stroke();
    }
    if(p.noise){
      ctx.save();ctx.setLineDash([3,3]);ctx.beginPath();ctx.arc(ax,ay,rad+9,0,Math.PI*2);ctx.strokeStyle=col.bad;ctx.lineWidth=2;ctx.stroke();ctx.restore();
    }else if(p.manual){
      ctx.beginPath();ctx.arc(ax,ay,rad+9,0,Math.PI*2);ctx.strokeStyle=col.muted;ctx.lineWidth=1.2;ctx.stroke();
    }
  });

  if(res&&S.showDist){
    ctx.font='600 11px '+col.font;ctx.textAlign='center';ctx.textBaseline='middle';
    res.nb.forEach(function(nn){
      if(S.k>9&&nn.p!==sel)return;
      var mx=(X(q.x)+X(nn.p.x))/2,my=(Y(q.y)+Y(nn.p.y))/2;
      var t='d='+fmtD(nn.d),tw=ctx.measureText(t).width+8;
      ctx.globalAlpha=0.92;ctx.fillStyle=col.surface;ctx.fillRect(mx-tw/2,my-8,tw,16);ctx.globalAlpha=1;
      ctx.fillStyle=col.ink;ctx.fillText(t,mx,my+0.5);
    });
  }

  if(q){
    var qx=X(q.x),qy=Y(q.y);
    var pc=(res&&res.pred!==null)?(res.pred?col.orange:col.blue):col.ink;
    ctx.beginPath();ctx.arc(qx,qy,12,0,Math.PI*2);ctx.fillStyle=col.surface;ctx.fill();
    ctx.lineWidth=4;ctx.strokeStyle=pc;ctx.stroke();
    ctx.fillStyle=col.ink;ctx.font='800 14px '+col.font;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText('?',qx,qy+1);
  }
}

/* ---------- Panels ---------- */
function renderResult(res){
  var el=$('#result'),C=CFG[S.mode],A=cur();
  if(!res){
    el.innerHTML='<h2>Votación</h2><p class="empty">Haz clic en el plano para colocar tu punto ❓ y ver cómo votan sus vecinos.</p>';
    return;
  }
  var v0=res.votes[0],v1=res.votes[1],k=res.nb.length,sel=effSel(res),verdict;
  if(res.pred===null){
    verdict='<p class="verdict tie">Empate: '+v0+' contra '+v1+'. El algoritmo no puede decidir.</p>';
  }else{
    var why=res.tie?' <span class="sub">(empate resuelto por '+(res.how==='nearest'?'el vecino más cercano':'el peso de la distancia')+')</span>':'';
    verdict='<p class="verdict"><span class="dot c'+res.pred+'"></span><span>'+C.pre+'<strong>'+C.verdict[res.pred]+'</strong>'+why+'</span></p>';
  }
  var prob='';
  if(S.mode==='rain'){
    prob='<p class="prob"><span class="big">'+Math.round(v1/k*100)+'%</span>probabilidad aproximada de lluvia ('+v1+' de '+k+' días parecidos tuvieron lluvia)</p>';
  }
  var bar='<div class="bar" role="img" aria-label="Votos: '+C.names[0]+' '+v0+', '+C.names[1]+' '+v1+'">'+
    '<span class="seg c0" style="flex-grow:'+v0+'">'+(v0||'')+'</span>'+
    '<span class="seg c1" style="flex-grow:'+v1+'">'+(v1||'')+'</span></div>'+
    '<div class="barlbl"><span>'+C.names[0]+'</span><span>'+C.names[1]+'</span></div>';
  var tie='';
  if(res.tie&&res.pred===null){
    tie='<div class="tiebox"><p>'+v0+' '+C.plural[0]+' y '+v1+' '+C.plural[1]+'. ¿Qué debería hacer el algoritmo?</p>'+
      '<div class="btns"><button class="btn" type="button" data-tie="odd">Elegir K impar</button>'+
      '<button class="btn" type="button" data-tie="nearest">Elegir el vecino más cercano</button>'+
      '<button class="btn" type="button" data-tie="weighted">Ponderar por distancia</button></div></div>';
  }else if(res.tie&&S.tieRule!=='none'){
    tie='<p class="rule">Regla de desempate activa. <button class="btn small" type="button" data-tie="none">Quitar regla</button></p>';
  }
  var list=res.nb.map(function(nn,i){
    var p=nn.p;
    var desc=S.mode==='rain'?(p.label+': '+p.x+'% de humedad, '+fy(p.y)+' °C'):('('+fx(p.x)+', '+fy(p.y)+')');
    var right=(S.mode==='rain'?C.names[p.c]+', ':'')+'d='+fmtD(nn.d);
    return '<li><button type="button" class="nb'+((p===sel&&S.showDist)?' on':'')+'" data-i="'+i+'"><span class="dot c'+p.c+'"></span>'+
      '<span class="nbtxt">'+desc+(p.noise?'<em>dato erróneo</em>':'')+'</span><span class="nbd">'+right+'</span></button></li>';
  }).join('');
  var preds=[],chips=[1,3,5,7,9,11,13,15].map(function(kk){
    var r=knn(A.pts,A.q,kk,'none');preds.push(r.pred);
    return '<button type="button" class="chip'+(kk===S.k?' on':'')+'" data-k="'+kk+'"><span class="dot c'+r.pred+'"></span>K='+kk+'</button>';
  }).join('');
  var differ=preds.some(function(p){return p!==preds[0];});
  var chipNote=differ?'La respuesta cambia según K: un K pequeño es más sensible al ruido, uno grande suaviza.':'Todos los K coinciden aquí: el punto está bien dentro de un grupo.';
  var foot=S.mode==='rain'?'<p class="hint">KNN no aprende una fórmula: busca ejemplos parecidos y vota.</p>':'';
  var listTitle=S.mode==='rain'?('Los '+k+' días más parecidos'):('Los '+k+' vecinos más cercanos');
  el.innerHTML='<h2>Votación</h2>'+verdict+prob+bar+tie+
    '<h3>'+listTitle+'</h3><ol class="nbs">'+list+'</ol>'+
    '<h3>¿Y con otro K?</h3><div class="chips">'+chips+'</div><p class="hint">'+chipNote+'</p>'+foot;
}

function renderCalc(res){
  var el=$('#calc');
  if(!res||!S.showDist){el.hidden=true;return;}
  el.hidden=false;
  var q=cur().q,p=effSel(res),s=sc(),dx=q.x-p.x,dy=q.y-p.y,h;
  var who=S.mode==='rain'?p.label+' ':'';
  h='<h2>Cálculo de distancia</h2>'+
    '<div class="ln">Punto nuevo: ('+fx(q.x)+', '+fy(q.y)+')</div>'+
    '<div class="ln">Vecino '+who+': ('+fx(p.x)+', '+fy(p.y)+')</div>';
  if(s[0]===1){
    var sum=dx*dx+dy*dy;
    h+='<div class="ln f">d = √((x₁ '+MINUS+' x₂)² + (y₁ '+MINUS+' y₂)²)</div>'+
      '<div class="ln f">d = √(('+fx(q.x)+' '+MINUS+' '+fx(p.x)+')² + ('+fy(q.y)+' '+MINUS+' '+fy(p.y)+')²)</div>'+
      '<div class="ln f">d = √('+(dx*dx).toFixed(2)+' + '+(dy*dy).toFixed(2)+')</div>'+
      '<div class="ln f">d = √'+sum.toFixed(2)+'</div>'+
      '<div class="ln f res">d = '+Math.sqrt(sum).toFixed(2)+'</div>';
  }else{
    var C=CFG.rain,a=dx*s[0],b=dy*s[1];
    h+='<div class="ln f">Δ humedad = ('+fx(q.x)+' '+MINUS+' '+fx(p.x)+') / '+(C.xmax-C.xmin)+' = '+a.toFixed(3)+'</div>'+
      '<div class="ln f">Δ temperatura = ('+fy(q.y)+' '+MINUS+' '+fy(p.y)+') / '+(C.ymax-C.ymin)+' = '+b.toFixed(3)+'</div>'+
      '<div class="ln f">d = √('+a.toFixed(3)+'² + '+b.toFixed(3)+'²) = √'+(a*a+b*b).toFixed(4)+'</div>'+
      '<div class="ln f res">d = '+Math.sqrt(a*a+b*b).toFixed(3)+'</div>';
  }
  h+='<p class="hint">Toca otro vecino en la lista o en el plano para calcular su distancia.</p>';
  el.innerHTML=h;
}

function renderGame(){
  var el=$('#game'),g=S.G;
  var h='<h2>Modo juego</h2><label class="chk"><input type="checkbox" id="gameOn"'+(g.on?' checked':'')+'> Activar retos</label>';
  if(g.on){
    var st=function(done,pts){return done?'<div class="st">Superado. +'+pts+' puntos</div>':'<div class="st">Pendiente. Vale '+pts+' puntos</div>';};
    h+='<p class="score" style="margin-top:12px">Puntos: <strong>'+g.score+'</strong> de 45</p><ul class="ret">'+
      '<li class="'+(g.d1?'ok':'')+'"><div class="t">Reto 1: coloca un punto que sea Azul con K=3.</div>'+st(g.d1,10)+
        '<div class="st'+(g.b1?'':'')+'">'+(g.b1?'Bonus logrado: votación 2 a 1. +5':'Bonus: que la votación sea 2 a 1. Vale 5 puntos')+'</div></li>'+
      '<li class="'+(g.d2?'ok':'')+'"><div class="t">Reto 2: encuentra un lugar donde K=1 y K=7 den respuestas distintas.</div>'+st(g.d2,15)+'</li>'+
      '<li class="'+(g.d3?'ok':'')+'"><div class="t">Reto 3: con ❓ colocado, agrega un dato azul o naranja que engañe a K=1.</div>'+st(g.d3,15)+
        '<div class="st">Elige "Dato azul" o "Dato naranja" arriba y colócalo junto a ❓, en la clase contraria a la mayoría.</div></li></ul>'+
      '<button class="btn" type="button" id="gameReset">Reiniciar retos</button>';
  }
  el.innerHTML=h;
}

function checkGame(){
  var g=S.G;
  if(!g.on||S.mode!=='abstract')return;
  var q=S.A.q;if(!q)return;
  var pts=S.A.pts,m=[];
  var r3=knn(pts,q,3,'none');
  if(!g.d1&&r3.pred===0){g.d1=true;g.score+=10;m.push('Reto 1 superado: +10.');}
  if(!g.b1&&r3.pred===0&&r3.votes[0]===2&&r3.votes[1]===1){g.b1=true;g.score+=5;m.push('Bonus del reto 1: +5.');}
  var r1n=knn(pts,q,1,'none'),r7=knn(pts,q,7,'none');
  if(!g.d2&&r1n.pred!==r7.pred){g.d2=true;g.score+=15;m.push('Reto 2 superado: +15.');}
  var near=r1n.nb[0].p;
  if(!g.d3&&near.manual&&near.c!==r7.pred){g.d3=true;g.score+=15;m.push('Reto 3 superado: +15.');}
  if(m.length)say(m.join(' '));
}
function resetGame(on){
  S.G={on:on,d1:false,b1:false,d2:false,d3:false,score:0};
  S.A.q=null;S.A.sel=null;
  S.A.pts=S.A.pts.filter(function(p){return !p.manual&&!p.noise;});
  S.place='query';
  say(on?'Modo juego listo. Empieza con el reto 1.':'');
}

function syncControls(){
  var C=CFG[S.mode],A=cur();
  document.body.className='mode-'+S.mode;
  $('#tab-abstract').setAttribute('aria-selected',S.mode==='abstract');
  $('#tab-rain').setAttribute('aria-selected',S.mode==='rain');
  $('#title').textContent=C.title;$('#lead').textContent=C.lead;
  $('#k').value=S.k;$('#kout').textContent='K = '+S.k;
  $('#showDist').checked=S.showDist;$('#showBound').checked=S.showBound;$('#norm').checked=S.norm;
  $('#normHint').textContent=S.norm?'Cada variable se divide por su rango: humedad y temperatura pesan igual en la distancia.':'Sin normalizar, la humedad (rango 70) pesa más que la temperatura (rango 25) en la distancia.';
  Array.prototype.forEach.call(document.querySelectorAll('input[name=place]'),function(r){r.checked=(r.value===S.place);});
  if(S.mode==='rain'){
    $('#hum').value=A.q.x;$('#tmp').value=A.q.y;
    $('#humOut').textContent=Math.round(A.q.x)+' %';$('#tmpOut').textContent=A.q.y.toFixed(1)+' °C';
  }
  var lg=S.mode==='abstract'
    ?'<span class="lg"><i class="dot c0"></i>Clase A (azul)</span><span class="lg"><i class="dot c1"></i>Clase B (naranja)</span><span class="lg"><i class="q">?</i>Punto nuevo</span><span class="lg"><i class="ring"></i>Dato erróneo</span>'
    :'<span class="lg"><i class="dot c0"></i>No llovió</span><span class="lg"><i class="dot c1"></i>Llovió</span><span class="lg"><i class="q">?</i>Hoy</span>';
  $('#legend').innerHTML=lg;
}

function render(){
  var A=cur();
  lastRes=A.q?knn(A.pts,A.q,S.k,S.tieRule):null;
  checkGame();
  syncControls();
  draw();
  renderResult(lastRes);
  renderCalc(lastRes);
  renderGame();
  $('#note').textContent=S.msg;
}

/* ---------- Acciones ---------- */
function setQ(x,y){
  var C=CFG[S.mode],A=cur();
  x=clamp(x,C.xmin,C.xmax);y=clamp(y,C.ymin,C.ymax);
  A.q={x:S.mode==='rain'?Math.round(x):r1(x),y:r1(y)};
}
function addNoise(){
  var A=S.A;
  if(!A.q)A.q={x:6.7,y:3.6};
  var base=knn(A.pts,A.q,9,'none'),cls=base.pred,opp=1-cls;
  var dn=knn(A.pts,A.q,1,'none').nb[0].d;
  var dd=Math.max(0.1,Math.min(0.5,dn*0.6)),px=A.q.x,py=A.q.y,tries=0;
  do{
    var ang=Math.random()*Math.PI*2;
    px=r1(clamp(A.q.x+Math.cos(ang)*dd,0.2,9.8));py=r1(clamp(A.q.y+Math.sin(ang)*dd,0.2,9.8));
    tries++;
  }while(Math.hypot(px-A.q.x,py-A.q.y)>=dn&&tries<30);
  A.pts.push({x:px,y:py,c:opp,noise:true});
  S.k=1;
  say('Agregaste un dato '+(opp?'naranja':'azul')+' dentro de la nube '+(cls?'naranja':'azul')+'. Con K=1 el punto cree al dato erróneo. Sube K a 5 y mira cómo se corrige.');
}
function makeTie(){
  var A=S.A,cands=[],x,y;
  for(x=0.5;x<=9.5;x+=0.5)for(y=0.5;y<=9.5;y+=0.5){
    var r=knn(A.pts,{x:x,y:y},4,'none');
    if(r.tie&&r.nb[0].d<r.nb[1].d-1e-9)cands.push({x:x,y:y});
  }
  if(!cands.length){say('No encontré un empate con este conjunto. Prueba con "Nuevo conjunto".');return;}
  var c=cands[Math.floor(Math.random()*cands.length)];
  A.q={x:r1(c.x),y:r1(c.y)};A.sel=null;S.k=4;S.tieRule='none';
  say('Escenario de empate: con K=4, dos vecinos son azules y dos naranjas.');
}

/* ---------- Eventos ---------- */
$('#k').addEventListener('input',function(e){S.k=+e.target.value;say('');render();});
$('#hum').addEventListener('input',function(e){S.R.q.x=+e.target.value;say('');render();});
$('#tmp').addEventListener('input',function(e){S.R.q.y=r1(+e.target.value);say('');render();});
$('#showDist').addEventListener('change',function(e){S.showDist=e.target.checked;render();});
$('#showBound').addEventListener('change',function(e){S.showBound=e.target.checked;render();});
$('#norm').addEventListener('change',function(e){S.norm=e.target.checked;say('');render();});
Array.prototype.forEach.call(document.querySelectorAll('input[name=place]'),function(r){
  r.addEventListener('change',function(){S.place=r.value;render();});
});
function setMode(m){S.mode=m;cur().sel=null;say('');render();}
$('#tab-abstract').addEventListener('click',function(){setMode('abstract');});
$('#tab-rain').addEventListener('click',function(){setMode('rain');});
$('#noise').addEventListener('click',function(){addNoise();render();});
$('#mkTie').addEventListener('click',function(){makeTie();render();});
$('#clear').addEventListener('click',function(){
  S.A.pts=S.A.pts.filter(function(p){return !p.manual&&!p.noise;});
  say('Quitaste los datos agregados.');render();
});
$('#reseed').addEventListener('click',function(){
  S.seed++;S.A.pts=genAbstract(S.seed);S.A.sel=null;say('Nuevo conjunto de datos.');render();
});

$('#result').addEventListener('click',function(e){
  var b=e.target.closest('button');if(!b)return;
  if(b.dataset.i!==undefined&&lastRes){
    cur().sel=lastRes.nb[+b.dataset.i].p;S.showDist=true;render();
  }else if(b.dataset.k){
    S.k=+b.dataset.k;say('');render();
  }else if(b.dataset.tie){
    var t=b.dataset.tie;
    if(t==='odd'){S.k=S.k>=15?S.k-1:S.k+1;say('Con K='+S.k+' el número de votos ya no puede repartirse en partes iguales.');}
    else if(t==='nearest'){S.tieRule='nearest';say('Desempate: gana la clase del vecino más cercano.');}
    else if(t==='weighted'){S.tieRule='weighted';say('Desempate: cada voto pesa 1/d, así los vecinos cercanos cuentan más.');}
    else{S.tieRule='none';say('');}
    render();
  }
});
$('#game').addEventListener('change',function(e){
  if(e.target.id==='gameOn'){resetGame(e.target.checked);render();}
});
$('#game').addEventListener('click',function(e){
  if(e.target.id==='gameReset'){resetGame(true);render();}
});

var drag=false;
function pos(e){var r=cv.getBoundingClientRect();return {px:(e.clientX-r.left)*(W/r.width),py:(e.clientY-r.top)*(H/r.height)};}
cv.addEventListener('pointerdown',function(e){
  var p=pos(e),A=cur(),q=A.q;setGeo();
  if(q&&Math.hypot(p.px-X(q.x),p.py-Y(q.y))<=16){drag=true;cv.setPointerCapture(e.pointerId);return;}
  if(S.showDist&&lastRes){
    var hit=null;
    lastRes.nb.forEach(function(nn){if(!hit&&Math.hypot(p.px-X(nn.p.x),p.py-Y(nn.p.y))<=11)hit=nn;});
    if(hit){A.sel=hit.p;render();return;}
  }
  var inside=p.px>=PAD.l&&p.px<=PAD.l+geo.pw&&p.py>=PAD.t&&p.py<=PAD.t+geo.ph;
  if(!inside)return;
  var x=IX(p.px),y=IY(p.py);
  if(S.mode==='rain'||S.place==='query'){
    setQ(x,y);say('');drag=true;cv.setPointerCapture(e.pointerId);
  }else{
    A.pts.push({x:r1(x),y:r1(y),c:+S.place,manual:true});say('');
  }
  render();
});
cv.addEventListener('pointermove',function(e){
  var p=pos(e);setGeo();
  if(drag){setQ(IX(p.px),IY(p.py));say('');render();return;}
  var q=cur().q;
  cv.style.cursor=(q&&Math.hypot(p.px-X(q.x),p.py-Y(q.y))<=16)?'grab':'crosshair';
});
function endDrag(){drag=false;}
cv.addEventListener('pointerup',endDrag);
cv.addEventListener('pointercancel',endDrag);
cv.addEventListener('keydown',function(e){
  var map={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,1],ArrowDown:[0,-1]},d=map[e.key];
  if(!d)return;
  e.preventDefault();
  var A=cur(),C=CFG[S.mode],m=e.shiftKey?5:1;
  if(!A.q){A.q={x:(C.xmin+C.xmax)/2,y:(C.ymin+C.ymax)/2};}
  else setQ(A.q.x+d[0]*(S.mode==='rain'?1:0.1)*m,A.q.y+d[1]*0.1*m);
  say('');render();
});

if(window.ResizeObserver)new ResizeObserver(resize).observe($('.plane'));
window.addEventListener('resize',resize);
if(window.matchMedia){
  var mq=window.matchMedia('(prefers-color-scheme: dark)');
  if(mq.addEventListener)mq.addEventListener('change',draw);
}
new MutationObserver(draw).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});

render();
resize();
})();
</script>
</body>
</html>
