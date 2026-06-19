---
layout: default
title: 损失函数对比：MSE / 交叉熵 / Hinge / Focal
permalink: /viz/loss-functions/
redirect_from:
  - /v/loss-functions/
---

{% raw %}
<style>
.lflab .axis{stroke:var(--color-border);stroke-width:1;}
.lflab .grid{stroke:var(--color-border);stroke-width:1;opacity:.35;}
.lflab .alab{font:10.5px var(--font-mono);fill:var(--color-text-muted);}
.lflab .czone{fill:#b5524a;opacity:.05;}
.lflab .ezone{fill:var(--color-forest);opacity:.05;}
.lflab .c-ce{fill:none;stroke:#b5524a;stroke-width:2.8;}
.lflab .c-hinge{fill:none;stroke:var(--color-gold);stroke-width:2.6;}
.lflab .c-mse{fill:none;stroke:var(--color-accent);stroke-width:2.6;}
.lflab .c-focal{fill:none;stroke:#2563eb;stroke-width:2.6;stroke-dasharray:6 4;}
.lflab .zline{stroke:var(--color-text);stroke-width:1.6;cursor:ew-resize;}
.lflab .zgrab{stroke:transparent;stroke-width:22;cursor:ew-resize;}
.lflab .zhandle{fill:var(--color-bg-pure);stroke:var(--color-text);stroke-width:2;cursor:ew-resize;}
.lflab svg{touch-action:none;}
.lflab .read{display:grid;grid-template-columns:auto 1fr;gap:7px 14px;font-size:.92rem;align-items:center;}
.lflab .read .sw{width:22px;height:0;border-top-width:3px;border-top-style:solid;display:inline-block;vertical-align:middle;}
.lflab .read .k{color:var(--color-text-soft);}
.lflab .read .v{font:700 1.05rem var(--font-mono);text-align:right;}
.lflab .ztag{font:700 .95rem var(--font-mono);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 损失函数对比：MSE / 交叉熵 / Hinge / Focal

同一道题，不同的损失函数会给出截然不同的“扣分标准”。这里固定一个正样本（真实标签 y=+1），横轴是模型打出的分数 z（越大越自信地判它为正），纵轴是各损失要扣的分。重点看左边“自信地答错”那一带：**交叉熵**会把分数压向无穷大，惩罚极重；**Hinge** 只在间隔内线性收一点；而 **MSE（作用在概率上）**几乎封顶在 1，对自信的错误近乎无动于衷；**Focal** 则反过来——它把“已经轻松分对”的样本权重压下去，好把注意力留给难样本。**在图上左右拖动**那条竖线，读四个损失值。

<section class="vizui lflab" id="lflab">
  <p class="vizui__lead">真实标签 <b>y=+1</b>，预测概率 <b>p=σ(z)</b>。拖动竖线选一个分数 z：左边是“自信答错”区（z≪0，p 很小），右边是“自信答对”区（z≫0，p→1）。看四条曲线在竖线上的高度差。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="gamma">Focal 的 γ</label>
        <input type="range" id="gamma" min="0" max="5" step="0.5" value="2" style="width:160px">
        <output id="gammaVal">2.0</output>
      </span>
      <span class="vizui-spacer"></span>
      <span class="vizui-field"><label for="zr">分数 z</label>
        <input type="range" id="zr" min="-4" max="4" step="0.1" value="-2.5" style="width:160px">
        <output id="zVal">-2.5</output>
      </span>
    </div>
  </div>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">损失 ℓ(z) · 横轴是分数 z</p>
      <svg class="vizui-chart" id="plot" viewBox="0 0 380 260" role="img" aria-label="四种损失函数随分数 z 的变化"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">竖线处 <span class="ztag" id="zptag" style="color:var(--color-text)">z=−2.5</span> 的损失值</p>
      <div style="text-align:center;margin:2px 0 12px;font-size:.9rem;color:var(--color-text-soft)">预测概率 p = σ(z) = <span style="font:700 1rem var(--font-mono);color:var(--color-text)" id="pval">—</span></div>
      <div class="read">
        <span class="sw" style="border-top-color:#b5524a"></span><span class="k">交叉熵 −log p</span><span class="v" id="vce" style="color:#b5524a">—</span>
        <span class="sw" style="border-top-color:var(--color-gold)"></span><span class="k">Hinge max(0,1−z)</span><span class="v" id="vhinge" style="color:var(--color-gold)">—</span>
        <span class="sw" style="border-top-color:var(--color-accent)"></span><span class="k">MSE (1−p)²</span><span class="v" id="vmse" style="color:var(--color-accent)">—</span>
        <span class="sw" style="border-top-color:#2563eb;border-top-style:dashed"></span><span class="k">Focal −(1−p)<sup>γ</sup>·log p</span><span class="v" id="vfocal" style="color:#2563eb">—</span>
      </div>
      <div style="margin-top:14px;padding:10px 12px;border-radius:var(--radius-md);background:var(--color-bg-section);font-size:.84rem;color:var(--color-text-soft)" id="ratio"></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>交叉熵：答错重罚</b><p>p→0 时 −log p→∞。自信地答错会被狠狠惩罚，逼模型别犯笃定的错误。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>MSE：对错误麻木</b><p>(1−p)² 最多≈1。哪怕自信答错，损失也封顶，梯度还很小——这就是分类一般不用 MSE 的原因。</p></div>
    <div class="card" style="--wc:#2563eb"><b>Focal：压低易样本</b><p>乘上 (1−p)<sup>γ</sup>，把“已经分对”的简单样本权重压下去，让难样本主导训练（目标检测常用）。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var ZMIN=-4,ZMAX=4,YMIN=0,YMAX=5,CLAMP=5;
var gamma=2, z0=-2.5, demoIv=null;
function sig(z){return 1/(1+Math.exp(-z));}
function L(name,z){
  var p=sig(z);
  if(name==="ce")return -Math.log(p);
  if(name==="hinge")return Math.max(0,1-z);
  if(name==="mse")return (1-p)*(1-p);
  if(name==="focal")return -Math.pow(1-p,gamma)*Math.log(p);
  return 0;
}
var SVGNS="http://www.w3.org/2000/svg",W=380,H=260,padL=34,padR=12,padT=14,padB=26;
function wx(z){return padL+(z-ZMIN)/(ZMAX-ZMIN)*(W-padL-padR);}
function wy(y){return (H-padB)-(Math.min(CLAMP,y)-YMIN)/(YMAX-YMIN)*(H-padT-padB);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function curve(svg,name,cls){var pts=[];for(var i=0;i<=160;i++){var z=ZMIN+(ZMAX-ZMIN)*i/160;pts.push(wx(z)+","+wy(L(name,z)));}E(svg,"polyline",{points:pts.join(" "),"class":cls});}

function drawPlot(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  // 背景区域：自信答错（左）/ 自信答对（右）
  E(svg,"rect",{x:wx(ZMIN),y:padT,width:wx(-1.5)-wx(ZMIN),height:(H-padB)-padT,"class":"czone"});
  E(svg,"rect",{x:wx(1.5),y:padT,width:wx(ZMAX)-wx(1.5),height:(H-padB)-padT,"class":"ezone"});
  // 网格 + 横轴刻度
  for(var z=-4;z<=4;z+=2){E(svg,"line",{x1:wx(z),y1:padT,x2:wx(z),y2:H-padB,"class":z===0?"axis":"grid"});E(svg,"text",{x:wx(z),y:H-padB+14,"text-anchor":"middle","class":"alab"}).textContent=z;}
  for(var y=0;y<=5;y++){E(svg,"line",{x1:padL,y1:wy(y),x2:W-padR,y2:wy(y),"class":y===0?"axis":"grid"});E(svg,"text",{x:padL-6,y:wy(y)+3.5,"text-anchor":"end","class":"alab"}).textContent=y;}
  E(svg,"text",{x:(wx(ZMIN)+wx(-1.5))/2,y:padT+13,"text-anchor":"middle","class":"alab",style:"fill:#b5524a;font-weight:700"}).textContent="自信答错";
  E(svg,"text",{x:(wx(1.5)+wx(ZMAX))/2,y:padT+13,"text-anchor":"middle","class":"alab",style:"fill:var(--color-forest);font-weight:700"}).textContent="自信答对";
  E(svg,"text",{x:W-padR,y:H-padB+24,"text-anchor":"end","class":"alab"}).textContent="分数 z →";
  // 四条曲线
  curve(svg,"mse","c-mse");
  curve(svg,"hinge","c-hinge");
  curve(svg,"focal","c-focal");
  curve(svg,"ce","c-ce");
  // 可拖动竖线
  var xz=wx(z0);
  E(svg,"line",{x1:xz,y1:padT,x2:xz,y2:H-padB,"class":"zline"});
  E(svg,"line",{x1:xz,y1:padT,x2:xz,y2:H-padB,"class":"zgrab"});
  E(svg,"circle",{cx:xz,cy:padT+6,r:6,"class":"zhandle"});
  // 各损失在竖线上的标记点
  [["mse","var(--color-accent)"],["hinge","var(--color-gold)"],["focal","#2563eb"],["ce","#b5524a"]].forEach(function(c){
    E(svg,"circle",{cx:xz,cy:wy(L(c[0],z0)),r:4,fill:c[1],stroke:"var(--color-bg-pure)","stroke-width":1.5});
  });
}
function render(){
  var p=sig(z0),ce=L("ce",z0),hi=L("hinge",z0),ms=L("mse",z0),fo=L("focal",z0);
  document.getElementById("zVal").textContent=z0.toFixed(1);
  document.getElementById("gammaVal").textContent=gamma.toFixed(1);
  document.getElementById("zptag").textContent="z="+(z0<0?"−"+Math.abs(z0).toFixed(1):z0.toFixed(1));
  document.getElementById("pval").textContent=p.toFixed(3);
  document.getElementById("vce").textContent=ce.toFixed(2);
  document.getElementById("vhinge").textContent=hi.toFixed(2);
  document.getElementById("vmse").textContent=ms.toFixed(2);
  document.getElementById("vfocal").textContent=fo.toFixed(2);
  // CE vs MSE 倍数
  var rat=document.getElementById("ratio");
  if(ms>0.01)rat.innerHTML="此处交叉熵是 MSE 的 <b>"+(ce/ms).toFixed(1)+" 倍</b>——同一个错误，交叉熵扣得狠得多。";
  else rat.innerHTML="此处四个损失都很小，几乎不扣分（已分对）。";
  drawPlot();caption(p,ce,hi,ms,fo);
}
function caption(p,ce,hi,ms,fo){
  var el=document.getElementById("caption"),m;
  if(z0<=-2){
    m="<b>自信地答错（z="+z0.toFixed(1)+"，p="+p.toFixed(3)+"）：</b>交叉熵高达 <b style='color:#b5524a'>"+ce.toFixed(2)+"</b>，是 MSE（"+ms.toFixed(2)+"）的好几倍——而 MSE 几乎封顶在 1，对这种笃定的错误几乎无动于衷。这正是分类用交叉熵、不用 MSE 的原因。";
  }else if(z0>=2){
    m="<b>自信地答对（z="+z0.toFixed(1)+"，p="+p.toFixed(3)+"）：</b>四个损失都趋近 0。注意 Focal（"+fo.toFixed(3)+"）比交叉熵（"+ce.toFixed(3)+"）更小——它乘了 (1−p)<sup>γ</sup>，把这类“已经分对”的简单样本进一步压低权重。";
  }else if(z0>=0.5){
    m="<b>勉强分对（z="+z0.toFixed(1)+"）：</b>Hinge 已经归零（过了间隔），但交叉熵还在收 "+ce.toFixed(2)+"——它要求模型不仅分对，还要更自信。";
  }else{
    m="<b>处在边界附近（z="+z0.toFixed(1)+"）：</b>Hinge 在 z=1 处才归零（带间隔），交叉熵和 Focal 仍随 z 平滑变化。往左拖到 z≪0 看交叉熵飙升，往右拖看四条曲线一起塌向 0。";
  }
  el.innerHTML=m;
}

// 拖动设置 z
var svg=document.getElementById("plot");
var dragging=false;
function zFromEvent(e){var r=svg.getBoundingClientRect();var px=(e.clientX-r.left)/r.width*W;var z=ZMIN+(px-padL)/(W-padL-padR)*(ZMAX-ZMIN);z=Math.max(ZMIN,Math.min(ZMAX,z));return Math.round(z*10)/10;}
function stopDemo(){if(demoIv){clearInterval(demoIv);demoIv=null;}}
svg.addEventListener("pointerdown",function(e){stopDemo();dragging=true;svg.setPointerCapture(e.pointerId);z0=zFromEvent(e);document.getElementById("zr").value=z0;render();});
svg.addEventListener("pointermove",function(e){if(!dragging)return;z0=zFromEvent(e);document.getElementById("zr").value=z0;render();});
svg.addEventListener("pointerup",function(){dragging=false;});
svg.addEventListener("pointercancel",function(){dragging=false;});
document.getElementById("zr").addEventListener("input",function(e){stopDemo();z0=+e.target.value;render();});
document.getElementById("gamma").addEventListener("input",function(e){stopDemo();gamma=+e.target.value;render();});

render();
/* 自动演示：从最有看点的“自信答错”扫到“自信答对” */
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){z0=-4;document.getElementById("zr").value=z0;render();return;}
  var seq=[-4,-3,-2,-1,0,1,2,3,-2.5],k=0,sl=document.getElementById("zr");
  demoIv=setInterval(function(){if(k>=seq.length){clearInterval(demoIv);demoIv=null;return;}z0=seq[k];sl.value=z0;render();k++;},760);
},900);
})();
</script>
{% endraw %}
