(* ::Package:: *)

(* 来源：全书图形/zeta模曲面-1.nb 中第 177075 行起的输入单元；对应书中 全书图形/8-Z模曲面-1.pdf *)

ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

reMin=-0.0;reMax=6;
imMin=-32;imMax=32;

modPlot=Plot3D[Abs[Zeta[x+I y]],{x,reMin,reMax},{y,imMin,imMax},PlotStyle->Directive[RGBColor[1.0,0.84,0.0],Opacity[0.80],Specularity[White,30]],Mesh->30,MeshStyle->Directive[GrayLevel[0.25],Opacity[0.35]],PlotPoints->100,MaxRecursion->4,PlotRange->{{-1.5,reMax+0.5},{imMin-0.5,imMax+2.5},{0,4.2}},ClippingStyle->None,Exclusions->{{x==1,y==0}},Boxed->False,Axes->True,AxesOrigin->{0,0,0},AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},AxesLabel->{Style["Re(s)",13,Bold,Black],Style["Im(s)",13,Bold,Black],Style["|\[Zeta](s)|",13,Bold,Black]},Ticks->{{-6,-4,-2,{0,"0"},1,3,5},{-30,-20,-10,{0,""},10,20,30},{1,2,3,4}},TicksStyle->Directive[Black,FontSize->10],AxesStyle->{Directive[Black,AbsoluteThickness[0.2]],Directive[Black,AbsoluteThickness[0.2]],Directive[Black,AbsoluteThickness[0.2]]}];

zeros={14.1347,21.0220,25.0109,30.4249};
zeroMarkers=Graphics3D[{Red,PointSize[0.008],Point[{1/2,#,0}]&/@zeros,Point[{1/2,-#,0}]&/@zeros}];

trivialZeros=-2 Range[1,10];
trivialMarkers=Graphics3D[{Red,PointSize[0.008],Point[{#,0,0}]&/@trivialZeros}];
trivialLabels=Graphics3D[Sequence@@(Text[Style["s="<>ToString[#],10,Bold,Red],{#,2.5,0.12}]&/@{-2,-4,-6})];

criticalLine=Graphics3D[{Directive[Blue,AbsoluteThickness[1.5],Opacity[0.9]],Line[{{1/2,imMin,0.0},{1/2,imMax,0.0}}]}];

refPlane=Graphics3D[{Opacity[0.25],GrayLevel[0.55],Polygon[{{reMin,imMin,0},{reMax,imMin,0},{reMax,imMax,0},{reMin,imMax,0}}]}];

realAxis=Graphics3D[{Directive[Black,Thickness[0.0001]],Line[{{reMin,0,0},{reMax,0,0}}]}];

criticalStrip=Graphics3D[{Opacity[0.30],RGBColor[0.0,0.75,0.2],Polygon[{{0,imMin,0},{1,imMin,0},{1,imMax,0},{0,imMax,0}}]}];


AriveLine=Graphics3D[{Directive[Red,AbsoluteThickness[0.5]],Line[{{0,imMin,0.0},{0,imMax,0.0}}]}];
(* ---- 统一画法（2026-10-06）：临界线、临界带、零点改用 书图样式.wl 中的函数；文字说明移入图例 ---- *)
pr94={{-1.5,reMax+0.5},{imMin-0.5,imMax+2.5},{0,4.2}};box94=bookBoxB[{-1.5,6.5}];
criticalStrip=Graphics3D[stripMark3D[{imMin,imMax}]];
criticalLine=Graphics3D[critLine3D[{imMin,imMax}]];
zeroMarkers=Graphics3D[zeroBalls[Join[{1/2,#,0}&/@zeros,{1/2,-#,0}&/@zeros],pr94,box94]];
trivialMarkers=Graphics3D[{}];trivialLabels=Graphics3D[{}];   (* 平凡零点在本图显示范围（Re ≥ -1.5）之外 *)

plot = Show[modPlot,refPlane,criticalStrip,realAxis,zeroMarkers,trivialMarkers,trivialLabels,criticalLine,AriveLine,BoxRatios->bookBoxB[{-1.5,6.5}],ViewPoint->viewB,ImageSize->imgW,shrink3D];
fig = Labeled[plot, bookLegend[{{bkLine[Red,1.0],"延拓推进线 Re(s) = 0"},"crit","strip","zero"}], Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图09.4-Z模曲面", fig];

(* ---- 调视点：本组（图 5.1、9.1–9.4、9.7）共用 书图样式.wl 中的 viewB ---- *)
vp = viewB;
Show[plot, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
