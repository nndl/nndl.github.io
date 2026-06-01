---
layout: default
title: 层归一化 vs 批归一化
permalink: /viz/layernorm/
redirect_from:
  - /v/layernorm/
---

{% raw %}
<style>
.lnlab svg{max-width:100%;height:auto;}
.lnlab .cell{stroke:#fff;stroke-width:1.5;}
.lnlab .val{font:12px var(--font-mono);fill:#1a1a1a;}
.lnlab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
.lnlab .grp{fill:none;stroke:var(--color-gold);stroke-width:2.5;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 层归一化 vs 批归一化

神经网络里数值忽大忽小会让训练很难。**归一化**的办法是把一组数减去均值、再除以标准差，拉回“均值 0、方差 1”的标准区间。但“一组”是哪一组？**批归一化（BatchNorm）**对**同一个特征、跨整批样本**归一（竖着看，按列）；**层归一化（LayerNorm）**对**同一个样本、跨所有特征**归一（横着看，按行）。一个跨样本、一个跨特征——切换下面的开关，看归一化沿哪个方向算、结果有什么不同。

<section class="vizui lnlab" id="lnlab">
  <p class="vizui__lead">上面是原始数据：每行一个样本，每列一个特征（注意各列的量纲差别很大）。下面是归一化后的结果。<b>金色框</b>圈出的是“一组”——BatchNorm 圈列、LayerNorm 圈行。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span>归一化方式：</span>
      <button class="vizui-btn vizui-btn--go" id="bn" type="button">BatchNorm（按列·跨样本）</button>
      <button class="vizui-btn" id="ln" type="button">LayerNorm（按行·跨特征）</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 360 330" role="img" aria-label="归一化网格"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>BatchNorm：跨样本</b><p>对每个特征、在整批样本上算均值方差。依赖批大小，序列/小批量时不稳。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>LayerNorm：跨特征</b><p>对每个样本、在它自己的所有特征上算。与批无关，Transformer 标配。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>都为稳训练</b><p>把数值拉回均值0方差1，梯度更平稳、收敛更快、对初始化更宽容。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var raw=[[2.1,8.0,-1.2,0.5,5.0],[1.0,9.5,-0.8,1.5,4.2],[3.2,7.0,-2.0,0.0,6.1],[0.4,8.8,-1.5,1.0,4.8]];
var N=4,D=5,mode="bn";
function norm(m){
  var out=[],i,j;
  for(i=0;i<N;i++)out.push([]);
  if(m==="bn"){ for(j=0;j<D;j++){var mu=0;for(i=0;i<N;i++)mu+=raw[i][j];mu/=N;var sd=0;for(i=0;i<N;i++)sd+=(raw[i][j]-mu)*(raw[i][j]-mu);sd=Math.sqrt(sd/N)||1;for(i=0;i<N;i++)out[i][j]=(raw[i][j]-mu)/sd;} }
  else { for(i=0;i<N;i++){var mu2=0;for(j=0;j<D;j++)mu2+=raw[i][j];mu2/=D;var sd2=0;for(j=0;j<D;j++)sd2+=(raw[i][j]-mu2)*(raw[i][j]-mu2);sd2=Math.sqrt(sd2/D)||1;for(j=0;j<D;j++)out[i][j]=(raw[i][j]-mu2)/sd2;} }
  return out;
}
var SVGNS="http://www.w3.org/2000/svg",cw=52,ch=30,x0=58,y0=24,y1=200;
function col(v,lo,hi){var t=(v-lo)/(hi-lo);t=t<0?0:t>1?1:t;var b=[37,99,235],w=[245,245,245],r=[181,82,74];var a,c;if(t<0.5){a=t/0.5;c=[b[0]+(w[0]-b[0])*a,b[1]+(w[1]-b[1])*a,b[2]+(w[2]-b[2])*a];}else{a=(t-0.5)/0.5;c=[w[0]+(r[0]-w[0])*a,w[1]+(r[1]-w[1])*a,w[2]+(r[2]-w[2])*a];}return"rgb("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+")";}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function grid(svg,data,gy,lo,hi){
  for(var i=0;i<N;i++)for(var j=0;j<D;j++){
    E(svg,"rect",{x:x0+j*cw,y:gy+i*ch,width:cw,height:ch,fill:col(data[i][j],lo,hi),"class":"cell"});
    E(svg,"text",{x:x0+j*cw+cw/2,y:gy+i*ch+ch/2+4,"text-anchor":"middle","class":"val"},data[i][j].toFixed(1));
  }
  for(var i2=0;i2<N;i2++)E(svg,"text",{x:x0-6,y:gy+i2*ch+ch/2+4,"text-anchor":"end","class":"lbl"},"样本"+(i2+1));
  for(var j2=0;j2<D;j2++)E(svg,"text",{x:x0+j2*cw+cw/2,y:gy-6,"text-anchor":"middle","class":"lbl"},"特征"+(j2+1));
}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var nd=norm(mode);
  E(svg,"text",{x:x0,y:14,"class":"lbl",style:"font-weight:600"},"原始数据");
  grid(svg,raw,y0,-2.5,9.5);
  E(svg,"text",{x:x0,y:y1-10,"class":"lbl",style:"font-weight:600"},"归一化后（均值0·方差1）");
  grid(svg,nd,y1,-1.8,1.8);
  // 金框：BN 圈一列，LN 圈一行（演示第1组）
  if(mode==="bn"){ E(svg,"rect",{x:x0-1,y:y0-1,width:cw+2,height:N*ch+2,"class":"grp"}); E(svg,"rect",{x:x0-1,y:y1-1,width:cw+2,height:N*ch+2,"class":"grp"}); }
  else { E(svg,"rect",{x:x0-1,y:y0-1,width:D*cw+2,height:ch+2,"class":"grp"}); E(svg,"rect",{x:x0-1,y:y1-1,width:D*cw+2,height:ch+2,"class":"grp"}); }
  document.getElementById("bn").className="vizui-btn"+(mode==="bn"?" vizui-btn--go":"");
  document.getElementById("ln").className="vizui-btn"+(mode==="ln"?" vizui-btn--go":"");
  document.getElementById("stat").textContent=mode==="bn"?"沿列归一（跨 4 个样本）":"沿行归一（跨 5 个特征）";
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  if(mode==="bn")el.innerHTML="<b>BatchNorm：</b>金框竖着圈住一整列——它对“特征1”在 4 个样本上算均值方差，再把这列拉成均值0方差1。每个特征各自标准化，但要凑齐一批样本才能算。";
  else el.innerHTML="<b>LayerNorm：</b>金框横着圈住一整行——它对“样本1”在它自己的 5 个特征上算均值方差。每个样本独立完成，不看别的样本，因此和批大小无关——这正是 Transformer 偏爱它的原因。";
}
document.getElementById("bn").addEventListener("click",function(){mode="bn";render();});
document.getElementById("ln").addEventListener("click",function(){mode="ln";render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  mode="ln";render();setTimeout(function(){mode="bn";render();},1600);},1000);
})();
</script>
{% endraw %}
