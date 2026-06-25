---
layout: default
title: 温度采样
description: "调‘温度’看模型挑下一个词的概率条重塑：低温保守稳定、高温有创意也容易胡说。"
permalink: /viz/temperature/
redirect_from:
  - /v/temperature/
---

{% raw %}
<style>
.tplab .ctx{font-family:var(--font-serif);font-size:1.2rem;text-align:center;margin:2px 0 6px;color:var(--color-text);}
.tplab .ctx b{color:var(--color-accent);}
.tplab .cand{display:flex;align-items:center;gap:10px;margin:8px 0;}
.tplab .tok{width:54px;text-align:right;font-weight:600;font-size:1.02rem;color:var(--color-text);flex-shrink:0;}
.tplab .barwrap{flex:1;height:26px;background:var(--color-bg-section);border-radius:7px;overflow:hidden;}
.tplab .bar{height:100%;background:var(--color-accent);border-radius:7px;transition:width .28s var(--ease-out),background .2s;min-width:1px;}
.tplab .pct{width:50px;font:600 .9rem var(--font-mono);color:var(--color-text-soft);flex-shrink:0;}
.tplab .cand.cut{opacity:.32;}
.tplab .cand.cut .bar{background:var(--color-text-muted);}
.tplab .cand.hot .bar{background:var(--color-gold);}
.tplab .samples{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;min-height:34px;align-items:center;}
.tplab .schip{font-family:var(--font-serif);font-size:1rem;padding:5px 11px;border-radius:8px;background:var(--color-accent-soft);border:1px solid rgba(21,94,117,.18);color:var(--color-accent);animation:pop .25s var(--ease-out);}
@keyframes pop{from{transform:scale(.6);opacity:0}to{transform:scale(1);opacity:1}}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 温度采样

大模型每写一个字，其实都是在一堆候选词里“抽签”——每个词有多大概率被抽中，由模型算出来。但抽签的“随机程度”可以调，这个旋钮就叫“温度”。温度低，它几乎只抽最稳的那个，保守但容易重复；温度高，连冷门词都有机会，有创意但也容易胡说。拖一下温度，看概率条怎么变。

<section class="vizui tplab" id="tplab">
  <p class="vizui__lead">下面是模型预测“今天天气真”之后可能接的词，以及各自的概率。温度只改变“抽签”的随机程度，不改变模型的原始打分。</p>

  <p class="ctx">今天天气真 <b id="ctxLast">…</b></p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="temp">温度 T</label>
        <input type="range" id="temp" min="0.1" max="2" step="0.05" value="1" style="width:170px">
        <output id="tempVal">1.00</output>
      </span>
      <span class="vizui-field"><label for="topp">top-p（只保留最可能的一撮）</label>
        <input type="range" id="topp" min="0.2" max="1" step="0.05" value="1" style="width:130px">
        <output id="toppVal">1.00</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="draw" type="button">🎲 采样 10 次</button>
    </div>
  </div>

  <div class="vizui-panel">
    <div id="bars"></div>
    <div class="samples" id="samples"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>低温（→0）</b><p>几乎总抽概率最高的词，输出稳定、可复现，但容易呆板、重复。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>高温（→大）</b><p>各词概率被拉平，冷门词也可能冒出来，更有创意，但也更容易跑题、胡说。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>top-p 截断</b><p>只在“最可能的一撮”词里抽签，砍掉长尾里那些离谱的选项，兼顾多样和靠谱。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var TOKS=["好","不错","热","冷","糟","蓝","鸭"];
var LOGITS=[3.0,2.4,2.1,1.6,1.0,0.4,-0.5];
var T=1.0, topp=1.0;

function softmax(z){var m=Math.max.apply(null,z),e=z.map(function(v){return Math.exp(v-m);}),s=e.reduce(function(a,b){return a+b;},0);return e.map(function(v){return v/s;});}
function probs(){return softmax(LOGITS.map(function(l){return l/T;}));}
/* top-p 掩码：按概率降序累计，保留到累计≥p（至少1个） */
function keepMask(p){
  var idx=p.map(function(v,i){return i;}).sort(function(a,b){return p[b]-p[a];});
  var cum=0,keep={},i;
  for(i=0;i<idx.length;i++){keep[idx[i]]=true;cum+=p[idx[i]];if(cum>=topp)break;}
  return keep;
}

function buildBars(){
  var host=document.getElementById("bars");host.innerHTML="";
  TOKS.forEach(function(tk,i){
    var row=document.createElement("div");row.className="cand";row.dataset.i=i;
    row.innerHTML='<span class="tok">'+tk+'</span><span class="barwrap"><span class="bar"></span></span><span class="pct"></span>';
    host.appendChild(row);
  });
}
function render(){
  document.getElementById("tempVal").textContent=T.toFixed(2);
  document.getElementById("toppVal").textContent=topp.toFixed(2);
  document.getElementById("ctxLast").textContent="？";
  var p=probs(), keep=keepMask(p);
  // 按概率排序展示
  var order=p.map(function(v,i){return i;}).sort(function(a,b){return p[b]-p[a];});
  var host=document.getElementById("bars"), rows=host.children, max=Math.max.apply(null,p);
  order.forEach(function(i,rank){
    var row=rows[rank];
    row.dataset.i=i;
    row.querySelector(".tok").textContent=TOKS[i];
    row.querySelector(".bar").style.width=(p[i]/max*100).toFixed(1)+"%";
    row.querySelector(".pct").textContent=(p[i]*100).toFixed(1)+"%";
    row.classList.toggle("cut",!keep[i]);
    row.classList.remove("hot");
  });
  caption(p,keep);
}
function caption(p,keep){
  var el=document.getElementById("caption");
  var top=p.map(function(v,i){return i;}).sort(function(a,b){return p[b]-p[a];})[0];
  var keptN=TOKS.filter(function(t,i){return keep[i];}).length;
  var msg;
  if(T<=0.3)msg="<b>温度很低（"+T.toFixed(2)+"）：</b>“"+TOKS[top]+"”的概率被推得很高，模型几乎总输出它——稳定但呆板。";
  else if(T>=1.5)msg="<b>温度很高（"+T.toFixed(2)+"）：</b>概率被拉平，连“蓝”“鸭”这种离谱的词都有机会——有创意，也容易胡说。";
  else msg="温度 "+T.toFixed(2)+"：“"+TOKS[top]+"”领先，但其他词也分到了概率；温度越高越随机。";
  if(topp<0.999)msg+=" top-p 把候选砍到最可能的 <b>"+keptN+"</b> 个，长尾里的离谱词被排除。";
  el.innerHTML=msg;
}

function sample(p,keep){
  var pool=[],sum=0,i;
  for(i=0;i<TOKS.length;i++)if(keep[i]){pool.push(i);sum+=p[i];}
  var r=Math.random()*sum,acc=0;
  for(i=0;i<pool.length;i++){acc+=p[pool[i]];if(r<=acc)return pool[i];}
  return pool[pool.length-1];
}
function draw10(){
  var p=probs(),keep=keepMask(p),host=document.getElementById("samples");host.innerHTML="";
  var counts={};
  var n=0;
  var iv=setInterval(function(){
    if(n>=10){clearInterval(iv);return;}
    var i=sample(p,keep);counts[i]=(counts[i]||0)+1;
    var c=document.createElement("span");c.className="schip";c.textContent=TOKS[i];host.appendChild(c);
    n++;
  },140);
}

document.getElementById("temp").addEventListener("input",function(e){T=+e.target.value;render();});
document.getElementById("topp").addEventListener("input",function(e){topp=+e.target.value;render();});
document.getElementById("draw").addEventListener("click",draw10);

/* 启动 + 自动演示：温度从低扫到高，再回到 1 */
buildBars();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[0.2,0.4,0.7,1.0,1.4,1.8,1.4,1.0],k=0,sl=document.getElementById("temp");
  var iv=setInterval(function(){if(k>=seq.length){clearInterval(iv);return;}T=seq[k];sl.value=T;render();k++;},620);
},900);
})();
</script>
{% endraw %}
