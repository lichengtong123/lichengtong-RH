(* ::Package:: *)

(* 来源：mathematica/图Xi实虚连排.nb（作者提供，2026-10-05）；分别导出图 10.1 实部曲面与图 10.2 虚部曲面。 *)

(*========================================================黎曼 \[Xi](s) 实部/虚部\[LongDash]\[LongDash]A4 规格适配与网格强化版 特点：1. 强白色网格 2. 宝石质感 3. 紧凑 A4 布局（无重叠） 叠加：x-y参考平面、细绿色临界线========================================================*)ClearAll["Global`*"];

(* ---- 载入全书共用版式（书图样式.wl） ---- *)
Get[FileNameJoin[{If[$InputFileName =!= "", DirectoryName[$InputFileName], NotebookDirectory[]], "书图样式.wl"}]];


(*--------1. \[Xi](s) 函数定义--------*)

xi[s_]:=1/2*s*(s-1)*Pi^(-s/2)*Gamma[s/2]*Zeta[s];

(*--------2. 绘图参数设定--------*)
reMin=-4;reMax=4;
imMin=-32;imMax=32;
(* 不再作 arctan 压缩（2026-10-06）：直接画 Re ξ、Im ξ。图示范围内 Re ξ ∈ [−0.07, 0.78]，Im ξ ∈ [−0.41, 0.41]，
   与相邻图 10.3 的 |ξ|（≤ 0.79）用同一线性尺度 *)
zLo=-0.5;zHi=1.0;
commonViewPoint={2.8,-2.8,1.8};
commonViewVertical={0,0,1};

(*整体偏移量*)
shiftX=0;(*原 0.3：曲面右移 0.3 而 Re 刻度与 Im 轴未随之移动，刻度偏差 0.3，Im 轴落在 Re(s) = −0.3 处；改为 0（2026-10-06）*)(*--------3. 材质定义--------*)redGem=Directive[RGBColor[0.47,0.18,0.18],Opacity[0.96],Specularity[White,15]];
blueGem=Directive[RGBColor[0.12,0.28,0.55],Opacity[0.96],(*深蓝*)Specularity[White,15]];
(*降低网格灰度：GrayLevel 值越小越暗，越大越亮*)

commonMeshStyle=Directive[GrayLevel[0.80],Opacity[0.6],Thickness[0.0005]];

(*--------4. 绘图核心函数（直接对坐标偏移）--------*)

(*左图：Re(\[Xi])*)

rePlot=Plot3D[Re[xi[(x-shiftX)+I y]],{x,reMin+shiftX,reMax+shiftX},{y,imMin,imMax},PlotStyle->redGem,Mesh->25,MeshStyle->commonMeshStyle,PlotPoints->100,MaxRecursion->3,PlotRange->{{reMin+shiftX,reMax+shiftX},{imMin,imMax},{zLo,zHi}},ClippingStyle->None,AxesLabel->{Style["Re(s)",Italic,fsLab],Style["Im(s)",Italic,fsLab],Style["Re(\[Xi])",Italic,fsLab]},Boxed->False,Axes->True,AxesOrigin->{0,0,0},AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},AxesStyle->Directive[Black,lwMid],Ticks->{Table[{x,x},{x,-4,4,2}],Table[{y,y},{y,-30,30,10}],{{-0.5,-0.5},{0.5,0.5},{1,1}}},TicksStyle->Directive[Black,FontSize->fsTick],BoxRatios->{1,2,2},ViewPoint->commonViewPoint,ViewVertical->commonViewVertical,Lighting->"Neutral",ImagePadding->All(* 原 {{50,20},{40,20}}：缩到印刷尺寸后上下的轴标签、刻度被裁掉（2026-10-06） *)];

(*右图：Im(\[Xi])*)

imPlot=Plot3D[Im[xi[(x-shiftX)+I y]],{x,reMin+shiftX,reMax+shiftX},{y,imMin,imMax},PlotStyle->blueGem,Mesh->25,MeshStyle->commonMeshStyle,PlotPoints->100,MaxRecursion->3,PlotRange->{{reMin+shiftX,reMax+shiftX},{imMin,imMax},{zLo,zHi}},ClippingStyle->None,AxesLabel->{Style["Re(s)",Italic,fsLab],Style["Im(s)",Italic,fsLab],Style["Im(\[Xi])",Italic,fsLab]},Boxed->False,Axes->True,AxesOrigin->{0,0,0},AxesEdge->{{-1,-1},{-1,-1},{-1,-1}},AxesStyle->Directive[Black,lwMid],Ticks->{Table[{x,x},{x,-4,4,2}],Table[{y,y},{y,-30,30,10}],{{-0.5,-0.5},{0.5,0.5},{1,1}}},TicksStyle->Directive[Black,FontSize->fsTick],BoxRatios->{1,2,2},ViewPoint->commonViewPoint,ViewVertical->commonViewVertical,Lighting->"Neutral",ImagePadding->All(* 原 {{50,20},{40,20}}：缩到印刷尺寸后上下的轴标签、刻度被裁掉（2026-10-06） *)];

(*--------4b.叠加元素--------*)

(*① 参考平面：z=0 的 x-y 平面，半透明白灰色（也偏移）*)

refPlane=Graphics3D[{EdgeForm[Directive[GrayLevel[0.7],Opacity[0.4],lwThin]],FaceForm[Directive[GrayLevel[0.92],Opacity[0.30]]],Polygon[{{reMin+shiftX,imMin,0},{reMax+shiftX,imMin,0},{reMax+shiftX,imMax,0},{reMin+shiftX,imMax,0}}]}];

(*② 临界带 0<Re(s)<1：半透明绿色浮面（也偏移）*)

critStrip=Graphics3D[{Opacity[0.20],RGBColor[0.0,0.75,0.2],Polygon[{{0+shiftX,imMin,0},{1+shiftX,imMin,0},{1+shiftX,imMax,0},{0+shiftX,imMax,0}}]}];

(*③ 临界线 Re(s)=1/2：画在参考平面上（z=0），不再跟随曲面*)

critLineRe=ParametricPlot3D[{1/2+shiftX,y,0},{y,imMin,imMax},PlotStyle->Directive[Green,Thickness[0.0005],Opacity[0.9]],MaxRecursion->4,PlotPoints->300];

critLineIm=ParametricPlot3D[{1/2+shiftX,y,0},{y,imMin,imMax},PlotStyle->Directive[Green,Thickness[0.0005],Opacity[0.9]],MaxRecursion->4,PlotPoints->300];

(*④ 非平凡零点：红色小球（画在参考平面上 z=0）*)

zeroT={14.134725,21.022040,25.010858,30.424876,32.935062};
zeroPointsRe=Table[{1/2+shiftX,t,0},{t,zeroT}];
zeroPointsIm=Table[{1/2+shiftX,t,0},{t,zeroT}];
zeroPointsReNeg=Table[{1/2+shiftX,-t,0},{t,zeroT}];
zeroPointsImNeg=Table[{1/2+shiftX,-t,0},{t,zeroT}];

zeroSpheresRe=Graphics3D[{RGBColor[0.85,0.10,0.10],Specularity[White,90],Sphere[#,0.04]&/@zeroPointsRe,Sphere[#,0.04]&/@zeroPointsReNeg}];

zeroSpheresIm=Graphics3D[{RGBColor[0.85,0.10,0.10],Specularity[White,90],Sphere[#,0.04]&/@zeroPointsIm,Sphere[#,0.04]&/@zeroPointsImNeg}];

(*⑤ 零点标注（放在参考平面上方一点）*)

zeroLabelsRe=Graphics3D[{Text[Style["14.13",9,Bold,RGBColor[0.85,0.10,0.10]],{1/2+shiftX,zeroT[[1]],0.12}],Text[Style["21.02",9,Bold,RGBColor[0.85,0.10,0.10]],{1/2+shiftX,zeroT[[2]],0.12}],Text[Style["25.01",9,Bold,RGBColor[0.85,0.10,0.10]],{1/2+shiftX,zeroT[[3]],0.12}]}];

zeroLabelsIm=Graphics3D[{Text[Style["14.13",9,Bold,RGBColor[0.85,0.10,0.10]],{1/2+shiftX,zeroT[[1]],0.12}],Text[Style["21.02",9,Bold,RGBColor[0.85,0.10,0.10]],{1/2+shiftX,zeroT[[2]],0.12}],Text[Style["25.01",9,Bold,RGBColor[0.85,0.10,0.10]],{1/2+shiftX,zeroT[[3]],0.12}]}];

(*⑥ 临界带和临界线标注（放在参考平面上方一点）*)

annotations=Graphics3D[{Text[Style["临界带 0<Re(s)<1",10,Bold,RGBColor[0.0,0.50,0.2]],{0.5+shiftX,imMin+3,0.10}],Text[Style["临界线 Re(s)=1/2",10,Bold,Green],{0.5+shiftX,imMax-3,0.10}]}];

(*手动绘制坐标轴线（确保所有轴可见）*)

axesLines=Graphics3D[{{Black,lwMid,Line[{{0,0,0},{4.5,0,0}}]},(*Re(s) 轴*){Black,lwMid,Line[{{0,-33,0},{0,33,0}}]},(*Im(s) 轴*){Black,lwMid,Line[{{0,0,zLo-0.05},{0,0,zHi+0.05}}]}  (*z 轴*)}];

(*--------5. 最终组装--------*)
(* ---- 统一画法（2026-10-06）：临界线、临界带、零点改用 书图样式.wl 中的函数；文字说明移入图例 ---- *)
pr101={{reMin+shiftX,reMax+shiftX},{imMin,imMax},{zLo,zHi}};box101={1,2,2};
critStrip=Graphics3D[Translate[stripMark3D[{imMin,imMax}],{shiftX,0,0}]];
critLineRe=critLineIm=Graphics3D[Translate[critLine3D[{imMin,imMax}],{shiftX,0,0}]];
zeroSpheresRe=zeroSpheresIm=Graphics3D[zeroBalls[Select[Join[zeroPointsRe,zeroPointsReNeg],Abs[#[[2]]]<=imMax&],pr101,box101]];
annotations=Graphics3D[{}];
(* 两图使用相同范围、视点及输出宽度；每幅单独保留完整图例。 *)
finalRe=Show[rePlot,refPlane,critStrip,critLineRe,zeroSpheresRe,annotations,axesLines,
  PlotRange->pr101,ImageSize->imgW,shrink3D];
finalIm=Show[imPlot,refPlane,critStrip,critLineIm,zeroSpheresIm,annotations,axesLines,
  PlotRange->pr101,ImageSize->imgW,shrink3D];
finalReDisplay=Labeled[finalRe,
  bookLegendRows[{{{bkSurf[RGBColor[0.47,0.18,0.18]],"Re ξ(s) 曲面"},"crit"},{"strip","zero"}}],
  Bottom,Spacings->0.6];
finalImDisplay=Labeled[finalIm,
  bookLegendRows[{{{bkSurf[RGBColor[0.12,0.28,0.55]],"Im ξ(s) 曲面"},"crit"},{"strip","zero"}}],
  Bottom,Spacings->0.6];
Column[{finalReDisplay,finalImDisplay},Alignment->Center,Spacings->2]

(* 导出到本目录（mathematica），不影响 全书图形/ *)
bookExport["图10.1-xi实部曲面", finalReDisplay];
bookExport["图10.2-xi虚部曲面", finalImDisplay];

(* ---- 调视点：两幅子图共用 commonViewPoint；用鼠标旋转下图（实部），下面一行实时显示视点坐标，
        满意后把数值写回上面的 commonViewPoint ---- *)
vp = commonViewPoint;
Show[rePlot, refPlane, critStrip, critLineRe, zeroSpheresRe, annotations, axesLines,
  PlotRange -> {{reMin + shiftX, reMax + shiftX}, {imMin, imMax}, {zLo, zHi}},
  ViewPoint -> Dynamic[vp], ImageSize -> imgW]
Dynamic[vp]



