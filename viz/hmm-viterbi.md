---
layout: default
title: HMM 维特比解码
permalink: /viz/hmm-viterbi/
redirect_from:
  - /v/hmm-viterbi/
---

{% raw %}
<style>
.hvlab svg{max-width:100%;height:auto;}
.hvlab .edge{stroke:var(--color-border-strong);stroke-width:1.5;fill:none;}
.hvlab .edge.win{stroke:var(--color-accent);stroke-width:2.4;opacity:.8;}
.hvlab .edge.best{stroke:var(--color-accent);stroke-width:4;opacity:1;}
.hvlab .node{stroke:#fff;stroke-width:2;}
.hvlab .node.best{stroke:var(--color-accent);stroke-width:3.5;}
.hvlab .nlbl{font:13px var(--font-sans);fill:#fff;font-weight:700;}
.hvlab .dval{font:10px var(--font-mono);fill:var(--color-text-muted);}
.hvlab .obs{font:12px var(--font-sans);fill:var(--color-text-soft);}
.hvlab .obschip{fill:var(--color-bg-section);stroke:var(--color-border);stroke-width:1;}
.hvlab .obschip.cur{stroke:var(--color-accent);stroke-width:2;}
.hvlab .day{font:10px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# HMM 维特比解码：从观测倒推隐藏状态

天气（**晴 / 雨**）你看不见，但能看见路人**带没带伞**——这就是隐马尔可夫模型：隐藏状态一天天按概率转移，每个状态又按概率“发射”出一个观测。给定一串观测，哪条隐藏天气序列最可能？逐天逐状态枚举会指数爆炸；**维特比算法**用动态规划只保留“到达每个状态的最优路径”：每个节点只记住一个最好的前驱，最后从终点回溯，就得到全局最优路径。点“下一步”，看每个节点怎样在两个前驱里挑赢家，最后回溯出整条最可能的天气。

<section class="vizui hvlab" id="hvlab">
  <p class="vizui__lead">上排是每天的观测；网格每列是一天、两行是两种天气（<span style="color:#b7791f">晴</span> / <span style="color:#2563eb">雨</span>）。节点里的小数是<b>到此为止最优路径的概率 δ</b>，颜色越深表示该天它越可能。<span style="color:var(--color-accent)">青色粗线</span>是每个节点选中的最优前驱；解完后串起来就是<b>最优路径</b>。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="step" type="button">▶ 下一步</button>
      <button class="vizui-btn" id="auto" type="button">自动</button>
      <button class="vizui-btn" id="seq" type="button">↻ 换观测</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 480 250" role="img" aria-label="HMM 维特比网格"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>转移 × 发射</b><p>到某状态的得分＝前驱得分 × 转移概率 × 当天发射概率，逐天相乘。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>只留最优前驱</b><p>每个节点只记一个最好的来路，指数级的路径枚举被压成逐列的动态规划。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>回溯得全局最优</b><p>从概率最大的终点沿记下的前驱往回走，串出的就是整体最可能的隐藏序列。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var STATES=["晴","雨"],SC=["#b7791f","#2563eb"],OBS=["没伞","带伞"];
var PI=[0.6,0.4],A=[[0.7,0.3],[0.4,0.6]],B=[[0.9,0.1],[0.2,0.8]];
var PRES=[[0,0,1,1,0],[1,0,1,1,0],[1,1,0,1,1]],pidx=0;
var obs=PRES[0],T=obs.length,rev=0,timer=null,playing=false,delta,psi,path;
function viterbi(){
  delta=[];psi=[];
  delta[0]=[PI[0]*B[0][obs[0]],PI[1]*B[1][obs[0]]];psi[0]=[-1,-1];
  for(var t=1;t<T;t++){delta[t]=[];psi[t]=[];
    for(var s=0;s<2;s++){var best=-1,bp=0;
      for(var p=0;p<2;p++){var v=delta[t-1][p]*A[p][s];if(v>best){best=v;bp=p;}}
      delta[t][s]=best*B[s][obs[t]];psi[t][s]=bp;}}
  path=[];var last=delta[T-1][0]>=delta[T-1][1]?0:1;path[T-1]=last;
  for(var t=T-1;t>0;t--)path[t-1]=psi[t][path[t]];
}
var SVGNS="http://www.w3.org/2000/svg";
function colX(t){return 46+t*((480-92)/Math.max(1,T-1));}
function rowY(s){return s===0?92:174;}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function fmt(v){return v>=0.001?v.toFixed(3):v.toExponential(1);}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var done=(rev>=T);
  /* 观测条 */
  for(var t=0;t<T;t++){var cx=colX(t);
    E(svg,"text",{x:cx,y:14,"text-anchor":"middle","class":"day"},"第"+(t+1)+"天");
    var w=44;E(svg,"rect",{x:cx-w/2,y:20,width:w,height:22,rx:6,"class":"obschip"+(t===rev-1&&!done?" cur":""),opacity:(t<rev?1:0.35)});
    E(svg,"text",{x:cx,y:35,"text-anchor":"middle","class":"obs",opacity:(t<rev?1:0.35)},OBS[obs[t]]);}
  /* 边：进入已揭示的每一列 */
  for(var t=1;t<rev;t++){for(var s=0;s<2;s++){for(var p=0;p<2;p++){
    var win=(psi[t][s]===p);
    E(svg,"line",{x1:colX(t-1),y1:rowY(p),x2:colX(t),y2:rowY(s),"class":"edge"+(win?" win":""),opacity:win?0.8:0.3});}}}
  /* 最优路径（解完后） */
  if(done){for(var t=1;t<T;t++)E(svg,"line",{x1:colX(t-1),y1:rowY(path[t-1]),x2:colX(t),y2:rowY(path[t]),"class":"edge best"});}
  /* 节点 */
  for(var t=0;t<rev;t++){var mx=Math.max(delta[t][0],delta[t][1]);
    for(var s=0;s<2;s++){var cx=colX(t),cy=rowY(s),norm=mx>0?delta[t][s]/mx:0,onPath=done&&path[t]===s;
      E(svg,"circle",{cx:cx,cy:cy,r:19,fill:SC[s],"fill-opacity":(0.25+0.65*norm).toFixed(2),"class":"node"+(onPath?" best":"")});
      E(svg,"text",{x:cx,y:cy+5,"text-anchor":"middle","class":"nlbl"},STATES[s]);
      E(svg,"text",{x:cx,y:(s===0?cy-26:cy+34),"text-anchor":"middle","class":"dval"},fmt(delta[t][s]));}}
  document.getElementById("stat").textContent=rev===0?"未开始":(done?"最优路径已解出":("已算到第 "+rev+" 天"));
  caption(done);
}
function caption(done){
  var el=document.getElementById("caption");
  if(rev===0){el.innerHTML="观测序列已给出（上排）。点“下一步”，从第 1 天开始逐列计算到达每种天气的最优概率 δ。";return;}
  if(!done){var t=rev-1;
    if(t===0){el.innerHTML="<b>第 1 天</b>（"+OBS[obs[0]]+"）：δ＝初始概率 × 发射概率。晴 "+fmt(delta[0][0])+"、雨 "+fmt(delta[0][1])+"——"+(delta[0][0]>delta[0][1]?"今天更像晴":"今天更像雨")+"。";return;}
    var s0=psi[t][0]===0?"晴":"雨",s1=psi[t][1]===0?"晴":"雨";
    el.innerHTML="<b>第 "+(t+1)+" 天</b>（"+OBS[obs[t]]+"）：到“晴”的最优前驱选了<b>"+s0+"</b>，到“雨”的选了<b>"+s1+"</b>（青线）。每个节点只留一个最好的来路——这就是动态规划省下的指数枚举。";return;}
  var seq=path.map(function(s){return STATES[s];}).join("");
  el.innerHTML="<b>回溯完成：</b>从概率最大的终点沿青色前驱往回走，最可能的天气是 <b>"+seq+"</b>（观测 "+obs.map(function(o){return OBS[o];}).join("、")+"）。带伞的日子被推成雨、没伞推成晴，转移概率又让它不会一天一变。";
}
function go(){if(rev>=T)return false;rev++;render();return true;}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="自动";}
function reset(){stop();viterbi();rev=0;render();}
document.getElementById("step").addEventListener("click",function(){stop();go();});
document.getElementById("auto").addEventListener("click",function(){if(playing){stop();return;}
  if(rev>=T){rev=0;render();}playing=true;document.getElementById("auto").textContent="⏸ 暂停";
  timer=setInterval(function(){if(!go())stop();},950);});
document.getElementById("seq").addEventListener("click",function(){stop();pidx=(pidx+1)%PRES.length;obs=PRES[pidx];T=obs.length;reset();});
document.getElementById("reset").addEventListener("click",reset);
viterbi();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){rev=T;render();return;}
  document.getElementById("auto").click();},1000);
})();
</script>
{% endraw %}

## 延伸阅读

<div class="resource-grid">
  <a class="resource-card" href="https://en.wikipedia.org/wiki/Viterbi_algorithm" target="_blank" rel="noopener">
    <h3>维特比算法（维基百科）↗</h3>
    <p>动态规划求最优状态序列的标准推导，含与本页一致的天气—活动示例。</p>
  </a>
  <a class="resource-card" href="https://web.stanford.edu/~jurafsky/slp3/A.pdf" target="_blank" rel="noopener">
    <h3>《Speech and Language Processing》附录 A · HMM ↗</h3>
    <p>Jurafsky &amp; Martin 对 HMM、前向算法与维特比的清晰讲解（英文 PDF）。</p>
  </a>
</div>
