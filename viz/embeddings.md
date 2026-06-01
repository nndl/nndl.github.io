---
layout: default
title: 词向量类比
permalink: /viz/embeddings/
redirect_from:
  - /v/embeddings/
---

{% raw %}
<style>
.emlab .dot{fill:var(--color-border-strong);}
.emlab .wlabel{font:500 12px var(--font-sans);fill:var(--color-text-soft);}
.emlab .arr{stroke-width:2.2;fill:none;}
.emlab .arr-rel{stroke:var(--color-accent);}
.emlab .arr-cpy{stroke:var(--color-gold);stroke-dasharray:5 4;}
.emlab .node-a{fill:var(--color-text-muted);}
.emlab .node-b{fill:var(--color-accent);}
.emlab .node-c{fill:var(--color-forest);}
.emlab .res{fill:var(--color-gold);stroke:#fff;stroke-width:1.5;}
.emlab .ring{fill:none;stroke:var(--color-gold);stroke-width:2.4;}
.emlab .hi .wlabel{fill:var(--color-text);font-weight:700;}
.emlab .ana{display:flex;flex-wrap:wrap;gap:8px;}
.emlab .ana button{appearance:none;font:inherit;font-size:.88rem;cursor:pointer;padding:7px 13px;border-radius:999px;border:1px solid var(--color-border);background:var(--color-bg-section);color:var(--color-text-soft);}
.emlab .ana button.on{background:var(--color-bg-pure);color:var(--color-accent);font-weight:600;border-color:var(--color-accent);box-shadow:var(--shadow-sm);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 词向量类比

模型把每个词变成一串数字（一个“向量”），相近意思的词靠得近。神奇的是，这些向量还藏着“关系”：“国王”减去“男人”、再加上“女人”,结果竟然正好落在“王后”附近——因为“性别”这层关系，在向量空间里是一个固定的方向。下面用二维示意图看看这种“词向量算术”。

<section class="vizui emlab" id="emlab">
  <p class="vizui__lead">真实词向量有几百维，这里压成二维示意。选一个类比“A 之于 B，正如 C 之于 ？”,看蓝色关系箭头被平移到 C 上，金点落在哪个词附近。</p>

  <div class="vizui-panel">
    <div class="ana" id="ana"></div>
  </div>

  <div class="vizui-panel">
    <svg class="vizui-chart" id="plane" viewBox="0 0 480 320" role="img" aria-label="词向量二维空间"></svg>
    <div id="eq" style="text-align:center;font:600 1rem var(--font-mono);color:var(--color-text-soft);margin-top:6px"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>关系 = 方向</b><p>“男→女”和“国王→王后”是同一个方向、同一段位移——性别这层意思被编码成了一个向量。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>词向量算术</b><p>B − A + C 把“A→B”的关系搬到 C 上，落点附近的词就是类比的答案。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>怎么来的</b><p>这些向量不是人工设定，而是模型读海量文本、根据上下文自动学出来的。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var WORDS={
  "男人":[2,1.2],"女人":[2,3.2],"国王":[5,1.2],"王后":[5,3.2],"王子":[4,1.4],"公主":[4,3.4],"男孩":[1,1.4],"女孩":[1,3.4],
  "中国":[2.4,5.6],"北京":[3.4,6.9],"日本":[5.2,5.6],"东京":[6.2,6.9],"法国":[8,5.6],"巴黎":[9,6.9]
};
var ANALOGIES=[
  {a:"男人",b:"女人",c:"国王"},
  {a:"国王",b:"王后",c:"王子"},
  {a:"中国",b:"北京",c:"日本"},
  {a:"中国",b:"北京",c:"法国"}
];
var ai=0;
var XMIN=0,XMAX=10,YMIN=0.3,YMAX=7.6;
var SVGNS="http://www.w3.org/2000/svg",W=480,H=320,pad=24;
function wx(x){return pad+(x-XMIN)/(XMAX-XMIN)*(W-2*pad);}
function wy(y){return (H-pad)-(y-YMIN)/(YMAX-YMIN)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function arrow(svg,x1,y1,x2,y2,cls){
  E(svg,"line",{x1:wx(x1),y1:wy(y1),x2:wx(x2),y2:wy(y2),"class":"arr "+cls});
  var ang=Math.atan2(wy(y2)-wy(y1),wx(x2)-wx(x1)),L=8;
  E(svg,"line",{x1:wx(x2),y1:wy(y2),x2:wx(x2)-L*Math.cos(ang-0.4),y2:wy(y2)-L*Math.sin(ang-0.4),"class":"arr "+cls});
  E(svg,"line",{x1:wx(x2),y1:wy(y2),x2:wx(x2)-L*Math.cos(ang+0.4),y2:wy(y2)-L*Math.sin(ang+0.4),"class":"arr "+cls});
}
function nearest(pt,exclude){
  var best=null,bd=1e9;
  for(var w in WORDS){if(exclude.indexOf(w)>=0)continue;var d=Math.hypot(WORDS[w][0]-pt[0],WORDS[w][1]-pt[1]);if(d<bd){bd=d;best=w;}}
  return best;
}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var an=ANALOGIES[ai],a=WORDS[an.a],b=WORDS[an.b],c=WORDS[an.c];
  var res=[b[0]-a[0]+c[0], b[1]-a[1]+c[1]];
  var ans=nearest(res,[an.a,an.b,an.c]);
  // 箭头：关系 a→b，复制到 c→res
  arrow(svg,a[0],a[1],b[0],b[1],"arr-rel");
  arrow(svg,c[0],c[1],res[0],res[1],"arr-cpy");
  // 所有词
  for(var w in WORDS){
    var p=WORDS[w],hi=(w===an.a||w===an.b||w===an.c||w===ans);
    var g=E(svg,"g",{"class":hi?"hi":""});
    var ncls=w===an.a?"node-a":w===an.b?"node-b":w===an.c?"node-c":"dot";
    E(g,"circle",{cx:wx(p[0]),cy:wy(p[1]),r:hi?5:3.5,"class":ncls});
    E(g,"text",{x:wx(p[0])+7,y:wy(p[1])+4,"class":"wlabel"}).textContent=w;
  }
  // 结果点 + 答案词环
  E(svg,"circle",{cx:wx(res[0]),cy:wy(res[1]),r:5.5,"class":"res"});
  if(ans)E(svg,"circle",{cx:wx(WORDS[ans][0]),cy:wy(WORDS[ans][1]),r:12,"class":"ring"});
  document.getElementById("eq").innerHTML=an.b+" − "+an.a+" + "+an.c+" ≈ <b style='color:var(--color-gold)'>"+ans+"</b>";
  caption(an,ans);
}
function caption(an,ans){
  document.getElementById("caption").innerHTML="“"+an.a+"”之于“"+an.b+"”,正如“"+an.c+"”之于<b>“"+ans+"”</b>。蓝色箭头（"+an.a+"→"+an.b+"）被原样搬到"+an.c+"身上，落点正好挨着"+ans+"——同一种关系，就是向量空间里同一个方向。";
}
document.getElementById("ana").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;ai=+b.dataset.i;document.querySelectorAll("#ana button").forEach(function(x,i){x.classList.toggle("on",i===ai);});render();});
(function build(){var h=document.getElementById("ana");ANALOGIES.forEach(function(an,i){var b=document.createElement("button");b.type="button";b.dataset.i=i;b.className=i===0?"on":"";b.textContent=an.a+" : "+an.b+" :: "+an.c+" : ?";h.appendChild(b);});})();
render();
/* 自动演示：轮播类比 */
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var k=0;var iv=setInterval(function(){k++;if(k>=ANALOGIES.length){clearInterval(iv);return;}ai=k;document.querySelectorAll("#ana button").forEach(function(x,i){x.classList.toggle("on",i===ai);});render();},1600);
},1100);
})();
</script>
{% endraw %}
