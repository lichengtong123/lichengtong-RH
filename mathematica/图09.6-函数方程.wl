(* ::Package:: *)

(* 来源：全书图形/函数方程.nb 中第 21 行起的输入单元；对应书中 全书图形/8-函数方程.pdf *)

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

view96 = {2.73811, -2.99949, 0.908749};   (* 作者在 Mathematica 中旋转选定（2026-10-05） *)



(* ================================================================黎曼 Zeta 函数泛函方程可视化（统一风格\[CenterDot]清晰区分版） 设计策略：-主曲面：亮金色（RGB[1.0,0.84,0.0]），透明度 0.80，网格深灰-对称曲面：红铜色（RGB[0.85,0.45,0.10]），透明度 0.55，网格浅灰-统一光照、坐标轴、刻度风格================================================================*)(*--------1. 范围控制--------*)reMin=-4;reMax=5;
imMin=-4;imMax=32;
zMax=4;

zeroImValues={14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,40.918719,43.327073,48.005151,49.773832};

(* ================================================================*)
(*主曲面|Zeta(s)| \[LongDash]亮金色*)
(* ================================================================*)

modPlot1=Plot3D[Abs[Zeta[x+I y]],{x,reMin,reMax},{y,imMin,imMax},PlotStyle->Directive[RGBColor[0.9,0.74,0.0],(*亮金色*)Opacity[0.80],Specularity[White,30]],Mesh->30,MeshStyle->Directive[GrayLevel[0.2],Opacity[0.9]],PlotPoints->100,MaxRecursion->4,PlotRange->{{reMin,reMax},{imMin,imMax},{0,zMax}},ClippingStyle->None,Exclusions->{{x==1,y==0}},Boxed->False,Axes->True,AxesOrigin->{0,0,0},AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},AxesLabel->{Style["Re(s)",Italic,13,Bold],Style["Im(s)",Italic,13,Bold],Style["|\[Zeta](s)|",13,Bold]},Ticks->{Table[{x,x},{x,-4,6,2}],{{-30,-30},{-20,-20},{-10,-10},{0,""},{10,10},{20,20},{30,30}},{{0,""},{1,1},{2,2},{3,3},{4,4}}},TicksStyle->Directive[Black,FontSize->fsTick],AxesStyle->Directive[Black,lwMid]];

(* ================================================================*)
(*对称曲面|Zeta(1-s)| \[LongDash]红铜色（与亮金色形成清晰对比）*)
(* ================================================================*)

modPlot2=Plot3D[Abs[Zeta[1-x-I y]],{x,reMin,reMax},{y,imMin,imMax},PlotStyle->Directive[RGBColor[0.65,0.45,0.10],(*红铜色\[LongDash]偏红偏暗*)Opacity[0.75],(*更透明，便于看到下方曲面*)Specularity[White,25]       (*光泽稍弱，与主曲面区分*)],Mesh->20,(*网格更疏，辅助识别*)MeshStyle->Directive[GrayLevel[1.0],Opacity[0.95]],PlotPoints->80,MaxRecursion->3,PlotRange->{{reMin,reMax},{imMin,imMax},{0,zMax}},ClippingStyle->None,Exclusions->{{x==0,y==0}},Boxed->False,Axes->True,AxesOrigin->{0,0,0},AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},AxesLabel->{Style["Re(s)",Italic,13,Bold],Style["Im(s)",Italic,13,Bold],Style["|\[Zeta](1-s)|",13,Bold]   (*标签区分*)},Ticks->{Table[{x,x},{x,-4,6,2}],{{-30,-30},{-20,-20},{-10,-10},{0,""},{10,10},{20,20},{30,30}},{{0,""},{1,1},{2,2},{3,3},{4,4}}},TicksStyle->Directive[Black,FontSize->fsTick],AxesStyle->Directive[Black,lwMid]];

(* ================================================================*)
(*组合图形+辅助元素*)
(* ================================================================*)

plot = Show[(*主曲面*)modPlot1,(*对称曲面*)modPlot2,(*半透明 z=0 参考平面*)Graphics3D[{Opacity[0.04],GrayLevel[0.75],Polygon[{{reMin,imMin,0},{reMax,imMin,0},{reMax,imMax,0},{reMin,imMax,0}}]}],Graphics3D[stripMark3D[{imMin,imMax}]],Graphics3D[critLine3D[{imMin,imMax}]],Graphics3D[zeroBalls[{1/2,#,0}&/@Select[zeroImValues,#<=imMax&],{{reMin,reMax},{imMin,imMax},{0,zMax}},{1,2,1}]],(*实轴截面曲线*)ParametricPlot3D[{x,0,Abs[Zeta[x]]},{x,reMin,reMax},PlotStyle->Directive[RGBColor[0.3,0.65,0.7],lwThin],PlotPoints->200,Exclusions->(x==1)],(* =====全局设置（继承 modPlot 风格）=====*)Boxed->False,Axes->True,AxesOrigin->{0,0,0},AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},AxesLabel->{Style["Re(s)",Italic,13,Bold],Style["Im(s)",Italic,13,Bold],Style["|\[Zeta](s)|",13,Bold]},Ticks->{Table[{x,x},{x,-4,6,2}],{{-30,-30},{-20,-20},{-10,-10},{0,""},{10,10},{20,20},{30,30}},{{0,""},{1,1},{2,2},{3,3},{4,4}}},TicksStyle->Directive[Black,FontSize->fsTick],AxesStyle->Directive[Black,lwMid],BoxRatios->{1,2,1},ViewPoint->view96,ImageSize->imgW,Background->None,shrink3D];
fig = Labeled[plot, bookLegend[{{bkSurf[RGBColor[0.9,0.74,0.0]],"|ζ(s)|"},{bkSurf[RGBColor[0.65,0.45,0.10]],"|ζ(1−s)|"},"crit","strip","zero"}], Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图09.6-函数方程", fig];

(* ---- 调视点：用鼠标旋转下图，下面一行实时显示当前视点坐标；
        满意后把数值抄到上面的 view96 ---- *)
vp = view96;
Show[plot, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
