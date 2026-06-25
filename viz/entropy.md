---
layout: default
title: 熵、交叉熵与 KL 散度
description: "拖动预测分布，看熵、交叉熵、KL 散度怎么变——几乎所有分类损失函数的根基。"
permalink: /viz/entropy/
redirect_from:
  - /v/entropy/
---

{% raw %}
<style>
.enlab .cats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;}
.enlab .cat{text-align:center;}
.enlab .cat .nm{font-family:var(--font-serif);font-size:1.1rem;margin-bottom:6px;}
.enlab .twin{display:flex;gap:6px;align-items:flex-end;justify-content:center;height:110px;}
.enlab .col{width:30px;display:flex;flex-direction:column;justify-content:flex-end;height:100%;}
.enlab .col .bar{border-radius:4px 4px 0 0;transition:height .25s var(--ease-out);}
.enlab .col.p .bar{background:var(--color-text-muted);}
.enlab .col.q .bar{background:var(--color-accent);}
.enlab .col .v{font:600 .7rem var(--font-mono);color:var(--color-text-muted);}
.enlab .qrange{width:100%;margin-top:8px;accent-color:var(--color-accent);}
.enlab .nums{display:flex;flex-wrap:wrap;gap:10px 22px;justify-content:center;margin-top:6px;}
.enlab .num{text-align:center;}
.enlab .num b{display:block;font:700 1.4rem var(--font-mono);}
.enlab .num span{font-size:.8rem;color:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 熵、交叉熵与 KL 散度

这三个词是信息论的核心，也是几乎所有分类模型损失函数的根。**熵**衡量一个分布有多“不确定”（越接近均匀越大）。**交叉熵**衡量：用你预测的分布 Q 去编码真实分布 P 的数据，平均要花多少代价——Q 越偏离真实 P，代价越高。两者之差就是 **KL 散度**，专门量化“Q 离 P 有多远”，且 Q=P 时正好为 0。训练分类器，本质就是调 Q 让交叉熵（也就是 KL）最小。拖动下面预测分布的滑块，看三个量怎么变。

<section class="enlab vizui" id="enlab">
  <p class="vizui__lead">灰条是<b>真实分布 P</b>（这张图正确答案大概率是“猫”），蓝条是你的<b>预测分布 Q</b>（拖滑块调整）。让 Q 越贴近 P，交叉熵越小、KL 越接近 0。</p>

  <div class="vizui-panel">
    <div class="cats" id="cats"></div>
    <div style="text-align:center;margin-top:12px"><button class="vizui-btn vizui-btn--go" id="match" type="button">把 Q 对齐到 P</button> <button class="vizui-btn" id="uniform" type="button">Q 变均匀</button></div>
    <div class="nums">
      <div class="num"><b id="hp" style="color:var(--color-text-soft)">—</b><span>熵 H(P)</span></div>
      <div class="num"><b id="ce" style="color:var(--color-accent)">—</b><span>交叉熵 H(P,Q)</span></div>
      <div class="num"><b id="kl" style="color:var(--color-gold)">—</b><span>KL 散度</span></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-text-muted)"><b>熵 = 不确定度</b><p>一个分布越接近均匀（什么都可能），熵越大；越确定（集中在一类），熵越小。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>交叉熵 = 损失</b><p>预测 Q 离真实 P 越远，交叉熵越大。分类模型就是在最小化它。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>KL = 交叉熵 − 熵</b><p>纯粹衡量 Q 与 P 的差距，Q=P 时为 0，永远 ≥ 0。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var CATS=["猫","狗","鸟","鱼"], P=[0.6,0.25,0.1,0.05], Qraw=[1,1,1,1];
function Qn(){var s=Qraw.reduce(function(a,b){return a+b;},0);return Qraw.map(function(v){return Math.max(1e-4,v/s);});}
function build(){
  var host=document.getElementById("cats");host.innerHTML="";
  CATS.forEach(function(c,i){var d=document.createElement("div");d.className="cat";
    d.innerHTML='<div class="nm">'+c+'</div><div class="twin"><div class="col p"><div class="bar" id="pb'+i+'"></div><div class="v">P</div></div><div class="col q"><div class="bar" id="qb'+i+'"></div><div class="v">Q</div></div></div>'+
      '<input class="qrange" type="range" min="0.02" max="1" step="0.02" value="'+Qraw[i]+'" data-i="'+i+'">';
    host.appendChild(d);});
  host.querySelectorAll("input").forEach(function(inp){inp.addEventListener("input",function(e){Qraw[+e.target.dataset.i]=+e.target.value;render();});});
}
function render(){
  var Q=Qn();
  for(var i=0;i<4;i++){document.getElementById("pb"+i).style.height=(P[i]*92)+"px";document.getElementById("qb"+i).style.height=(Q[i]*92)+"px";}
  var hp=0,ce=0;for(var j=0;j<4;j++){if(P[j]>0)hp-=P[j]*Math.log2(P[j]);ce-=P[j]*Math.log2(Q[j]);}
  var kl=ce-hp;
  document.getElementById("hp").textContent=hp.toFixed(2);
  document.getElementById("ce").textContent=ce.toFixed(2);
  document.getElementById("kl").textContent=kl.toFixed(2);
  caption(kl,ce,hp);
}
function caption(kl,ce,hp){
  var el=document.getElementById("caption");
  if(kl<0.03)el.innerHTML="<b>Q ≈ P：</b>预测和真实几乎一致，KL ≈ 0，交叉熵 "+ce.toFixed(2)+" 降到了它的下限——也就是熵 H(P)="+hp.toFixed(2)+"。这就是分类训练的目标。";
  else if(kl>0.8)el.innerHTML="<b>Q 离 P 很远：</b>预测严重偏离真实，KL 高达 "+kl.toFixed(2)+"，交叉熵 "+ce.toFixed(2)+" 也很大——模型会因此受到很大的惩罚（损失大）。";
  else el.innerHTML="当前 KL = "+kl.toFixed(2)+"，交叉熵 = "+ce.toFixed(2)+"（= 熵 "+hp.toFixed(2)+" + KL "+kl.toFixed(2)+"）。把蓝条调得更像灰条，KL 会继续往 0 走。";
}
function animTo(target){var start=Qraw.slice(),k=0;var iv=setInterval(function(){k++;var t=k/16;for(var i=0;i<4;i++)Qraw[i]=start[i]+(target[i]-start[i])*t;
  document.querySelectorAll("#cats input").forEach(function(inp,i){inp.value=Qraw[i];});render();if(k>=16)clearInterval(iv);},45);}
document.getElementById("match").addEventListener("click",function(){animTo(P.slice());});
document.getElementById("uniform").addEventListener("click",function(){animTo([0.25,0.25,0.25,0.25]);});
build();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){Qraw=P.slice();document.querySelectorAll("#cats input").forEach(function(inp,i){inp.value=Qraw[i];});render();return;}
  Qraw=[0.25,0.25,0.25,0.25];document.querySelectorAll("#cats input").forEach(function(inp,i){inp.value=Qraw[i];});render();
  setTimeout(function(){animTo(P.slice());},1200);},1000);
})();
</script>
{% endraw %}
