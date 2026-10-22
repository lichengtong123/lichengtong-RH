(* ::Package:: *)

(* 来源：mathematica/Gamma-4.nb（作者从备份恢复，2026-10-05）；对应书中 全书图形/6-G模曲面.pdf，图 7.2 *)

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];


(* ============================================================
   |\[CapitalGamma](s)| 模曲面
   递推分带：积分定义域 + 四层向左延拓（共五层着色）
   三轴交于原点，无框式标注
   ============================================================ *)

(* -------- 公共参数 -------- *)
(* Re 下限扩至 -4，以容纳第三、四层延拓带 *)
reMin = -4; reMax = 4;
imMin = -4; imMax = 4;
(* 模 |\[CapitalGamma]| >= 0：竖直轴从 0 起，上端裁剪尖峰 *)
zMin = 0;
zMax = 6;

reRange = {x, reMin, reMax};
imRange = {y, imMin, imMax};

poleColor = RGBColor[0.55, 0.10, 0.05];
labelColor = GrayLevel[0.20];

(* 极点 s=0,-1,...,-5 覆盖四层延拓边界 *)
poleMaxN = 5;
polePositions = Table[{-n, 0}, {n, 0, poleMaxN}];

(* -------- 灰色复平面网格 -------- *)
grayPlane = Graphics3D[{
   Opacity[0.08], GrayLevel[0.5],
   Polygon[{{reMin, imMin, 0}, {reMax, imMin, 0}, {reMax, imMax, 0}, {reMin, imMax, 0}}],
   Opacity[0.12], GrayLevel[0.4], Thickness[0.0005],
   Line[Table[{{x, imMin, 0}, {x, imMax, 0}}, {x, reMin, reMax, 0.5}]],
   Line[Table[{{reMin, y, 0}, {reMax, y, 0}}, {y, imMin, imMax, 0.5}]]
   }];

(* -------- 三条轴线：均过原点 (0,0,0) -------- *)
axisThick = Directive[Black, lwMid];   (* 全书统一：坐标轴黑色 lwMid（原 Thickness[0.0008]） *)
tickW = Directive[Black, lwThin];   (* 刻度线 lwThin（原 Thickness[0.0005]） *)

reAxisLine = Graphics3D[{axisThick, Line[{{reMin - 0.1, 0, 0}, {reMax + 0.3, 0, 0}}]}];
imAxisLine = Graphics3D[{axisThick, Line[{{0, imMin - 0.2, 0}, {0, imMax + 0.3, 0}}]}];
zAxisLine = Graphics3D[{axisThick, Line[{{0, 0, zMin - 0.05}, {0, 0, zMax + 0.3}}]}];

(* -------- Re(s) 轴刻度 -------- *)
sTickObjs = Table[
   {Graphics3D[{tickW, Line[{{xv, 0, 0}, {xv, 0, -0.25}}]}],
    Graphics3D[Text[Style[xv, fsTick, Black], {xv, 0, -0.55}]]},
   {xv, DeleteCases[Range[reMin, reMax, 1], 0]}];
s0Tick = {Graphics3D[{tickW, Line[{{0, 0, 0}, {0, 0, -0.25}}]}]};
reAxisLabel = Graphics3D[Text[Style["Re(s)", fsLab, Black], {reMax + 0.45, 0, 0}]];

(* -------- Im(s) 轴刻度 -------- *)
tTickObjs = Table[
   {Graphics3D[{tickW, Line[{{0, yv, 0}, {-0.12, yv, 0}}]}],
    Graphics3D[Text[Style[yv, fsTick, Black], {-0.30, yv, 0}]]},
   {yv, DeleteCases[Range[imMin, imMax, 1], 0]}];
t0Tick = {Graphics3D[{tickW, Line[{{0, 0, 0}, {-0.12, 0, 0}}]}]};
imAxisLabel = Graphics3D[Text[Style["Im(s)", fsLab, Black], {0, imMax + 0.5, 0}]];

(* -------- z 轴刻度（模值） -------- *)
zTickObjs = Table[
   {Graphics3D[{tickW, Line[{{0, 0, zv}, {-0.12, 0, zv}}]}],
    Graphics3D[Text[Style[zv, fsTick, Black], {-0.32, 0, zv}]]},
   {zv, DeleteCases[Range[Ceiling[zMin], Floor[zMax], 1], 0]}];
z0Tick = {Graphics3D[{tickW, Line[{{0, 0, 0}, {-0.12, 0, 0}}]}]};

(* -------- 原点 -------- *)
originDot = Graphics3D[{Black, PointSize[0.012], Point[{0, 0, 0}]}];
originLabel = Graphics3D[Text[Style["O", fsLab, Black], {-0.28, -0.4, -0.4}]];

(* -------- 极点虚线与小球 -------- *)
poleAnnotations = Graphics3D[{
   poleColor, Opacity[0.50], Dashing[{0.015, 0.01}], Thickness[0.001],
   Table[
    Line[{{polePositions[[i, 1]], 0, zMin}, {polePositions[[i, 1]], 0, zMax}}],
    {i, Length[polePositions]}],
   poleColor,
   Table[Sphere[{polePositions[[i, 1]], 0, 0}, 0.08], {i, Length[polePositions]}]
   }];   (* 图内「极点 s=…」文字已移入图下方图例（2026-10-06，全书统一：图内不写文字） *)

(* -------- 递推公式说明：再向左、贴 +Im 外侧空白区，不挡曲面 -------- *)
formulaLabel = Graphics3D[{}];   (* 递推公式说明已移入图下方图例 *)

(* -------- 递推分带：统一金黄色系，逐层加大明暗/饱和差 --------
   积分定义域 Re(s)>0
   第1层 -1 < Re <= 0
   第2层 -2 < Re <= -1
   第3层 -3 < Re <= -2
   第4层 -4 < Re <= -3
   自右向左：浅亮金 \[RightArrow] 金 \[RightArrow] 深金 \[RightArrow] 暗金棕 \[RightArrow] 深褐金（同色相、对比拉开）
*)
primaryColor = RGBColor[1.00, 0.92, 0.35];      (* 主：浅亮金  Re(s)>0  *)
extension1Color = RGBColor[1.00, 0.78, 0.05];   (* 第1层：标准金 *)
extension2Color = RGBColor[0.92, 0.58, 0.00];   (* 第2层：深金/琥珀 *)
extension3Color = RGBColor[0.72, 0.40, 0.02];   (* 第3层：暗金棕 *)
extension4Color = RGBColor[0.48, 0.26, 0.04];   (* 第4层：深褐金 *)
outerColor = RGBColor[0.32, 0.22, 0.10];        (* Re(s)<=-4：更深褐金示意 *)

colorFuncAbs = Function[{x, y, z},
   Which[
    x > 0, primaryColor,
    -1 < x <= 0, extension1Color,
    -2 < x <= -1, extension2Color,
    -3 < x <= -2, extension3Color,
    -4 < x <= -3, extension4Color,
    True, outerColor
    ]];

(* 图例：再向左（减小 Re）并移到 +Im 外侧空白，避免遮挡模曲面 *)
legendX = 0.2;
legendY = imMax + 0.55;
legendZ = {0.92, 0.84, 0.76, 0.68, 0.60}*zMax;

(* ============================================================
   |\[CapitalGamma](s)| 模曲面
   ============================================================ *)
absPlot = Plot3D[
   Abs[Gamma[x + I y]],
   reRange, imRange,
   RegionFunction -> Function[{x, y, z}, zMin <= z < zMax],
   PlotRange -> {{reMin, reMax}, {imMin, imMax}, {zMin, zMax}},
   (* 主外观：金黄半透明 + 高光 *)
   PlotStyle -> Directive[RGBColor[1.0, 0.84, 0.0], Opacity[0.80], Specularity[White, 30]],
   ColorFunction -> colorFuncAbs,
   ColorFunctionScaling -> False,
   Lighting -> "Neutral",
   Mesh -> 30,
   MeshStyle -> Directive[GrayLevel[0.95], Opacity[0.7]],
   PlotPoints -> 100,
   MaxRecursion -> 4,
   BoundaryStyle -> Directive[White, Opacity[0.9], Thickness[0.0015]],
   ClippingStyle -> None,
   (* 非正整数极点处排除，避免数值爆炸 *)
   Exclusions -> (Element[x, Integers] && y == 0 && x <= 0),
   Axes -> False,
   Boxed -> False
   ];

absPlotFinal = Show[
   absPlot,
   grayPlane,
   poleAnnotations,
   formulaLabel,
   reAxisLine, Sequence @@ Flatten[sTickObjs], Sequence @@ Flatten[s0Tick], reAxisLabel,
   imAxisLine, Sequence @@ Flatten[tTickObjs], Sequence @@ Flatten[t0Tick], imAxisLabel,
   zAxisLine, Sequence @@ Flatten[zTickObjs], Sequence @@ Flatten[z0Tick],
   Graphics3D[Text[Style["|\[CapitalGamma](s)|", fsLab, Black], {0, 0, zMax + 0.55}]],
   originDot, originLabel,
   PlotRange -> {{reMin - 0.3, reMax + 0.6}, {imMin - 0.6, imMax + 1.2}, {zMin - 0.15, zMax + 0.7}},
   BoxRatios -> {1.5, 1, 0.8},
   Boxed -> False,
   Axes -> False,
   ViewPoint -> viewA,
   ImageSize -> imgW,
   Background -> None,
   shrink3D   (* 去掉上方大片白边（2026-10-06） *)
   ];

(* ====== 图例（图下方）：五层着色、极点、递推公式；原图内中文文字一律移到这里 ====== *)
legend72 = bookLegendRows[{
    {{bkSurf[primaryColor], "积分定义域 Re(s) > 0"}, {bkSurf[extension1Color], "第 1 层 −1 < Re(s) ≤ 0"},
     {bkSurf[extension2Color], "第 2 层 −2 < Re(s) ≤ −1"}},
    {{bkSurf[extension3Color], "第 3 层 −3 < Re(s) ≤ −2"}, {bkSurf[extension4Color], "第 4 层 −4 < Re(s) ≤ −3"},
     {bkDisk[poleColor], "极点 s = 0, −1, −2, …"}},
    {{Spacer[0], "递推公式 Γ(s) = Γ(s+1)/s"}}}];
fig72 = Labeled[absPlotFinal, legend72, Bottom, Spacings -> 0.6];

(* ====== 输出并导出 PDF ====== *)
fig72

(* 导出到本目录（mathematica），不影响 全书图形/；原程序写到另一项目目录的导出语句已删去 *)
bookExport["图07.2-G模曲面", fig72];

(* ---- 调视点：用鼠标旋转下图，下面一行实时显示当前视点坐标；
        满意后把数值替换上面 Show 中的 ViewPoint -> viewA ---- *)
vp = viewA;
Show[absPlotFinal, ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]
