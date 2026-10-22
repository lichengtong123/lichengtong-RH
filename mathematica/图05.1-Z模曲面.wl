(* ::Package:: *)

(* 来源：全书图形/zeta模曲面-1.nb 中第 23 行起的输入单元；对应书中 全书图形/5-Z模曲面.pdf *)

ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

(* ==========1. 参数==========*)
reMin=1.05;reMax=6;
imMin=-32;imMax=32;
nMax=100;
zetaSeries[s_,nmax_]:=Sum[1/n^s,{n,1,nmax}];

(* ==========2. 模曲面（2026-10-06 改为与图 9.1 相同的画法：Plot3D 自带三轴、同一刻度与标签、
   同一 PlotRange / BoxRatios / 视点，并去白边；原手绘坐标轴、刻度一段删去）==========*)
modulusPlot=Plot3D[Abs[zetaSeries[x+I y,nMax]],{x,reMin,reMax},{y,imMin,imMax},PlotStyle->Directive[RGBColor[1.0,0.84,0.0],Opacity[0.80],Specularity[White,30]],Mesh->30,MeshStyle->Directive[GrayLevel[0.25],Opacity[0.35]],PlotPoints->100,MaxRecursion->4,PlotRange->{{-1.5,reMax+0.5},{imMin-0.5,imMax+2.5},{0,4.2}},ClippingStyle->None,Boxed->False,Axes->True,AxesOrigin->{0,0,0},
AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},
AxesStyle->{Directive[Black,AbsoluteThickness[0.2]],Directive[Black,AbsoluteThickness[0.2]],Directive[Black,AbsoluteThickness[0.2]]},AxesLabel->{Style["Re(s)",13,Bold,Black],Style["Im(s)",13,Bold,Black],Style[Row[{"|",Subscript["\[Zeta]","N"],"(s)|"}],13,Bold,Black]},Ticks->{{-6,-4,-2,{0,"0"},1,3,5},{-30,-20,-10,{0,""},10,20,30},{1,2,3,4}},TicksStyle->Directive[Black,FontSize->10],FaceGrids->None,Background->None];

(* ==========3. 收敛边界采用灰色虚线，与后文解析延拓位置的红线区分==========*)
xPlotMin=0;
refPlane=Graphics3D[{Opacity[0.25],GrayLevel[0.55],Polygon[{{xPlotMin,imMin,0},{reMax,imMin,0},{reMax,imMax,0},{xPlotMin,imMax,0}}]}];
convLine=Graphics3D[{Directive[GrayLevel[0.35],AbsoluteThickness[0.8],Dashed],Line[{{1,imMin,0.0},{1,imMax,0.0}}]}];(* 收敛边界为 1，曲面起绘位置为 reMin=1.05 *)

(* ==========4. 组合输出==========*)
plot = Show[modulusPlot,refPlane,convLine,PlotRange->{{-1.5,reMax+0.5},{imMin-0.5,imMax+2.5},{0,4.2}},BoxRatios->bookBoxB[{-1.5,6.5}],ViewPoint->viewB,ImageSize->imgW,shrink3D];
(* 图例：ζ_N 的下标用 Subscript 排出（原字符串 "ζ_N" 会照字面显示下划线，2026-10-06） *)
boundaryKey=Graphics[{GrayLevel[0.35],AbsoluteThickness[0.8],Dashed,Line[{{0,0},{1,0}}]},ImageSize->{26,8},PlotRangePadding->None];
legend51 = Column[{
    bkItem[bkSurf[RGBColor[1.0,0.84,0.0]],Row[{"曲面 |",Subscript["\[Zeta]","N"],"(s)|（N = 100；1.05 \[LessEqual] Re(s) \[LessEqual] 6）"}]],
    bkItem[boundaryKey,"Dirichlet 级数收敛边界 Re(s) = 1"]
  },Alignment->Center,Spacings->0.35];
fig = Labeled[plot, legend51, Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图05.1-Z模曲面", fig];

(* ---- 调视点：用鼠标旋转下图，下面一行实时显示当前视点坐标；
        本组（图 5.1、9.1–9.4、9.7）共用 书图样式.wl 中的 viewB，改那里即可全组同步 ---- *)
vp = viewB;
Show[plot, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
