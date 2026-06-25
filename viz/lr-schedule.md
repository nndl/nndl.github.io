---
layout: default
title: 学习率调度（预热 + 余弦退火）
description: "学习率随步数的“形状”才关键：没预热的大学习率开头就把损失冲飞；预热 + 余弦退火则平稳下降、收得更低。"
permalink: /viz/lr-schedule/
redirect_from:
  - /v/lr-schedule/
---

{% raw %}
<style>
.lrlab .axis{stroke:var(--color-border);stroke-width:1;}
.lrlab .gridl{stroke:var(--color-border);stroke-width:1;opacity:.4;}
.lrlab .alab{font:10px var(--font-mono);fill:var(--color-text-muted);}
.lrlab .lrcurve{fill:none;stroke:var(--color-accent);stroke-width:2.8;stroke-linejoin:round;}
.lrlab .losscurve{fill:none;stroke:#b5524a;stroke-width:2.6;stroke-linejoin:round;}
.lrlab .warmband{fill:var(--color-accent);opacity:.10;}
.lrlab .vline{stroke:var(--color-text-muted);stroke-width:1.2;stroke-dasharray:3 3;opacity:.55;}
.lrlab .cursor{fill:var(--color-gold);stroke:#fff;stroke-width:1.6;}
.lrlab .blowtag{font:600 11px var(--font-sans);fill:#b5524a;}
.lrlab .heads{display:flex;gap:6px;flex-wrap:wrap;}
.lrlab .heads .opt{cursor:pointer;border:1px solid var(--color-border-strong);background:var(--color-bg-pure);color:var(--color-text-muted);border-radius:999px;padding:3px 12px;font-size:.86rem;line-height:1.4;transition:all .15s;}
.lrlab .heads .opt[aria-pressed="true"]{background:var(--color-accent);border-color:var(--color-accent);color:#fff;font-weight:600;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 学习率调度（预热 + 余弦退火）

学习率不是设一个常数就完事——它**随训练步数变化的“形状”**才是关键。开头如果直接用大学习率，模型还没站稳就被一脚踹飞，损失瞬间爆掉；正确的做法是先**预热（warmup）**：用一小段时间把步长从很小慢慢拉到峰值，等参数稳住，再让学习率沿**余弦曲线**缓缓退火，稳稳落进谷底。上面是学习率随步数的曲线（真正要看的内容），下面是它带来的**损失（示意）**。切换调度方式，调峰值和预热步数，看上下两条线怎么联动。

<section class="lrlab vizui" id="lrlab">
  <p class="vizui__lead">上图 <span style="color:var(--color-accent);font-weight:600">蓝线</span>是学习率随步数的调度曲线（<span style="color:var(--color-accent)">淡蓝带</span>是预热区间）；下图 <span style="color:#b5524a;font-weight:600">红线</span>是对应的损失（示意）。<span style="color:var(--color-gold);font-weight:600">金点</span>是当前步。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label>调度方式</label>
        <span class="heads" id="sched">
          <span class="opt" data-s="const">常数</span>
          <span class="opt" data-s="cos">余弦退火</span>
          <span class="opt" data-s="warmcos" aria-pressed="true">预热+余弦</span>
        </span>
      </span>
    </div>
    <div class="vizui-bar">
      <span class="vizui-field"><label for="warm">预热步数</label><input type="range" id="warm" min="0" max="40" step="1" value="12" style="width:150px"><output id="warmVal"></output></span>
      <span class="vizui-field"><label for="peak">峰值学习率</label><input type="range" id="peak" min="0.2" max="1.2" step="0.05" value="0.9" style="width:150px"><output id="peakVal"></output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="finalPill">最终损失 —</span>
    </div>
    <svg class="vizui-chart" id="lrPlot" viewBox="0 0 460 200" role="img" aria-label="学习率随步数的调度曲线"></svg>
    <svg class="vizui-chart" id="lossPlot" viewBox="0 0 460 200" role="img" aria-label="损失随步数的示意曲线"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>预热（warmup）</b><p>开头小步慢走，把学习率从接近 0 渐渐拉到峰值，等模型稳住再加速，避免一上来步子太大、直接发散冲飞。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>余弦退火</b><p>后期沿余弦曲线把学习率逐渐减小到 0，相当于落地时收油门，稳稳落进损失谷底、收得更低。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>这是标配</b><p>从 ResNet 到大语言模型，几乎所有大规模训练都用“预热 + 余弦（或线性）退火”这套学习率调度。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var T=120;                          /* 总步数（固定） */
var k0=2.6, kf=0.18, tau=26;        /* 早期曲率大、随步数衰减：k_t = k0·e^{-t/tau} + kf */
var CLAMP=6, FLOOR=0.04, DIVERGED=5.5;
var state={sched:"warmcos", warmup:12, peak:0.9};
var SVGNS="http://www.w3.org/2000/svg";

/* ---- 学习率公式（精确） ---- */
function lrAt(step){
  var s=state.sched, p=state.peak, w=state.warmup;
  if(s==="const") return p;
  if(s==="cos")   return p*0.5*(1+Math.cos(Math.PI*step/T));
  /* warmcos */
  if(step<w)      return w>0 ? p*step/w : p;
  return p*0.5*(1+Math.cos(Math.PI*(step-w)/(T-w)));
}
/* ---- 损失（示意）：一维参数在早期病态/带噪目标上滚动 ---- */
function pseudoNoise(step){return 0.012*Math.sin(step*1.7)+0.008*Math.cos(step*0.43);}
function simulate(){
  var x=1.0, loss=[], blown=false;
  for(var s=0;s<=T;s++){
    var k=k0*Math.exp(-s/tau)+kf;
    x=x*(1-lrAt(s)*k)+pseudoNoise(s);     /* 大学习率×大曲率 → |1-lr·k|>1 → x 爆掉 */
    var L=Math.min(x*x+FLOOR, CLAMP);
    if(L>=DIVERGED) blown=true;
    if(blown) L=CLAMP;                     /* 训练一旦“飞了”就回不来——保持高位 */
    loss.push(L);
  }
  return loss;
}

var W=460,H=200,pl=42,pr=16,pt=16,pb=30;
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function px(step){return pl+step/T*(W-pl-pr);}
function pyLR(v,vmax){return (H-pb)-(v/vmax)*(H-pt-pb);}
function pyLoss(v){return (H-pb)-(v/CLAMP)*(H-pt-pb);}

function axes(svg,ylab){
  for(var gx=0;gx<=T;gx+=20){E(svg,"line",{x1:px(gx),y1:pt,x2:px(gx),y2:H-pb,"class":"gridl"});E(svg,"text",{x:px(gx),y:H-pb+13,"text-anchor":"middle","class":"alab"}).textContent=gx;}
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});
  E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});
  E(svg,"text",{x:pl,y:pt-4,"text-anchor":"middle","class":"alab"}).textContent=ylab;
  E(svg,"text",{x:W-pr,y:H-pb+24,"text-anchor":"end","class":"alab"}).textContent="训练步数";
}

function drawLR(cursor){
  var svg=document.getElementById("lrPlot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var vmax=Math.max(state.peak,0.2)*1.08;
  /* 预热带 */
  if(state.sched==="warmcos" && state.warmup>0)
    E(svg,"rect",{x:pl,y:pt,width:px(state.warmup)-pl,height:(H-pb)-pt,"class":"warmband"});
  axes(svg,"学习率");
  var pts=[];for(var s=0;s<=T;s++)pts.push(px(s)+","+pyLR(lrAt(s),vmax));
  E(svg,"polyline",{points:pts.join(" "),"class":"lrcurve"});
  E(svg,"line",{x1:px(cursor),y1:pt,x2:px(cursor),y2:H-pb,"class":"vline"});
  E(svg,"circle",{cx:px(cursor),cy:pyLR(lrAt(cursor),vmax),r:5,"class":"cursor"});
  if(state.sched==="warmcos" && state.warmup>0)
    E(svg,"text",{x:px(state.warmup/2),y:pt+13,"text-anchor":"middle","class":"alab",style:"fill:var(--color-accent)"}).textContent="预热";
}

function drawLoss(loss,cursor){
  var svg=document.getElementById("lossPlot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  axes(svg,"损失(示意)");
  var pts=[];for(var s=0;s<=cursor;s++)pts.push(px(s)+","+pyLoss(loss[s]));
  E(svg,"polyline",{points:pts.join(" "),"class":"losscurve"});
  /* 爆掉提示 */
  if(loss[cursor]>=CLAMP-1e-6)
    E(svg,"text",{x:(pl+W-pr)/2,y:pt+18,"text-anchor":"middle","class":"blowtag"}).textContent="损失飙升——训练发散冲飞";
  E(svg,"circle",{cx:px(cursor),cy:pyLoss(loss[cursor]),r:5,"class":"cursor"});
}

function setHeads(){
  var opts=document.querySelectorAll("#sched .opt");
  for(var i=0;i<opts.length;i++)opts[i].setAttribute("aria-pressed", opts[i].getAttribute("data-s")===state.sched ? "true":"false");
  /* 预热步数仅在 warmcos 下有意义 */
  document.getElementById("warm").disabled = (state.sched!=="warmcos");
}

function blowStep(loss){for(var s=0;s<=T;s++)if(loss[s]>=CLAMP-1e-6)return s;return -1;}

function caption(loss){
  var el=document.getElementById("caption"), bs=blowStep(loss), pk=state.peak.toFixed(2), last=loss[T];
  if(bs>=0){
    el.innerHTML="峰值学习率 <b>"+pk+"</b>，"+(state.sched==="warmcos"?"预热 "+state.warmup+" 步仍偏大":"开头没有预热")+"——第 <b>"+bs+"</b> 步左右损失就<b style=\"color:#b5524a\">飙升</b>（步子太大冲飞，训练发散）。试试切到“预热+余弦”，或调小峰值。";
  } else if(state.sched==="warmcos"){
    el.innerHTML="峰值学习率 <b>"+pk+"</b>，加 <b>"+state.warmup+"</b> 步预热再余弦退火：开头小步慢走稳住，再加速，后期慢慢收油——损失平稳下降，最后收到约 <b>"+last.toFixed(2)+"</b>。";
  } else if(state.sched==="cos"){
    el.innerHTML="余弦退火、峰值 <b>"+pk+"</b>，没有发散，最终损失约 <b>"+last.toFixed(2)+"</b>。把峰值调大一点，会看到没有预热时开头容易冲飞。";
  } else {
    el.innerHTML="常数学习率、峰值 <b>"+pk+"</b>，稳着没飞，最终损失约 <b>"+last.toFixed(2)+"</b>。把峰值调大，常数学习率开头就会把损失顶到天花板。";
  }
}

function render(cursor){
  if(cursor===undefined)cursor=T;
  document.getElementById("warmVal").textContent=state.warmup+" 步";
  document.getElementById("peakVal").textContent=state.peak.toFixed(2);
  setHeads();
  var loss=simulate();
  drawLR(cursor); drawLoss(loss,cursor);
  document.getElementById("finalPill").textContent="最终损失 "+loss[T].toFixed(2);
  if(cursor===T)caption(loss);
}

/* ---- 交互 ---- */
var autoIv=null;
function stopAuto(){if(autoIv){clearInterval(autoIv);autoIv=null;}}
document.querySelectorAll("#sched .opt").forEach(function(o){
  o.addEventListener("click",function(){stopAuto();state.sched=o.getAttribute("data-s");render();});
});
document.getElementById("warm").addEventListener("input",function(e){stopAuto();state.warmup=+e.target.value;render();});
document.getElementById("peak").addEventListener("input",function(e){stopAuto();state.peak=+e.target.value;render();});

render();

/* ---- 自动演示：金点从 0 扫到 T，逐步画出两条曲线 ---- */
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){render();return;}
  var c=0;
  autoIv=setInterval(function(){
    c+=3; if(c>=T){c=T;render(c);stopAuto();return;}
    render(c);
  },70);
},900);
})();
</script>
{% endraw %}
