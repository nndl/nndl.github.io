---
layout: default
title: RNN 隐状态：滚动的记忆
permalink: /viz/rnn-unroll/
redirect_from:
  - /v/rnn-unroll/
---

{% raw %}
<style>
.rulab svg{max-width:100%;height:auto;}
.rulab .tok{fill:#dceaf5;stroke:#9aa3a8;stroke-width:1;}
.rulab .cell{fill:#ece3f5;stroke:var(--color-purple,#7c5cbf);stroke-width:1.5;}
.rulab .cell.on{fill:#e2d2f5;stroke-width:2.5;}
.rulab .ttext{font:13px var(--font-sans);fill:#1a1a1a;}
.rulab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
.rulab .rec{stroke:var(--color-forest);stroke-width:2;fill:none;}
.rulab .inp{stroke:#9aa3a8;stroke-width:1.5;fill:none;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# RNN 隐状态：滚动的记忆

循环神经网络（RNN）读一句话，不是一眼看完，而是**一个词一个词地读**，边读边在心里记一份“笔记”——这份笔记就是**隐状态**。每读一个新词，它把笔记和新词揉在一起，更新成新的笔记，再往下传。关键有两点：①这份笔记是一份**滚动的记忆**，把前面看过的都压缩在里面；②每一步用的是**同一套权重**（同一个 RNN 单元反复使用）。点“下一步”，看隐状态怎样一格一格被读进来的词改写、向右传递。

<section class="vizui rulab" id="rulab">
  <p class="vizui__lead">底部是依次读入的词；中间紫色是 RNN 单元（每步都是同一个）；上面 4 根小条是隐状态向量（<span style="color:#2563eb">蓝负</span>/<span style="color:#b5524a">红正</span>）。绿色箭头是上一份笔记传给下一步。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="step" type="button">▶ 下一步</button>
      <button class="vizui-btn" id="auto" type="button">自动</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">读了 0 个词</span>
    </div>
    <svg id="plane" viewBox="0 0 500 250" role="img" aria-label="RNN 隐状态展开"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-forest)"><b>隐状态=滚动记忆</b><p>它把读过的内容压缩进一个向量，一路携带、不断更新。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>权重共享</b><p>每个时间步用的是同一套参数——所以 RNN 能处理任意长度的序列。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>顺序处理</b><p>信息从左到右一步步流动，天然适合语言、语音、时间序列。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var toks=["我","爱","科幻","电影","。"],D=4,N=toks.length;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
var r=rng(7);
function mat(R,C,sc){var m=[];for(var i=0;i<R;i++){m.push([]);for(var j=0;j<C;j++)m[i].push((r()*2-1)*sc);}return m;}
var Wh=mat(D,D,0.5),Wx=mat(D,D,0.7),emb=[];for(var t=0;t<N;t++){var e=[];for(var d=0;d<D;d++)e.push((r()*2-1));emb.push(e);}
var H=[];(function(){var h=[0,0,0,0];for(var t=0;t<N;t++){var nh=[];for(var i=0;i<D;i++){var s=0;for(var j=0;j<D;j++)s+=Wh[i][j]*h[j]+Wx[i][j]*emb[t][j];nh.push(Math.tanh(s*0.6));}h=nh;H.push(h.slice());}})();
var step=0,timer=null,SVGNS="http://www.w3.org/2000/svg";
var colW=92,x0=20,cellY=120,tokY=200,hY=30;
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function col(v){return v<0?"#2563eb":"#b5524a";}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var defs=E(svg,"defs",{});[["ruArrowG","var(--color-forest)"],["ruArrowS","#9aa3a8"]].forEach(function(m){var mk=E(defs,"marker",{id:m[0],markerUnits:"userSpaceOnUse",markerWidth:8,markerHeight:8,refX:6,refY:3,orient:"auto"});E(mk,"path",{d:"M0,0 L6,3 L0,6 z",fill:m[1]});});
  for(var t=0;t<step;t++){
    var cx=x0+t*colW+30;
    // recurrence arrow from prev hidden chain
    if(t>0)E(svg,"line",{x1:x0+(t-1)*colW+30+22,y1:cellY+16,x2:cx-22,y2:cellY+16,"class":"rec","marker-end":"url(#ruArrowG)"});
    // input arrow
    E(svg,"line",{x1:cx,y1:tokY-4,x2:cx,y2:cellY+34,"class":"inp","marker-end":"url(#ruArrowS)"});
    // token
    var w=Math.max(34,toks[t].length*15+12);
    E(svg,"rect",{x:cx-w/2,y:tokY,width:w,height:28,rx:5,"class":"tok"});
    E(svg,"text",{x:cx,y:tokY+19,"text-anchor":"middle","class":"ttext"},toks[t]);
    // cell
    var on=(t===step-1);
    E(svg,"rect",{x:cx-22,y:cellY,width:44,height:34,rx:6,"class":"cell"+(on?" on":"")});
    E(svg,"text",{x:cx,y:cellY+22,"text-anchor":"middle","class":"lbl",style:"fill:#6a4fa0"},"RNN");
    // hidden bars
    var h=H[t];
    for(var d=0;d<D;d++){var bh=Math.abs(h[d])*26,bx=cx-20+d*10;E(svg,"rect",{x:bx,y:hY+30-(h[d]>0?bh:0),width:8,height:bh,fill:col(h[d]),rx:1});}
    E(svg,"text",{x:cx,y:hY+46,"text-anchor":"middle","class":"lbl"},"h"+(t+1));
  }
  E(svg,"text",{x:x0,y:hY+8,"class":"lbl"},"隐状态");
  document.getElementById("stat").textContent="读了 "+step+" 个词";
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  if(step===0)el.innerHTML="还没开始读。点“下一步”，RNN 会读入第一个词、生成第一份笔记（隐状态 h₁）。";
  else if(step<N)el.innerHTML="读到第 "+step+" 个词“"+toks[step-1]+"”：RNN 把<b>上一份笔记 h"+(step-1||"₀")+"</b>和这个新词揉在一起，更新成 <b>h"+step+"</b>。注意中间的 RNN 单元每步都一样。";
  else el.innerHTML="整句读完。最后那份笔记 <b>h"+N+"</b> 浓缩了整句话的信息，可以拿去做分类、翻译等任务。隐状态就是这样一路滚动、携带记忆的。";
}
function next(){if(step>=N)return;step++;render();}
document.getElementById("step").addEventListener("click",next);
document.getElementById("auto").addEventListener("click",function(){if(timer)return;timer=setInterval(function(){next();if(step>=N){clearInterval(timer);timer=null;}},800);});
document.getElementById("reset").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;}step=0;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){step=N;render();return;}
  timer=setInterval(function(){next();if(step>=N){clearInterval(timer);timer=null;}},850);},1000);
})();
</script>
{% endraw %}
