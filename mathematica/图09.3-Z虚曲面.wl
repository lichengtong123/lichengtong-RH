(* ::Package:: *)

(* 来源：全书图形/zeta虚曲面-1.nb 中第 76894 行起的输入单元；对应书中 全书图形/8-Z虚曲面.pdf *)

ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

(* ==========1. 参数==========*)
sMin=1.0;sMax=6.0(* 与图 5.1、9.1 统一 *);
tMin=-32.0;tMax=32.0;
zMin=-4.0;zMax=4.0;(*Im[Zeta] 关于 t 反对称，范围对称*)(* ==========2. 曲面风格==========*)surfaceStyle=Directive[RGBColor[0.12,0.28,0.55],Opacity[0.96],(*深蓝*)Specularity[White,15]];
meshStyle=Directive[GrayLevel[0.95],Opacity[0.7]];

(* ==========3. 曲面（虚部）==========*)
imagPlot=Plot3D[Im[Zeta[s+I t]],{s,sMin,sMax},{t,tMin,tMax},PlotRange->{{0,sMax},{tMin,tMax},{zMin,zMax}},PlotPoints->100,MaxRecursion->3,Mesh->{35,35},MeshStyle->meshStyle,PlotStyle->surfaceStyle,BoxRatios->bookBoxB[{-1.5,6.5}],BoundaryStyle->None,Boxed->False,Axes->False,Exclusions->{{s==1,t==0}},ClippingStyle->None,Lighting->{{"Ambient",GrayLevel[0.50]},{"Directional",GrayLevel[0.90],ImageScaled[{1,1,2}]},{"Directional",GrayLevel[0.25],ImageScaled[{-1,0,1}]},{"Directional",GrayLevel[0.20],ImageScaled[{1,-1,1}]},{"Directional",GrayLevel[0.20],ImageScaled[{0,1,1}]}}];

(* ==========4. 参考平面 z=0==========*)
refPlane=Graphics3D[{Opacity[0.10],GrayLevel[0.55],Polygon[{{0,tMin,0},{sMax,tMin,0},{sMax,tMax,0},{0,tMax,0}}]}];

(* ==========5. 三条轴线，均从原点出发==========*)
axisThick=Directive[Black,Thickness[0.0005]];
reAxisLine=Graphics3D[{axisThick,Line[{{0,0,0},{sMax+0.3,0,0}}]}];
imAxisLine=Graphics3D[{axisThick,Line[{{0,tMin-0.5,0},{0,tMax+1,0}}]}];
zAxisLine=Graphics3D[{axisThick,Line[{{0,0,zMin-0.1},{0,0,zMax+0.2}}]}];

(* ==========6. 刻度与标签==========*)
tickW=Directive[Black,Thickness[0.0005]];

(*----Re(s) 轴----*)
sTickLen=1.2;sLabelT=2.8;
sTickObjs=Table[{Graphics3D[{tickW,Line[{{sv,0,0},{sv,sTickLen,0}}]}],Graphics3D[Text[Style[sv,10,Black],{sv,sLabelT,0}]]},{sv,{1,3,5}}];(* 与图 9.1 相同：Re 轴只标 1, 3, 5（原每 0.5 一格，过挤） *)
reLabel=Graphics3D[Text[Style["Re(s)",Italic,12,Black],{sMax+0.25,3.2,0}]];

(*----Im(s) 轴----*)
tTickS=0.05;tLabelS=-0.3;
tTickObjs=Table[{Graphics3D[{tickW,Line[{{0,tv,0},{-tTickS,tv,0}}]}],Graphics3D[Text[Style[tv,10,Black],{tLabelS,tv,0}]]},{tv,DeleteCases[Range[-30,30,10],0]}];
t0Tick={Graphics3D[{tickW,Line[{{0,0,0},{-tTickS,0,0}}]}]};(* 原点处不另标 0，与图 9.1 相同 *)
imLabel=Graphics3D[Text[Style["Im(s)",Italic,12,Black],{-1.1,tMax+2.5,0}]];

(*----z 轴：对称范围-4 到 4，步长 1----*)
zTickS=0.05;zLabelS=-0.2;
zTickObjs=Table[{Graphics3D[{tickW,Line[{{0,0,zv},{-zTickS,0,zv}}]}],Graphics3D[Text[Style[zv,10,Black],{zLabelS,0,zv}]]},{zv,{-4,-2,2,4}}];(* z 轴隔 2 标注 *)
z0Tick={Graphics3D[{tickW,Line[{{0,0,0},{-zTickS,0,0}}]}]};
zLabel=Graphics3D[Text[Style["Im(\[Zeta](s))",Italic,12,Black],{-1.1,0,zMax+0.25}]];

(*----原点----*)
originDot=Graphics3D[{Black,PointSize[0.005],Point[{0,0,0}]}];
originLabel=Graphics3D[Text[Style["O",11,Bold,Black],{-0.28,-1.8,-0.10}]];

(* ==========7. 平面说明与极点线==========*)
planeLabel=Graphics3D[Text[Style["z = 0",11,Bold,GrayLevel[0.40]],{0.35 sMax,tMin+0.12 (tMax-tMin),0.07}]];

AriveLine=Graphics3D[{Directive[Red,AbsoluteThickness[0.5]],Line[{{1.0,-32.0,0.0},{1.0,32.0,0.0}}]}];

(* ==========8. 组合输出==========*)
plot = Show[imagPlot,refPlane,planeLabel,reAxisLine,Sequence@@Flatten[sTickObjs],reLabel,imAxisLine,Sequence@@Flatten[tTickObjs],Sequence@@Flatten[t0Tick],imLabel,zAxisLine,Sequence@@Flatten[zTickObjs],Sequence@@Flatten[z0Tick],zLabel,originDot,originLabel,AriveLine,PlotRange->{{-1.5,sMax+0.5},{tMin-0.5,tMax+2.5},{zMin-0.2,zMax+0.4}},BoxRatios->bookBoxB[{-1.5,6.5}],Boxed->False,Axes->False,ViewPoint->viewB,ImageSize->imgW,shrink3D];
fig = Labeled[plot, bookLegend[{{bkSurf[RGBColor[0.12,0.28,0.55]],"曲面 Im ζ(s)"},{bkLine[Red,1.0],"延拓推进线 Re(s) = 1"}}], Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图09.3-Z虚曲面", fig];

(* ---- 调视点：用鼠标旋转下图，下面一行实时显示当前视点坐标；
        本组（图 5.1、9.1–9.4、9.7）共用 书图样式.wl 中的 viewB，改那里即可全组同步 ---- *)
vp = viewB;
Show[plot, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
