(* ::Package:: *)

(* 来源：全书图形/Z曲面重叠.nb 中第 310559 行起的输入单元；对应书中 全书图形/11-Z虚曲面.pdf *)

(*====================================================*)(*Zeta(s) 虚部曲面（出版版配色）+临界线+两阶段分析*)(*====================================================*)ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

(*====================参数====================*)
sMin=re17[[1]];sMax=re17[[2]];(* 与图 17.4 相同 *)
tMin=-32;tMax=32;
zMin=-2.5;zMax=2.5;
criticalRe=0.5;
(*====================非平凡零点====================*)
zerosT={14.134725,21.022040,25.010858};
zeroPoints=Table[{0.5,t,0},{t,zerosT}];

(*====================两阶段区域划分====================*)
(*Stage 1:低虚部区域 (|Im(s)| <16)*)
(*Stage 2:高虚部区域 (|Im(s)| >=16)*)
tBoundary=16;

(*====================曲面部分====================*)
(*A.参考平面*)
refPlane=Plot3D[0,{s,sMin,sMax},{t,tMin,tMax},PlotRange->{{sMin,sMax},{tMin,tMax},{zMin,zMax}},PlotStyle->Directive[GrayLevel[0.86,0.35]],Mesh->None,BoundaryStyle->None];

(*B.虚部零迹线投影*)
zeroTrace=Plot3D[0,{s,sMin,sMax},{t,tMin,tMax},PlotRange->{{sMin,sMax},{tMin,tMax},{zMin,zMax}},MeshFunctions->{Function[{s,t,z},Im[Zeta[s+I t]]]},Mesh->{{0}},MeshStyle->{Directive[GrayLevel[0.95],lwMid]},PlotPoints->180,MaxRecursion->6,PlotStyle->None,BoundaryStyle->None];

(*C.虚部曲面-Stage 1（低虚部）*)
imagSurf1=Plot3D[Im[Zeta[s+I t]],{s,sMin,sMax},{t,-tBoundary,tBoundary},PlotRange->{{sMin,sMax},{-tBoundary,tBoundary},{zMin,zMax}},PlotPoints->100,Mesh->None,ClippingStyle->None,PlotStyle->Directive[RGBColor[0.18,0.28,0.50],Opacity[0.70],Specularity[White,15]]];

(*D.虚部曲面-Stage 2（高虚部）*)
imagSurf2=Plot3D[Im[Zeta[s+I t]],{s,sMin,sMax},{t,tBoundary,tMax},PlotRange->{{sMin,sMax},{tBoundary,tMax},{zMin,zMax}},PlotPoints->80,Mesh->None,ClippingStyle->None,PlotStyle->Directive[RGBColor[0.18,0.28,0.50],Opacity[0.70],Specularity[White,12]]];

imagSurf3=Plot3D[Im[Zeta[s+I t]],{s,sMin,sMax},{t,tMin,-tBoundary},PlotRange->{{sMin,sMax},{tMin,-tBoundary},{zMin,zMax}},PlotPoints->80,Mesh->None,ClippingStyle->None,PlotStyle->Directive[RGBColor[0.18,0.28,0.50],Opacity[0.70],Specularity[White,12]]];

(*E.临界线可视化-在 Re(s)=0.5 处*)
(*E1.临界线上的曲线*)
criticalCurve=ParametricPlot3D[{0.5,t,Im[Zeta[0.5+I t]]},{t,tMin,tMax},PlotPoints->250,MaxRecursion->7,PlotStyle->Directive[RGBColor[0.95,0.15,0.15],lwThick,Opacity[1.0]]];

(*E2.临界线背景平面（半透明）*)
criticalPlane=Plot3D[0,{s,0.4,0.6},{t,tMin,tMax},PlotStyle->Directive[RGBColor[1.0,0.9,0.85],Opacity[0.12]],Mesh->None,BoundaryStyle->None];

(*F.非平凡零点（在临界线上）*)
prAll={{sMin-0.5,sMax+1.0},{tMin-0.5,tMax+2.5},{zMin-0.2,zMax+0.4}};boxAll=box17[{sMin-0.5,sMax+1.0}];
zeroSpheres=Graphics3D[zeroBalls[Join[zeroPoints,zeroPoints/.{x_,y_,z_}:>{x,-y,z}],prAll,boxAll]];

(*G.参考平面上的临界带和临界线*)
(*G1.临界带左边界：Re(s)=0*)
stripLeftBoundary=Graphics3D[{Directive[cStrip,lwMid,dashStrip],Line[{{0,tMin,0},{0,tMax,0}}]}];

(*G2.临界带右边界：Re(s)=1*)
stripRightBoundary=Graphics3D[{Directive[cStrip,lwMid,dashStrip],Line[{{1,tMin,0},{1,tMax,0}}]}];

(*G3.临界线：Re(s)=1/2（实线，更粗，颜色更深）*)
criticalLineBase=Graphics3D[{Directive[cGreen,lwThick],Line[{{0.5,tMin,0},{0.5,tMax,0}}]}];

(*H.阶段分界线指示（在参考平面上）*)
stageBoundaryLine1=Graphics3D[{Directive[RGBColor[0.3,0.5,0.8],lwMid,AbsoluteDashing[{2,3}]],Line[{{sMin,tBoundary,0},{sMax,tBoundary,0}}]}];

stageBoundaryLine2=Graphics3D[{Directive[RGBColor[0.3,0.5,0.8],lwMid,AbsoluteDashing[{2,3}]],Line[{{sMin,-tBoundary,0},{sMax,-tBoundary,0}}]}];

(*====================手动三轴（从原点出发）====================*)
axisThick=Directive[Black,lwMid];
tickW=Directive[Black,lwThin];

(*轴线*)
reAxisLine=Graphics3D[{axisThick,Line[{{sMin-0.5,0,0},{sMax+0.8,0,0}}]}];
imAxisLine=Graphics3D[{axisThick,Line[{{0,tMin-0.5,0},{0,tMax+1.0,0}}]}];
zAxisLine=Graphics3D[{axisThick,Line[{{0,0,zMin-0.1},{0,0,zMax+0.2}}]}];

(*Re(s) 轴刻度：步长 4，凸出方向+t*)
sTickLen=1.8;sLabelT=4.0;
sTickObjs=Table[{Graphics3D[{tickW,Line[{{sv,0,0},{sv,sTickLen,0}}]}],Graphics3D[Text[Style[sv,fsTick,Black],{sv,sLabelT,0}]]},{sv,reTicks17}];
s0Tick={Graphics3D[{tickW,Line[{{0,0,0},{0,sTickLen,0}}]}]};
reLabel=Graphics3D[Text[Style["Re(s)",fsLab,Black],{sMax+1.2,4.5,0}]];

(*Im(s) 轴刻度：步长 10，凸出方向-s*)
tTickS=0.5;tLabelS=-1.5;
tTickObjs=Table[{Graphics3D[{tickW,Line[{{0,tv,0},{-tTickS,tv,0}}]}],Graphics3D[Text[Style[tv,fsTick,Black],{tLabelS,tv,0}]]},{tv,DeleteCases[Range[-30,30,10](*原 Range[tMin,tMax,10]：tMin=-32 时刻度成 -32,-22,…,28（2026-10-06）*),0]}];
t0Tick={Graphics3D[{tickW,Line[{{0,0,0},{-tTickS,0,0}}]}]};
imLabel=Graphics3D[Text[Style["Im(s)",fsLab,Black],{-1.8,tMax+2.5,0}]];

(*z 轴刻度：步长 1，凸出方向-s*)
zTickS=0.5;zLabelS=-1.5;
zTickObjs=Table[{Graphics3D[{tickW,Line[{{0,0,zv},{-zTickS,0,zv}}]}],Nothing (* 高度轴刻度数值取消 *)},{zv,DeleteCases[Range[zMin,zMax,1]//N,0.]}];
z0Tick={Graphics3D[{tickW,Line[{{0,0,0},{-zTickS,0,0}}]}]};
zLabel=Graphics3D[Text[Style["Im \[Zeta](s)",fsLab,Black],{-2.0,0,zMax+0.3}]];

(*原点*)
originDot=Graphics3D[{Black,PointSize[0.008],Point[{0,0,0}]}];
originLabel=Graphics3D[Text[Style["O",fsLab,Black],{-1.0,-2.5,-0.15}]];

(*====================阶段和临界区域标签====================*)
(*Stage 1 标签：低虚部区域*)
stage1Label=Graphics3D[Text[Style["阶段 1：|t| < 16",fsAnn,RGBColor[0.18,0.28,0.50],FontFamily->cjk],{sMax-2.5,8,zMax-0.3}]];

(*Stage 2 标签：高虚部区域*)
stage2Label=Graphics3D[Text[Style["阶段 2：|t| \[GreaterEqual] 16",fsAnn,RGBColor[0.18,0.28,0.50],FontFamily->cjk],{sMax-2.5,24,zMax-0.3}]];

(*临界线标签（在参考平面上）*)
criticalLineLabel=Graphics3D[Text[Style["临界线 \[Sigma] = 1/2",fsAnn,cGreen,FontFamily->cjk],{0.5,-4,-0.3}]];

(*临界带标签（在参考平面上）*)
criticalStripLabel=Graphics3D[Text[Style["临界带 0 < \[Sigma] < 1",fsAnn,cStrip,FontFamily->cjk],{0.5,-10,-0.15}]];

(* ---- 统一画法（2026-10-06）：临界线、临界带、零点改用 书图样式.wl 中的函数；文字说明移入图例 ---- *)
criticalLineLabel=Graphics3D[{}];criticalStripLabel=Graphics3D[{}];
(*====================组合输出====================*)
(* 17.1、17.2 只画单个曲面，尚未涉及 Re = 0 与 Im = 0 的交点，故不画零点小球；零点自图 17.3 起出现（2026-10-06） *)
plot = Show[refPlane,zeroTrace,imagSurf1,imagSurf2,imagSurf3,stripLeftBoundary,stripRightBoundary,criticalLineBase,stageBoundaryLine1,stageBoundaryLine2,reAxisLine,Sequence@@Flatten[sTickObjs],Sequence@@Flatten[s0Tick],reLabel,imAxisLine,Sequence@@Flatten[tTickObjs],Sequence@@Flatten[t0Tick],imLabel,zAxisLine,Sequence@@Flatten[zTickObjs],Sequence@@Flatten[z0Tick],zLabel,originDot,originLabel,criticalLineLabel,criticalStripLabel,PlotRange->prAll,BoxRatios->boxAll,Boxed->False,Axes->False,ViewPoint->viewC,ImageSize->imgW,shrink3D(*去掉图与图例之间的空白（2026-10-06）*)];
fig = Labeled[plot, bookLegendRows[{{{bkLine[GrayLevel[0.55],1.0],"Im \[Zeta](s) = 0 零迹线"},"crit","strip"},{{bkLine[RGBColor[0.3,0.5,0.8],1.0],"|Im s| = 16 阶段分界"}}}], Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图17.2-Z虚曲面", fig];

(* 调视点用：取消下面三行的注释，鼠标旋转后读出 vp
vp = viewC;
Show[plot, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
*)
