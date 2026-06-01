---
layout: default
title: 束搜索与贪心解码
permalink: /viz/beam-search/
redirect_from:
  - /v/beam-search/
---

{% raw %}
<style>
.bslab .edge{stroke:var(--color-border-strong);stroke-width:1.5;fill:none;}
.bslab .edge.greedy{stroke:#b5524a;stroke-width:3;}
.bslab .edge.beam{stroke:var(--color-forest);stroke-width:3;}
.bslab .node{fill:var(--color-bg-pure);stroke:var(--color-border-strong);stroke-width:1.4;}
.bslab .node.greedy{stroke:#b5524a;stroke-width:2.4;}
.bslab .node.beam{stroke:var(--color-forest);stroke-width:2.4;}
.bslab .node.kept{fill:#eef6f1;}
.bslab .nw{font:600 13px var(--font-serif);fill:var(--color-text);text-anchor:middle;}
.bslab .np{font:10px var(--font-mono);fill:var(--color-text-muted);text-anchor:middle;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 束搜索与贪心解码

模型给出每个词的概率后，怎么把一整句话挑出来？最简单的**贪心**：每一步都选当前概率最高的词。但这样很短视——这一步最优，未必整句最优。**束搜索**则在每一步保留概率最高的 k 条候选路径，往后多探几步，更可能找到整体得分更高的句子。看下面这棵解码树，贪心怎样掉进“局部最优”的坑，而束搜索绕开了它。

<section class="bslab vizui" id="bslab">
  <p class="vizui__lead">每条边上的数字是“接这个词”的概率，一条路径的总分是沿途概率相乘。<span style="color:#b5524a;font-weight:600">红=贪心</span>每步只挑最高的；<span style="color:var(--color-forest);font-weight:600">绿=束搜索</span>保留 k 条候选。看两者最终选出的句子和总分。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="k">束宽 k</label><input type="range" id="k" min="1" max="3" step="1" value="2" style="width:120px"><output id="kVal">2</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="verdict">—</span>
    </div>
    <svg class="vizui-chart" id="tree" viewBox="0 0 520 300" role="img" aria-label="解码树"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>贪心：每步最优</b><p>简单快，但只看眼前——第一步选了高分词，后面却接不下去好词，整句反而差。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>束搜索：留 k 条</b><p>每步保留最有希望的 k 条路径，给“先抑后扬”的句子留机会，整体更优。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>权衡</b><p>k 越大越可能找到好句，但算得越慢；k=1 就退化成贪心。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
/* 解码树：root -> 第一个词 -> 第二个词。设计成贪心会掉坑。 */
var L1=[{w:"它",p:0.6,x:200,ch:[{w:"跑",p:0.3},{w:"是",p:0.22},{w:"在",p:0.18}]},
        {w:"今天",p:0.4,x:200,ch:[{w:"天气",p:0.95},{w:"很",p:0.03}]}];
var k=2;
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var key in a)e.setAttribute(key,a[key]);p.appendChild(e);return e;}
function node(svg,x,y,w,p,cls){var g=E(svg,"g",{});E(g,"rect",{x:x-30,y:y-15,width:60,height:30,rx:8,"class":"node "+cls});
  E(g,"text",{x:x,y:y-1,"class":"nw"}).textContent=w;if(p!=null)E(g,"text",{x:x,y:y+11,"class":"np"}).textContent=p.toFixed(2);return g;}

function compute(){
  // 所有完整路径 (第一词,第二词) 总分
  var paths=[];L1.forEach(function(a){a.ch.forEach(function(b){paths.push({seq:[a.w,b.w],score:a.p*b.p,a:a,b:b});});});
  // 贪心：第一步最高 a，再它的最高 b
  var ga=L1.slice().sort(function(x,y){return y.p-x.p;})[0];
  var gb=ga.ch.slice().sort(function(x,y){return y.p-x.p;})[0];
  var greedy={seq:[ga.w,gb.w],score:ga.p*gb.p};
  // 束搜索：保留前 k 个第一词，扩展，取总分最高
  var keptA=L1.slice().sort(function(x,y){return y.p-x.p;}).slice(0,k);
  var cand=[];keptA.forEach(function(a){a.ch.forEach(function(b){cand.push({seq:[a.w,b.w],score:a.p*b.p,a:a,b:b});});});
  cand.sort(function(x,y){return y.score-x.score;});
  return {paths:paths,greedy:greedy,beam:cand[0],keptA:keptA};
}
function draw(){
  var svg=document.getElementById("tree");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var R=compute();
  var rootX=60,rootY=150;
  var l1y=[90,210];
  var greedyA=R.greedy.seq[0],greedyB=R.greedy.seq[1],beamA=R.beam.seq[0],beamB=R.beam.seq[1];
  // 边 root->L1
  L1.forEach(function(a,i){a._y=l1y[i];a._x=220;
    var cls=(a.w===greedyA?"greedy":"")||(R.keptA.indexOf(a)>=0?"beam":"");
    E(svg,"path",{d:"M90,"+rootY+" C150,"+rootY+" 160,"+a._y+" 190,"+a._y,"class":"edge "+(a.w===greedyA?"greedy":a.w===beamA?"beam":"")});
    E(svg,"text",{x:150,y:(rootY+a._y)/2-4,"class":"np"}).textContent=a.p.toFixed(2);
  });
  // L1->L2
  L1.forEach(function(a){var n=a.ch.length;a.ch.forEach(function(b,j){var by=a._y-((n-1)/2)*30+j*30; b._x=400;b._y=by;
    var isG=(a.w===greedyA&&b.w===greedyB),isB=(a.w===beamA&&b.w===beamB);
    E(svg,"path",{d:"M250,"+a._y+" C320,"+a._y+" 330,"+by+" 370,"+by,"class":"edge "+(isG?"greedy":isB?"beam":"")});
    E(svg,"text",{x:325,y:(a._y+by)/2-3,"class":"np"}).textContent=b.p.toFixed(2);
  });});
  node(svg,60,rootY,"开始",null,"");
  L1.forEach(function(a){node(svg,220,a._y,a.w,a.p,(a.w===greedyA?"greedy ":"")+(R.keptA.indexOf(a)>=0?"kept":""));});
  L1.forEach(function(a){a.ch.forEach(function(b){var isG=(a.w===greedyA&&b.w===greedyB),isB=(a.w===beamA&&b.w===beamB);
    node(svg,400,b._y,b.w,a.p*b.p,isG?"greedy":isB?"beam":"");});});
  return R;
}
function render(){
  document.getElementById("kVal").textContent=k;
  var R=draw();
  var gWin=R.greedy.score>=R.beam.score-1e-9;
  document.getElementById("verdict").textContent="贪心 “"+R.greedy.seq.join("")+"” "+R.greedy.score.toFixed(2)+"　束搜索 “"+R.beam.seq.join("")+"” "+R.beam.score.toFixed(2);
  caption(R);
}
function caption(R){
  var el=document.getElementById("caption"),same=R.greedy.seq.join("")===R.beam.seq.join("");
  if(k===1)el.innerHTML="<b>k=1：</b>束搜索退化成贪心，两者一样——都选了“"+R.greedy.seq.join("")+"”（总分 "+R.greedy.score.toFixed(2)+"）。把 k 调到 2 看差别。";
  else if(same)el.innerHTML="这次两者选了一样的句子。";
  else el.innerHTML="<b>看差别了！</b>贪心第一步贪了概率高的“"+R.greedy.seq[0]+"”，结果后面接不出好词，整句“"+R.greedy.seq.join("")+"”只有 "+R.greedy.score.toFixed(2)+"；束搜索留住了“"+R.beam.seq[0]+"”这条，后面接上高分词，整句“"+R.beam.seq.join("")+"”拿到 <b>"+R.beam.score.toFixed(2)+"</b>——整体更优。";
}
document.getElementById("k").addEventListener("input",function(e){k=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[1,2,1,2],n=0,sl=document.getElementById("k");var iv=setInterval(function(){k=seq[n];sl.value=k;render();n++;if(n>=seq.length)clearInterval(iv);},1100);},1000);
})();
</script>
{% endraw %}
