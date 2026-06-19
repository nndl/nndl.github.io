---
layout: default
title: 混淆矩阵与多类指标
permalink: /viz/confusion-matrix/
redirect_from:
  - /v/confusion-matrix/
---

{% raw %}
<style>
.cmlab .heads{display:inline-flex;flex-wrap:wrap;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.cmlab .heads button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.88rem;color:var(--color-text-soft);padding:7px 15px;border-radius:999px;}
.cmlab .heads button.on{background:var(--color-bg-pure);color:var(--color-accent);font-weight:600;box-shadow:var(--shadow-sm);}
.cmlab .grid-lbl{font:600 12px var(--font-mono);fill:var(--color-text-muted);}
.cmlab .axis-lbl{font:600 12px var(--font-sans);fill:var(--color-text-soft);}
.cmlab .cell-n{font:700 16px var(--font-mono);}
.cmlab .cell-diag{stroke:var(--color-forest);stroke-width:2.5;}
.cmlab .cell-off{stroke:var(--color-border);stroke-width:1;}
.cmlab .row{display:flex;align-items:center;gap:8px;margin:7px 0;font-size:.86rem;}
.cmlab .row .rk{width:74px;flex-shrink:0;color:var(--color-text-soft);font-weight:600;}
.cmlab .row .track{flex:1;height:11px;background:var(--color-bg-section);border-radius:6px;overflow:hidden;display:flex;}
.cmlab .row .track i{height:100%;border-radius:6px;transition:width .3s var(--ease-out);}
.cmlab .row .pr{width:118px;flex-shrink:0;text-align:right;font:600 .8rem var(--font-mono);color:var(--color-text-muted);}
.cmlab .pills{display:flex;flex-wrap:wrap;gap:10px;margin-top:4px;}
.cmlab .pill{flex:1;min-width:96px;text-align:center;padding:11px 8px;border-radius:var(--radius-md);background:var(--color-bg-section);border:1px solid var(--color-border);}
.cmlab .pill small{display:block;font-size:.74rem;color:var(--color-text-muted);margin-bottom:3px;}
.cmlab .pill b{font:700 1.45rem var(--font-mono);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 混淆矩阵与多类指标

一个“准确率 89%”的模型，听上去挺靠谱。可如果其中有个稀有类别几乎全被认错，这个总分照样很高——因为它被海量的多数类“稀释”掉了。要看穿这种假象，得把每个类别拆开算精确率和召回率，再用**宏平均**（每类一票）和**微平均**（每个样本一票）两种方式汇总。类别不平衡时，这两个平均会明显分叉。点下面三个预设，盯着右边那几个数字怎么变。

<section class="vizui cmlab" id="cmlab">
  <p class="vizui__lead">这是一个三分类的<span style="color:var(--color-accent);font-weight:600">混淆矩阵</span>：行是<b>真实类别</b>、列是<b>预测类别</b>，格子里的数是样本个数。<span style="color:var(--color-forest);font-weight:600">对角线（绿框）= 预测对了</span>，对角线外都是认错的。换个预设，看准确率和宏/微平均怎么分家。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label>选个场景</label>
        <span class="heads" id="presets" role="tablist">
          <button type="button" data-p="0">均衡且准</button>
          <button type="button" data-p="1">某一类总被误判</button>
          <button type="button" data-p="2" class="on">类别不平衡</button>
        </span>
      </span>
    </div>
  </div>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">混淆矩阵 C[真实][预测]（格子越深，样本越多）</p>
      <svg class="vizui-chart" id="mat" viewBox="0 0 300 290" style="max-width:340px;margin:0 auto;display:block" role="img" aria-label="三分类混淆矩阵"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">各类精确率 / 召回率 / F1</p>
      <div id="bars"></div>
      <div class="pills" style="margin-top:16px">
        <div class="pill"><small>准确率</small><b id="pAcc" style="color:var(--color-accent)">—</b></div>
        <div class="pill"><small>宏平均 F1</small><b id="pMacro" style="color:var(--color-gold)">—</b></div>
        <div class="pill"><small>微平均 F1</small><b id="pMicro" style="color:var(--color-forest)">—</b></div>
      </div>
      <div style="margin-top:12px;padding:9px 12px;border-radius:var(--radius-md);background:var(--color-bg-section);font-size:.8rem;color:var(--color-text-soft);line-height:1.6">
        <span style="font-family:var(--font-mono)">精确率<sub>k</sub>=C[k][k]/列和</span>　·　<span style="font-family:var(--font-mono)">召回率<sub>k</sub>=C[k][k]/行和</span>　·　微平均 F1＝准确率
      </div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>准确率会骗人</b><p>它只数对角线占总数的比例。多数类一大、稀有类一小，稀有类全错也拉不动这个总分。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>宏平均：每类一票</b><p>先各类单独算 F1 再取平均。稀有类和多数类同等权重，所以稀有类拉胯会立刻把它拖下来。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>微平均：每样本一票</b><p>把所有类的 TP/FP/FN 汇总再算。单标签下它恰好等于准确率，天然偏向样本多的类。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var NAMES=["A","B","C"];
/* C[true][pred]，每个预设都是手工构造、数值已与下方指标核对一致 */
var PRESETS=[
  {name:"均衡且准", C:[[28,1,1],[2,27,1],[1,2,27]]},
  {name:"某一类总被误判", C:[[27,2,1],[14,12,4],[2,1,27]]},
  {name:"类别不平衡", C:[[78,2,0],[3,34,3],[2,4,4]]}
];
var cur=2, C=PRESETS[cur].C, animTimer=null;

function metrics(C){
  var K=C.length, N=0, diag=0, k, t, p;
  for(k=0;k<K;k++){for(p=0;p<K;p++){N+=C[k][p];} diag+=C[k][k];}
  var per=[], sumTP=0, sumFP=0, sumFN=0;
  for(k=0;k<K;k++){
    var TP=C[k][k], col=0, row=0;
    for(t=0;t<K;t++)col+=C[t][k];   // 预测为 k 的总数（列和）
    for(p=0;p<K;p++)row+=C[k][p];   // 真实为 k 的总数（行和）
    var P=col>0?TP/col:0, R=row>0?TP/row:0, F=(P+R)>0?2*P*R/(P+R):0;
    per.push({P:P,R:R,F1:F});
    sumTP+=TP; sumFP+=(col-TP); sumFN+=(row-TP);
  }
  var acc=N>0?diag/N:0;
  var macroF1=0; for(k=0;k<K;k++)macroF1+=per[k].F1; macroF1/=K;
  var microP=sumTP/(sumTP+sumFP), microR=sumTP/(sumTP+sumFN);
  var microF1=(microP+microR)>0?2*microP*microR/(microP+microR):0;
  return {N:N,acc:acc,per:per,macroF1:macroF1,microF1:microF1};
}

var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function lerp(t){ // 0→浅蓝填充，1→饱和青；t 为该格相对最大值的比例
  var r=Math.round(238-(238-21)*t), g=Math.round(243-(243-94)*t), b=Math.round(245-(245-117)*t);
  return "rgb("+r+","+g+","+b+")";
}
function drawMatrix(){
  var svg=document.getElementById("mat");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var K=C.length, ox=58, oy=46, cs=72, max=1, k, p;
  for(k=0;k<K;k++)for(p=0;p<K;p++)if(C[k][p]>max)max=C[k][p];
  // 顶标题：预测
  E(svg,"text",{x:ox+cs*K/2,y:18,"text-anchor":"middle","class":"axis-lbl"}).textContent="预测类别 →";
  // 左标题：真实（竖排）
  var yl=E(svg,"text",{x:16,y:oy+cs*K/2,"text-anchor":"middle","class":"axis-lbl",transform:"rotate(-90 16 "+(oy+cs*K/2)+")"});yl.textContent="真实类别 →";
  for(p=0;p<K;p++)E(svg,"text",{x:ox+cs*p+cs/2,y:oy-8,"text-anchor":"middle","class":"grid-lbl"}).textContent=NAMES[p];
  for(k=0;k<K;k++)E(svg,"text",{x:ox-10,y:oy+cs*k+cs/2+5,"text-anchor":"end","class":"grid-lbl"}).textContent=NAMES[k];
  for(k=0;k<K;k++)for(p=0;p<K;p++){
    var v=C[k][p], frac=v/max, diag=(k===p);
    E(svg,"rect",{x:ox+cs*p+3,y:oy+cs*k+3,width:cs-6,height:cs-6,rx:8,fill:lerp(frac),"class":diag?"cell-diag":"cell-off"});
    var dark=frac>0.5||diag;
    E(svg,"text",{x:ox+cs*p+cs/2,y:oy+cs*k+cs/2+6,"text-anchor":"middle","class":"cell-n",fill:dark?(diag?"#0b3d4c":"#fff"):"var(--color-text-soft)"}).textContent=v;
  }
}

function barRow(i,m){
  var col=["var(--color-accent)","var(--color-gold)","var(--color-forest)"][i];
  return '<div class="row"><span class="rk" style="color:'+col+'">类别 '+NAMES[i]+'</span>'
    +'<span class="track"><i style="width:'+(m.F1*100).toFixed(1)+'%;background:'+col+'"></i></span>'
    +'<span class="pr">P '+(m.P*100).toFixed(0)+'% R '+(m.R*100).toFixed(0)+'% F1 '+(m.F1*100).toFixed(0)+'%</span></div>';
}
function render(){
  var M=metrics(C);
  drawMatrix();
  var host=document.getElementById("bars"), html="";
  for(var i=0;i<M.per.length;i++)html+=barRow(i,M.per[i]);
  host.innerHTML=html;
  document.getElementById("pAcc").textContent=(M.acc*100).toFixed(1)+"%";
  document.getElementById("pMacro").textContent=(M.macroF1*100).toFixed(1)+"%";
  document.getElementById("pMicro").textContent=(M.microF1*100).toFixed(1)+"%";
  caption(M);
}
function caption(M){
  var el=document.getElementById("caption");
  var gap=(M.microF1-M.macroF1)*100;
  // 找最差的类（按 F1）
  var worst=0; for(var i=1;i<M.per.length;i++)if(M.per[i].F1<M.per[worst].F1)worst=i;
  var w=M.per[worst];
  if(gap<2){
    el.innerHTML="三个类别表现接近，<b>宏平均 F1（"+(M.macroF1*100).toFixed(1)+"%）</b>和<b>微平均 F1（"+(M.microF1*100).toFixed(1)+"%）几乎相等</b>，准确率也是这个数——此时一个总分就够用，没什么被掩盖。";
  } else {
    el.innerHTML="类别 <b>"+NAMES[worst]+"</b> 的召回率只有 <b>"+(w.R*100).toFixed(0)+"%</b>（F1 "+(w.F1*100).toFixed(0)+"%），但它样本少，拖不动总分："
      +"<b>微平均 F1 = 准确率 = "+(M.microF1*100).toFixed(1)+"%</b> 依旧很漂亮，而<b>宏平均 F1 掉到 "+(M.macroF1*100).toFixed(1)+"%</b>——两者差了约 "+gap.toFixed(0)+" 个百分点。只报准确率，就把 "+NAMES[worst]+" 类的崩盘藏起来了。";
  }
}

function clearAnim(){ if(animTimer){clearInterval(animTimer);animTimer=null;} }
function setPreset(i){
  cur=i; C=PRESETS[i].C;
  var btns=document.getElementById("presets").children;
  for(var b=0;b<btns.length;b++)btns[b].classList.toggle("on",b===i);
  render();
}
document.getElementById("presets").addEventListener("click",function(e){
  var btn=e.target.closest("button"); if(!btn)return;
  clearAnim();
  setPreset(+btn.getAttribute("data-p"));
});

/* 启动 + 自动演示：依次走 均衡→某类误判→不平衡，最后停在不平衡（分叉最明显） */
setPreset(2);
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){setPreset(2);return;}
  var seq=[0,1,2], k=0;
  setPreset(seq[0]); k=1;
  animTimer=setInterval(function(){
    if(k>=seq.length){clearAnim();return;}
    setPreset(seq[k]); k++;
  },1500);
},900);
})();
</script>
{% endraw %}
