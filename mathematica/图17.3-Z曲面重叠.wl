(* ::Package:: *)

(* 来源：全书图形/Z曲面重叠-1.nb 中第 23 行起的输入单元；对应书中 全书图形/Z曲面重叠.pdf *)

ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

sMin=re17[[1]];sMax=re17[[2]];(* 与图 17.4 相同 *)
tMin=-32;tMax=32;

zerosT={14.134725,21.022040,25.010858,30.424876};(*补 γ_4 = 30.42（|γ| ≤ 32 内共四对，同图 17.5，2026-10-06）*)
zMin=-2.5;zMax=2.5;
prAll={{sMin-0.5,sMax+1.0},{tMin-0.5,tMax+2.5},{zMin-0.2,zMax+0.4}};boxAll=box17[{sMin-0.5,sMax+1.0}];   (* 与图 17.1、17.2 完全相同 *)   (* 与 PlotRangePadding 后的显示范围近似一致，用于零点小球换算 *)
(*非平凡零点：正虚部与负虚部（共轭对）*)

zeroPoints=Table[{0.5,t,0},{t,zerosT}]~Join~Table[{0.5,-t,0},{t,zerosT}];
(*标签位置：正虚部上方，负虚部下方适当偏移*)

labelPointsPos=Table[{0.5,t,0.45},{t,zerosT}];
labelPointsNeg=Table[{0.5,-t,-0.45},{t,zerosT}];
labelsPos={"\[Gamma]₁ \[TildeTilde] 14.13","\[Gamma]₂ \[TildeTilde] 21.02","\[Gamma]₃ \[TildeTilde] 25.01"};
labelsNeg={"-\[Gamma]₁ \[TildeTilde] -14.13","-\[Gamma]₂ \[TildeTilde] -21.02","-\[Gamma]₃ \[TildeTilde] -25.01"};

plot = Show[(*底层灰色底面*)Plot3D[0,{s,sMin,sMax},{t,tMin,tMax},PlotStyle->Directive[GrayLevel[0.92,0.4]],Mesh->None,BoundaryStyle->None],Graphics3D[stripMark3D[{tMin,tMax}]],(*零等高线投影（红=Re=0,蓝=Im=0）*)Plot3D[0,{s,sMin,sMax},{t,tMin,tMax},MeshFunctions->{Function[{s,t,z},Re[Zeta[s+I t]]],Function[{s,t,z},Im[Zeta[s+I t]]]},Mesh->{{0},{0}},MeshStyle->{Directive[cRed,lwMid],Directive[cBlue,lwMid]},PlotPoints->150,MaxRecursion->5,PlotStyle->None,BoundaryStyle->None],(*双曲面（实部红，虚部蓝）*)Plot3D[{Re[Zeta[s+I t]],Im[Zeta[s+I t]]},{s,sMin,sMax},{t,tMin,tMax},PlotRange->{-2.5,2.5},ClippingStyle->None,(* 不画截断处的灰色平面，与其他 3D 图一致 *)PlotPoints->120,Mesh->None,PlotStyle->{Directive[Lighter[Red,0.5],Opacity[0.25],Specularity[White,50]],Directive[Lighter[Blue,0.5],Opacity[0.25],Specularity[White,50]]}],Graphics3D[{zeroBalls[zeroPoints,prAll,boxAll],trivialBalls[{#,0,0}&/@{-2,-4,-6,-8},prAll,boxAll],poleBall[{1,0,0},prAll,boxAll]}],Graphics3D[critLine3D[{tMin,tMax}]],(*坐标轴设置：三轴从原点出发*)Boxed->False,Axes->True,AxesOrigin->{0,0,0},AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},AxesStyle->Directive[Black,lwMid],AxesLabel->{Style["Re(s)",fsLab,Black],Style["Im(s)",fsLab,Black],Style["Re ζ, Im ζ",fsLab,Black]},Ticks->{Table[{s,s},{s,reTicks17}],Table[{t,t},{t,-30,30,10}],Table[{z,""},{z,-2.5,2.5,0.5}](* 高度轴刻度数值取消 *)},TicksStyle->Directive[Black,FontSize->fsTick],BoxRatios->boxAll, ViewPoint -> viewC,ImageSize->imgW,PlotRange->prAll,PlotRangePadding->None,shrink3D(*去掉图与图例之间的空白（2026-10-06）*)];
fig = Labeled[plot, bookLegendRows[{{{bkSurf[Lighter[Red,0.5]],"Re ζ(s) 曲面"},{bkSurf[Lighter[Blue,0.5]],"Im ζ(s) 曲面"},{bkLine[cRed,1.0],"Re ζ = 0"},{bkLine[cBlue,1.0],"Im ζ = 0"}},{"crit","strip","zero","triv","pole"}}], Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图17.3-Z曲面重叠", fig];

(* ---- 调视点：用鼠标旋转下图，下面一行实时显示当前视点坐标；本图与 17.1、17.2 共用 viewC ---- *)
vp = viewC;
Show[plot, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
