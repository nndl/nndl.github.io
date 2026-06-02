---
layout: default
title: 精确率与召回率
permalink: /viz/precision-recall/
redirect_from:
  - /v/precision-recall/
---

{% raw %}
<style>
.prlab .axis{stroke:var(--color-border);stroke-width:1;}
.prlab .alab{font:11px var(--font-mono);fill:var(--color-text-muted);}
.prlab .thr{stroke:var(--color-accent);stroke-width:2;}
.prlab .thr-lbl{font:600 11px var(--font-mono);fill:var(--color-accent);}
.prlab .dot-pos{fill:var(--color-accent-light);}
.prlab .dot-neg{fill:#b5524a;}
.prlab .dim{opacity:.28;}
.prlab .cm{display:grid;grid-template-columns:auto 1fr 1fr;gap:4px;font-size:.82rem;max-width:340px;margin:0 auto;}
.prlab .cm .h{display:flex;align-items:center;justify-content:center;color:var(--color-text-muted);font-weight:600;text-align:center;padding:2px;}
.prlab .cm .cell{border-radius:6px;padding:8px 4px;text-align:center;color:#fff;}
.prlab .cm .cell b{display:block;font:700 1.2rem var(--font-mono);}
.prlab .cm .cell small{font-size:.72rem;opacity:.92;}
.prlab .tp{background:var(--color-forest);}
.prlab .tn{background:#5a7d72;}
.prlab .fp{background:#b5524a;}
.prlab .fn{background:#c97c54;}
.prlab .mbar{height:12px;border-radius:6px;background:var(--color-bg-section);overflow:hidden;margin-top:3px;}
.prlab .mbar i{display:block;height:100%;border-radius:6px;transition:width .3s var(--ease-out);}
.prlab .roc-pt{fill:var(--color-gold);stroke:#fff;stroke-width:1.5;}
.prlab .roc-curve{fill:none;stroke:var(--color-accent);stroke-width:2;}
.prlab .roc-diag{stroke:var(--color-border-strong);stroke-width:1;stroke-dasharray:3 3;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 精确率与召回率

判断一个模型“准不准”，光看准确率往往不够。比如查垃圾邮件：你可以把阈值调得很松，把可疑的全拦下来——召回率（该抓的都抓到了）很高，但精确率（抓的里面有多少真是垃圾）会下降，好邮件也被误杀。这两个指标天生此消彼长。拖动判定阈值，亲眼看它俩怎么互相拉扯。

<section class="vizui prlab" id="prlab">
  <p class="vizui__lead">每个点是一封邮件：<span style="color:var(--color-accent-light);font-weight:600">蓝点=真垃圾</span>，<span style="color:#b5524a;font-weight:600">红点=正常邮件</span>，横轴是模型打的“垃圾分”。竖线右边会被判为垃圾。拖动它看四种结果和指标怎么变。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="thr">判定阈值</label>
        <input type="range" id="thr" min="0" max="1" step="0.01" value="0.5" style="width:220px">
        <output id="thrVal">0.50</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 扫一遍阈值</button>
    </div>
    <svg class="vizui-chart" id="strip" viewBox="0 -12 460 122" role="img" aria-label="邮件分数分布与阈值"></svg>
  </div>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">混淆矩阵</p>
      <div class="cm" id="cm">
        <div class="h"></div><div class="h">实际垃圾</div><div class="h">实际正常</div>
        <div class="h">判为垃圾</div><div class="cell tp" id="cTP"><b>0</b><small>抓对 TP</small></div><div class="cell fp" id="cFP"><b>0</b><small>误杀 FP</small></div>
        <div class="h">判为正常</div><div class="cell fn" id="cFN"><b>0</b><small>漏掉 FN</small></div><div class="cell tn" id="cTN"><b>0</b><small>放对 TN</small></div>
      </div>
      <div style="margin-top:14px">
        <div style="display:flex;justify-content:space-between;font-size:.86rem"><span>精确率（抓的里多少是真垃圾）</span><b id="precV" style="font-family:var(--font-mono);color:var(--color-accent)">—</b></div>
        <div class="mbar"><i id="precBar" style="background:var(--color-accent)"></i></div>
        <div style="display:flex;justify-content:space-between;font-size:.86rem;margin-top:8px"><span>召回率（真垃圾抓到多少）</span><b id="recV" style="font-family:var(--font-mono);color:var(--color-gold)">—</b></div>
        <div class="mbar"><i id="recBar" style="background:var(--color-gold)"></i></div>
      </div>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">ROC 曲线（整体能力）</p>
      <svg class="vizui-chart" id="roc" viewBox="0 0 220 220" style="max-width:260px;margin:0 auto;display:block" role="img" aria-label="ROC 曲线"></svg>
      <div style="text-align:center;font:.82rem var(--font-mono);color:var(--color-text-muted)">横轴=误杀率　纵轴=抓到率　AUC=<span id="auc">—</span></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var thr=0.5, items=[], playing=false, timer=null;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function gen(){var r=rng(7);items=[];
  for(var i=0;i<22;i++)items.push({s:Math.max(0,Math.min(1,0.66+gauss(r)*0.17)),pos:true,jy:r()});
  for(var j=0;j<22;j++)items.push({s:Math.max(0,Math.min(1,0.36+gauss(r)*0.17)),pos:false,jy:r()});
}
function counts(t){var TP=0,FP=0,FN=0,TN=0;items.forEach(function(it){var pp=it.s>=t;if(it.pos&&pp)TP++;else if(!it.pos&&pp)FP++;else if(it.pos&&!pp)FN++;else TN++;});return {TP:TP,FP:FP,FN:FN,TN:TN};}

var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function sx(v){return 24+v*(460-44);}
function drawStrip(){
  var svg=document.getElementById("strip");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:24,y1:88,x2:460-20,y2:88,"class":"axis"});
  [0,0.5,1].forEach(function(v){E(svg,"text",{x:sx(v),y:103,"text-anchor":"middle","class":"alab"}).textContent=v.toFixed(1);});
  items.forEach(function(it){var pp=it.s>=thr;
    E(svg,"circle",{cx:sx(it.s),cy:18+it.jy*60,r:4.5,"class":(it.pos?"dot-pos":"dot-neg")+(pp?"":" dim")});});
  E(svg,"line",{x1:sx(thr),y1:8,x2:sx(thr),y2:92,"class":"thr"});
  E(svg,"text",{x:sx(thr),y:6,"text-anchor":"middle","class":"thr-lbl"}).textContent="阈值";
}
function drawROC(){
  var svg=document.getElementById("roc");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var P=22,Ngn=22,pad=24,S=220-2*pad;
  function rx(f){return pad+f*S;} function ry(t){return (220-pad)-t*S;}
  E(svg,"line",{x1:pad,y1:220-pad,x2:220-pad,y2:220-pad,"class":"axis"});
  E(svg,"line",{x1:pad,y1:pad,x2:pad,y2:220-pad,"class":"axis"});
  E(svg,"line",{x1:rx(0),y1:ry(0),x2:rx(1),y2:ry(1),"class":"roc-diag"});
  // 扫阈值生成曲线 + AUC
  var pts=[],auc=0,prev=null;
  for(var t=1.001;t>=-0.001;t-=0.02){var c=counts(t);var fpr=c.FP/(c.FP+c.TN||1),tpr=c.TP/(c.TP+c.FN||1);pts.push([fpr,tpr]);
    if(prev)auc+=(fpr-prev[0])*(tpr+prev[1])/2; prev=[fpr,tpr];}
  E(svg,"polyline",{points:pts.map(function(p){return rx(p[0])+","+ry(p[1]);}).join(" "),"class":"roc-curve"});
  var cc=counts(thr);var cf=cc.FP/(cc.FP+cc.TN||1),ct=cc.TP/(cc.TP+cc.FN||1);
  E(svg,"circle",{cx:rx(cf),cy:ry(ct),r:5,"class":"roc-pt"});
  document.getElementById("auc").textContent=auc.toFixed(2);
}
function setCell(id,n){document.querySelector("#"+id+" b").textContent=n;}
function render(){
  document.getElementById("thrVal").textContent=thr.toFixed(2);
  var c=counts(thr);
  setCell("cTP",c.TP);setCell("cFP",c.FP);setCell("cFN",c.FN);setCell("cTN",c.TN);
  var prec=c.TP+c.FP>0?c.TP/(c.TP+c.FP):1, rec=c.TP+c.FN>0?c.TP/(c.TP+c.FN):0;
  document.getElementById("precV").textContent=(prec*100).toFixed(0)+"%";
  document.getElementById("recV").textContent=(rec*100).toFixed(0)+"%";
  document.getElementById("precBar").style.width=(prec*100)+"%";
  document.getElementById("recBar").style.width=(rec*100)+"%";
  drawStrip();drawROC();caption(prec,rec,c);
}
function caption(prec,rec,c){
  var el=document.getElementById("caption");
  if(thr<=0.12)el.innerHTML="阈值很低：几乎把所有邮件都判成垃圾，<b>召回率</b> "+(rec*100).toFixed(0)+"%（真垃圾基本没漏），但<b>精确率</b>只有 "+(prec*100).toFixed(0)+"%——大量正常邮件被误杀（红点也被拦）。";
  else if(thr>=0.88)el.innerHTML="阈值很高：只有最像垃圾的才被拦，<b>精确率</b> "+(prec*100).toFixed(0)+"%（抓的几乎都对），但<b>召回率</b>掉到 "+(rec*100).toFixed(0)+"%——很多真垃圾溜了过去（蓝点没被拦）。";
  else el.innerHTML="当前阈值：精确率 <b>"+(prec*100).toFixed(0)+"%</b>、召回率 <b>"+(rec*100).toFixed(0)+"%</b>。往左拖召回率升、精确率降；往右拖反过来——这就是两者的权衡。";
}

document.getElementById("thr").addEventListener("input",function(e){thr=+e.target.value;render();});
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 扫一遍阈值";}
document.getElementById("auto").addEventListener("click",function(){
  if(playing){stop();return;}playing=true;document.getElementById("auto").textContent="⏸ 暂停";var v=0.0,sl=document.getElementById("thr");
  timer=setInterval(function(){v+=0.02;if(v>1){stop();return;}thr=v;sl.value=v;render();},120);
});

/* 启动 + 自动演示 */
gen();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  document.getElementById("auto").click();
},1000);
})();
</script>
{% endraw %}
