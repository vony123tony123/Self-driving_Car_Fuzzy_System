# Self-driving_Car_Fuzzy_System
計算型智慧 Computational Intelligence 作業一 模糊系統\
Practice using fuzzing System to finish self-driving Car\
車體大小設定為直徑 6 單位，初始角度+90 度\
車體中心設有感測器，可偵測正前方與左右各 45 度之距離。根據前左右三個感測器
的數值，輸入RBFN網路並輸出方向盤角度，並透過改變方向盤角度（注意：方向盤的
角度右轉為正 ）讓車輛能在不碰壁的狀況下到達終點，畫出過程並記錄各項數值。

## Pre-Requisites

Install project with requirments.txt

```bash
conda create --name CIHomework python=3.9
```
```
pip install -r requirements.txt
```

## User Guide
1. select the map file path
2. push start! buttom

## 原理說明
本次採用模糊規則為函數式模糊規則，具體歸屬函式圖形如下，本次使用的去模糊法為權重平均法，使用符合模糊規則之啟動強度去乘以模糊規則推論出的結果來去模糊化\
前左右Sensor之歸屬函數:\
![Figure_2](https://user-images.githubusercontent.com/43849007/230393082-8198cb02-69cf-4cef-9524-02bd618a1b03.png)\
left: right-left < 0\
right: right – left > 0\
straight: right-left = 0
\
輸入輸出之函數關係:\
![Figure_1](https://user-images.githubusercontent.com/43849007/230393145-4f73d10b-cc48-451a-9c1e-187dd901ea0e.png)\
phi = +40 (right – left >= 5)\
phi = 8 * (right-left) (5 > right – left > 0)\
phi = 0 (right-left = 0)\
phi = 8* (right - left) (0 > right-left > -5)\
phi = -40 (right-left >= -5)

## Demo
![圖片1](https://user-images.githubusercontent.com/43849007/230392113-39c47701-7035-4b8b-bd7f-edcd236280e2.png)
