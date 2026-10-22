(* ::Package:: *)

(* 来源：全书图形/li函数图形.nb 中第 34 行起的输入单元；对应书中 全书图形/13-li模曲面.pdf *)

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];

viewLi = {0.788403, -3.14653, 0.963199};   (* 作者在 Mathematica 中旋转选定（2026-10-05） *)



(* |li(z)| modulus surface on the book's domain (定义 13.4.1):
   Omega = C \ ((-Infinity,0] U [1,+Infinity)), normalized by the real integral on 0<t<1.
   Mathematica's LogIntegral[z] uses a different branch (cut (-Infinity,1], continuous across x>1).
   The book's branch is  liOmega[z] = LogIntegral[z] - I Pi Sign[Im z]  (2026-10-07):
     - continuous across (0,1); jump across (1,+Infinity);
     - boundary values on x>1:  li(x +- i0) = li(x) -+ I Pi, modulus >= Pi;
     - no zero inside Omega; |li| -> 0 only as z -> 0 (a boundary point).
   The Soldner zero mu belongs to the real principal value li(x), not to this surface. *)
(* gold yellow matches zeta/Gamma modulus surfaces in the book *)

ClearAll[liOmega, liAbs, plotLiModulus, plotLiContour, plotLiRealAxis, plotLiVsLiOffset, LiOffset];

liOmega[z_?NumericQ] := LogIntegral[z] - I Pi Sign[Im[z]];
liAbs[x_?NumericQ, y_?NumericQ] := Abs[liOmega[x + I y]];
LiOffset[x_?NumericQ] := LogIntegral[x] - LogIntegral[2];

(* Soldner constant: unique zero of the REAL principal value li(x) on (1,+Infinity); not a zero of liOmega *)
soldnerMu = 1.4513692348833811;

(* 分支自检（2026-10-07）：应输出 {0, -3.14159 I, 3.14159}
   第 1 项：穿过 (0,1) 连续；第 2 项：li(mu + i0) = li(mu) - I Pi = -I Pi；第 3 项：该处模为 Pi，不为 0 *)
Print[{Chop[liOmega[0.5 + 10.^-12 I] - liOmega[0.5 - 10.^-12 I], 10^-6],
       Chop[liOmega[soldnerMu + 10.^-12 I], 10^-6],
       Abs[liOmega[soldnerMu + 10.^-12 I]]}];

plotLiModulus[xMin_ : -2, xMax_ : 4, yMin_ : -3, yMax_ : 3, n_ : 80, zMax_ : 8] :=
  Module[{surf, marks},
   surf = Plot3D[liAbs[x, y], {x, xMin, xMax}, {y, yMin, yMax},
     PlotPoints -> n, MaxRecursion -> 3,
     PlotRange -> {{xMin, xMax}, {yMin, yMax}, {0, zMax}},
     Axes -> True, Boxed -> False, AxesOrigin -> {0, 0, 0},
     AxesStyle -> Directive[Black, lwMid],
     AxesLabel -> {Style["Re(z)", fsLab, Black], Style["Im(z)", fsLab, Black], Style["|li(z)|", fsLab, Black]},
     TicksStyle -> Directive[Black, FontSize -> fsTick],   (* 原为默认小字号（2026-10-06） *)
     PlotStyle -> Directive[RGBColor[1.0, 0.84, 0.0], Opacity[0.80], Specularity[White, 30]],
     MeshFunctions -> {#1 &, #2 &, #3 &},
     Mesh -> {28, 28, 16},
     MeshStyle -> {
       Directive[GrayLevel[0.35], Opacity[0.90], AbsoluteThickness[0.6]],
       Directive[GrayLevel[0.35], Opacity[0.90], AbsoluteThickness[0.6]],
       Directive[GrayLevel[0.25], Opacity[0.95], AbsoluteThickness[0.7]]
     },
     Lighting -> "Neutral",
     Exclusions -> {y == 0 && x >= 1, y == 0 && x <= 0},   (* 两条割线（2026-10-07） *) BoxRatios -> {1, 1, 0.55}, ViewPoint -> viewLi,
     ImageSize -> imgW];
   (* marks（2026-10-07 第二版）：
      割线两侧函数值互为共轭（li(conj z) = conj li(z)），模的边界值相等，图中作拼接显示；
      红色实线标示割线两侧共同的模边界值，不表示原分支在割线上取值，也不预设拼接处处不光滑。
      x>1 处拼接高度为 Sqrt[li(x)^2 + Pi^2] >= Pi。
      支点 z=1：红球 + 竖线；边界点 z=0：蓝球（|li|->0，不是零点）。小球用 ballRad 保证各向等大。
      Soldner 零点不在此曲面上，已移到实主值图（正文图 13.1）。 *)
   marks = Graphics3D[{
     Directive[Red, AbsoluteThickness[1.8]],
     Line[Table[{x, 0, Abs[liOmega[x + 10.^-9 I]]}, {x, 1.001, xMax, 0.01}]],
     Line[Table[{x, 0, Abs[liOmega[x + 10.^-9 I]]}, {x, xMin, -0.001, 0.01}]],
     Directive[Red, Opacity[0.7], AbsoluteThickness[1.0]],
     Line[{{1, 0, 0}, {1, 0, zMax}}],
     Specularity[White, 20],
     Red, Ellipsoid[{1, 0, 0}, ballRad[{{xMin, xMax}, {yMin, yMax}, {0, zMax}}, {1, 1, 0.55}, 0.014]],
     Blue, Ellipsoid[{0, 0, 0}, ballRad[{{xMin, xMax}, {yMin, yMax}, {0, zMax}}, {1, 1, 0.55}, 0.014]]
     (* 图内文字标注放在图下图例 legend133 *)
     }];
   Show[surf, marks,
    PlotRange -> {{xMin, xMax}, {yMin, yMax}, {0, zMax}},
    Boxed -> False, Axes -> True, AxesOrigin -> {0, 0, 0},
    BoxRatios -> {1, 1, 0.55}, ViewPoint -> viewLi, ImageSize -> imgW, shrink3D]
   ];

plotLiContour[xMin_ : -2, xMax_ : 4, yMin_ : -3, yMax_ : 3] :=
  Module[{mu = soldnerMu},
   ContourPlot[liAbs[x, y], {x, xMin, xMax}, {y, yMin, yMax},
     PlotPoints -> 100, Contours -> 20,
     ColorFunction -> (Blend[{RGBColor[1.0, 0.95, 0.55], RGBColor[1.0, 0.84, 0.0], RGBColor[0.72, 0.40, 0.02]}, #] &),
     FrameLabel -> {"Re z", "Im z"},
     Epilog -> {
       Red, Thick, Line[{{1, 0}, {xMax, 0}}], Line[{{xMin, 0}, {0, 0}}],
       PointSize[0.028], Point[{1, 0}], Blue, Point[{0, 0}],
       Text[Style["支点 z=1", fsAnn, Red, Bold],
        {1, -0.22 (yMax - yMin)}, {0, 1}]
       }, ImageSize -> 480]
   ];

(* 实主值 li(x) 与 Omega 分支在割线两侧的边界模 |li(x+-i0)| = Sqrt[li(x)^2 + Pi^2] *)
plotLiRealAxis[xMin_ : 1.05, xMax_ : 6] :=
  Plot[{LogIntegral[x], Abs[liOmega[x + 10.^-8 I]], Abs[liOmega[x - 10.^-8 I]]},
    {x, xMin, xMax},
    PlotLegends -> {"li(x)（实主值）", "|li(x+i0)|", "|li(x-i0)|"},
    AxesLabel -> {"x", None}, ImageSize -> 480];

plotLiVsLiOffset[xMin_ : 1.1, xMax_ : 20] :=
  Plot[{LogIntegral[x], LiOffset[x]}, {x, xMin, xMax},
    PlotLegends -> {"li(x)", "Li(x)=li(x)-li(2)"},
    AxesLabel -> {"x", None}, ImageSize -> 480];
(* 书中图 13.3 为默认参数的输出；说明文字放在图下图例中，图内不标字 *)
plot133 = plotLiModulus[];
legend133 = bookLegendRows[{
    {{bkDisk[Red], "支点 z = 1，|li(z)| \[Rule] \[Infinity]"},
     {bkDisk[Blue], "边界点 z = 0，|li(z)| \[Rule] 0"}},
    {{bkLine[Red], "割线两侧模边界值的拼接显示；x > 1 处 |li(x ± i0)| = √(li(x)² + π²) ≥ π"}}}];
fig = Labeled[plot133, legend133, Bottom, Spacings -> 0.6];
fig

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图13.3-li模曲面", fig];

(* ---- 调视点：用鼠标旋转下图，下面一行实时显示当前视点坐标；
        满意后把数值抄到上面的 viewLi ---- *)
vp = viewLi;
Show[plot133, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
