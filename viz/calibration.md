---
layout: default
title: 概率校准：模型说的90%靠谱吗
permalink: /viz/calibration/
redirect_from:
  - /v/calibration/
---

{% raw %}
<style>
.cblab .axis{stroke:var(--color-border);stroke-width:1;}
.cblab .grid{stroke:var(--color-border);stroke-width:1;opacity:.4;}
.cblab .alab{font:11px var(--font-mono);fill:var(--color-text-muted);}
.cblab .diag{stroke:var(--color-border-strong);stroke-width:1.4;stroke-dasharray:4 3;}
.cblab .gap{stroke:#b5524a;stroke-width:1.6;opacity:.55;}
.cblab .relbar{fill:var(--color-accent);opacity:.18;stroke:var(--color-accent);stroke-width:1;}
.cblab .relpt{fill:var(--color-accent-light);stroke:#fff;stroke-width:1.4;}
.cblab .relline{fill:none;stroke:var(--color-accent);stroke-width:2.2;}
.cblab .axtitle{font:11px var(--font-sans);fill:var(--color-text-muted);}
.cblab .ecepill{font:700 1.1rem var(--font-mono);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 概率校准：模型说的90%靠谱吗

模型不只给答案，还给一个“把握”——“我有90%的把握这是猫”。可这个90%能信吗？一个**校准良好**的模型，凡是它说90%把握的那些预测，约90%真的对；说60%的，约60%对。把预测按把握分桶，横轴画“平均把握”、纵轴画“实际正确率”，校准完美就落在**对角线**上。可惜现代神经网络几乎都**过度自信**：点全在对角线**下方**——嘴上90%，实际只有70%。有个出奇简单的修法叫**温度缩放**：把打分（logit）统统除以一个温度 T，就能把曲线拉回对角线。拖动温度试试。

<section class="vizui cblab" id="cblab">
  <p class="vizui__lead">600 个二分类样本，原始模型（T=1）把话说得太满。横轴是模型的平均把握，纵轴是这一桶里真正答对的比例：<span style="color:var(--color-accent-light);font-weight:600">蓝点</span>落在<span style="color:var(--color-text-muted)">虚线对角线</span>下方，就说明它过度自信。调大温度，看点怎么爬回对角线、ECE 怎么变小。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="temp">温度 T</label>
        <input type="range" id="temp" min="0.5" max="4" step="0.05" value="1" style="width:230px">
        <output id="tempVal">1.00</output>
      </span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill">ECE = <span class="ecepill" id="ecePill">—</span></span>
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动校准</button>
    </div>
  </div>

  <div class="vizui-panel">
    <p class="vizui-panel__title">可靠性图（reliability diagram）</p>
    <svg class="vizui-chart" id="rel" viewBox="0 0 360 300" style="max-width:420px;margin:0 auto;display:block" role="img" aria-label="可靠性图：平均把握对实际正确率"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>低温 / 原始 → 过度自信</b><p>T≤1 时打分被放大，模型把话说太满，点落在对角线<b>下方</b>：说90%，实际只对70%。ECE 大。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>调大温度 → 校准回对角线</b><p>除以一个合适的 T，把过满的概率往 0.5 拉平，点贴回对角线，ECE 降到最低。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>温度再大 → 又欠自信</b><p>T 过头，概率被压得太平，点跑到对角线<b>上方</b>，变成不敢下判断，ECE 又升回去。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var T=1.0, playing=false, timer=null;
var N=600, S=2.2, B=10;

/* 确定性种子 RNG（mulberry32）+ Box-Muller 高斯 */
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function sig(x){return 1/(1+Math.exp(-x));}

/* 生成样本：潜变量 z；真标签以 σ(z) 为概率取 1；原始模型 logit = S·z（S>1 → 过度自信） */
var items=[];
(function gen(){
  var r=rng(42);
  for(var i=0;i<N;i++){
    var z=gauss(r)*1.6;
    var y=(r()<sig(z))?1:0;
    items.push({z:z,y:y});
  }
})();

/* 给定 T，分桶算每桶 平均把握 / 正确率 / 数量，以及 ECE */
function bins(t){
  var bn=[],bc=[],ba=[],b;
  for(b=0;b<B;b++){bn[b]=0;bc[b]=0;ba[b]=0;}
  items.forEach(function(it){
    var p=sig(S*it.z/t);
    var conf=Math.max(p,1-p);
    var correct=((p>=0.5?1:0)===it.y)?1:0;
    var k=Math.min(B-1,Math.floor((conf-0.5)/0.5*B));if(k<0)k=0;
    bn[k]++;bc[k]+=conf;ba[k]+=correct;
  });
  var rows=[],ece=0;
  for(b=0;b<B;b++){
    if(bn[b]===0){rows.push(null);continue;}
    var mc=bc[b]/bn[b],ma=ba[b]/bn[b];
    ece+=(bn[b]/N)*Math.abs(ma-mc);
    rows.push({n:bn[b],conf:mc,acc:ma});
  }
  return {rows:rows,ece:ece};
}

var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}

/* 绘图坐标：对角线区域为 [0.5,1]×[0,1] 映射到正方形画布 */
var PL=46,PR=18,PT=14,PB=40,GX=360,GY=300;
function px(c){return PL+(c-0.5)/0.5*(GX-PL-PR);}     // 把握 0.5..1
function py(a){return (GY-PB)-a*(GY-PT-PB);}          // 正确率 0..1

function drawRel(){
  var svg=document.getElementById("rel");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var d=bins(T);
  // 网格
  [0.5,0.6,0.7,0.8,0.9,1.0].forEach(function(v){E(svg,"line",{x1:px(v),y1:PT,x2:px(v),y2:GY-PB,"class":"grid"});});
  [0,0.2,0.4,0.6,0.8,1.0].forEach(function(v){E(svg,"line",{x1:PL,y1:py(v),x2:GX-PR,y2:py(v),"class":"grid"});});
  E(svg,"line",{x1:PL,y1:GY-PB,x2:GX-PR,y2:GY-PB,"class":"axis"});
  E(svg,"line",{x1:PL,y1:PT,x2:PL,y2:GY-PB,"class":"axis"});
  // 对角线 = 完美校准
  E(svg,"line",{x1:px(0.5),y1:py(0.5),x2:px(1.0),y2:py(1.0),"class":"diag"});
  // 每桶：误差条（柱顶=正确率）、把握→正确率的落差竖线、点
  var pts=[];
  d.rows.forEach(function(row,b){
    if(!row)return;
    var cx=px(row.conf);
    // 柱：以这桶平均把握为 x，画一根从对角线到实际正确率的灰柱不好叠，改画淡条表示样本量
    var bw=(GX-PL-PR)/B*0.62;
    var bx0=PL+b/B*(GX-PL-PR)+((GX-PL-PR)/B-bw)/2;
    E(svg,"rect",{x:bx0,y:py(row.acc),width:bw,height:(GY-PB)-py(row.acc),"class":"relbar"});
    // 落差线：从 (conf, conf) 对角点 到 (conf, acc) 实际点
    E(svg,"line",{x1:cx,y1:py(row.conf),x2:cx,y2:py(row.acc),"class":"gap"});
    pts.push([cx,py(row.acc)]);
  });
  // 折线 + 点
  if(pts.length>1)E(svg,"polyline",{points:pts.map(function(p){return p[0]+","+p[1];}).join(" "),"class":"relline"});
  pts.forEach(function(p){E(svg,"circle",{cx:p[0],cy:p[1],r:4.2,"class":"relpt"});});
  // 轴刻度
  [0.5,0.7,0.9,1.0].forEach(function(v){E(svg,"text",{x:px(v),y:GY-PB+15,"text-anchor":"middle","class":"alab"}).textContent=v.toFixed(1);});
  [0,0.5,1.0].forEach(function(v){E(svg,"text",{x:PL-7,y:py(v)+4,"text-anchor":"end","class":"alab"}).textContent=v.toFixed(1);});
  E(svg,"text",{x:(PL+GX-PR)/2,y:GY-6,"text-anchor":"middle","class":"axtitle"}).textContent="平均把握（模型说的概率）";
  E(svg,"text",{x:14,y:(PT+GY-PB)/2,"text-anchor":"middle","class":"axtitle",transform:"rotate(-90 14 "+((PT+GY-PB)/2)+")"}).textContent="实际正确率";
  return d;
}

function render(){
  document.getElementById("tempVal").textContent=T.toFixed(2);
  var d=drawRel();
  var pill=document.getElementById("ecePill");
  pill.textContent=d.ece.toFixed(3);
  pill.style.color=d.ece>0.09?"#b5524a":d.ece<0.06?"var(--color-forest)":"var(--color-gold)";
  caption(d);
}

function caption(d){
  var el=document.getElementById("caption");
  // 高把握桶（conf>0.8）的平均落差，判断在对角线哪一侧
  var sg=0,sn=0;
  d.rows.forEach(function(r){if(r&&r.conf>0.8){sg+=(r.acc-r.conf)*r.n;sn+=r.n;}});
  var gap=sn?sg/sn:0;
  var msg;
  if(T<=1.05)
    msg="<b>原始模型（T="+T.toFixed(2)+"）：</b>高把握的那些桶里，实际正确率比嘴上的把握低约 <b>"+Math.abs(gap*100).toFixed(0)+" 个百分点</b>，点全在对角线<b>下方</b>——典型的过度自信，ECE 高达 "+d.ece.toFixed(3)+"。";
  else if(d.ece<=0.06)
    msg="<b>校准良好（T="+T.toFixed(2)+"）：</b>点贴回了对角线，说90%就约90%对，ECE 降到 "+d.ece.toFixed(3)+"——温度缩放把过满的概率拉平到刚刚好。";
  else if(gap>0.04)
    msg="<b>温度过头（T="+T.toFixed(2)+"）：</b>概率被压得太平，点跑到对角线<b>上方</b>，模型变得欠自信，ECE 又回升到 "+d.ece.toFixed(3)+"。";
  else
    msg="温度 T="+T.toFixed(2)+"：ECE = "+d.ece.toFixed(3)+"。继续调大温度让点贴近对角线，ECE 会降到最低再反弹。";
  el.innerHTML=msg;
}

function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动校准";}
document.getElementById("temp").addEventListener("input",function(e){stop();T=+e.target.value;render();});
document.getElementById("auto").addEventListener("click",function(){
  if(playing){stop();return;}
  playing=true;document.getElementById("auto").textContent="⏸ 暂停";
  var v=0.5,sl=document.getElementById("temp");
  timer=setInterval(function(){v+=0.1;if(v>4.0){stop();return;}T=v;sl.value=v.toFixed(2);render();},150);
});

/* 启动 + 自动演示：从过度自信 T=0.5 一路升到 T=4，看点爬回对角线再越过 */
render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){
    var sl=document.getElementById("temp");T=2.2;sl.value="2.20";render();return;  // 直接跳到最校准的状态
  }
  document.getElementById("auto").click();
},900);
})();
</script>
{% endraw %}
