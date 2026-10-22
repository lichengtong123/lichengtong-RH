(* ::Package:: *)

(* 来源：mathematica /Mathmatica.nb 中第 141089 行起的输入单元；对应书中 全书图形/xi零迹线.pdf *)

(* 图 17.6  \[Xi](s) 零迹线（纵轴 Re(s) 正方向向下，与图 17.1\[Dash]17.4 一致）
   修订要点：
   1. 临界线绿色虚线加粗并压在最上层，与下面的 Im \[Xi]=0 蓝线交替可见；
   2. 零点只取 |\[Gamma]| \[LessEqual] 32 的四对，并用更精确的数值；
   3. 字号按排版尺寸重设：ImageSize\[RightArrow]560，排入 0.90\textwidth 后文字约 8\[Dash]9 pt；
   4. 纵轴标签注明「正方向向下」，标题同 17.4；图例「½」\[RightArrow]「1/2」；
   5. 竖向网格线与刻度对齐（-30,-20,\[Ellipsis],30）；
   6. 图例移到图框下方，不再压住曲线；中文用 Songti SC，与正文一致。
   7. 与图 17.4（zeta零迹线-修订.wl）统一：AspectRatio 0.46、PlotPoints 250、
      零点圆点与 \[Rho] 标号的屏幕尺寸和间距相同（纵向数据单位按 8/12.5 换算）。 *)

ClearAll["Global`*"];
xi[s_] := 1/2*s*(s - 1)*Pi^(-s/2)*Gamma[s/2]*Zeta[s];

reMin = -4; reMax = 4;
imMin = -32; imMax = 32;

(* ---- 版式参数 ---- *)
imgW   = 560;                 (* 排入 0.90\textwidth \[TildeTilde] 386 pt，缩放约 0.69 *)
fsTick = 12; fsLab = 13; fsTitle = 13; fsRho = 13; fsLeg = 12;
cjk    = "Songti SC";
cRed   = RGBColor[0.80, 0.02, 0.02];
cBlue  = RGBColor[0.02, 0.10, 0.80];
cGreen = RGBColor[0.00, 0.55, 0.10];
cZero  = RGBColor[1.00, 0.75, 0.00];

(* ---- 零迹线：显示坐标 r = -Re(s)，故 Re(s) 负值在上 ---- *)
reZero = ContourPlot[Re[xi[-r + I t]] == 0, {t, imMin, imMax}, {r, -reMax, -reMin},
   ContourStyle -> Directive[cRed, Thickness[0.0022]],
   Exclusions -> None, PlotPoints -> 250, MaxRecursion -> 6,
   Frame -> False, Axes -> False, Background -> None];

imZero = ContourPlot[Im[xi[-r + I t]] == 0, {t, imMin, imMax}, {r, -reMax, -reMin},
   ContourStyle -> Directive[cBlue, Thickness[0.0022]],
   Exclusions -> None, PlotPoints -> 250, MaxRecursion -> 6,
   Frame -> False, Axes -> False, Background -> None];

(* ---- 临界线 Re(s)=1/2（显示坐标 r=-1/2）：比蓝线粗，放在零迹线之上 ---- *)
critLine = Graphics[{cGreen, Thickness[0.0045],
    CapForm["Butt"], Line[{{imMin, -1/2}, {imMax, -1/2}}]}];

(* ---- 非平凡零点（|\[Gamma]| \[LessEqual] 32） ---- *)
zeroT = {14.134725, 21.022040, 25.010858, 30.424876};
zeroMarkers = Graphics[{cZero, EdgeForm[{Black, AbsoluteThickness[0.6]}],
    Table[Disk[{t, -1/2}, {0.50, 0.16}], {t, Join[zeroT, -zeroT]}]}];

rhoLabels = Graphics[{
    Table[Text[Style[Subscript[Style["\[Rho]", Italic], k], fsRho, Black],
       {zeroT[[k]], 0.36}, {0, 0}], {k, Length[zeroT]}],
    Table[Text[Style[OverBar[Subscript[Style["\[Rho]", Italic], k]], fsRho, Black],
       {-zeroT[[k]], -1.43}, {0, 0}], {k, Length[zeroT]}]}];

(* ---- 图例（置于图框下方） ---- *)
legItem[g_, txt_, col_] := Row[{g, Style[txt, fsLeg, col, FontFamily -> cjk]}, " "];
legLine[col_, dash_] := Graphics[{col, AbsoluteThickness[1.6], dash,
     Line[{{0, 0}, {1, 0}}]}, ImageSize -> {26, 8}, PlotRangePadding -> None];
legend = Row[{
    legItem[legLine[cRed, {}], "Re \[Xi] = 0", cRed],
    legItem[legLine[cBlue, {}], "Im \[Xi] = 0", cBlue],
    legItem[legLine[cGreen, {}], "临界线 Re(s) = 1/2", cGreen],
    legItem[Graphics[{cZero, EdgeForm[{Black, AbsoluteThickness[0.6]}], Disk[]},
       ImageSize -> 9], "非平凡零点", Black]}, Spacer[14]];

(* ---- 组装 ---- *)
plot = Show[reZero, imZero, critLine, zeroMarkers, rhoLabels,
   Frame -> True, FrameStyle -> Directive[GrayLevel[0.35], AbsoluteThickness[0.6]],
   FrameLabel -> {
     Style["Im(s)", fsLab, Black],
     Style["Re(s)（正方向向下）", fsLab, Black, FontFamily -> cjk], None, None},
   FrameTicks -> {
     {Table[{r, Style[ToString[-r], fsTick]}, {r, Range[-4, 4, 1]}], None},
     {Table[{t, Style[ToString[t], fsTick]}, {t, Range[-30, 30, 10]}], None}},
   GridLines -> {Range[-30, 30, 10], Range[-4, 4, 1]},
   GridLinesStyle -> Directive[GrayLevel[0.85], AbsoluteDashing[{2, 2}]],
   PlotRange -> {{imMin, imMax}, {-reMax, -reMin}}, PlotRangePadding -> None,
   AspectRatio -> 0.46, ImageSize -> imgW, Background -> None];

fig = Labeled[plot, legend, Bottom, Spacings -> 0.6];
fig

Export[FileNameJoin[{NotebookDirectory[], "图17.6-xi零迹线.pdf"}], fig];
