---
layout: default
title: KV 缓存与注意力 O(n²)
permalink: /viz/kv-cache/
redirect_from:
  - /v/kv-cache/
---

{% raw %}
<style>
.kvlab .grid{display:grid;gap:2px;justify-content:center;}
.kvlab .c{width:24px;height:24px;border-radius:3px;background:var(--color-bg-section);display:flex;align-items:center;justify-content:center;font:9px var(--font-mono);}
.kvlab .c.now{background:var(--color-accent);color:#fff;}
.kvlab .c.cached{background:#cfe3e0;color:#5a8;}
.kvlab .c.done{background:#dfeae8;}
.kvlab .toks{display:flex;gap:5px;justify-content:center;margin-bottom:10px;flex-wrap:wrap;}
.kvlab .tk{font-family:var(--font-serif);padding:4px 9px;border-radius:7px;background:var(--color-bg-pure);border:1px solid var(--color-border);font-size:.95rem;}
.kvlab .tk.new{border-color:var(--color-accent);background:var(--color-accent-soft);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# KV 缓存与注意力 O(n²)

大模型从左到右一个词一个词地生成，每生成一个新词，它都要回头“看”前面所有词——这就是注意力。麻烦在于：序列越长，要看的越多。如果每生成一步都把前面所有词重新算一遍“键(Key)和值(Value)”，那么生成 n 个词的总计算量是 1+2+…+n ≈ n²/2，随长度**平方级**增长，长上下文因此又慢又贵。KV 缓存的办法很简单：每个词的 K、V 只在它第一次出现时算一次、**存起来反复用**，后面就不重算了。于是总量降到约 n（线性）。点“生成下一个词”，对比开/关缓存的累计计算量。

<section class="kvlab vizui" id="kvlab">
  <p class="vizui__lead">下面的三角格子表示“在第几步、给第几个词算 K/V”。<span style="color:var(--color-accent);font-weight:600">蓝=这步新算的</span>，<span style="color:#5a8;font-weight:600">浅青=从缓存直接取的</span>。开缓存时只有对角线要算，关缓存时整片三角都要重算。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <label style="display:inline-flex;align-items:center;gap:8px;cursor:pointer"><input type="checkbox" id="cache" checked> 开启 KV 缓存</label>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="gen" type="button">▶ 生成下一个词</button>
      <button class="vizui-btn" id="auto" type="button">自动</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
    </div>
    <div class="toks" id="toks"></div>
    <div class="grid" id="grid"></div>
    <div style="text-align:center;margin-top:14px;font:600 1rem var(--font-mono)" id="counter"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>注意力 ~ O(n²)</b><p>每步都重算前面所有词，生成 n 个词总量约 n²/2，随长度平方增长——长上下文贵在这里。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>KV 缓存 ~ O(n)</b><p>每个词的 K/V 只算一次存起来，后续直接取，总量降到线性，生成快得多。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>代价是显存</b><p>缓存要占显存，序列越长占得越多——这也是长上下文的另一道坎。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var WORDS=["从","前","有","座","山","山","里","有","座","庙"];
var step=0, cache=true, playing=false, timer=null;
function buildToks(){var h=document.getElementById("toks");h.innerHTML="";for(var i=0;i<step;i++){var d=document.createElement("div");d.className="tk"+(i===step-1?" new":"");d.textContent=WORDS[i];h.appendChild(d);}}
function buildGrid(){
  var h=document.getElementById("grid");h.innerHTML="";h.style.gridTemplateColumns="repeat("+Math.max(1,step)+",24px)";
  for(var s=0;s<step;s++)for(var j=0;j<step;j++){
    var c=document.createElement("div");
    if(j>s){c.style.visibility="hidden";c.className="c";}
    else{var cls="c";
      if(s===step-1){ // 当前步
        if(!cache||j===s)cls+=" now"; else cls+=" cached";
      }else cls+=" done";
      c.className=cls;}
    h.appendChild(c);
  }
}
function counts(){var noC=step*(step+1)/2, withC=step;return {noC:noC,withC:withC};}
function render(){
  buildToks();buildGrid();
  var c=counts();
  document.getElementById("counter").innerHTML="生成 "+step+" 个词 · 累计算 K/V：<b style='color:#b5524a'>无缓存 "+c.noC+" 次</b> vs <b style='color:var(--color-accent)'>有缓存 "+c.withC+" 次</b>"+(step>1?" （省 "+(c.noC/c.withC).toFixed(1)+"×）":"");
  caption(c);
}
function caption(c){
  var el=document.getElementById("caption");
  if(step===0)el.innerHTML="点“生成下一个词”，一个个往外蹦。看右下角累计计算量怎么涨。";
  else el.innerHTML="已生成 "+step+" 个词。"+(cache?
    "<b>开缓存：</b>每步只给新词算一次 K/V（蓝对角线），旧词直接从缓存取（浅青）——累计才 "+c.withC+" 次。":
    "<b>关缓存：</b>每步把前面所有词的 K/V 全部重算（整片蓝三角），累计已 "+c.noC+" 次，随长度平方膨胀。")+(step>=8?"序列越长，两者差距越悬殊。":"");
}
function gen(){if(step<WORDS.length){step++;render();}}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="自动";}
document.getElementById("gen").addEventListener("click",function(){stop();gen();});
document.getElementById("auto").addEventListener("click",function(){if(playing){stop();return;}playing=true;document.getElementById("auto").textContent="暂停";timer=setInterval(function(){if(step>=WORDS.length){stop();return;}gen();},700);});
document.getElementById("reset").addEventListener("click",function(){stop();step=0;render();});
document.getElementById("cache").addEventListener("change",function(e){cache=e.target.checked;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){step=WORDS.length;render();return;}document.getElementById("auto").click();},1000);
})();
</script>
{% endraw %}
