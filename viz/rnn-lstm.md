---
layout: default
title: 循环神经网络与门控机制
description: "交互实验台：切换三种结构、编辑输入序列、单步观察门的开合与记忆沿时间的演化。"
permalink: /viz/rnn-lstm/
redirect_from:
  - /v/rnn-lstm/
---

{% raw %}
<style>
/* ======================= 记忆力小实验 ======================= */
.memlab{
  --good:#206a4f;      /* 记得住 = 绿 */
  --bad:#b5524a;       /* 忘掉了 = 红 */
  --ink:var(--color-text);
  margin:26px 0 8px;font-family:var(--font-sans);color:var(--color-text);
}
.memlab *{box-sizing:border-box;}
.memlab__lead{color:var(--color-text-soft);max-width:60ch;margin:0 0 22px;}

/* 第一步：设定要记的数字 */
.memlab__setup{display:flex;flex-wrap:wrap;align-items:center;gap:14px 22px;
  background:var(--color-bg-pure);border:1px solid var(--color-border);
  border-radius:var(--radius-lg);box-shadow:var(--shadow-sm);padding:18px 22px;margin-bottom:18px;}
.memlab__field{display:flex;align-items:center;gap:12px;}
.memlab__field label{font-size:.94rem;color:var(--color-text-soft);}
.memlab__num{font:700 1.5rem var(--font-mono);color:var(--color-accent);min-width:2.6ch;text-align:center;}
.memlab input[type=range]{accent-color:var(--color-accent);cursor:pointer;width:160px;height:22px;}
.memlab__btns{display:flex;gap:10px;margin-left:auto;}
.membtn{appearance:none;font:inherit;font-size:.95rem;cursor:pointer;padding:9px 20px;border-radius:var(--radius-md);
  border:1px solid var(--color-border-strong);background:var(--color-bg-pure);color:var(--color-text-soft);
  transition:all .18s var(--ease-out);}
.membtn:hover{border-color:var(--color-accent);color:var(--color-accent);}
.membtn--go{background:var(--color-accent);border-color:var(--color-accent);color:#fff;}
.membtn--go:hover{background:var(--color-accent-hover);border-color:var(--color-accent-hover);color:#fff;}

/* 干扰输入条 */
.memlab__feed{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:4px 2px 16px;
  font-size:.9rem;color:var(--color-text-muted);}
.memlab__feed .lbl{margin-right:2px;}
.feedchip{display:inline-flex;align-items:center;justify-content:center;min-width:38px;height:32px;padding:0 8px;
  border-radius:8px;background:var(--color-bg-section);border:1px solid var(--color-border);
  font:600 .9rem var(--font-mono);color:var(--color-text-soft);opacity:.25;transition:opacity .25s,transform .25s var(--ease-out);}
.feedchip.on{opacity:1;}
.feedchip.first{background:var(--color-accent-soft);border-color:var(--color-accent);color:var(--color-accent);}
.feedchip.now{transform:translateY(-3px);box-shadow:var(--shadow-sm);}

/* 两条赛道 */
.memlab__lanes{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.lane{border:1px solid var(--color-border);border-radius:var(--radius-lg);background:var(--color-bg-pure);
  box-shadow:var(--shadow-sm);padding:16px 18px;border-top:4px solid var(--ac,var(--color-border-strong));}
.lane--rnn{--ac:var(--bad);}
.lane--lstm{--ac:var(--good);}
.lane h4{margin:0 0 2px;font-family:var(--font-serif);font-size:1.08rem;color:var(--color-text);}
.lane__sub{font-size:.82rem;color:var(--color-text-muted);margin-bottom:10px;min-height:1.2em;}
.lane__chart{width:100%;height:auto;display:block;}
.lane__chart .axisline{stroke:var(--color-border);stroke-width:1;}
.lane__chart .refline{stroke:var(--color-accent);stroke-width:1.5;stroke-dasharray:5 4;opacity:.65;}
.lane__chart .reftx{font:600 11px var(--font-mono);fill:var(--color-accent);}
.lane__chart .trace{fill:none;stroke-width:2.5;stroke-linejoin:round;stroke-linecap:round;}
.lane__chart .dot{stroke:#fff;stroke-width:1.5;}
.lane__verdict{display:flex;align-items:baseline;gap:8px;margin-top:10px;font-size:.9rem;color:var(--color-text-soft);}
.lane__verdict b{font:700 1.35rem var(--font-mono);}
.lane__tag{margin-left:auto;font-size:.82rem;font-weight:600;padding:3px 10px;border-radius:999px;}
.lane__tag.is-good{background:rgba(32,106,79,.12);color:var(--good);}
.lane__tag.is-bad{background:rgba(181,82,74,.12);color:var(--bad);}

/* LSTM 的闸门旋钮 */
.knob{display:flex;align-items:center;gap:10px;background:var(--color-bg-section);border:1px solid var(--color-border);
  border-radius:var(--radius-md);padding:8px 12px;margin-bottom:12px;font-size:.84rem;color:var(--color-text-soft);}
.knob label{white-space:nowrap;}
.knob input{flex:1;accent-color:var(--good);}
.knob .ends{font-size:.74rem;color:var(--color-text-muted);}

/* 实时旁白 */
.memlab__caption{margin:16px 0 4px;padding:14px 18px;border-radius:var(--radius-md);
  background:linear-gradient(120deg,var(--color-accent-soft),rgba(183,121,31,.08));
  border:1px solid rgba(21,94,117,.16);font-size:.95rem;line-height:1.65;color:var(--color-text-soft);}
.memlab__caption b{color:var(--color-accent);}

/* 为什么 */
.memlab__why{margin:26px 0 6px;}
.memlab__why h3{font-family:var(--font-serif);font-size:1.15rem;margin:0 0 12px;}
.whygrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;}
.whycard{border:1px solid var(--color-border);border-radius:var(--radius-md);background:var(--color-bg-pure);
  padding:15px 16px;border-left:4px solid var(--wc,var(--color-accent));}
.whycard b{display:block;margin-bottom:5px;color:var(--color-text);}
.whycard p{margin:0;font-size:.9rem;color:var(--color-text-muted);line-height:1.6;}

details.deep{margin:22px 0 8px;border:1px solid var(--color-border);border-radius:var(--radius-md);
  background:var(--color-bg-pure);padding:0 18px;}
details.deep summary{cursor:pointer;padding:14px 0;font-weight:600;color:var(--color-text-soft);}
details.deep[open] summary{border-bottom:1px solid var(--color-border);margin-bottom:14px;}
details.deep .eq{font:.9rem/1.9 var(--font-mono);color:var(--color-text-soft);}
details.deep .eq sub{font-size:.74em;}

@media (max-width:620px){
  .memlab__lanes{grid-template-columns:1fr;}
  .memlab__btns{margin-left:0;width:100%;}
  .membtn{flex:1;}
}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 循环神经网络与门控机制

循环神经网络是用来处理“一连串”数据（一句话、一段语音、一串股价）的。它每次只看一个，靠一份不断更新的“记忆”把前后串起来。难点在于：**很久以前看到的东西，常常没传到后面就被忘光了。** 下面用一个小实验直观感受这件事——以及 LSTM 是怎么把记忆守住的。

<section class="memlab" id="memlab">
  <p class="memlab__lead">游戏规则：先给两个网络看同一个数字，让它们记住；接着不停塞新数字进去干扰。走到最后，谁还记得最初那个数字？</p>

  <div class="memlab__setup">
    <div class="memlab__field">
      <label for="sig">① 要记住的数字</label>
      <input type="range" id="sig" min="5" max="95" step="1" value="70">
      <span class="memlab__num" id="sigVal">70</span>
    </div>
    <div class="memlab__btns">
      <button class="membtn membtn--go" id="go" type="button">▶ 开始</button>
      <button class="membtn" id="reset" type="button">重置</button>
    </div>
  </div>

  <div class="memlab__feed" id="feed"><span class="lbl">② 依次喂入：</span></div>

  <div class="memlab__lanes">
    <div class="lane lane--rnn">
      <h4>普通循环网络</h4>
      <div class="lane__sub">只有一份随手涂改的便签</div>
      <svg class="lane__chart" id="chartRnn" viewBox="0 0 320 130" role="img" aria-label="普通 RNN 的记忆变化"></svg>
      <div class="lane__verdict">最后记成 <b id="rnnVal">—</b><span id="rnnTag" class="lane__tag"></span></div>
    </div>
    <div class="lane lane--lstm">
      <h4>LSTM</h4>
      <div class="lane__sub">多了一条记忆传送带和闸门</div>
      <div class="knob">
        <label for="forget">记忆闸门</label>
        <span class="ends">容易忘</span>
        <input type="range" id="forget" min="40" max="100" step="1" value="97">
        <span class="ends">记得牢</span>
      </div>
      <svg class="lane__chart" id="chartLstm" viewBox="0 0 320 130" role="img" aria-label="LSTM 的记忆变化"></svg>
      <div class="lane__verdict">最后记成 <b id="lstmVal">—</b><span id="lstmTag" class="lane__tag"></span></div>
    </div>
  </div>

  <div class="memlab__caption" id="caption"></div>

  <div class="memlab__why">
    <h3>为什么会差这么多？</h3>
    <div class="whygrid">
      <div class="whycard" style="--wc:var(--bad)">
        <b>普通 RNN：随手涂改的便签</b>
        <p>每读到一个新数字，就把整张便签重写一遍。新内容不断覆盖旧内容，所以很久以前的事很快被抹掉。</p>
      </div>
      <div class="whycard" style="--wc:var(--good)">
        <b>LSTM：传送带 + 闸门</b>
        <p>另设一条专门的记忆传送带。几扇“闸门”决定何时保留旧记忆、何时才写入新内容——重要信息于是能一路保留。试着把上面的“记忆闸门”往“容易忘”方向拉，看 LSTM 怎样退化成普通 RNN。</p>
      </div>
      <div class="whycard" style="--wc:var(--color-accent-light)">
        <b>GRU：精简版 LSTM</b>
        <p>用更少的闸门做到差不多的事，参数更少、跑得更快，是实际中常用的轻量替代。</p>
      </div>
    </div>
  </div>

  <details class="deep">
    <summary>给好奇的读者：闸门背后的公式</summary>
    <p style="font-size:.9rem;color:var(--color-text-muted);margin-top:0;">LSTM 在每个时刻用三扇门（σ 输出 0~1 的开度）调控一条细胞状态 c：</p>
    <p class="eq">
      遗忘门 f<sub>t</sub> = σ(W<sub>f</sub> x<sub>t</sub> + U<sub>f</sub> h<sub>t-1</sub> + b<sub>f</sub>) &nbsp;— 旧记忆保留多少<br>
      输入门 i<sub>t</sub> = σ(W<sub>i</sub> x<sub>t</sub> + U<sub>i</sub> h<sub>t-1</sub> + b<sub>i</sub>) &nbsp;— 新内容写入多少<br>
      输出门 o<sub>t</sub> = σ(W<sub>o</sub> x<sub>t</sub> + U<sub>o</sub> h<sub>t-1</sub> + b<sub>o</sub>) &nbsp;— 当前用出多少<br>
      细胞状态 c<sub>t</sub> = f<sub>t</sub> ⊙ c<sub>t-1</sub> + i<sub>t</sub> ⊙ c̃<sub>t</sub><br>
      隐藏状态 h<sub>t</sub> = o<sub>t</sub> ⊙ tanh(c<sub>t</sub>)
    </p>
    <p style="font-size:.9rem;color:var(--color-text-muted);">上面实验里的“记忆闸门”就对应遗忘门 f：拉到“记得牢”即 f≈1（旧记忆几乎全留），拉到“容易忘”即 f 变小（旧记忆迅速流失）。</p>
  </details>
</section>

{% raw %}
<script>
(function(){
"use strict";
var T=8;                          /* 共 8 步 */
var sig=70, forget=0.97;          /* 要记的数字 / LSTM 闸门(0.4~1) */
var t=1;                          /* 已揭示到第几步（1~8） */
var playing=false, timer=null, runSeed=0;
var feed=[];                      /* feed[0]=原始数字, feed[1..7]=干扰数字 */
var rnn=[], lstm=[];              /* 两条记忆轨迹 */

/* 几套预设的干扰数字：确定性，保证普通 RNN 必然被冲偏、对照鲜明（重置时轮换） */
var PATTERNS=[
  [20,80,35,72,25,62,46],
  [84,30,76,40,88,34,52],
  [44,74,22,66,28,82,50],
  [60,26,70,44,80,30,48]
];
function clamp(v,a,b){return v<a?a:(v>b?b:v);}

function makeFeed(){
  feed=[sig].concat(PATTERNS[runSeed%PATTERNS.length]);
}
function compute(){
  rnn=[sig]; lstm=[sig];
  for(var i=1;i<T;i++){
    var x=feed[i];
    rnn.push(clamp(0.55*rnn[i-1]+0.45*x,0,100));           /* 旧记忆每步对半冲淡 */
    lstm.push(clamp(forget*lstm[i-1]+(1-forget)*x,0,100));  /* 闸门 f 留旧记忆，(1−f) 写入新内容：f→1 记得牢，f→小 退化成随输入覆盖 */
  }
}

/* ---- 颜色：离原始值越近越绿，越远越红 ---- */
function near(v){
  var d=Math.min(1,Math.abs(v-sig)/45), g=[32,106,79], b=[181,82,74];
  function h(n){n=Math.round(n);return(n<16?"0":"")+n.toString(16);}
  return "#"+h(g[0]+(b[0]-g[0])*d)+h(g[1]+(b[1]-g[1])*d)+h(g[2]+(b[2]-g[2])*d);
}

/* ---- 画一条赛道的折线图 ---- */
var SVGNS="http://www.w3.org/2000/svg";
function E(p,tag,a){var e=document.createElementNS(SVGNS,tag);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
var PAD_L=14, PAD_R=14, PAD_T=14, PAD_B=16, W=320, Hh=130;
function px(i){return PAD_L+i/(T-1)*(W-PAD_L-PAD_R);}
function py(v){return (Hh-PAD_B)-v/100*(Hh-PAD_T-PAD_B);}
function drawLane(svgId,trace){
  var svg=document.getElementById(svgId); while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:PAD_L,y1:Hh-PAD_B,x2:W-PAD_R,y2:Hh-PAD_B,"class":"axisline"});
  /* 原始值参考线 */
  var yr=py(sig);
  E(svg,"line",{x1:PAD_L,y1:yr,x2:W-PAD_R,y2:yr,"class":"refline"});
  var tx=E(svg,"text",{x:W-PAD_R,y:yr-5,"text-anchor":"end","class":"reftx"});tx.textContent="原始 "+sig;
  /* 轨迹折线（揭示到第 t 步） */
  var n=Math.min(t,T), pts=[];
  for(var i=0;i<n;i++)pts.push(px(i)+","+py(trace[i]));
  if(pts.length>1){
    var col=near(trace[n-1]);
    E(svg,"polyline",{points:pts.join(" "),"class":"trace",stroke:col});
  }
  for(var j=0;j<n;j++)E(svg,"circle",{cx:px(j),cy:py(trace[j]),r:(j===n-1?5:3.2),"class":"dot",fill:near(trace[j])});
}

/* ---- 干扰数字条 ---- */
function buildFeed(){
  var host=document.getElementById("feed");
  host.querySelectorAll(".feedchip").forEach(function(c){c.remove();});
  for(var i=0;i<T;i++){
    var c=document.createElement("span");
    c.className="feedchip"+(i===0?" first":"");
    c.dataset.i=i; c.textContent=feed[i];
    host.appendChild(c);
  }
}
function renderFeed(){
  var chips=document.querySelectorAll("#feed .feedchip");
  chips.forEach(function(c,i){
    c.textContent=feed[i];
    c.classList.toggle("on",i<t);
    c.classList.toggle("now",i===t-1 && t>1);
  });
}

/* ---- 结论标签 ---- */
function verdict(id,tagId,val){
  document.getElementById(id).textContent=Math.round(val);
  var tag=document.getElementById(tagId), d=Math.abs(val-sig);
  if(t<T){tag.textContent="";tag.className="lane__tag";return;}
  if(d<=12){tag.textContent="✓ 记住了";tag.className="lane__tag is-good";}
  else{tag.textContent="✗ 记岔了";tag.className="lane__tag is-bad";}
}

function caption(){
  var el=document.getElementById("caption");
  if(t<=1){
    el.innerHTML="两个网络都先记下了 <b>"+sig+"</b>。点 <b>开始</b>，看它们一边读新数字、一边还记不记得这个 "+sig+"。";
    return;
  }
  if(t<T){
    el.innerHTML="第 "+t+" 步：刚塞进一个新数字 <b>"+feed[t-1]+"</b>。普通 RNN 的便签正被一遍遍覆盖，LSTM 则把闸门关着护住旧记忆……";
    return;
  }
  var rv=Math.round(rnn[T-1]), lv=Math.round(lstm[T-1]);
  el.innerHTML="结束！最初要记的是 <b>"+sig+"</b>。普通 RNN 现在记成了 <b>"+rv+"</b>（被冲掉了），LSTM 还记成 <b>"+lv+"</b>（基本守住）。这就是 LSTM 的“闸门”在长距离记忆上的作用。";
}

function render(){
  document.getElementById("sigVal").textContent=sig;
  drawLane("chartRnn",rnn); drawLane("chartLstm",lstm);
  renderFeed();
  verdict("rnnVal","rnnTag",rnn[Math.min(t,T)-1]);
  verdict("lstmVal","lstmTag",lstm[Math.min(t,T)-1]);
  caption();
}

function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 开始";}
function play(){
  if(t>=T){t=1;render();}
  playing=true;document.getElementById("go").textContent="⏸ 暂停";
  timer=setInterval(function(){
    if(t>=T){stop();return;}
    t++;render();
    if(t>=T)stop();
  },720);
}
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("reset").addEventListener("click",function(){stop();runSeed++;makeFeed();compute();buildFeed();t=1;render();});
document.getElementById("sig").addEventListener("input",function(e){stop();sig=+e.target.value;feed[0]=sig;compute();t=1;render();});
document.getElementById("forget").addEventListener("input",function(e){forget=(+e.target.value)/100;compute();render();});

/* 启动 */
makeFeed();compute();buildFeed();render();

/* 首次加载后自动演示一遍，让读者一眼看懂；尊重“减少动效”偏好 */
var autoDone=false;
function autoDemo(){
  if(autoDone)return; autoDone=true;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  if(reduce){t=T;render();}else{play();}
}
setTimeout(autoDemo,900);
})();
</script>
{% endraw %}

## 延伸阅读

<div class="resource-grid">
  <a class="resource-card" href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/" target="_blank" rel="noopener">
    <h3>Understanding LSTM Networks ↗</h3>
    <p>Chris Olah 的经典图解，一步步拆开 LSTM 与 GRU 的每一扇门，配图清晰。</p>
  </a>
  <a class="resource-card" href="https://karpathy.github.io/2015/05/21/rnn-effectiveness/" target="_blank" rel="noopener">
    <h3>The Unreasonable Effectiveness of RNNs ↗</h3>
    <p>Andrej Karpathy 用循环网络逐字生成文本，直观展示它的序列建模能力。</p>
  </a>
  <a class="resource-card" href="https://zh.d2l.ai/chapter_recurrent-modern/index.html" target="_blank" rel="noopener">
    <h3>《动手学深度学习》· 现代循环神经网络 ↗</h3>
    <p>中文教材，含 GRU / LSTM 的公式推导与可运行代码，想深入可看。</p>
  </a>
</div>
