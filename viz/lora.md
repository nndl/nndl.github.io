---
layout: default
title: LoRA 低秩微调
permalink: /viz/lora/
redirect_from:
  - /v/lora/
---

{% raw %}
<style>
.lolab .cell{stroke:#fff;stroke-width:.6;}
.lolab .frozen{fill:#cdd6d4;}
.lolab .train{fill:var(--color-accent);}
.lolab .delta{fill:var(--color-gold);opacity:.5;}
.lolab .mlab{font:600 12px var(--font-mono);fill:var(--color-text-soft);text-anchor:middle;}
.lolab .op{font:600 18px var(--font-mono);fill:var(--color-text-muted);text-anchor:middle;}
.lolab .lock{font-size:13px;}
.lolab .pcompare{display:grid;grid-template-columns:auto 1fr auto;gap:6px 12px;align-items:center;margin-top:6px;}
.lolab .pbar{height:20px;border-radius:6px;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# LoRA 低秩微调

把一个几百亿参数的大模型微调到你的新任务上，如果每个权重都更新，既费显存又费时间，还得为每个任务存一整份模型。LoRA 的巧思是：**把原来的大权重矩阵冻住完全不动，只在旁边训练一个“低秩补丁”**——用两个又瘦又长的小矩阵 A、B 相乘得到一个修正量 ΔW = A·B，加到原权重上。因为 A、B 很小，要训练的参数从 d×d 骤降到 2×d×r（r 很小，比如 4、8）。一个几 GB 的模型，补丁可能只有几 MB。拖动维度和秩，看要训练的参数少了多少。

<section class="lolab vizui" id="lolab">
  <p class="vizui__lead"><span style="color:#9aa5a3;font-weight:600">灰=冻结的原权重 W（不训练）</span>，<span style="color:var(--color-accent);font-weight:600">蓝=要训练的小矩阵 A、B</span>。A、B 相乘得到低秩修正 ΔW，与冻结的 W 相加，就是金色的更新后权重 W′。真正训练的只有蓝色那点。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="d">权重维度 d</label><input type="range" id="d" min="6" max="16" step="1" value="12" style="width:120px"><output id="dVal">12</output></span>
      <span class="vizui-field"><label for="r">秩 r</label><input type="range" id="r" min="1" max="6" step="1" value="2" style="width:120px"><output id="rVal">2</output></span>
    </div>
    <svg class="vizui-chart" id="diagram" viewBox="0 0 460 220" role="img" aria-label="LoRA 矩阵分解"></svg>
    <div class="pcompare" id="pcompare"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#9aa5a3"><b>冻结原权重</b><p>大矩阵 W 一个数都不改，省去对它求梯度、存优化器状态的开销。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>只训低秩补丁</b><p>用两个瘦长矩阵 A·B 表达修正，参数从 d² 降到 2dr——常常省 99% 以上。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>一基座多补丁</b><p>不同任务训不同的小补丁、共用同一个大模型，切换任务只换补丁，几 MB 而已。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var d=12, r=2;
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function grid(svg,x,y,cols,rows,cls,cs){for(var i=0;i<rows;i++)for(var j=0;j<cols;j++)E(svg,"rect",{x:x+j*cs,y:y+i*cs,width:cs-0.5,height:cs-0.5,"class":"cell "+cls});}
function draw(){
  var svg=document.getElementById("diagram");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var cs=Math.min(11,140/d), Wd=d*cs;
  var y0=30;
  // W (frozen)
  var xW=20;grid(svg,xW,y0,d,d,"frozen",cs);
  E(svg,"text",{x:xW+Wd/2,y:y0-8,"class":"mlab"}).textContent="W（"+d+"×"+d+"）";
  E(svg,"text",{x:xW+Wd/2,y:y0+Wd+16,"class":"mlab lock"}).textContent="🔒 冻结";
  E(svg,"text",{x:xW+Wd+20,y:y0+Wd/2+6,"class":"op"}).textContent="+";
  // A (d×r)
  var xA=xW+Wd+40;grid(svg,xA,y0,r,d,"train",cs);
  E(svg,"text",{x:xA+r*cs/2,y:y0-8,"class":"mlab"}).textContent="A";
  E(svg,"text",{x:xA+r*cs+12,y:y0+Wd/2+6,"class":"op"}).textContent="×";
  // B (r×d)
  var xB=xA+r*cs+24;grid(svg,xB,y0,d,r,"train",cs);
  E(svg,"text",{x:xB+Wd/2,y:y0-8,"class":"mlab"}).textContent="B";
  E(svg,"text",{x:xB+Wd+18,y:y0+Wd/2+6,"class":"op"}).textContent="=";
  // 结果：更新后的权重 W′ = W + A·B（d×d）
  var xD=xB+Wd+34;grid(svg,xD,y0,d,d,"delta",cs);
  E(svg,"text",{x:xD+Wd/2,y:y0-8,"class":"mlab",style:"fill:var(--color-gold)"}).textContent="W′";
  E(svg,"text",{x:xD+Wd/2,y:y0+Wd+16,"class":"mlab"}).textContent="更新后";
  // A·B 即低秩修正 ΔW —— 真正训练的只有这部分（秩 r）
  E(svg,"text",{x:(xA+xB+Wd)/2,y:y0+Wd+16,"class":"mlab"}).textContent="A·B = ΔW（秩 "+r+"）";
  // 动态 viewBox：随 d、r 自适应，矩阵再大也不会超出图框被裁剪
  svg.setAttribute("viewBox","0 0 "+(xD+Wd+12)+" "+(y0+Wd+28));
}
function render(){
  document.getElementById("dVal").textContent=d;document.getElementById("rVal").textContent=r;
  draw();
  var full=d*d, lora=2*d*r, ratio=full/lora;
  var host=document.getElementById("pcompare");host.innerHTML="";
  function row(label,val,frac,col){return '<span style="font-size:.85rem">'+label+'</span><div class="pbar" style="background:'+col+';width:'+Math.max(4,frac*100)+'%"></div><b style="font-family:var(--font-mono)">'+val+'</b>';}
  host.innerHTML=row("全量微调 d²",full+" 个",1,"#cdd6d4")+row("LoRA 2·d·r",lora+" 个",lora/full,"var(--color-accent)");
  caption(full,lora,ratio);
}
function caption(full,lora,ratio){
  document.getElementById("caption").innerHTML="d="+d+"、r="+r+"：全量微调要训 <b>"+full+"</b> 个参数，LoRA 只训 <b style='color:var(--color-accent)'>"+lora+"</b> 个，省了 <b>"+ratio.toFixed(1)+"×</b>。真实模型里 d 是几千，省得更夸张——比如 d=4096、r=8，比例是 4096/16 = <b>256×</b>。";
}
document.getElementById("d").addEventListener("input",function(e){d=+e.target.value;render();});
document.getElementById("r").addEventListener("input",function(e){r=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[[12,2],[16,1],[16,6],[10,2]],k=0,sd=document.getElementById("d"),sr=document.getElementById("r");
  var iv=setInterval(function(){d=seq[k][0];r=seq[k][1];sd.value=d;sr.value=r;render();k++;if(k>=seq.length)clearInterval(iv);},1100);},1000);
})();
</script>
{% endraw %}
