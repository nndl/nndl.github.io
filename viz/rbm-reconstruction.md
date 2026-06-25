---
layout: default
title: 受限玻尔兹曼机：编码与重构
description: "两层网络来回采样：把带噪数字编码成几个特征隐单元，再只凭它们重构回来——噪声被滤掉，叠起来就是深度信念网络。"
permalink: /viz/rbm-reconstruction/
redirect_from:
  - /v/rbm-reconstruction/
---

{% raw %}
<style>
.rblab svg{max-width:100%;height:auto;}
.rblab .px{stroke:#fff;stroke-width:0.6;}
.rblab .hcell{stroke:#fff;stroke-width:0.4;}
.rblab .hbox{fill:var(--color-bg-section);stroke:var(--color-border);stroke-width:1;}
.rblab .conn{stroke:var(--color-border-strong);stroke-width:1;fill:none;}
.rblab .conn.on{stroke:var(--color-accent);stroke-width:2.2;}
.rblab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
.rblab .tag{font:10px var(--font-mono);fill:var(--color-text-soft);}
.rblab .ph{font:12px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 受限玻尔兹曼机：压成特征，再重构回来

受限玻尔兹曼机（RBM）有两层：能看见的**可见层**（这里是图像像素）和看不见的**隐藏层**（少量特征单元）。“受限”指的是**层内没有连接**，只有可见↔隐藏之间全连着，而且来回用同一套权重。它的招牌动作是来回采样：先由图像算出隐单元（**编码 v→h**），再只凭这几个隐单元把图像画回来（**重构 h→v′**）。训练后，每个隐单元会学成一个**特征检测器**——于是 35 个像素被压进 3 个特征，重构时把激活的特征叠加起来，反而能把输入里的噪声滤掉。给一张带噪的数字，点“下一步”，看它被编码、再被干净地重构出来。

<section class="vizui rblab" id="rblab">
  <p class="vizui__lead">左边是带噪输入 v；中间 3 个隐单元各自显示它学到的特征（一个数字模板），点亮程度＝被激活的强度；右边是只凭隐单元重构出的 v′。<b>层内无连接</b>，每个像素与每个隐单元全连接，来回共用权重。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="step" type="button">▶ 下一步</button>
      <button class="vizui-btn" id="auto" type="button">自动</button>
      <button class="vizui-btn" id="digit" type="button">↻ 换数字</button>
      <button class="vizui-btn" id="noise" type="button">重新加噪</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 500 250" role="img" aria-label="RBM 编码与重构"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>受限＝层内无连接</b><p>只有可见↔隐藏之间相连，来回共用同一套权重——这让条件分布好算、能高效采样。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>隐单元＝学到的特征</b><p>训练后每个隐单元变成一个特征检测器；35 个像素被压成 3 个特征，是一种瓶颈编码。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>重构＝叠加激活的特征</b><p>只凭激活的隐单元重画图像，画不出噪声，于是输入被去噪／补全——堆叠多层即深度信念网络。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var GLY={
 "1":["..#..",".##..","..#..","..#..","..#..","..#..",".###."],
 "4":["#..#.","#..#.","#..#.","#####","...#.","...#.","...#."],
 "7":["#####","....#","...#.","..#..","..#..","..#..","..#.."]
};
var PN=["1","4","7"],R=7,Cc=5,M=R*Cc;
function flat(g){var a=[];for(var r=0;r<R;r++)for(var c=0;c<Cc;c++)a.push(g[r][c]==="#"?1:0);return a;}
var P=PN.map(function(n){return flat(GLY[n]);}),K=P.length;
function sig(z){return 1/(1+Math.exp(-z));}
function encode(v){var a=[];for(var k=0;k<K;k++){var s=0;for(var i=0;i<M;i++)s+=(2*v[i]-1)*(2*P[k][i]-1);a.push(sig(9*(s/M-0.42)));}return a;}
function reconstruct(a){var v=[];for(var i=0;i<M;i++){var s=0;for(var k=0;k<K;k++)s+=a[k]*(2*P[k][i]-1);v.push(sig(5*s));}return v;}
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
var curIdx=0,seed=3,v0=[],step=0,timer=null,playing=false,MAXS=3;
function corrupt(){var b=P[curIdx].slice(),r=rng(seed+curIdx*101),idx=[];for(var i=0;i<M;i++)idx.push(i);
  for(var i=M-1;i>0;i--){var j=(r()*(i+1))|0,t=idx[i];idx[i]=idx[j];idx[j]=t;}
  for(var i=0;i<5;i++)b[idx[i]]=1-b[idx[i]];v0=b;}
function compute(){var a1=encode(v0),v2=reconstruct(a1),a2=encode(v2),v3=reconstruct(a2);
  return {a:(step>=3?a2:a1),v:(step>=3?v3:v2)};}
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function pcol(val){var t=val<0?0:val>1?1:val,lo=[244,246,248],hi=[31,41,55];
  return "rgb("+Math.round(lo[0]+(hi[0]-lo[0])*t)+","+Math.round(lo[1]+(hi[1]-lo[1])*t)+","+Math.round(lo[2]+(hi[2]-lo[2])*t)+")";}
function grid(svg,vals,ox,oy,cs,soft){for(var r=0;r<R;r++)for(var c=0;c<Cc;c++){var v=vals?vals[r*Cc+c]:0;
  E(svg,"rect",{x:ox+c*cs,y:oy+r*cs,width:cs,height:cs,fill:vals?pcol(soft?v:(v>0.5?1:0)):"#f4f6f8","class":"px"});}}
var HX=250,HY=[44,108,172];
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var st=compute(),a=st.a;
  /* 连接线 */
  for(var k=0;k<K;k++){var cy=HY[k]+14;
    E(svg,"line",{x1:120,y1:108,x2:HX-12,y2:cy,"class":"conn"+(step===1||step>=3?" on":"")});
    E(svg,"line",{x1:HX+12,y1:cy,x2:380,y2:108,"class":"conn"+(step>=2?" on":"")});}
  /* 输入 */
  E(svg,"text",{x:80,y:36,"text-anchor":"middle","class":"lbl"},"输入 v（带噪）");
  grid(svg,v0,40,52,16,false);
  /* 隐单元（特征模板 + 激活光圈） */
  E(svg,"text",{x:HX,y:30,"text-anchor":"middle","class":"lbl"},"隐单元 h（学到的特征）");
  for(var k=0;k<K;k++){var oy=HY[k],ak=(step>=1?a[k]:0),hc=4;
    E(svg,"rect",{x:HX-12,y:oy-3,width:24,height:34,rx:4,"class":"hbox",stroke:(ak>0.5?"var(--color-accent)":"var(--color-border)"),"stroke-width":(1+3.4*ak).toFixed(1),opacity:(0.35+0.65*ak).toFixed(2)});
    for(var r=0;r<R;r++)for(var c=0;c<Cc;c++){var ink=P[k][r*Cc+c];
      E(svg,"rect",{x:HX-10+c*hc,y:oy-1+r*hc,width:hc,height:hc,fill:ink?"var(--color-accent)":"#e7ecee","class":"hcell",opacity:(0.3+0.7*ak).toFixed(2)});}
    E(svg,"text",{x:HX,y:oy+40,"text-anchor":"middle","class":"tag"},(step>=1?(ak*100).toFixed(0)+"%":"—"));}
  /* 重构 */
  E(svg,"text",{x:420,y:36,"text-anchor":"middle","class":"lbl"},"重构 v′");
  if(step>=2)grid(svg,st.v,380,52,16,true);
  else{grid(svg,null,380,52,16,false);E(svg,"text",{x:420,y:114,"text-anchor":"middle","class":"ph"},"待重构");}
  E(svg,"text",{x:250,y:228,"text-anchor":"middle","class":"lbl"},"层内无连接 · 像素↔隐单元全连接 · 来回共用权重");
  var names=["输入 v（带噪）","编码 v→h","重构 h→v′","再采样一轮（吉布斯）"];
  document.getElementById("stat").textContent=names[step];
  caption();
}
function caption(){
  var el=document.getElementById("caption"),name=PN[curIdx];
  if(step===0){el.innerHTML="一张带噪的数字“<b>"+name+"</b>”（随机翻了几个像素）。点“下一步”，先把它编码成隐单元。";return;}
  var a=encode(v0),best=0;for(var k=1;k<K;k++)if(a[k]>a[best])best=k;
  if(step===1){el.innerHTML="<b>编码 v→h：</b>每个隐单元拿自己的特征模板和输入比对——最像“<b>"+PN[best]+"</b>”的那个被强烈激活（"+(a[best]*100).toFixed(0)+"%），其余明显更弱。35 个像素压成了 3 个数。";return;}
  if(step===2){el.innerHTML="<b>重构 h→v′：</b>只凭激活的隐单元把图像画回来。它只会画自己学过的特征，画不出噪点——于是输入被<b>去噪</b>，干净的“"+PN[best]+"”回来了。";return;}
  el.innerHTML="<b>再采样一轮：</b>把重构 v′ 再编码、再重构，图像几乎不变——已落入能量低谷、采样稳定。RBM 训练（对比散度）正是这样来回采样的；多个 RBM 叠起来就是<b>深度信念网络</b>。";
}
function go(){if(step>=MAXS)return false;step++;render();return true;}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="自动";}
document.getElementById("step").addEventListener("click",function(){stop();if(step>=MAXS){step=0;}go();});
document.getElementById("auto").addEventListener("click",function(){if(playing){stop();return;}
  if(step>=MAXS){step=0;render();}playing=true;document.getElementById("auto").textContent="⏸ 暂停";
  timer=setInterval(function(){if(!go())stop();},1050);});
document.getElementById("digit").addEventListener("click",function(){stop();curIdx=(curIdx+1)%PN.length;corrupt();step=0;render();});
document.getElementById("noise").addEventListener("click",function(){stop();seed++;corrupt();step=0;render();});
corrupt();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){step=MAXS;render();return;}
  document.getElementById("auto").click();},1000);
})();
</script>
{% endraw %}

## 延伸阅读

<div class="resource-grid">
  <a class="resource-card" href="https://en.wikipedia.org/wiki/Restricted_Boltzmann_machine" target="_blank" rel="noopener">
    <h3>受限玻尔兹曼机（维基百科）↗</h3>
    <p>能量函数、条件分布 P(h|v) 与 P(v|h)、对比散度训练的标准定义。</p>
  </a>
  <a class="resource-card" href="https://www.cs.toronto.edu/~hinton/absps/guideTR.pdf" target="_blank" rel="noopener">
    <h3>Hinton · 训练 RBM 实用指南 ↗</h3>
    <p>Geoffrey Hinton 讲 RBM 的吉布斯采样、对比散度与堆叠成 DBN（英文 PDF）。</p>
  </a>
</div>
