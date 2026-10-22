(* ::Package:: *)

(* 来源：mathematica /Mathmatica.nb 中第 23 行起的输入单元；对应书中 全书图形/zeta零迹线.pdf *)

(* 图 17.4  \[Zeta](s) 零迹线（纵轴 Re(s) 正方向向下，平凡零点在图上方）
   版式与图 17.6（xi零迹线-修订.wl）统一：
   1. ImageSize\[RightArrow]560，字号 12\[Dash]13；排入 0.90\textwidth 后文字约 8\[Dash]9 pt；
   2. 图例移到图框下方；原「t_k 数值表」删去（零点位置由刻度与标号即可读出）；
   3. 临界线绿色虚线加粗、压在最上层；零迹线 Thickness 0.0022；
   4. 非平凡零点取 |\[Gamma]| \[LessEqual] 32 的四对，数值 6 位；
   5. 竖向网格线与刻度对齐；图例「½」\[RightArrow]「1/2」；中文用 Songti SC。 *)

ClearAll["Global`*"];

reMin = -8.5; reMax = 4;       (* Re(s) 范围；-8.5 使 s=-8 的平凡零点不压边框 *)
imMin = -32;  imMax = 32;

(* ---- 版式参数（与 xi 图相同） ---- *)
imgW   = 560;
fsTick = 12; fsLab = 13; fsTitle = 13; fsRho = 13; fsLeg = 12; fsTriv = 11;
cjk    = "Songti SC";
cRed   = RGBColor[0.80, 0.02, 0.02];
cBlue  = RGBColor[0.02, 0.10, 0.80];
cGreen = RGBColor[0.00, 0.55, 0.10];
cZero  = RGBColor[1.00, 0.75, 0.00];
cTriv  = RGBColor[0.55, 0.00, 0.75];

(* ---- 零迹线：显示坐标 r = -Re(s)，故 Re(s) 负值在上 ---- *)
reZero = ContourPlot[Re[Zeta[-r + I t]] == 0, {t, imMin, imMax}, {r, -reMax, -reMin},
   ContourStyle -> Directive[cRed, Thickness[0.0022]],
   Exclusions -> None, PlotPoints -> 250, MaxRecursion -> 6,
   Frame -> False, Axes -> False, Background -> None];

imZero = ContourPlot[Im[Zeta[-r + I t]] == 0, {t, imMin, imMax}, {r, -reMax, -reMin},
   ContourStyle -> Directive[cBlue, Thickness[0.0022]],
   Exclusions -> None, PlotPoints -> 250, MaxRecursion -> 6,
   Frame -> False, Axes -> False, Background -> None];

(* ---- 临界线 Re(s)=1/2（显示坐标 r=-1/2） ---- *)
critLine = Graphics[{cGreen, Thickness[0.0045],
    CapForm["Butt"], Line[{{imMin, -1/2}, {imMax, -1/2}}]}];

(* ---- 非平凡零点（|\[Gamma]| \[LessEqual] 32） ---- *)
zeroT = {14.134725, 21.022040, 25.010858, 30.424876};
zeroMarkers = Graphics[{cZero, EdgeForm[{Black, AbsoluteThickness[0.6]}],
    Table[Disk[{t, -1/2}, {0.50, 0.25}], {t, Join[zeroT, -zeroT]}]}];

rhoLabels = Graphics[{
    Table[Text[Style[Subscript[Style["\[Rho]", Italic], k], fsRho, Black],
       {zeroT[[k]], 0.85}, {0, 0}], {k, Length[zeroT]}],
    Table[Text[Style[OverBar[Subscript[Style["\[Rho]", Italic], k]], fsRho, Black],
       {-zeroT[[k]], -1.95}, {0, 0}], {k, Length[zeroT]}]}];

(* ---- 平凡零点 s=-2,-4,-6,-8（显示坐标 r=2,4,6,8，位于 t=0） ---- *)
trivialZeros = {-2, -4, -6, -8};
trivialMarkers = Graphics[{cTriv, EdgeForm[{Black, AbsoluteThickness[0.6]}],
    Table[Disk[{0, -s}, {0.50, 0.25}], {s, trivialZeros}]}];
trivialLabels = Graphics[
   Table[Text[Style["s = " <> ToString[s], fsTriv, cTriv], {1.0, -s}, {-1, 0}],
    {s, trivialZeros}]];

(* ---- 图例（置于图框下方） ---- *)
legItem[g_, txt_, col_] := Row[{g, Style[txt, fsLeg, col, FontFamily -> cjk]}, " "];
legLine[col_, dash_] := Graphics[{col, AbsoluteThickness[1.6], dash,
     Line[{{0, 0}, {1, 0}}]}, ImageSize -> {26, 8}, PlotRangePadding -> None];
legDisk[col_] := Graphics[{col, EdgeForm[{Black, AbsoluteThickness[0.6]}], Disk[]},
    ImageSize -> 9];
legend = Row[{
    legItem[legLine[cRed, {}], "Re \[Zeta] = 0", cRed],
    legItem[legLine[cBlue, {}], "Im \[Zeta] = 0", cBlue],
    legItem[legLine[cGreen, {}], "临界线 Re(s) = 1/2", cGreen],
    legItem[legDisk[cZero], "非平凡零点", Black],
    legItem[legDisk[cTriv], "平凡零点", cTriv]}, Spacer[14]];

(* ---- 组装 ---- *)
plot = Show[reZero, imZero, critLine, zeroMarkers, rhoLabels, trivialMarkers, trivialLabels,
   Frame -> True, FrameStyle -> Directive[GrayLevel[0.35], AbsoluteThickness[0.6]],
   FrameLabel -> {
     Style["Im(s)", fsLab, Black],
     Style["Re(s)（正方向向下）", fsLab, Black, FontFamily -> cjk], None, None},
   FrameTicks -> {
     {Table[{r, Style[ToString[-r], fsTick]}, {r, Range[-4, 8, 1]}], None},
     {Table[{t, Style[ToString[t], fsTick]}, {t, Range[-30, 30, 10]}], None}},
   GridLines -> {Range[-30, 30, 10], Range[-4, 8, 1]},
   GridLinesStyle -> Directive[GrayLevel[0.85], AbsoluteDashing[{2, 2}]],
   PlotRange -> {{imMin, imMax}, {-reMax, -reMin}}, PlotRangePadding -> None,
   AspectRatio -> 0.46, ImageSize -> imgW, Background -> None];

fig = Labeled[plot, legend, Bottom, Spacings -> 0.6];
fig

Export[FileNameJoin[{NotebookDirectory[], "图17.4-zeta零迹线.pdf"}], fig];
