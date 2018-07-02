# 二维卷积示例 

## 卷积

 p 表示零填充大小（zero-padding）， s 表示步长（stride），d表示膨胀率（dilation）。

## 转置卷积

<table style="width:100%; table-layout:fixed;">
<tr>
<td><img width="150px" src="cnn-no_padding_no_strides.gif"></td>
<td><img width="150px" src="cnn-no_padding_strides.gif"></td>
</tr>
<tr>
<td>p = 0 ,s = 1 </td>
<td>p = 0 ,s = 2 </td>
</tr>
<tr>
<td><img width="150px" src="cnn-no_padding_no_strides_transposed.gif"></td>
<td><img width="150px" src="cnn-no_padding_strides_transposed.gif"></td>
</tr>
<tr>
<td>p = 0 ,s = 1 ,转置</td>
<td>p = 0 ,s = 2 ,转置</td>
</tr>
</table>
 p 表示零填充大小（zero-padding）， s 表示步长（stride），d表示膨胀率（dilation）。
## 空洞卷积


<table style="width:25%"; table-layout:fixed;>
<tr>
<td><img width="150px" src="cnn-dilation.gif"></td>
</tr>
<tr><td>p  = 0, s = 1, d=2</td></tr>
</table>
 p 表示零填充大小（zero-padding）， s 表示步长（stride），d表示膨胀率（dilation）。

图片修改自： Vincent Dumoulin, Francesco Visin - [A guide to convolution arithmetic
for deep learning](https://arxiv.org/abs/1603.07285)