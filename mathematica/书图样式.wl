(* ::Package:: *)

(* 书图样式.wl —— 全书 Mathematica 图形的共用版式参数
   各图形程序在 ClearAll 之后以 Get 载入本文件；改全书风格只改这里。 *)

(* ---- 视角 ----
   viewA：标准视角（右前上方），用于大多数 3D 图；
   viewB：左侧低视角，用于第 9 章「向左延拓」系列（图 5.1、9.1–9.4、9.7），
          便于看清新延拓进来的左侧区域与负实轴上的平凡零点。 *)
viewA    = {2.4, -3.0, 1.6};
viewB    = {-4.6, -4.0, 2.6};   (* 原 {-6.2,-2.5,0.8} 过低过平，图形扁宽；2026-10-05 改 *)
viewVert = {0, 0, 1};
(* viewC：第 17 章视角（自 +Re 一侧斜上方看）。Im 轴横贯画面、左负右正，Re 负方向在画面上方，
   与图 17.4、17.6 零迹线图（纵轴 Re 正方向向下）的版面方向一致；
   临界带在左侧「峭壁」之前，不被遮挡；长度与 viewA 相同（≈4.2），透视强度一致。 *)
viewC    = {3.48438, -0.727659, 2.1563};   (* 作者在 Mathematica 中旋转选定（2026-10-05） *)

(* ---- 盒子比例 ----
   Im 方向固定为 64 个单位（-32..32）对应盒长 2；Re 方向每 12 个单位对应盒长 1
   （相对 Im 方向放大约 2.7 倍，与原图观感相近）。
   同一比例尺下，Re 范围不同的图（如截断模曲面与延拓后的模曲面）可以直接对照。 *)
boxH = 0.8;
bookBox[{x1_, x2_}, h_ : boxH] := {(x2 - x1)/12, 2, h};
(* 第 9 章延拓系列（viewB 组：图 5.1、9.1–9.4、9.7）专用比例：
   这组图 Re 范围窄（8 个单位左右），按 bookBox 会被压成窄条，故 Re 方向每 1 个单位取盒长 0.15、高度取 1.1。 *)
bookBoxB[{x1_, x2_}, h_ : 1.1] := {0.15 (x2 - x1), 2, h};

(* ---- 3D 图去白边（2026-10-06）----
   Graphics3D 默认按整个盒子投影留出画框，视角较高时成近正方形，上下大片空白、图例离图形远。
   ShrinkWrap 让画框紧贴实际画出的内容（曲面、轴线、文字），宽扁的曲面得到宽扁的画框。
   用法：在最终 Show[...] 中加入 shrink3D。 *)
shrink3D = Method -> {"ShrinkWrap" -> True};

(* ---- 版式（与图 17.4、17.6 零迹线图一致） ---- *)
imgW   = 560;
fsTick = 12; fsLab = 13; fsTitle = 13; fsRho = 13; fsLeg = 12;
cjk    = "Songti SC";
cRed   = RGBColor[0.80, 0.02, 0.02];
cBlue  = RGBColor[0.02, 0.10, 0.80];
cGreen = RGBColor[0.00, 0.55, 0.10];
cZero  = RGBColor[1.00, 0.75, 0.00];
cStrip = RGBColor[0.60, 0.40, 0.20];   (* 临界带边界：棕色虚线 *)
fsAnn  = 11;                           (* 图内注记（临界带、零点标注等），印出约 7.7 pt *)

(* ---- 线宽（绝对值，pt；缩放 0.70 印出后：0.35 / 0.56 / 0.84 / 1.26 pt） ---- *)
lwThin  = AbsoluteThickness[0.5];      (* 刻度线 *)
lwMid   = AbsoluteThickness[0.8];      (* 坐标轴、零迹线、临界带边界 *)
lwThick = AbsoluteThickness[1.2];      (* 临界线 *)
lwHeavy = AbsoluteThickness[1.8];
dashStrip = AbsoluteDashing[{}];       (* 临界带边界为实线；原为 {}，放在 Directive 中无效，导致图 17.1、17.2 出现粉红错误底色 *)

(* ---- 零点小球：按盒子比例换算成椭球，屏幕上呈圆形 ----
   pr 为 Show 的 PlotRange，box 为 BoxRatios，r 为相对盒长的半径 *)
ballRad[pr_, box_, r_ : 0.012] := r*{(pr[[1, 2]] - pr[[1, 1]])/box[[1]],
    (pr[[2, 2]] - pr[[2, 1]])/box[[2]], (pr[[3, 2]] - pr[[3, 1]])/box[[3]]};
zeroBalls[pts_, pr_, box_, r_ : 0.008] := {cZero, Specularity[White, 60],
    Ellipsoid[#, ballRad[pr, box, r]] & /@ pts};

(* ---- 非平凡零点（|γ| ≤ 32），6 位 ---- *)
zeroT = {14.134725, 21.022040, 25.010858, 30.424876};

(* ---- 导出：写到本目录（mathematica），不触动 全书图形/ ---- *)
bookDir = If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]];
bookExport[name_String, g_] :=
  Export[FileNameJoin[{bookDir, name <> ".pdf"}], g, ImageResolution -> 600];

(* ================= 临界线、临界带、零点的统一画法与图例（2026-10-06） =================
   规则：图中不写文字标注，说明一律放在图下方的图例中；图内不放标题（由 LaTeX 图题说明）。
     临界线 Re(s) = 1/2 ：绿色实线 cGreen、lwThick
     临界带 0 < Re(s) < 1：两条棕色实线边界 cStrip、lwMid（不填充）
     非平凡零点         ：金色小球 cZero（zeroBalls，半径 0.008 盒长）
     平凡零点           ：紫色小球 cTriv（trivialBalls，同样大小）
     极点 s = 1         ：黑色小球（poleBall） *)
cTriv = RGBColor[0.55, 0.00, 0.75];
critLine3D[{y1_, y2_}] := {cGreen, lwThick, Line[{{1/2, y1, 0}, {1/2, y2, 0}}]};
stripMark3D[{y1_, y2_}] := {cStrip, lwMid, Line[{{0, y1, 0}, {0, y2, 0}}], Line[{{1, y1, 0}, {1, y2, 0}}]};
trivialBalls[pts_, pr_, box_, r_ : 0.008] := {cTriv, Specularity[White, 60], Ellipsoid[#, ballRad[pr, box, r]] & /@ pts};
poleBall[p_, pr_, box_, r_ : 0.008] := {Black, Ellipsoid[p, ballRad[pr, box, r]]};

bkItem[g_, txt_] := Row[{g, Style[txt, fsLeg, Black, FontFamily -> cjk]}, " "];
bkLine[col_, lw_ : 1.6] := Graphics[{col, AbsoluteThickness[lw], Line[{{0, 0}, {1, 0}}]}, ImageSize -> {26, 8}, PlotRangePadding -> None];
bkDisk[col_] := Graphics[{col, EdgeForm[{Black, AbsoluteThickness[0.5]}], Disk[]}, ImageSize -> 8];
bkSurf[col_] := Graphics[{EdgeForm[{GrayLevel[0.4], AbsoluteThickness[0.5]}], col, Rectangle[{0, 0}, {2, 1}]}, ImageSize -> {20, 10}, PlotRangePadding -> None];
bookLegendItem["crit"]  := bkItem[bkLine[cGreen], "临界线 Re(s) = 1/2"];
bookLegendItem["strip"] := bkItem[bkLine[cStrip, 1.0], "临界带边界 Re(s) = 0, 1"];
bookLegendItem["zero"]  := bkItem[bkDisk[cZero], "非平凡零点"];
bookLegendItem["triv"]  := bkItem[bkDisk[cTriv], "平凡零点 s = −2, −4, …"];
bookLegendItem["pole"]  := bkItem[bkDisk[Black], "极点 s = 1"];
bookLegendItem[{g_, txt_String}] := bkItem[g, txt];
bookLegend[keys_List] := Row[bookLegendItem /@ keys, Spacer[12]];
bookLegendRows[rows_List] := Column[bookLegend /@ rows, Alignment -> Center, Spacings -> 0.4];

(* ---- 第 17 章 3D 图（17.1–17.3）的比例：与零迹线平面图 17.4 相同 ----
   17.4 的画面：Im 方向 64 个单位为宽，Re 方向 12.5 个单位为高，AspectRatio 0.46。
   3D 盒子里 Im 方向盒长取 2，则 Re 方向每单位盒长 = 2 × 0.46 / 12.5，Re 与 Im 的相对比例与 17.4 一致。 *)
yLen17 = 3;   (* Im 方向盒长：原为 2，加长到 3 使 17.1–17.3 画面横向展开，接近 17.4 的长条版面（2026-10-06） *)
box17[{x1_, x2_}, h_ : boxH] := {yLen17*0.46*(x2 - x1)/12.5, yLen17, h};
re17 = {-8.5, 4};      (* 与图 17.4 的 Re 范围相同：平凡零点 −2 … −8 均在图内 *)
reTicks17 = {-8, -6, -4, -2, 2, 4};
