# 二维卷积示例 

## 卷积

 p 表示零填充大小（zero-padding）， s 表示步长（stride），d表示膨胀率（dilation）。

## 转置卷积

|               p = 0 ,s = 1               |               p = 0 ,s = 2               |
| :--------------------------------------: | :--------------------------------------: |
| <img width="150px" src="cnn-no_padding_no_strides.gif"> | <img width="150px" src="cnn-no_padding_strides.gif"> |
|                    卷积                    |                    卷积                    |
| <img width="150px" src="cnn-no_padding_no_strides_transposed.gif"> | <img width="150px" src="cnn-no_padding_strides_transposed.gif"> |
|                   转置卷积                   |                   转置卷积                   |


 p 表示零填充大小（zero-padding）， s 表示步长（stride）。

## 空洞卷积

|                                          |                   |
| :--------------------------------------: | :---------------: |
| <img width="150px" src="cnn-dilation.gif"> |                   |
|            p = 0, s = 1, d=2             | p = 0, s = 1, d=2 |
 p 表示零填充大小（zero-padding）， s 表示步长（stride），d表示膨胀率（dilation）。

图片修改自： Vincent Dumoulin, Francesco Visin - [A guide to convolution arithmetic
for deep learning](https://arxiv.org/abs/1603.07285)