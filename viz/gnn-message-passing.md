---
layout: default
title: 图神经网络：消息传递
description: "节点沿边把特征传给邻居取平均，拖层数看信息扩散，以及层数太多时所有节点趋同的‘过平滑’。"
permalink: /viz/gnn-message-passing/
redirect_from:
  - /v/gnn-message-passing/
---

{% raw %}
<style>
.gnnlab svg{max-width:100%;height:auto;background:var(--color-bg-soft,#f4f1ec);border-radius:var(--radius-sm);}
.gnnlab .edge{stroke:#b9c2c7;stroke-width:2;}
.gnnlab .node{stroke:#fff;stroke-width:2;}
.gnnlab .nlbl{font:11px var(--font-mono);fill:#fff;font-weight:600;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 图神经网络：消息传递

社交网络、分子、知识图谱都是**图**：一堆节点，靠边连起来。图神经网络（GNN）处理图的核心动作叫**消息传递**：每个节点把自己的特征发给邻居，再把收到的邻居特征汇总（取平均）来更新自己。叠一层，每个节点就“认识”了它的直接邻居；叠两层，认识邻居的邻居……信息顺着边一圈圈扩散。但层数太多会出问题：所有节点越来越像，最后糊成一团、谁也分不出谁——这叫**过平滑**。拖动“传播层数”，看两簇泾渭分明的节点怎样慢慢被“熨平”成一锅粥。

<section class="vizui gnnlab" id="gnnlab">
  <p class="vizui__lead">两簇节点：左簇初始值高（<span style="color:#b5524a">红</span>），右簇初始值低（<span style="color:#2563eb">蓝</span>），中间一个桥节点。每传播一层，节点 = 自己和邻居的平均。看颜色怎样沿边扩散、最终趋同。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="L">传播层数</label><input type="range" id="L" min="0" max="9" step="1" value="0" style="width:170px"><output id="lVal">0</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 360 220" role="img" aria-label="图消息传递"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>消息传递</b><p>节点收邻居特征、取平均更新自己。这是几乎所有 GNN 的统一框架。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>多层=看更远</b><p>L 层后，每个节点融合了 L 跳范围内的信息，感受野沿图结构扩大。</p></div>
    <div class="card" style="--wc:#b5524a"><b>过平滑陷阱</b><p>层数太多，所有节点趋同、特征被“熨平”，反而分不开——GNN 通常不宜太深。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var pos=[[55,60],[105,32],[118,98],[55,140],[180,80],[250,42],[305,80],[292,140],[238,118]];
var edges=[[0,1],[0,2],[1,2],[2,3],[0,3],[2,4],[4,5],[5,6],[6,7],[7,8],[5,8],[6,8],[3,5],[1,6]];
var init=[0.92,0.9,0.88,0.9,0.5,0.1,0.08,0.1,0.12],N=9;
var adj=[];for(var i=0;i<N;i++)adj.push([]);edges.forEach(function(e){adj[e[0]].push(e[1]);adj[e[1]].push(e[0]);});
function propagate(L){var v=init.slice();for(var t=0;t<L;t++){var nv=[];for(var i=0;i<N;i++){var s=v[i],c=1;adj[i].forEach(function(j){s+=v[j];c++;});nv.push(s/c);}v=nv;}return v;}
var L=0,SVGNS="http://www.w3.org/2000/svg";
function col(v){var t=v<0?0:v>1?1:v,b=[37,99,235],w=[238,236,232],r=[181,82,74],a,c;if(t<0.5){a=t/0.5;c=[b[0]+(w[0]-b[0])*a,b[1]+(w[1]-b[1])*a,b[2]+(w[2]-b[2])*a];}else{a=(t-0.5)/0.5;c=[w[0]+(r[0]-w[0])*a,w[1]+(r[1]-w[1])*a,w[2]+(r[2]-w[2])*a];}return"rgb("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+")";}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var v=propagate(L);
  edges.forEach(function(e){E(svg,"line",{x1:pos[e[0]][0],y1:pos[e[0]][1],x2:pos[e[1]][0],y2:pos[e[1]][1],"class":"edge"});});
  for(var i=0;i<N;i++){E(svg,"circle",{cx:pos[i][0],cy:pos[i][1],r:16,fill:col(v[i]),"class":"node"});E(svg,"text",{x:pos[i][0],y:pos[i][1]+4,"text-anchor":"middle","class":"nlbl",fill:(v[i]>0.55||v[i]<0.18)?"#fff":"#444"},v[i].toFixed(2));}
  var mu=0;v.forEach(function(x){mu+=x;});mu/=N;var vr=0;v.forEach(function(x){vr+=(x-mu)*(x-mu);});vr/=N;
  document.getElementById("lVal").textContent=L;
  document.getElementById("stat").textContent="节点间差异（方差）"+(vr*1000).toFixed(0)+"‰";
  caption(vr);
}
function caption(vr){
  var el=document.getElementById("caption");
  if(L===0)el.innerHTML="<b>0 层：</b>两簇节点颜色分明、各有特色（差异大）。点开传播，看消息怎样沿边扩散。";
  else if(vr>0.04)el.innerHTML="<b>"+L+" 层：</b>颜色开始沿边混合——红簇被邻居拉低、蓝簇被拉高，信息在扩散，但两簇还分得出。";
  else el.innerHTML="<b>"+L+" 层：</b>所有节点颜色几乎一样了（差异降到 "+(vr*1000).toFixed(0)+"‰），泾渭不再分明——这就是<b>过平滑</b>：层数太多，特征被熨平，节点反而没法区分。";
}
document.getElementById("L").addEventListener("input",function(e){L=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){L=8;document.getElementById("L").value=8;render();return;}
  var seq=[1,2,3,5,8],k=0,sl=document.getElementById("L");var iv=setInterval(function(){L=seq[k];sl.value=L;render();k++;if(k>=seq.length)clearInterval(iv);},950);},1000);
})();
</script>
{% endraw %}
