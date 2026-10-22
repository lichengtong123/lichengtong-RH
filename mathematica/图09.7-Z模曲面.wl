(* ::Package:: *)

(* 来源：全书图形/zeta模曲面-1.nb 中第 286043 行起的输入单元；对应书中 全书图形/8-Z模曲面-4.pdf *)

ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

reMin=-6;reMax=6;
(* 本图单独定视点：从 viewB（左前上方）看，Im 较大处的「峭壁」会挡住实轴上的平凡零点 −2, −4, −6；
   沿用原图的低角度左侧视点，平凡零点在前缘清楚可见。比例尺仍与本组（bookBoxB）一致。 *)
(* 原 {-6.2,-2.5,0.8} 从 -Im 一侧低角度看，|t| 较大处被截断的「峭壁」挡住了 t = 0 附近的谷底；
   改为几乎沿实轴方向、从左上方看进谷底。 *)
view97={-6.51266,-0.57456,1.60782};   (* 作者在 Mathematica 中旋转选定（2026-10-05） *)
imMin=-32;imMax=32;
(* PlotRange：前缘 Re 轴画在 Im = imMin-0.5，刻度与数字在 Im = imMin-0.5 … imMin-3.1，「Re(s)」在 Im = imMin-5、Re = reMax+0.9。
   原 PlotRange 的 Im 下界为 imMin-0.5、Re 上界为 reMax+0.5，这些都落在范围外被裁掉，Re 轴因而不显示（2026-10-06 修正）。
   现把 Im 下界放宽到 imMin-6、Re 上界放宽到 reMax+1.5，并按本组比例尺（Re 每单位盒长 0.15，Im 每 67 个单位盒长 2）相应加长盒子。 *)
pr97={{reMin-0.5,reMax+1.5},{imMin-6,imMax+2.5},{0,4.2}};
box97={0.15 (pr97[[1,2]]-pr97[[1,1]]), 2 (pr97[[2,2]]-pr97[[2,1]])/67, 1.1};

modPlot=Plot3D[Abs[Zeta[x+I y]],{x,reMin,reMax},{y,imMin,imMax},PlotStyle->Directive[RGBColor[1.0,0.84,0.0],Opacity[0.80],Specularity[White,30]],Mesh->30,MeshStyle->Directive[GrayLevel[0.25],Opacity[0.35]],PlotPoints->100,MaxRecursion->4,PlotRange->{{reMin-0.5,reMax+0.5},{imMin-0.5,imMax+2.5},{0,4.2}},ClippingStyle->None,Exclusions->{{x==1,y==0}},Boxed->False,Axes->{False,True,True},AxesOrigin->{0,0,0},AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},AxesLabel->{Style["Re(s)",13,Bold,Black],Style["Im(s)",13,Bold,Black],Style["|\[Zeta](s)|",13,Bold,Black]},Ticks->{{-6,-4,-2,{0,"0"},1,3,5},{-30,-20,-10,{0,""},10,20,30},{1,2,3,4}},TicksStyle->Directive[Black,FontSize->10],AxesStyle->{Directive[Black,AbsoluteThickness[0.2]],Directive[Black,AbsoluteThickness[0.2]],Directive[Black,AbsoluteThickness[0.2]]}];

(*非平凡零点*)
zeros={14.1347,21.0220,25.0109,30.4249};
zeroMarkers=Graphics3D[{Red,PointSize[0.008],Point[{1/2,#,0}]&/@zeros,Point[{1/2,-#,0}]&/@zeros}];

(*平凡零点（负偶数）*)
trivialZeros=-2 Range[1,10];
(* 平凡零点处 |ζ| 贴近 z = 0，点标记会被曲面和参考平面盖住：
   改为略高于 z = 0 的红色小球，并在上方标注 *)
trivialShow={-2,-4,-6};
trivialMarkers=Graphics3D[{Red,Specularity[White,40],Ellipsoid[{#,0,0.04},ballRad[pr97,box97,0.010]]&/@trivialShow}];
trivialLabels=Graphics3D[Text[Style["s = "<>ToString[#],fsAnn,Red],{#,0,0.45}]&/@trivialShow];

(*临界线 Re(s)=1/2*)
criticalLine=Graphics3D[{Directive[Blue,AbsoluteThickness[1.5],Opacity[0.9]],Line[{{1/2,imMin,0.0},{1/2,imMax,0.0}}]}];

(*参考平面 z=0*)
refPlane=Graphics3D[{Opacity[0.25],GrayLevel[0.55],Polygon[{{reMin,imMin,0},{reMax,imMin,0},{reMax,imMax,0},{reMin,imMax,0}}]}];

(*实轴*)
realAxis=Graphics3D[{Directive[Black,Thickness[0.0001]],Line[{{reMin,0,0},{reMax,0,0}}]}];

(*临界带 0<Re(s)<1*)
criticalStrip=Graphics3D[{Opacity[0.30],RGBColor[0.0,0.75,0.2],Polygon[{{0,imMin,0},{1,imMin,0},{1,imMax,0},{0,imMax,0}}]}];


(* Re(s) 轴：视线几乎顺着实轴，若轴画在 Im = 0 上，刻度数字与「Re(s)」会和平凡零点叠在一起；
   改画在前缘 Im = imMin 处（与实轴平行），刻度与标签随之移开 *)
reAxisY=imMin-0.5;
reAxisFront=Graphics3D[{Black,AbsoluteThickness[0.4],Line[{{reMin-0.5,reAxisY,0},{reMax+0.5,reAxisY,0}}],
    Table[{Line[{{k,reAxisY,0},{k,reAxisY-0.8,0}}],Text[Style[ToString[k],10,Black],{k,reAxisY-2.6,0}]},{k,{-6,-4,-2,0,1,3,5}}],
    Text[Style["Re(s)",13,Bold,Black],{reMax+0.9,reAxisY-4.5,0}]}];

AriveLine=Graphics3D[{Directive[Red,AbsoluteThickness[0.5]],Line[{{-6,imMin,0.0},{-6,imMax,0.0}}]}];
(* ---- 统一画法（2026-10-06）：临界线、临界带、零点改用 书图样式.wl 中的函数；文字说明移入图例 ---- *)
criticalStrip=Graphics3D[stripMark3D[{imMin,imMax}]];
criticalLine=Graphics3D[critLine3D[{imMin,imMax}]];
zeroMarkers=Graphics3D[zeroBalls[Join[{1/2,#,0}&/@zeros,{1/2,-#,0}&/@zeros],pr97,box97]];
trivialMarkers=Graphics3D[trivialBalls[{#,0,0.04}&/@trivialShow,pr97,box97]];   (* 略高于 z = 0，避免被谷底曲面盖住 *)
trivialLabels=Graphics3D[{}];

plot = Show[modPlot,refPlane,criticalStrip,realAxis,zeroMarkers,trivialMarkers,trivialLabels,criticalLine,AriveLine,reAxisFront,PlotRange->pr97,BoxRatios->box97,ViewPoint->view97,ImageSize->imgW,shrink3D];
fig = Labeled[plot, bookLegend[{{bkLine[Red,1.0],"延拓推进线 Re(s) = −6"},"crit","strip","zero","triv"}], Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图09.7-Z模曲面", fig];

(* ---- 调视点：本图用自己的 view97（见文件开头），转好后抄到 view97 ---- *)
vp = view97;
Show[plot, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
