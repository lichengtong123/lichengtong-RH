(* ::Package:: *)

(* 来源：全书图形/zeta模曲面-1.nb 中第 103134 行起的输入单元；对应书中 全书图形/8-Z模曲面-0.pdf *)

ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

reMin=1;reMax=6;(*曲面绘图域，可任意调整*)imMin=-32;imMax=32;
xPlotMin=0;(*坐标系/PlotRange 的 x 下界，固定为 0*)modPlot=Plot3D[Abs[Zeta[x+I y]],{x,reMin,reMax},{y,imMin,imMax},PlotStyle->Directive[RGBColor[1.0,0.84,0.0],Opacity[0.80],Specularity[White,30]],Mesh->30,MeshStyle->Directive[GrayLevel[0.25],Opacity[0.35]],PlotPoints->100,MaxRecursion->4,(*PlotRange x 下界固定为 0，与坐标原点对齐*)PlotRange->{{-1.5,reMax+0.5},{imMin-0.5,imMax+2.5},{0,4.2}},ClippingStyle->None,Exclusions->{{x==1,y==0}},Boxed->False,Axes->True,AxesOrigin->{0,0,0},(*三轴交于原点*)
AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},
AxesStyle->{Directive[Black,AbsoluteThickness[0.2]],Directive[Black,AbsoluteThickness[0.2]],Directive[Black,AbsoluteThickness[0.2]]},AxesLabel->{Style["Re(s)",13,Bold,Black],Style["Im(s)",13,Bold,Black],Style["|\[Zeta](s)|",13,Bold,Black]},Ticks->{{-6,-4,-2,{0,"0"},1,3,5},{-30,-20,-10,{0,""},10,20,30},{1,2,3,4}},TicksStyle->Directive[Black,FontSize->10],FaceGrids->None,Background->None];

(* =====非平凡零点=====*)
zeros={14.1347,21.0220,25.0109,30.4249};
zeroMarkers=Graphics3D[{Red,PointSize[0.008],Point[{1/2,#,0}]&/@zeros,Point[{1/2,-#,0}]&/@zeros}];

(* =====平凡零点=====*)
trivialZeros={-2,-4,-6};
trivialSpheres=Graphics3D[{Red,PointSize[0.008],Sequence@@(Point[{#,0,0}]&/@trivialZeros)}];
trivialLabels=Graphics3D[Sequence@@(Text[Style["s="<>ToString[#],10,Bold,Red],{#,2.5,0.12}]&/@trivialZeros)];

(* =====临界线、极点线=====*)
criticalLine=Graphics3D[{Directive[Blue,AbsoluteThickness[1.5],Opacity[0.9]],Line[{{1/2,imMin,0.0},{1/2,imMax,0.0}}]}];
poleLine=Graphics3D[{Directive[Red,AbsoluteThickness[0.5]],Line[{{1,imMin,0.0},{1,imMax,0.0}}]}];

(* =====参考平面・临界带：x 下界用 xPlotMin=0=====*)
refPlane=Graphics3D[{Opacity[0.25],GrayLevel[0.55],Polygon[{{xPlotMin,imMin,0},{reMax,imMin,0},{reMax,imMax,0},{xPlotMin,imMax,0}}]}];
criticalStrip=Graphics3D[{Opacity[0.30],RGBColor[0.0,0.75,0.2],Polygon[{{0,imMin,0},{1,imMin,0},{1,imMax,0},{0,imMax,0}}]}];
stripBoundary=Graphics3D[{Directive[RGBColor[0.0,0.55,0.1],AbsoluteThickness[1.5]],Line[{{0,imMin,0},{0,imMax,0}}]}];

(* =====组合输出=====*)
plot = Show[modPlot,refPlane,poleLine,(*Show 层也固定 PlotRange x 下界为 0*)PlotRange->{{-1.5,reMax+0.5},{imMin-0.5,imMax+2.5},{0,4.2}},BoxRatios->bookBoxB[{-1.5,6.5}],ViewPoint->viewB,ImageSize->imgW,shrink3D];
fig = Labeled[plot, bookLegend[{{bkSurf[RGBColor[1.0,0.84,0.0]],"曲面 |ζ(s)|"},{bkLine[Red,1.0],"延拓推进线 Re(s) = 1"}}], Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图09.1-Z模曲面", fig];

(* ---- 调视点：用鼠标旋转下图，下面一行实时显示当前视点坐标；
        本组（图 5.1、9.1–9.4、9.7）共用 书图样式.wl 中的 viewB，改那里即可全组同步 ---- *)
vp = viewB;
Show[plot, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
