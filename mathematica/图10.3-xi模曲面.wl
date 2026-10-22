(* ::Package:: *)

(* 图 10.2  ξ 的模曲面 z = |ξ(s)|
   原程序未找到（全书图形/xi模曲面.pdf 为 7 月 1 日导出，对应 .nb 未存盘），2026-10-05 按书中原图重写：
   金黄色模曲面 + 白色网格、参考平面 z = 0、临界带与临界线、非平凡零点；
   版式（字号、线宽、配色、图例在图下方、导出）与第 17 章各图统一。
   正文要点：模非负；关于 Re(s) = 1/2 与实轴 Im(s) = 0 镜面对称。 *)

ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

xi[s_] := 1/2*s*(s - 1)*Pi^(-s/2)*Gamma[s/2]*Zeta[s];
(* 网格点恰落在 s = 0, 1, -2, -4 … 时 Γ 或 ζ 的极点与零因子相消，数值上会得 Indeterminate；
   在这些实轴整数点上微移 10^-8（远小于绘图分辨率） *)
xiN[s_?NumericQ] := Quiet@xi[If[Abs[Im[s]] < 10^-12 && Abs[Re[s] - Round[Re[s]]] < 10^-12, s + 10.^-8, s]];

(* ---- 几何参数与相邻的图 10.1 一致（2026-10-06）：同一 Re、Im 范围，同一视点；
        每单位长度的比例与图 10.1 相同（图 10.1 盒高 2 对应竖轴 −0.5 … 1 共 1.5 个单位） ---- *)
reMin = -4; reMax = 4;            (* 同图 10.1（原 −4 … 5） *)
imMin = -32; imMax = 32;
zMax  = 1.0;                      (* 竖轴到 1：图示范围内 |ξ| 最大约 0.79 *)
pr    = {{reMin, reMax}, {imMin, imMax}, {0, zMax}};
boxR  = {1, 2, 2 zMax/1.5};       (* Re、Im 盒长同图 10.1；竖轴每单位长度同图 10.1（原 {1, 2, 2}） *)
viewPt = {2.8, -2.8, 1.8};        (* 同图 10.1（原 {3.55131, -2.17521, 1.25602}） *)
viewVert = {0, 0, 1};             (* 同图 10.1 *)
cGold = RGBColor[1.00, 0.84, 0.00];

(* ---- 模曲面 ---- *)
surf = Plot3D[Abs[xiN[x + I y]], {x, reMin, reMax}, {y, imMin, imMax},
   PlotRange -> pr, ClippingStyle -> None,
   PlotStyle -> Directive[cGold, Opacity[0.85], Specularity[White, 30]],
   MeshFunctions -> {#1 &, #2 &}, Mesh -> {18, 32},
   MeshStyle -> Directive[White, Opacity[0.75], lwThin],
   BoundaryStyle -> Directive[GrayLevel[0.4], lwThin],
   PlotPoints -> {60, 140}, MaxRecursion -> 3, Lighting -> "Neutral"];

(* ---- 参考平面、临界带、临界线 ---- *)
refPlane = Graphics3D[{EdgeForm[None], FaceForm[Directive[GrayLevel[0.9], Opacity[0.35]]],
    Polygon[{{reMin, imMin, 0}, {reMax, imMin, 0}, {reMax, imMax, 0}, {reMin, imMax, 0}}]}];
stripLines = Graphics3D[{cStrip, lwMid, dashStrip,
    Line[{{0, imMin, 0}, {0, imMax, 0}}], Line[{{1, imMin, 0}, {1, imMax, 0}}]}];
critLine = Graphics3D[{cGreen, lwThick,
    Line[{{1/2, imMin, 0}, {1/2, imMax, 0}}]}];

(* ---- 非平凡零点（|γ| ≤ 32，共轭成对） ---- *)
zeroMarkers = Graphics3D[zeroBalls[Join[{1/2, #, 0} & /@ zeroT, {1/2, -#, 0} & /@ zeroT], pr, boxR]];

(* ---- 图例（置于图框下方，样式同第 17 章） ---- *)
legItem[g_, txt_, col_] := Row[{g, Style[txt, fsLeg, col, FontFamily -> cjk]}, " "];
legLine[col_, dash_] := Graphics[{col, AbsoluteThickness[1.6], dash, Line[{{0, 0}, {1, 0}}]},
   ImageSize -> {26, 8}, PlotRangePadding -> None];
legSurf[col_] := Graphics[{EdgeForm[{GrayLevel[0.4], AbsoluteThickness[0.6]}], col, Rectangle[{0, 0}, {2, 1}]},
   ImageSize -> {20, 10}, PlotRangePadding -> None];
legend = bookLegendRows[{{{bkSurf[cGold],"曲面 |ξ(s)|"},"crit"},{"strip","zero"}}];   (* 图幅变窄，图例分两行 *)

(* ---- 组装 ---- *)
plot = Show[surf, refPlane, stripLines, critLine, zeroMarkers,
   Boxed -> False, Axes -> True, AxesOrigin -> {0, 0, 0},
   AxesStyle -> Directive[Black, lwMid],   (* 全书统一：坐标轴黑色 *)
   AxesLabel -> {Style["Re(s)", fsLab, Black], Style["Im(s)", fsLab, Black],
     Style["|ξ(s)|", fsLab, Black]},
   Ticks -> {
     Table[{k, Style[ToString[k], fsTick]}, {k, {-4, -2, 2, 4}}],
     Table[{k, Style[ToString[k], fsTick]}, {k, {-30, -20, -10, 10, 20, 30}}],
     Table[{k, Style[ToString[k], fsTick]}, {k, {0.5, 1}}]},
   PlotRange -> pr, BoxRatios -> boxR,
   ViewPoint -> viewPt, ViewVertical -> viewVert,
   ImageSize -> imgW, Background -> None, shrink3D];
   (* 与全书单幅图统一输出宽度，并在正文中按 0.90\textwidth 排版。 *)

fig = Labeled[plot, legend, Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图10.3-xi模曲面", fig];

(* ---- 调视点：用鼠标旋转下图，下面一行实时显示当前视点坐标；满意后抄到上面的 viewPt ---- *)
vp = viewPt;
Show[plot, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
