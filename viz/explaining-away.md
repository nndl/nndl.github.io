---
layout: default
title: 解释消除（贝叶斯网络）
permalink: /viz/explaining-away/
redirect_from:
  - /v/explaining-away/
---

{% raw %}
<style>
.ealab .edge{stroke:var(--color-border-strong);stroke-width:2.2;fill:none;}
.ealab .nodebox{stroke-width:2.4;cursor:pointer;rx:14;}
.ealab .nodebox.obs{stroke-width:3.4;}
.ealab .ntitle{font:700 15px var(--font-sans);}
.ealab .nprob{font:700 13px var(--font-mono);}
.ealab .barbg{fill:var(--color-bg-section);stroke:var(--color-border);stroke-width:1;}
.ealab .barfg{stroke:none;}
.ealab .pin{font:700 13px var(--font-sans);}
.ealab .hint{font:11px var(--font-sans);fill:var(--color-text-muted);}
.ealab svg{touch-action:manipulation;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 解释消除（贝叶斯网络）

草坪湿了，可能是**下雨**，也可能是**洒水器**开过。两个原因本来互不相干——下不下雨和有没有开洒水器毫无关系。可一旦看到草是湿的，两个原因的可能性**都会同时上升**：总得有人为这摊水负责。妙处在下一步：要是你又确认了“昨晚确实下雨了”，那这摊水已经有了着落，洒水器的嫌疑反而被**压了回去**——明明它俩先验独立，却在观测之后变得此消彼长。这就是**解释消除**，也是贝叶斯网络里“对撞结构”的招牌现象。**点节点**给它派证据，看概率怎么动。

<section class="vizui ealab" id="ealab">
  <p class="vizui__lead">三个节点组成一张因果图：<span style="color:var(--color-accent-light);font-weight:600">下雨 R</span> 和 <span style="color:var(--color-gold);font-weight:600">洒水器 S</span> 各指向 <span style="color:var(--color-forest);font-weight:600">草湿 W</span>。条形是每个原因当前的概率；被钉住的节点是“已观测”的证据。点任意节点循环切换：未知 → 观测为“是” → 观测为“否” → 未知。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="story" type="button">▶ 演示解释消除</button>
      <button class="vizui-btn" id="reset" type="button">重置（无证据）</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stage">阶段：先验</span>
    </div>
    <svg class="vizui-chart" id="net" viewBox="0 0 460 320" style="max-width:480px;margin:0 auto" role="img" aria-label="下雨、洒水器、草湿的贝叶斯网络"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>结果把原因都点亮</b><p>共同结果一旦被观测——草湿了，下雨和洒水器的概率会<b>同时</b>上升，因为总要有原因来解释它。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>解释消除</b><p>已知确实下雨了，这摊水就有了交代，于是洒水器的概率被<b>压回去</b>——一个原因解释了结果，另一个就没那么必要。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>对撞结构的脾气</b><p>两个原因本来相互独立，却因为<b>共享一个结果</b>，在观测之后变得相互竞争——这正是对撞（collider）结构的特性。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
// 噪声-或参数（与正文一致）
var PR=0.2, PS=0.3, leak=0.05, qR=0.8, qS=0.8;
// 证据：null=未知, 1=观测为是, 0=观测为否
var ev={R:null,S:null,W:null};
var timer=null;
function pW(R,S){return 1-(1-leak)*Math.pow(1-qR,R)*Math.pow(1-qS,S);}
function priorRS(R,S){return (R?PR:1-PR)*(S?PS:1-PS);}
// 枚举 R,S,W∈{0,1}，按当前证据过滤、求边缘后验
function posterior(){
  var num={R:0,S:0,W:0}, tot=0;
  for(var R=0;R<2;R++)for(var S=0;S<2;S++)for(var W=0;W<2;W++){
    if(ev.R!==null&&ev.R!==R)continue;
    if(ev.S!==null&&ev.S!==S)continue;
    if(ev.W!==null&&ev.W!==W)continue;
    var pw=W?pW(R,S):1-pW(R,S);
    var w=priorRS(R,S)*pw;
    tot+=w; if(R)num.R+=w; if(S)num.S+=w; if(W)num.W+=w;
  }
  return tot>0?{R:num.R/tot,S:num.S/tot,W:num.W/tot}:{R:NaN,S:NaN,W:NaN};
}
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,at){var e=document.createElementNS(SVGNS,t);for(var k in at)e.setAttribute(k,at[k]);p.appendChild(e);return e;}
// 节点几何
var NW=126,NH=70;
var nodes={
  R:{x:24,y:26,title:"下雨 R",col:"var(--color-accent-light)",cc:"#2563eb"},
  S:{x:310,y:26,title:"洒水器 S",col:"var(--color-gold)",cc:"#b7791f"},
  W:{x:167,y:206,title:"草湿 W",col:"var(--color-forest)",cc:"#2f7d4f"}
};
function cx(n){return nodes[n].x+NW/2;}
function bottom(n){return nodes[n].y+NH;}
function drawEdge(svg,a,b){
  var x1=cx(a),y1=bottom(a),x2=cx(b),y2=nodes[b].y;
  // 终点略上移给箭头留位
  var an=Math.atan2(y2-y1,x2-x1),ex=x2-12*Math.cos(an),ey=y2-12*Math.sin(an);
  E(svg,"line",{x1:x1,y1:y1,x2:ex,y2:ey,"class":"edge"});
  var L=11;
  E(svg,"line",{x1:ex,y1:ey,x2:ex-L*Math.cos(an-0.42),y2:ey-L*Math.sin(an-0.42),"class":"edge"});
  E(svg,"line",{x1:ex,y1:ey,x2:ex-L*Math.cos(an+0.42),y2:ey-L*Math.sin(an+0.42),"class":"edge"});
}
function drawNode(svg,n,prob){
  var nd=nodes[n],e=ev[n],obs=(e!==null);
  // 观测节点：实心淡填充 + 加粗边；推断节点：白底
  // 观测为“是”：节点色淡填充(opacity .16)；观测为“否”：灰底；推断：白底
  var fill=obs?(e?nd.col:"var(--color-bg-section)"):"var(--color-bg-pure)";
  var fo=(obs&&e)?0.16:1;
  E(svg,"rect",{x:nd.x,y:nd.y,width:NW,height:NH,fill:fill,"fill-opacity":fo,stroke:nd.col,"class":"nodebox"+(obs?" obs":""),"data-n":n});
  E(svg,"text",{x:nd.x+12,y:nd.y+22,"class":"ntitle",fill:nd.cc,"data-n":n,style:"pointer-events:none"}).textContent=nd.title;
  if(obs){
    var tag=e?"✓ 观测：是":"✗ 观测：否";
    E(svg,"text",{x:nd.x+12,y:nd.y+48,"class":"pin",fill:e?nd.cc:"var(--color-text-muted)","data-n":n,style:"pointer-events:none"}).textContent=tag;
  }else{
    // 概率条
    var bx=nd.x+12,by=nd.y+40,bw=NW-24,bh=14;
    E(svg,"rect",{x:bx,y:by,width:bw,height:bh,"class":"barbg","data-n":n,style:"pointer-events:none"});
    E(svg,"rect",{x:bx,y:by,width:Math.max(0,bw*prob),height:bh,fill:nd.col,"class":"barfg","data-n":n,style:"pointer-events:none"});
    E(svg,"text",{x:nd.x+NW-12,y:nd.y+34,"text-anchor":"end","class":"nprob",fill:nd.cc,"data-n":n,style:"pointer-events:none"}).textContent="P = "+(prob*100).toFixed(0)+"%";
  }
}
function draw(){
  var svg=document.getElementById("net");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var post=posterior();
  drawEdge(svg,"R","W");drawEdge(svg,"S","W");
  drawNode(svg,"R",post.R);drawNode(svg,"S",post.S);drawNode(svg,"W",post.W);
  E(svg,"text",{x:230,y:314,"text-anchor":"middle","class":"hint"}).textContent="点节点切换证据：未知 → 是 → 否 → 未知";
  return post;
}
function fmt(p){return isNaN(p)?"—":(p*100).toFixed(0)+"%";}
function stageLabel(){
  if(ev.W===1&&ev.R===1)return"阶段：解释消除";
  if(ev.W===1)return"阶段：观测草湿";
  if(ev.R===null&&ev.S===null&&ev.W===null)return"阶段：先验";
  return"阶段：自定义证据";
}
function render(){
  var post=draw();
  document.getElementById("stage").textContent=stageLabel();
  caption(post);
}
function caption(post){
  var el=document.getElementById("caption");
  if(ev.W===1&&ev.R===1){
    el.innerHTML="再确认<b>确实下雨了</b>：草湿已经有了解释，洒水器的概率从观测草湿时的 64% <b>跌回 "+fmt(post.S)+"</b>——这就是“解释消除”。两个先验独立的原因，因为共享同一个结果，观测后变得此消彼长。";
  }else if(ev.W===1&&ev.R===0){
    el.innerHTML="已知<b>没下雨</b>，但草还是湿的——那只能赖洒水器了，它的概率被顶到 <b>"+fmt(post.S)+"</b>。一个原因被排除，全部责任压到另一个原因身上。";
  }else if(ev.W===1){
    el.innerHTML="观测到<b>草湿了</b>：下雨升到 <b>"+fmt(post.R)+"</b>、洒水器升到 <b>"+fmt(post.S)+"</b>，两个原因<b>同时</b>变得更可能（先验只有 20% 和 30%）。总得有原因解释这摊水。";
  }else if(ev.R===null&&ev.S===null&&ev.W===null){
    el.innerHTML="没有任何证据，显示的是<b>先验</b>：下雨 20%、洒水器 30%，两者相互独立、井水不犯河水。点“草湿 W”节点观测它，看会发生什么。";
  }else if(ev.W===0){
    el.innerHTML="已知<b>草没湿</b>：两个原因都被压低（下雨 "+fmt(post.R)+"、洒水器 "+fmt(post.S)+"）——既然结果没发生，原因发生过的可能性自然更小。";
  }else{
    el.innerHTML="当前证据下：下雨 <b>"+fmt(post.R)+"</b>、洒水器 <b>"+fmt(post.S)+"</b>、草湿 <b>"+fmt(post.W)+"</b>。试着先观测草湿，再观测下雨，体会洒水器先升后降。";
  }
}
function stop(){if(timer){clearTimeout(timer);timer=null;}document.getElementById("story").textContent="▶ 演示解释消除";}
function setStage(k){
  if(k===0){ev={R:null,S:null,W:null};}
  else if(k===1){ev={R:null,S:null,W:1};}
  else{ev={R:1,S:null,W:1};}
  render();
}
// 点节点循环证据
document.getElementById("net").addEventListener("click",function(e){
  var t=e.target,n=t.getAttribute&&t.getAttribute("data-n");if(!n)return;
  stop();
  ev[n]=(ev[n]===null)?1:(ev[n]===1?0:null);
  render();
});
document.getElementById("reset").addEventListener("click",function(){stop();setStage(0);});
document.getElementById("story").addEventListener("click",function(){
  if(timer){stop();return;}
  document.getElementById("story").textContent="⏸ 演示中";
  var k=0;setStage(0);
  function step(){k++;if(k>2){stop();return;}setStage(k);timer=setTimeout(step,1700);}
  timer=setTimeout(step,1700);
});
render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){setStage(2);return;}
  document.getElementById("story").click();
},900);
})();
</script>
{% endraw %}
