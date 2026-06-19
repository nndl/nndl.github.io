---
layout: default
title: VAE 的潜空间
permalink: /viz/vae/
redirect_from:
  - /v/vae/
---

{% raw %}
<style>
.vaelab svg{max-width:100%;height:auto;}
.vaelab .plane{fill:var(--color-bg-soft,#f4f1ec);stroke:var(--color-border-strong);stroke-width:1;}
.vaelab .axis{stroke:#b9c2c7;stroke-width:1;}
.vaelab .dot{fill:var(--color-gold);stroke:#fff;stroke-width:2;}
.vaelab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
.vaelab .face{stroke:#5a4a2a;stroke-width:2;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# VAE 的潜空间

变分自编码器（VAE）把一张图压成几个数字（叫**潜变量**），再从这几个数字解码还原。神奇的是：它学出的这个低维**潜空间**是**连续而有意义**的——你在里面平移一点点，解码出的图也只变一点点；不同方向往往对应不同的语义属性（比如表情、胖瘦）。所以从潜空间随便取一个点解码，就能“生成”一张全新的、却很自然的图。下面把潜空间简化成 2 维：拖动 z₁、z₂，看右边的脸连续变形；背景网格是潜空间各处解码出的“脸的地图”。

<section class="vizui vaelab" id="vaelab">
  <p class="vizui__lead">左边是 2 维潜空间（横轴 z₁ 控制嘴型、纵轴 z₂ 控制眼睛与气色），金点是当前位置。右边是该点解码出的脸。注意：相邻的点解码出的脸也相近——潜空间是“平滑”的。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="z1">z₁（嘴）</label><input type="range" id="z1" min="-1" max="1" step="0.02" value="-0.6" style="width:130px"></span>
      <span class="vizui-field"><label for="z2">z₂（眼/气色）</label><input type="range" id="z2" min="-1" max="1" step="0.02" value="0.5" style="width:130px"></span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn" id="rand" type="button">🎲 随机采样</button>
    </div>
    <svg id="plane" viewBox="0 0 460 250" role="img" aria-label="VAE 潜空间"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>压成几个数</b><p>编码器把高维图压进低维潜变量，解码器再还原——逼模型抓住要点。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>平滑潜空间</b><p>VAE 的训练让潜空间连续规整，移动一点、图变一点，不会突变。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>采样即生成</b><p>在潜空间任取一点解码，就得到一张全新但自然的图——这就是生成。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var z1=-0.6,z2=0.5;
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function lerp(a,b,t){return a+(b-a)*t;}
function headColor(z2){var c1=[169,199,232],c2=[246,217,107],t=(z2+1)/2;return "rgb("+Math.round(lerp(c1[0],c2[0],t))+","+Math.round(lerp(c1[1],c2[1],t))+","+Math.round(lerp(c1[2],c2[2],t))+")";}
function face(svg,cx,cy,R,a,b){
  E(svg,"circle",{cx:cx,cy:cy,r:R,fill:headColor(b),"class":"face"});
  var er=0.07*R+0.06*R*(b+1)/2, sp=0.26*R;
  E(svg,"circle",{cx:cx-sp,cy:cy-0.18*R,r:er,fill:"#3a3a3a"});
  E(svg,"circle",{cx:cx+sp,cy:cy-0.18*R,r:er,fill:"#3a3a3a"});
  var my=cy+0.34*R,ctrl=my+a*0.5*R;
  E(svg,"path",{d:"M "+(cx-0.4*R)+" "+my+" Q "+cx+" "+ctrl+" "+(cx+0.4*R)+" "+my,fill:"none",stroke:"#7a3b2e","stroke-width":Math.max(2,R*0.06),"stroke-linecap":"round"});
}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  // 潜空间平面
  var px=20,py=20,PW=210,PH=210;
  E(svg,"rect",{x:px,y:py,width:PW,height:PH,rx:6,"class":"plane"});
  E(svg,"line",{x1:px,y1:py+PH/2,x2:px+PW,y2:py+PH/2,"class":"axis"});
  E(svg,"line",{x1:px+PW/2,y1:py,x2:px+PW/2,y2:py+PH,"class":"axis"});
  E(svg,"text",{x:px+PW-4,y:py+PH/2-5,"text-anchor":"end","class":"lbl"},"z₁→");
  E(svg,"text",{x:px+PW/2+5,y:py+12,"class":"lbl"},"z₂↑");
  // 迷你脸网格
  var G=5;
  for(var gi=0;gi<G;gi++)for(var gj=0;gj<G;gj++){
    var a=-1+2*gi/(G-1),b=1-2*gj/(G-1);
    var mx=px+PW*(gi+0.5)/G,myy=py+PH*(gj+0.5)/G;
    face(svg,mx,myy,15,a,b);
  }
  // 当前点
  var dx=px+(z1+1)/2*PW,dy=py+(1-(z2+1)/2)*PH;
  E(svg,"circle",{cx:dx,cy:dy,r:7,"class":"dot"});
  // 大脸
  face(svg,350,130,82,z1,z2);
  E(svg,"text",{x:350,y:235,"text-anchor":"middle","class":"lbl"},"解码结果");
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  var mood=z1>0.3?"在笑":z1<-0.3?"在皱眉":"面无表情";
  var look=z2>0.3?"睁大眼、暖气色":z2<-0.3?"眯眼、冷气色":"普通";
  el.innerHTML="当前潜变量 z=("+z1.toFixed(2)+", "+z2.toFixed(2)+")，解码出一张<b>"+mood+"、"+look+"</b>的脸。微调滑块，脸会<b>连续</b>地变——这正是潜空间平滑、可采样生成的体现。";
}
document.getElementById("z1").addEventListener("input",function(e){z1=+e.target.value;render();});
document.getElementById("z2").addEventListener("input",function(e){z2=+e.target.value;render();});
document.getElementById("rand").addEventListener("click",function(){z1=+(Math.random()*2-1).toFixed(2);z2=+(Math.random()*2-1).toFixed(2);document.getElementById("z1").value=z1;document.getElementById("z2").value=z2;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var k=0;var iv=setInterval(function(){k++;z1=Math.cos(k*0.5)*0.8;z2=Math.sin(k*0.5)*0.8;document.getElementById("z1").value=z1;document.getElementById("z2").value=z2;render();if(k>=13)clearInterval(iv);},420);},1000);
})();
</script>
{% endraw %}
