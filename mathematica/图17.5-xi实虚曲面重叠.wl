(* 黎曼 ξ(s) 实部曲面（淡红）+ 虚部曲面（淡蓝）叠合图
   实部零迹线（红）+ 虚部零迹线（蓝），投影于参考平面 z = 0
   版式与图 17.4（ζ 零迹线）、图 17.6（ξ 零迹线）统一：
   1. 配色：cRed / cBlue / cGreen / cZero 与两张零迹线图相同；曲面用同色、Opacity 0.30；
   2. ImageSize → 560，字号 12–13，中文用 Songti SC；轴标签与刻度为黑色、不加粗；
   3. 非平凡零点取 |γ| ≤ 32 的四对，数值 6 位（原 32.935 在 Im 范围之外，删去）；
      零点标记金色，并标 ρ_k / ρ̄_k；
   4. 临界线 Re(s) = 1/2：绿色虚线，画在参考平面上，与零迹线图一致；
   5. 零迹线 PlotPoints 250、MaxRecursion 6，与零迹线图相同；
   6. 图例由图框上方的 Epilog 改为图框下方（Labeled），不再压住曲面；
   7. 修正：虚部零迹线的 x 范围原写作 {x, reMin, imMax}，改为 {x, reMin, reMax}；
   8. 零点标记用椭球按 BoxRatios 换算半径，屏幕上呈圆球（原 Sphere 在 y 向被压扁）。 *)

ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];


xi[s_] := 1/2*s*(s - 1)*Pi^(-s/2)*Gamma[s/2]*Zeta[s];

reMin = -4;  reMax = 4;
imMin = -32; imMax = 32;
(* ---- 曲面高度的三种画法（2026-10-06，供比较） ----
   "arctan"：arctan(ξ/0.25)，原图画法；竖轴 −1.3 … 1.3。
   "raw"   ：ξ 本身，不压缩；图示范围内 Re ξ ∈ [−0.07, 0.78]，Im ξ ∈ [−0.41, 0.41]；竖轴 −0.5 … 1，与图 10.1 相同。
   "norm"  ：ξ 除以只依赖 t 的正函数 w(t)（ξ 在临界线上的 Γ 包络），零迹线与零点位置完全不变，
             全段起伏量级一致；但 Re(s) = ±4 附近 ξ/w 可达 ±38，仍须 arctan(·/3) 压缩；竖轴 −1.6 … 1.6。
   零迹线始终由 ξ 本身的 Re ξ = 0、Im ξ = 0 计算，三种画法完全相同。 *)
mode175 = "raw";   (* 定稿（2026-10-06）：不压缩，与图 10.1 一致；另两种画法保留在 makeFig175 中备查 *)
wEnv[t_?NumericQ] := Abs[(1/2 + I t) (-1/2 + I t)]/2 Pi^(-1/4) Abs[Gamma[1/4 + I t/2]];

(* ---- 版式参数（与 ζ、ξ 零迹线图相同） ---- *)
imgW   = 560;
fsTick = 12; fsLab = 13; fsTitle = 13; fsRho = 13; fsLeg = 12;
cjk    = "Songti SC";
cRed   = RGBColor[0.80, 0.02, 0.02];
cBlue  = RGBColor[0.02, 0.10, 0.80];
cGreen = RGBColor[0.00, 0.55, 0.10];
cZero  = RGBColor[1.00, 0.75, 0.00];

(* 本图单独定比例与视点：ξ 的 Re 范围只有 8 个单位，不沿用图 17.1–17.3 的统一比例尺；
   比例与视点取原图程序的值。 *)
boxR    = {1, 2, 1.5};   (* 与原图程序相同 *)
viewPt  = {3.55131, -2.17521, 1.25602}   (* 作者在 Mathematica 中旋转选定（2026-10-05） *);
viewVer = {0, 0, 1};

(* ---- 曲面材质：与零迹线同色相，半透明 ---- *)
redSurf  = Directive[cRed,  Opacity[0.30], Specularity[White, 40]];
blueSurf = Directive[cBlue, Opacity[0.30], Specularity[White, 50]];

(* ---- 零迹线（投影于 z = 0） ---- *)
traceOpts = {Mesh -> {{0}}, PlotPoints -> 250, MaxRecursion -> 6,
   PlotStyle -> None, BoundaryStyle -> None};

reZeroLine = Plot3D[0, {x, reMin, reMax}, {y, imMin, imMax},
   MeshFunctions -> {Function[{x, y, z}, Re[xi[x + I y]]]},
   MeshStyle -> Directive[cRed, AbsoluteThickness[1.2]], Evaluate[traceOpts]];

imZeroLine = Plot3D[0, {x, reMin, reMax}, {y, imMin, imMax},
   MeshFunctions -> {Function[{x, y, z}, Im[xi[x + I y]]]},
   MeshStyle -> Directive[cBlue, AbsoluteThickness[1.2]], Evaluate[traceOpts]];

(* ---- 参考平面 z = 0 ---- *)
refPlane = Graphics3D[{
    EdgeForm[Directive[GrayLevel[0.7], Opacity[0.4], AbsoluteThickness[0.5]]],
    FaceForm[Directive[GrayLevel[0.92], Opacity[0.28]]],
    Polygon[{{reMin, imMin, 0}, {reMax, imMin, 0}, {reMax, imMax, 0}, {reMin, imMax, 0}}]}];

(* ---- 临界线 Re(s) = 1/2（绿色虚线，压在零迹线之上） ---- *)
critLine = Graphics3D[{cGreen, lwThick,
    Line[{{1/2, imMin, 0}, {1/2, imMax, 0}}]}];

zeroT = {14.134725, 21.022040, 25.010858, 30.424876};
rBox  = 0.008;   (* 原 0.018，偏大 *)

(* ---- 图例部件（置于图框下方，样式同零迹线图） ---- *)
legItem[g_, txt_, col_] := Row[{g, Style[txt, fsLeg, col, FontFamily -> cjk]}, " "];
legLine[col_, dash_] := Graphics[{col, AbsoluteThickness[1.6], dash,
     Line[{{0, 0}, {1, 0}}]}, ImageSize -> {26, 8}, PlotRangePadding -> None];
legSurf[col_] := Graphics[{EdgeForm[{col, AbsoluteThickness[0.6]}],
     Directive[col, Opacity[0.30]], Rectangle[{0, 0}, {2, 1}]},
     ImageSize -> {20, 10}, PlotRangePadding -> None];

(* ---- 按画法 m 生成整幅图（曲面高度、竖轴范围、刻度、零点球半径、图例文字随 m 变） ---- *)
makeFig175[m_String] := Module[{val, comp, zLo, zHi, zTk, pr, surfOpts, rePlot, imPlot, rad,
    zeroMarkers, rhoLabels, legTxt, legend, plot},
   (* val：复值（ξ 或 ξ/w）；comp：对实部、虚部分别作用的实函数（压缩或恒等） *)
   {val, comp} = Switch[m,
     "arctan", {Function[s, xi[s]],             Function[r, ArcTan[r/0.25]]},
     "raw",    {Function[s, xi[s]],             Function[r, r]},
     "norm",   {Function[s, xi[s]/wEnv[Im[s]]], Function[r, ArcTan[r/3]]}];
   {zLo, zHi} = Switch[m, "arctan", {-1.3, 1.3}, "raw", {-0.5, 1.0}, "norm", {-1.6, 1.6}];
   zTk = Switch[m, "arctan", {-1, -0.5, 0.5, 1}, "raw", {-0.5, 0.5, 1}, "norm", {-1.5, -1, -0.5, 0.5, 1, 1.5}];
   pr = {{reMin, reMax}, {imMin, imMax}, {zLo, zHi}};
   surfOpts = {Mesh -> None, PlotPoints -> 100, MaxRecursion -> 3,
     PlotRange -> pr, ClippingStyle -> None, Lighting -> "Neutral"};
   rePlot = Plot3D[comp[Re[val[x + I y]]], {x, reMin, reMax}, {y, imMin, imMax},
     PlotStyle -> redSurf, Evaluate[surfOpts]];
   imPlot = Plot3D[comp[Im[val[x + I y]]], {x, reMin, reMax}, {y, imMin, imMax},
     PlotStyle -> blueSurf, Evaluate[surfOpts]];
   (* 非平凡零点（|γ| ≤ 32）：椭球半径按 BoxRatios 换算，屏幕上为圆 *)
   rad = rBox*{(reMax - reMin)/boxR[[1]], (imMax - imMin)/boxR[[2]], (zHi - zLo)/boxR[[3]]};
   zeroMarkers = Graphics3D[{cZero, Specularity[White, 80],
      Table[Ellipsoid[{1/2, t, 0}, rad], {t, Join[zeroT, -zeroT]}]}];
   rhoLabels = Graphics3D[{
      Table[Text[Style[Subscript[Style["ρ", Italic], k], fsRho, Black],
         {1/2, zeroT[[k]], 0.22}], {k, Length[zeroT]}],
      Table[Text[Style[OverBar[Subscript[Style["ρ", Italic], k]], fsRho, Black],
         {1/2, -zeroT[[k]], 0.22}], {k, Length[zeroT]}]}];
   legTxt = Switch[m,
     "arctan", {"Re ξ 曲面，高度 arctan(Re ξ / 0.25)", "Im ξ 曲面，高度 arctan(Im ξ / 0.25)"},
     "raw",    {"Re ξ(s) 曲面", "Im ξ(s) 曲面"},
     "norm",   {"Re ξ 曲面，高度 arctan(Re(ξ/w) / 3)", "Im ξ 曲面，高度 arctan(Im(ξ/w) / 3)"}];
   legend = Column[{
      Row[{legItem[legSurf[cRed], legTxt[[1]], cRed],
        legItem[legSurf[cBlue], legTxt[[2]], cBlue]}, Spacer[14]],
      Row[{
        legItem[legLine[cRed, {}],  "Re ξ = 0", cRed],
        legItem[legLine[cBlue, {}], "Im ξ = 0", cBlue],
        legItem[legLine[cGreen, {}], "临界线 Re(s) = 1/2", cGreen],
        legItem[Graphics[{cZero, EdgeForm[{Black, AbsoluteThickness[0.6]}], Disk[]},
           ImageSize -> 9], "非平凡零点", Black]}, Spacer[14]]},
     Alignment -> Center, Spacings -> 0.4];
   plot = Show[rePlot, imPlot, refPlane, reZeroLine, imZeroLine, critLine,
     zeroMarkers, rhoLabels,
     Boxed -> False, Axes -> True, AxesOrigin -> {0, 0, 0},
     AxesStyle -> Directive[Black, lwMid],
     AxesLabel -> {Style["Re(s)", fsLab, Black], Style["Im(s)", fsLab, Black],
       Style["Re(\[Xi]), Im(\[Xi])", fsLab, Black]},
     Ticks -> {
       Table[{k, Style[ToString[k], fsTick]}, {k, -4, 4, 2}],
       Table[{k, Style[ToString[k], fsTick]}, {k, -30, 30, 10}],
       Table[{k, Style[ToString[k], fsTick]}, {k, zTk}]},
     PlotRange -> pr, BoxRatios -> boxR,
     ViewPoint -> viewPt, ViewVertical -> viewVer,
     ImageSize -> imgW, Background -> None, shrink3D];
   Labeled[plot, legend, Bottom, Spacings -> 0.6]];

fig = makeFig175[mode175];
fig

(* 3D 半透明曲面导出 PDF 时会栅格化；ImageResolution 600 使印刷分辨率约 600 dpi
   （ImageSize 560 pt × 600/72 ≈ 4670 像素宽；排入 0.90\textwidth 后实际约 860 dpi） *)
bookExport["图17.5-xi实虚曲面重叠", fig];

(* ---- 调视点：用鼠标旋转下图，下面一行实时显示当前视点坐标；
        满意后把数值抄到上面的 viewPt。正式出图不需要这一段，可整段注释掉。 ---- *)
vp = viewPt;
Show[First[fig], ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
