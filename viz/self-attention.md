---
layout: default
title: 点词看注意力
permalink: /viz/self-attention/
redirect_from:
  - /v/self-attention/
---

{% raw %}
<style>
.attlab .att-heads{display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.attlab .att-heads button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.9rem;color:var(--color-text-soft);padding:7px 16px;border-radius:999px;transition:all .2s var(--ease-out);}
.attlab .att-heads button.on{background:var(--color-bg-pure);color:var(--color-accent);font-weight:600;box-shadow:var(--shadow-sm);}
.attlab .att-stage{position:relative;padding:84px 6px 16px;overflow:hidden;}
.attlab .att-arcs{position:absolute;left:0;top:0;pointer-events:none;overflow:visible;}
.attlab .att-words{display:flex;flex-wrap:wrap;gap:10px 8px;justify-content:center;position:relative;}
.attlab .att-word{font-family:var(--font-serif);font-size:1.4rem;line-height:1;padding:10px 12px;border-radius:10px;
  border:1px solid var(--color-border);background:var(--color-bg-pure);color:var(--color-text);cursor:pointer;
  transition:transform .15s var(--ease-out),border-color .2s,box-shadow .2s;user-select:none;}
.attlab .att-word:hover{transform:translateY(-2px);border-color:var(--color-accent);}
.attlab .att-word.q{border-color:var(--color-accent);box-shadow:0 0 0 2px var(--color-accent-soft);font-weight:600;}
.attlab .att-readout{margin-top:14px;font-size:.95rem;color:var(--color-text-soft);min-height:1.5em;text-align:center;}
.attlab .att-readout b{color:var(--color-accent);}
.attlab .att-hint{font-size:.86rem;color:var(--color-text-muted);text-align:center;margin-top:4px;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 点词看注意力

Transformer（也就是当下大模型的核心）能读懂长句子，靠的是“自注意力”：句子里的每个词，都会去“看”其他词，再决定自己的含义。比如“它”到底指谁？模型就是靠注意力把“它”连回“小猫”的。**点下面句子里的任意一个词，看看它在注意谁。**

<section class="vizui attlab" id="attlab">
  <p class="vizui__lead">连线越粗、词底色越深，表示当前这个词对它的“注意力”越强。换“注意力头”能看到模型同时在用好几套不同的看法。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="sent">例句</label>
        <select class="vizui-pill" id="sent" style="padding:6px 12px;cursor:pointer">
          <option value="0">小猫追老鼠（“它”指谁？）</option>
          <option value="1">东京是日本的首都</option>
        </select>
      </span>
      <span class="vizui-spacer"></span>
      <span class="att-heads" id="heads" role="group" aria-label="注意力头">
        <button data-h="0" class="on" type="button">语义关联</button>
        <button data-h="1" type="button">相邻局部</button>
        <button data-h="2" type="button">句首锚点</button>
      </span>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="att-stage" id="stage">
      <svg class="att-arcs" id="arcs"></svg>
      <div class="att-words" id="words"></div>
    </div>
    <div class="att-readout" id="readout"></div>
    <div class="att-hint">点不同的词试试 · 切换上方“注意力头”看不同模式</div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>语义关联</b><p>把含义相关的词连起来，比如代词“它”连回“小猫”、“首都”连向“东京”。这是理解句子的关键。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>相邻局部</b><p>主要关注左右挨着的词，负责把短语、搭配粘合在一起。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>多个头并行</b><p>真实模型有很多个“头”,各看一种关系，合起来才读懂整句——这里只展示三种示意。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
/* links：有向带权 [query 索引, key 索引, 权重]，表示“query 这个词去看 key”的强度 */
var SENTS=[
  {toks:["小猫","追","老鼠","，","因为","它","饿","了"],
   links:[[5,0,1.6],[1,0,1.0],[1,2,1.0],[6,5,1.2],[6,0,0.5],[4,6,0.8]], focus:5},
  {toks:["东京","是","日本","的","首都"],
   links:[[4,0,1.4],[4,2,0.9],[2,0,0.8],[1,4,0.7]], focus:4}
];
var HEAD_COLOR=["#155e75","#206a4f","#b7791f"];
var si=0, head=0, sel=null, mats=[];

function buildMats(){
  var toks=SENTS[si].toks, n=toks.length, links=SENTS[si].links;
  function norm(M){return M.map(function(row){var s=row.reduce(function(a,b){return a+b;},0)||1;return row.map(function(v){return v/s;});});}
  // 头0 语义关联
  var sem=[]; for(var i=0;i<n;i++){var row=[];for(var j=0;j<n;j++)row.push(i===j?0.5:0.04);sem.push(row);}
  links.forEach(function(l){sem[l[0]][l[1]]+=l[2];});
  // 头1 相邻局部
  var adj=[]; for(var i2=0;i2<n;i2++){var r2=[];for(var j2=0;j2<n;j2++)r2.push(Math.exp(-(i2-j2)*(i2-j2)/2.0));adj.push(r2);}
  // 头2 句首锚点
  var anc=[]; for(var i3=0;i3<n;i3++){var r3=[];for(var j3=0;j3<n;j3++)r3.push((j3===0?1.0:0.05)+(i3===j3?0.35:0));anc.push(r3);}
  mats=[norm(sem),norm(adj),norm(anc)];
}

function buildWords(){
  var host=document.getElementById("words"); host.innerHTML=""; var toks=SENTS[si].toks;
  toks.forEach(function(tk,i){
    var b=document.createElement("button"); b.className="att-word"; b.type="button"; b.dataset.i=i; b.textContent=tk;
    b.addEventListener("click",function(){sel=i;draw();});
    host.appendChild(b);
  });
}

var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function mix(c,a){ // tint: white→accent-ish by alpha a
  return "rgba("+c+","+a.toFixed(3)+")";
}

function draw(){
  var stage=document.getElementById("stage"), svg=document.getElementById("arcs"),
      words=stage.querySelectorAll(".att-word");
  var W=stage.clientWidth, Hh=stage.clientHeight;
  svg.setAttribute("viewBox","0 0 "+W+" "+Hh); svg.setAttribute("width",W); svg.setAttribute("height",Hh);
  while(svg.firstChild)svg.removeChild(svg.firstChild);
  var col=HEAD_COLOR[head], colRGB=(head===0?"21,94,117":head===1?"32,106,79":"183,121,31");
  // 还原底色与选中态
  words.forEach(function(el){el.style.background="";el.classList.remove("q");});
  if(sel==null){document.getElementById("readout").innerHTML="";return;}
  var row=mats[head][sel];
  var sRect=stage.getBoundingClientRect();
  function cx(el){var r=el.getBoundingClientRect();return r.left-sRect.left+r.width/2;}
  function ty(el){var r=el.getBoundingClientRect();return r.top-sRect.top;}
  var qx=cx(words[sel]), qy=ty(words[sel]);
  // 连线（按权重从小到大画，强的在上层）
  var order=[]; for(var k=0;k<row.length;k++) if(k!==sel) order.push(k);
  order.sort(function(a,b){return row[a]-row[b];});
  order.forEach(function(k){
    var w=row[k]; if(w<0.03) return;
    var kx=cx(words[k]), ky=ty(words[k]);
    var d=Math.abs(kx-qx), arcH=Math.min(Math.max(26,d*0.42), Math.min(qy,ky)-8);
    var cyc=Math.min(qy,ky)-arcH;
    E(svg,"path",{d:"M"+qx+","+qy+" Q"+((qx+kx)/2)+","+cyc+" "+kx+","+ky,
      fill:"none",stroke:col,"stroke-width":(1+w*9).toFixed(1),"stroke-linecap":"round",opacity:(0.18+w*0.8).toFixed(2)});
  });
  // 底色 tint
  words.forEach(function(el,k){el.style.background=mix(colRGB,0.05+row[k]*0.7);});
  words[sel].classList.add("q");
  // readout
  var ranked=row.map(function(v,k){return [k,v];}).filter(function(p){return p[0]!==sel;}).sort(function(a,b){return b[1]-a[1];});
  var toks=SENTS[si].toks;
  var top=ranked[0], second=ranked[1];
  document.getElementById("readout").innerHTML="“<b>"+toks[sel]+"</b>” 最关注 → “<b>"+toks[top[0]]+"</b>”（"+Math.round(top[1]*100)+"%）"+
    (second&&second[1]>0.08?"，其次 “"+toks[second[0]]+"”（"+Math.round(second[1]*100)+"%）":"");
}

function caption(){
  var el=document.getElementById("caption"), names=["语义关联","相邻局部","句首锚点"];
  var sem0=si===0?"这一“头”专看含义关系：点“它”,连线最粗的指向“小猫”——模型就是这样判断代词指代谁的。"
                 :"这一“头”专看含义关系：点“首都”,连线最粗的指向“东京”——含义相关的词被连到一起。";
  var txt={0:sem0,
           1:"这一“头”主要关注左右相邻的词，负责把短语粘合起来；语义上不相关的远处词几乎不看。",
           2:"这一“头”让大多数词都去看句子开头——这是真实模型里常见的一种“锚点”模式。"};
  el.innerHTML="<b>当前注意力头："+names[head]+"</b>　"+txt[head];
}

function setHead(h){head=h;document.querySelectorAll("#heads button").forEach(function(b){b.classList.toggle("on",+b.dataset.h===h);});caption();draw();}
function loadSent(){buildMats();buildWords();sel=null;draw();}

document.getElementById("heads").addEventListener("click",function(e){var b=e.target.closest("button");if(b)setHead(+b.dataset.h);});
document.getElementById("sent").addEventListener("change",function(e){si=+e.target.value;loadSent();sel=SENTS[si].focus;draw();caption();});
window.addEventListener("resize",function(){if(sel!=null)draw();});

/* 启动：默认选中“焦点词”演示一次 */
loadSent(); caption();
setTimeout(function(){sel=SENTS[si].focus;draw();},600);
})();
</script>
{% endraw %}
