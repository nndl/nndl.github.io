# 二维卷积示例 

## 卷积
|                 步长 s = 1                 |                 步长 s = 2                 |
| :--------------------------------------: | :--------------------------------------: |
| <img width="250px" src="cnn-in_5_out_3_p_0_s_0.gif"> | <img width="250px" src="cnn-in_5_out_4_p_2_s_2.gif"> |
|           m = 3, p = 0 ,s = 1            |           m = 3, p = 2 ,s = 2            |
| <img width="250px" src="cnn-in_3_out_5.gif"> | <img width="250px" src="cnn-in_9_out_5.gif"> |
|           m = 3, p = 2 ,s = 1            |            m=5, p = 2 ,s = 2             |

 m表示卷积核大小，p 表示零填充大小（zero-padding）， s 表示步长（stride）。

## 转置卷积

|           m = 3, p = 0 ,s = 1            |           m = 3,  p = 0 ,s = 2           |
| :--------------------------------------: | :--------------------------------------: |
| <img width="250px" src="cnn-no_padding_no_strides.gif"> | <img width="250px" src="cnn-no_padding_strides.gif"> |
|                    卷积                    |                    卷积                    |
| <img width="250px" src="cnn-no_padding_no_strides_transposed.gif"> | <img width="250px" src="cnn-no_padding_strides_transposed.gif"> |
|                   转置卷积                   |                   转置卷积                   |


 m表示卷积核大小， p 表示零填充大小（zero-padding）， s 表示步长（stride）。

## 空洞卷积

|           m = 3, p = 0, s = 1            |           m = 3, p = 0, s = 1            |
| :--------------------------------------: | :--------------------------------------: |
| <img width="250px" src="cnn-dilation-in_7_out_3.gif"> | <img width="250px" src="cnn-dilation.gif"> |
|                   d=1                    |                   d=2                    |
  m表示卷积核大小，p 表示零填充大小（zero-padding）， s 表示步长（stride），d表示膨胀率（dilation）。

图片修改自： Vincent Dumoulin, Francesco Visin - [A guide to convolution arithmetic
for deep learning](https://arxiv.org/abs/1603.07285)