# gist_scenes_train.cdc -- native training data (phases-only).
# Each module: c0..c2 evidence phases, c3 the teacher label pole.
# Labels computed BY the C runtime: converged (40x0.25) fixed-
# pyramid singular. Deterministic generator seed 101.
field scenes-train dt=0.125 gain=1.0 deadband=0.5

module s0 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s0.c0 module=s0 theta=1.452591347262 amplitude=1.0 omega=0.0
cell s0.c1 module=s0 theta=1.394943308182 amplitude=1.0 omega=0.0
cell s0.c2 module=s0 theta=0.212535562392 amplitude=1.0 omega=0.0
cell s0.c3 module=s0 theta=1.570796326795 amplitude=1.0 omega=0.0
module s1 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s1.c0 module=s1 theta=0.955035875928 amplitude=1.0 omega=0.0
cell s1.c1 module=s1 theta=1.662998429081 amplitude=1.0 omega=0.0
cell s1.c2 module=s1 theta=0.326510014235 amplitude=1.0 omega=0.0
cell s1.c3 module=s1 theta=1.570796326795 amplitude=1.0 omega=0.0
module s2 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s2.c0 module=s2 theta=1.650837882501 amplitude=1.0 omega=0.0
cell s2.c1 module=s2 theta=1.436279020253 amplitude=1.0 omega=0.0
cell s2.c2 module=s2 theta=0.051402468278 amplitude=1.0 omega=0.0
cell s2.c3 module=s2 theta=1.570796326795 amplitude=1.0 omega=0.0
module s3 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s3.c0 module=s3 theta=1.822401549308 amplitude=1.0 omega=0.0
cell s3.c1 module=s3 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s3.c2 module=s3 theta=0.033079184120 amplitude=1.0 omega=0.0
cell s3.c3 module=s3 theta=1.570796326795 amplitude=1.0 omega=0.0
module s4 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s4.c0 module=s4 theta=1.352851933582 amplitude=1.0 omega=0.0
cell s4.c1 module=s4 theta=1.867654682986 amplitude=1.0 omega=0.0
cell s4.c2 module=s4 theta=0.044351826475 amplitude=1.0 omega=0.0
cell s4.c3 module=s4 theta=1.570796326795 amplitude=1.0 omega=0.0
module s5 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s5.c0 module=s5 theta=1.687858727263 amplitude=1.0 omega=0.0
cell s5.c1 module=s5 theta=1.427444022477 amplitude=1.0 omega=0.0
cell s5.c2 module=s5 theta=3.123490578777 amplitude=1.0 omega=0.0
cell s5.c3 module=s5 theta=1.570796326795 amplitude=1.0 omega=0.0
module s6 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s6.c0 module=s6 theta=0.171993919819 amplitude=1.0 omega=0.0
cell s6.c1 module=s6 theta=2.990212534059 amplitude=1.0 omega=0.0
cell s6.c2 module=s6 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s6.c3 module=s6 theta=1.570796326795 amplitude=1.0 omega=0.0
module s7 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s7.c0 module=s7 theta=2.628116415418 amplitude=1.0 omega=0.0
cell s7.c1 module=s7 theta=0.287802041803 amplitude=1.0 omega=0.0
cell s7.c2 module=s7 theta=2.719909471615 amplitude=1.0 omega=0.0
cell s7.c3 module=s7 theta=1.570796326795 amplitude=1.0 omega=0.0
module s8 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s8.c0 module=s8 theta=3.137107739592 amplitude=1.0 omega=0.0
cell s8.c1 module=s8 theta=0.134868751149 amplitude=1.0 omega=0.0
cell s8.c2 module=s8 theta=0.113197462881 amplitude=1.0 omega=0.0
cell s8.c3 module=s8 theta=0.000000000000 amplitude=1.0 omega=0.0
module s9 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s9.c0 module=s9 theta=0.197049035399 amplitude=1.0 omega=0.0
cell s9.c1 module=s9 theta=0.013311975838 amplitude=1.0 omega=0.0
cell s9.c2 module=s9 theta=1.698948005108 amplitude=1.0 omega=0.0
cell s9.c3 module=s9 theta=0.000000000000 amplitude=1.0 omega=0.0
module s10 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s10.c0 module=s10 theta=2.521274673710 amplitude=1.0 omega=0.0
cell s10.c1 module=s10 theta=1.763543322824 amplitude=1.0 omega=0.0
cell s10.c2 module=s10 theta=1.474198017676 amplitude=1.0 omega=0.0
cell s10.c3 module=s10 theta=1.570796326795 amplitude=1.0 omega=0.0
module s11 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s11.c0 module=s11 theta=1.745864354950 amplitude=1.0 omega=0.0
cell s11.c1 module=s11 theta=1.528479693186 amplitude=1.0 omega=0.0
cell s11.c2 module=s11 theta=1.615711045622 amplitude=1.0 omega=0.0
cell s11.c3 module=s11 theta=1.570796326795 amplitude=1.0 omega=0.0
module s12 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s12.c0 module=s12 theta=0.086733209175 amplitude=1.0 omega=0.0
cell s12.c1 module=s12 theta=3.089288478403 amplitude=1.0 omega=0.0
cell s12.c2 module=s12 theta=2.523498132480 amplitude=1.0 omega=0.0
cell s12.c3 module=s12 theta=3.141592653590 amplitude=1.0 omega=0.0
module s13 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s13.c0 module=s13 theta=3.019665666477 amplitude=1.0 omega=0.0
cell s13.c1 module=s13 theta=2.956331740326 amplitude=1.0 omega=0.0
cell s13.c2 module=s13 theta=1.602981525140 amplitude=1.0 omega=0.0
cell s13.c3 module=s13 theta=3.141592653590 amplitude=1.0 omega=0.0
module s14 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s14.c0 module=s14 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s14.c1 module=s14 theta=2.892194208825 amplitude=1.0 omega=0.0
cell s14.c2 module=s14 theta=0.287488953836 amplitude=1.0 omega=0.0
cell s14.c3 module=s14 theta=1.570796326795 amplitude=1.0 omega=0.0
module s15 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s15.c0 module=s15 theta=1.648568674758 amplitude=1.0 omega=0.0
cell s15.c1 module=s15 theta=0.320970846365 amplitude=1.0 omega=0.0
cell s15.c2 module=s15 theta=1.271147614754 amplitude=1.0 omega=0.0
cell s15.c3 module=s15 theta=0.000000000000 amplitude=1.0 omega=0.0
module s16 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s16.c0 module=s16 theta=1.319363173387 amplitude=1.0 omega=0.0
cell s16.c1 module=s16 theta=1.019037198432 amplitude=1.0 omega=0.0
cell s16.c2 module=s16 theta=1.865477754630 amplitude=1.0 omega=0.0
cell s16.c3 module=s16 theta=1.570796326795 amplitude=1.0 omega=0.0
module s17 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s17.c0 module=s17 theta=2.899598571501 amplitude=1.0 omega=0.0
cell s17.c1 module=s17 theta=2.259377491418 amplitude=1.0 omega=0.0
cell s17.c2 module=s17 theta=0.263385560843 amplitude=1.0 omega=0.0
cell s17.c3 module=s17 theta=1.570796326795 amplitude=1.0 omega=0.0
module s18 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s18.c0 module=s18 theta=1.630800514868 amplitude=1.0 omega=0.0
cell s18.c1 module=s18 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s18.c2 module=s18 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s18.c3 module=s18 theta=1.570796326795 amplitude=1.0 omega=0.0
module s19 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s19.c0 module=s19 theta=1.552516938674 amplitude=1.0 omega=0.0
cell s19.c1 module=s19 theta=0.281503064942 amplitude=1.0 omega=0.0
cell s19.c2 module=s19 theta=3.140275672288 amplitude=1.0 omega=0.0
cell s19.c3 module=s19 theta=1.570796326795 amplitude=1.0 omega=0.0
module s20 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s20.c0 module=s20 theta=0.627262919200 amplitude=1.0 omega=0.0
cell s20.c1 module=s20 theta=2.058928087676 amplitude=1.0 omega=0.0
cell s20.c2 module=s20 theta=2.939468862691 amplitude=1.0 omega=0.0
cell s20.c3 module=s20 theta=1.570796326795 amplitude=1.0 omega=0.0
module s21 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s21.c0 module=s21 theta=0.026919504800 amplitude=1.0 omega=0.0
cell s21.c1 module=s21 theta=1.566282523293 amplitude=1.0 omega=0.0
cell s21.c2 module=s21 theta=1.683707518402 amplitude=1.0 omega=0.0
cell s21.c3 module=s21 theta=1.570796326795 amplitude=1.0 omega=0.0
module s22 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s22.c0 module=s22 theta=0.361734495357 amplitude=1.0 omega=0.0
cell s22.c1 module=s22 theta=2.996142007785 amplitude=1.0 omega=0.0
cell s22.c2 module=s22 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s22.c3 module=s22 theta=3.141592653590 amplitude=1.0 omega=0.0
module s23 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s23.c0 module=s23 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s23.c1 module=s23 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s23.c2 module=s23 theta=2.635850502424 amplitude=1.0 omega=0.0
cell s23.c3 module=s23 theta=0.000000000000 amplitude=1.0 omega=0.0
module s24 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s24.c0 module=s24 theta=2.460745263521 amplitude=1.0 omega=0.0
cell s24.c1 module=s24 theta=1.404316182568 amplitude=1.0 omega=0.0
cell s24.c2 module=s24 theta=2.930549685865 amplitude=1.0 omega=0.0
cell s24.c3 module=s24 theta=1.570796326795 amplitude=1.0 omega=0.0
module s25 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s25.c0 module=s25 theta=1.832724679888 amplitude=1.0 omega=0.0
cell s25.c1 module=s25 theta=1.434238962256 amplitude=1.0 omega=0.0
cell s25.c2 module=s25 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s25.c3 module=s25 theta=1.570796326795 amplitude=1.0 omega=0.0
module s26 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s26.c0 module=s26 theta=0.314280775080 amplitude=1.0 omega=0.0
cell s26.c1 module=s26 theta=1.226582545495 amplitude=1.0 omega=0.0
cell s26.c2 module=s26 theta=1.477553927368 amplitude=1.0 omega=0.0
cell s26.c3 module=s26 theta=1.570796326795 amplitude=1.0 omega=0.0
module s27 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s27.c0 module=s27 theta=1.587083954750 amplitude=1.0 omega=0.0
cell s27.c1 module=s27 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s27.c2 module=s27 theta=0.740148567234 amplitude=1.0 omega=0.0
cell s27.c3 module=s27 theta=0.000000000000 amplitude=1.0 omega=0.0
module s28 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s28.c0 module=s28 theta=0.402121866326 amplitude=1.0 omega=0.0
cell s28.c1 module=s28 theta=1.711070519893 amplitude=1.0 omega=0.0
cell s28.c2 module=s28 theta=2.010639128828 amplitude=1.0 omega=0.0
cell s28.c3 module=s28 theta=1.570796326795 amplitude=1.0 omega=0.0
module s29 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s29.c0 module=s29 theta=1.287295950365 amplitude=1.0 omega=0.0
cell s29.c1 module=s29 theta=2.829089760963 amplitude=1.0 omega=0.0
cell s29.c2 module=s29 theta=1.824110378558 amplitude=1.0 omega=0.0
cell s29.c3 module=s29 theta=3.141592653590 amplitude=1.0 omega=0.0
module s30 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s30.c0 module=s30 theta=1.314366614238 amplitude=1.0 omega=0.0
cell s30.c1 module=s30 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s30.c2 module=s30 theta=1.688708204038 amplitude=1.0 omega=0.0
cell s30.c3 module=s30 theta=3.141592653590 amplitude=1.0 omega=0.0
module s31 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s31.c0 module=s31 theta=1.701265450426 amplitude=1.0 omega=0.0
cell s31.c1 module=s31 theta=1.543452024808 amplitude=1.0 omega=0.0
cell s31.c2 module=s31 theta=0.998359830759 amplitude=1.0 omega=0.0
cell s31.c3 module=s31 theta=1.570796326795 amplitude=1.0 omega=0.0
module s32 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s32.c0 module=s32 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s32.c1 module=s32 theta=0.053224738282 amplitude=1.0 omega=0.0
cell s32.c2 module=s32 theta=2.854660455029 amplitude=1.0 omega=0.0
cell s32.c3 module=s32 theta=0.000000000000 amplitude=1.0 omega=0.0
module s33 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s33.c0 module=s33 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s33.c1 module=s33 theta=1.143886413851 amplitude=1.0 omega=0.0
cell s33.c2 module=s33 theta=0.883422212901 amplitude=1.0 omega=0.0
cell s33.c3 module=s33 theta=1.570796326795 amplitude=1.0 omega=0.0
module s34 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s34.c0 module=s34 theta=1.494601675442 amplitude=1.0 omega=0.0
cell s34.c1 module=s34 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s34.c2 module=s34 theta=2.102127717479 amplitude=1.0 omega=0.0
cell s34.c3 module=s34 theta=0.000000000000 amplitude=1.0 omega=0.0
module s35 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s35.c0 module=s35 theta=1.596484803322 amplitude=1.0 omega=0.0
cell s35.c1 module=s35 theta=2.023819567004 amplitude=1.0 omega=0.0
cell s35.c2 module=s35 theta=2.731325387371 amplitude=1.0 omega=0.0
cell s35.c3 module=s35 theta=1.570796326795 amplitude=1.0 omega=0.0
module s36 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s36.c0 module=s36 theta=1.757879773216 amplitude=1.0 omega=0.0
cell s36.c1 module=s36 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s36.c2 module=s36 theta=3.072432245219 amplitude=1.0 omega=0.0
cell s36.c3 module=s36 theta=1.570796326795 amplitude=1.0 omega=0.0
module s37 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s37.c0 module=s37 theta=1.615931632257 amplitude=1.0 omega=0.0
cell s37.c1 module=s37 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s37.c2 module=s37 theta=2.039344591044 amplitude=1.0 omega=0.0
cell s37.c3 module=s37 theta=3.141592653590 amplitude=1.0 omega=0.0
module s38 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s38.c0 module=s38 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s38.c1 module=s38 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s38.c2 module=s38 theta=2.865144031190 amplitude=1.0 omega=0.0
cell s38.c3 module=s38 theta=1.570796326795 amplitude=1.0 omega=0.0
module s39 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s39.c0 module=s39 theta=1.508966718787 amplitude=1.0 omega=0.0
cell s39.c1 module=s39 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s39.c2 module=s39 theta=1.839477759190 amplitude=1.0 omega=0.0
cell s39.c3 module=s39 theta=3.141592653590 amplitude=1.0 omega=0.0
module s40 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s40.c0 module=s40 theta=1.812845841597 amplitude=1.0 omega=0.0
cell s40.c1 module=s40 theta=1.298074779738 amplitude=1.0 omega=0.0
cell s40.c2 module=s40 theta=1.402063025927 amplitude=1.0 omega=0.0
cell s40.c3 module=s40 theta=1.570796326795 amplitude=1.0 omega=0.0
module s41 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s41.c0 module=s41 theta=2.904482507184 amplitude=1.0 omega=0.0
cell s41.c1 module=s41 theta=0.318535652539 amplitude=1.0 omega=0.0
cell s41.c2 module=s41 theta=1.289153741812 amplitude=1.0 omega=0.0
cell s41.c3 module=s41 theta=1.570796326795 amplitude=1.0 omega=0.0
module s42 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s42.c0 module=s42 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s42.c1 module=s42 theta=1.765931861313 amplitude=1.0 omega=0.0
cell s42.c2 module=s42 theta=1.462539310093 amplitude=1.0 omega=0.0
cell s42.c3 module=s42 theta=1.570796326795 amplitude=1.0 omega=0.0
module s43 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s43.c0 module=s43 theta=1.588199268630 amplitude=1.0 omega=0.0
cell s43.c1 module=s43 theta=1.565400813336 amplitude=1.0 omega=0.0
cell s43.c2 module=s43 theta=1.848368740647 amplitude=1.0 omega=0.0
cell s43.c3 module=s43 theta=1.570796326795 amplitude=1.0 omega=0.0
module s44 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s44.c0 module=s44 theta=1.488540609575 amplitude=1.0 omega=0.0
cell s44.c1 module=s44 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s44.c2 module=s44 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s44.c3 module=s44 theta=3.141592653590 amplitude=1.0 omega=0.0
module s45 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s45.c0 module=s45 theta=1.651571443481 amplitude=1.0 omega=0.0
cell s45.c1 module=s45 theta=3.003254824681 amplitude=1.0 omega=0.0
cell s45.c2 module=s45 theta=1.768701360956 amplitude=1.0 omega=0.0
cell s45.c3 module=s45 theta=3.141592653590 amplitude=1.0 omega=0.0
module s46 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s46.c0 module=s46 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s46.c1 module=s46 theta=0.318223697304 amplitude=1.0 omega=0.0
cell s46.c2 module=s46 theta=0.609686624320 amplitude=1.0 omega=0.0
cell s46.c3 module=s46 theta=0.000000000000 amplitude=1.0 omega=0.0
module s47 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s47.c0 module=s47 theta=0.020923525441 amplitude=1.0 omega=0.0
cell s47.c1 module=s47 theta=2.684503809613 amplitude=1.0 omega=0.0
cell s47.c2 module=s47 theta=1.292956296918 amplitude=1.0 omega=0.0
cell s47.c3 module=s47 theta=1.570796326795 amplitude=1.0 omega=0.0
module s48 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s48.c0 module=s48 theta=2.372401755832 amplitude=1.0 omega=0.0
cell s48.c1 module=s48 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s48.c2 module=s48 theta=1.606283268158 amplitude=1.0 omega=0.0
cell s48.c3 module=s48 theta=3.141592653590 amplitude=1.0 omega=0.0
module s49 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s49.c0 module=s49 theta=1.348875158122 amplitude=1.0 omega=0.0
cell s49.c1 module=s49 theta=0.374744264991 amplitude=1.0 omega=0.0
cell s49.c2 module=s49 theta=1.805466808905 amplitude=1.0 omega=0.0
cell s49.c3 module=s49 theta=0.000000000000 amplitude=1.0 omega=0.0
module s50 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s50.c0 module=s50 theta=1.367690697313 amplitude=1.0 omega=0.0
cell s50.c1 module=s50 theta=2.946354250243 amplitude=1.0 omega=0.0
cell s50.c2 module=s50 theta=1.481559906969 amplitude=1.0 omega=0.0
cell s50.c3 module=s50 theta=3.141592653590 amplitude=1.0 omega=0.0
module s51 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s51.c0 module=s51 theta=0.284987147121 amplitude=1.0 omega=0.0
cell s51.c1 module=s51 theta=2.242099519546 amplitude=1.0 omega=0.0
cell s51.c2 module=s51 theta=1.702183219566 amplitude=1.0 omega=0.0
cell s51.c3 module=s51 theta=1.570796326795 amplitude=1.0 omega=0.0
module s52 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s52.c0 module=s52 theta=1.283371748001 amplitude=1.0 omega=0.0
cell s52.c1 module=s52 theta=0.444547760902 amplitude=1.0 omega=0.0
cell s52.c2 module=s52 theta=2.228978083364 amplitude=1.0 omega=0.0
cell s52.c3 module=s52 theta=1.570796326795 amplitude=1.0 omega=0.0
module s53 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s53.c0 module=s53 theta=1.556757140226 amplitude=1.0 omega=0.0
cell s53.c1 module=s53 theta=2.940769821653 amplitude=1.0 omega=0.0
cell s53.c2 module=s53 theta=3.014424401220 amplitude=1.0 omega=0.0
cell s53.c3 module=s53 theta=3.141592653590 amplitude=1.0 omega=0.0
module s54 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s54.c0 module=s54 theta=1.565183938207 amplitude=1.0 omega=0.0
cell s54.c1 module=s54 theta=1.493042720329 amplitude=1.0 omega=0.0
cell s54.c2 module=s54 theta=2.804237266517 amplitude=1.0 omega=0.0
cell s54.c3 module=s54 theta=1.570796326795 amplitude=1.0 omega=0.0
module s55 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s55.c0 module=s55 theta=1.928073130486 amplitude=1.0 omega=0.0
cell s55.c1 module=s55 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s55.c2 module=s55 theta=1.494060298432 amplitude=1.0 omega=0.0
cell s55.c3 module=s55 theta=3.141592653590 amplitude=1.0 omega=0.0
module s56 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s56.c0 module=s56 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s56.c1 module=s56 theta=1.354002377675 amplitude=1.0 omega=0.0
cell s56.c2 module=s56 theta=1.626619354524 amplitude=1.0 omega=0.0
cell s56.c3 module=s56 theta=1.570796326795 amplitude=1.0 omega=0.0
module s57 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s57.c0 module=s57 theta=2.858414479373 amplitude=1.0 omega=0.0
cell s57.c1 module=s57 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s57.c2 module=s57 theta=2.880772263406 amplitude=1.0 omega=0.0
cell s57.c3 module=s57 theta=1.570796326795 amplitude=1.0 omega=0.0
module s58 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s58.c0 module=s58 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s58.c1 module=s58 theta=1.768692101466 amplitude=1.0 omega=0.0
cell s58.c2 module=s58 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s58.c3 module=s58 theta=0.000000000000 amplitude=1.0 omega=0.0
module s59 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s59.c0 module=s59 theta=3.115606119558 amplitude=1.0 omega=0.0
cell s59.c1 module=s59 theta=1.523368835968 amplitude=1.0 omega=0.0
cell s59.c2 module=s59 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s59.c3 module=s59 theta=1.570796326795 amplitude=1.0 omega=0.0
module s60 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s60.c0 module=s60 theta=1.617046976473 amplitude=1.0 omega=0.0
cell s60.c1 module=s60 theta=1.581972628853 amplitude=1.0 omega=0.0
cell s60.c2 module=s60 theta=0.297889130746 amplitude=1.0 omega=0.0
cell s60.c3 module=s60 theta=1.570796326795 amplitude=1.0 omega=0.0
module s61 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s61.c0 module=s61 theta=1.877018284621 amplitude=1.0 omega=0.0
cell s61.c1 module=s61 theta=0.696594230083 amplitude=1.0 omega=0.0
cell s61.c2 module=s61 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s61.c3 module=s61 theta=0.000000000000 amplitude=1.0 omega=0.0
module s62 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s62.c0 module=s62 theta=1.811649021915 amplitude=1.0 omega=0.0
cell s62.c1 module=s62 theta=0.995264161640 amplitude=1.0 omega=0.0
cell s62.c2 module=s62 theta=1.401343472109 amplitude=1.0 omega=0.0
cell s62.c3 module=s62 theta=1.570796326795 amplitude=1.0 omega=0.0
module s63 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s63.c0 module=s63 theta=1.656102042706 amplitude=1.0 omega=0.0
cell s63.c1 module=s63 theta=1.636737491994 amplitude=1.0 omega=0.0
cell s63.c2 module=s63 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s63.c3 module=s63 theta=1.570796326795 amplitude=1.0 omega=0.0
module s64 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s64.c0 module=s64 theta=1.587245930588 amplitude=1.0 omega=0.0
cell s64.c1 module=s64 theta=0.774963638391 amplitude=1.0 omega=0.0
cell s64.c2 module=s64 theta=3.042963390212 amplitude=1.0 omega=0.0
cell s64.c3 module=s64 theta=1.570796326795 amplitude=1.0 omega=0.0
module s65 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s65.c0 module=s65 theta=1.397215960992 amplitude=1.0 omega=0.0
cell s65.c1 module=s65 theta=2.070205473597 amplitude=1.0 omega=0.0
cell s65.c2 module=s65 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s65.c3 module=s65 theta=1.570796326795 amplitude=1.0 omega=0.0
module s66 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s66.c0 module=s66 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s66.c1 module=s66 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s66.c2 module=s66 theta=1.601414475501 amplitude=1.0 omega=0.0
cell s66.c3 module=s66 theta=1.570796326795 amplitude=1.0 omega=0.0
module s67 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s67.c0 module=s67 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s67.c1 module=s67 theta=1.367516490662 amplitude=1.0 omega=0.0
cell s67.c2 module=s67 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s67.c3 module=s67 theta=3.141592653590 amplitude=1.0 omega=0.0
module s68 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s68.c0 module=s68 theta=1.622669663149 amplitude=1.0 omega=0.0
cell s68.c1 module=s68 theta=2.792791292376 amplitude=1.0 omega=0.0
cell s68.c2 module=s68 theta=2.942490589327 amplitude=1.0 omega=0.0
cell s68.c3 module=s68 theta=3.141592653590 amplitude=1.0 omega=0.0
module s69 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s69.c0 module=s69 theta=2.272379842876 amplitude=1.0 omega=0.0
cell s69.c1 module=s69 theta=0.087211903080 amplitude=1.0 omega=0.0
cell s69.c2 module=s69 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s69.c3 module=s69 theta=0.000000000000 amplitude=1.0 omega=0.0
module s70 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s70.c0 module=s70 theta=1.844216002998 amplitude=1.0 omega=0.0
cell s70.c1 module=s70 theta=1.822479140583 amplitude=1.0 omega=0.0
cell s70.c2 module=s70 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s70.c3 module=s70 theta=1.570796326795 amplitude=1.0 omega=0.0
module s71 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s71.c0 module=s71 theta=1.293581234611 amplitude=1.0 omega=0.0
cell s71.c1 module=s71 theta=1.493858003583 amplitude=1.0 omega=0.0
cell s71.c2 module=s71 theta=1.826660560457 amplitude=1.0 omega=0.0
cell s71.c3 module=s71 theta=1.570796326795 amplitude=1.0 omega=0.0
module s72 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s72.c0 module=s72 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s72.c1 module=s72 theta=0.079767271862 amplitude=1.0 omega=0.0
cell s72.c2 module=s72 theta=0.160783162965 amplitude=1.0 omega=0.0
cell s72.c3 module=s72 theta=0.000000000000 amplitude=1.0 omega=0.0
module s73 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s73.c0 module=s73 theta=3.090012836213 amplitude=1.0 omega=0.0
cell s73.c1 module=s73 theta=2.705746910855 amplitude=1.0 omega=0.0
cell s73.c2 module=s73 theta=1.542692008514 amplitude=1.0 omega=0.0
cell s73.c3 module=s73 theta=3.141592653590 amplitude=1.0 omega=0.0
module s74 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s74.c0 module=s74 theta=1.727162249015 amplitude=1.0 omega=0.0
cell s74.c1 module=s74 theta=2.660330144239 amplitude=1.0 omega=0.0
cell s74.c2 module=s74 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s74.c3 module=s74 theta=3.141592653590 amplitude=1.0 omega=0.0
module s75 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s75.c0 module=s75 theta=2.438568474792 amplitude=1.0 omega=0.0
cell s75.c1 module=s75 theta=1.594939736945 amplitude=1.0 omega=0.0
cell s75.c2 module=s75 theta=1.483556998171 amplitude=1.0 omega=0.0
cell s75.c3 module=s75 theta=1.570796326795 amplitude=1.0 omega=0.0
module s76 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s76.c0 module=s76 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s76.c1 module=s76 theta=1.364719030195 amplitude=1.0 omega=0.0
cell s76.c2 module=s76 theta=1.153320869154 amplitude=1.0 omega=0.0
cell s76.c3 module=s76 theta=1.570796326795 amplitude=1.0 omega=0.0
module s77 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s77.c0 module=s77 theta=3.083411207228 amplitude=1.0 omega=0.0
cell s77.c1 module=s77 theta=2.950683016060 amplitude=1.0 omega=0.0
cell s77.c2 module=s77 theta=1.454472568437 amplitude=1.0 omega=0.0
cell s77.c3 module=s77 theta=3.141592653590 amplitude=1.0 omega=0.0
module s78 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s78.c0 module=s78 theta=1.273766291201 amplitude=1.0 omega=0.0
cell s78.c1 module=s78 theta=1.533344847911 amplitude=1.0 omega=0.0
cell s78.c2 module=s78 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s78.c3 module=s78 theta=1.570796326795 amplitude=1.0 omega=0.0
module s79 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s79.c0 module=s79 theta=2.722920045993 amplitude=1.0 omega=0.0
cell s79.c1 module=s79 theta=2.994226993204 amplitude=1.0 omega=0.0
cell s79.c2 module=s79 theta=1.873296519143 amplitude=1.0 omega=0.0
cell s79.c3 module=s79 theta=3.141592653590 amplitude=1.0 omega=0.0
module s80 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s80.c0 module=s80 theta=1.596444630118 amplitude=1.0 omega=0.0
cell s80.c1 module=s80 theta=1.727132111639 amplitude=1.0 omega=0.0
cell s80.c2 module=s80 theta=3.125483062667 amplitude=1.0 omega=0.0
cell s80.c3 module=s80 theta=1.570796326795 amplitude=1.0 omega=0.0
module s81 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s81.c0 module=s81 theta=2.927367977770 amplitude=1.0 omega=0.0
cell s81.c1 module=s81 theta=0.008953398766 amplitude=1.0 omega=0.0
cell s81.c2 module=s81 theta=0.296465553955 amplitude=1.0 omega=0.0
cell s81.c3 module=s81 theta=0.000000000000 amplitude=1.0 omega=0.0
module s82 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s82.c0 module=s82 theta=2.897974679742 amplitude=1.0 omega=0.0
cell s82.c1 module=s82 theta=3.013160607483 amplitude=1.0 omega=0.0
cell s82.c2 module=s82 theta=1.516447841340 amplitude=1.0 omega=0.0
cell s82.c3 module=s82 theta=3.141592653590 amplitude=1.0 omega=0.0
module s83 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s83.c0 module=s83 theta=1.655305377065 amplitude=1.0 omega=0.0
cell s83.c1 module=s83 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s83.c2 module=s83 theta=2.078789596143 amplitude=1.0 omega=0.0
cell s83.c3 module=s83 theta=3.141592653590 amplitude=1.0 omega=0.0
module s84 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s84.c0 module=s84 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s84.c1 module=s84 theta=1.399568157851 amplitude=1.0 omega=0.0
cell s84.c2 module=s84 theta=3.059476037668 amplitude=1.0 omega=0.0
cell s84.c3 module=s84 theta=1.570796326795 amplitude=1.0 omega=0.0
module s85 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s85.c0 module=s85 theta=0.759363317328 amplitude=1.0 omega=0.0
cell s85.c1 module=s85 theta=0.336674300166 amplitude=1.0 omega=0.0
cell s85.c2 module=s85 theta=0.121037404726 amplitude=1.0 omega=0.0
cell s85.c3 module=s85 theta=0.000000000000 amplitude=1.0 omega=0.0
module s86 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s86.c0 module=s86 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s86.c1 module=s86 theta=1.676923790340 amplitude=1.0 omega=0.0
cell s86.c2 module=s86 theta=1.691357004113 amplitude=1.0 omega=0.0
cell s86.c3 module=s86 theta=1.570796326795 amplitude=1.0 omega=0.0
module s87 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s87.c0 module=s87 theta=1.368681802530 amplitude=1.0 omega=0.0
cell s87.c1 module=s87 theta=1.766335812266 amplitude=1.0 omega=0.0
cell s87.c2 module=s87 theta=0.040084417943 amplitude=1.0 omega=0.0
cell s87.c3 module=s87 theta=1.570796326795 amplitude=1.0 omega=0.0
module s88 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s88.c0 module=s88 theta=1.337965791985 amplitude=1.0 omega=0.0
cell s88.c1 module=s88 theta=1.857988736975 amplitude=1.0 omega=0.0
cell s88.c2 module=s88 theta=2.851823235251 amplitude=1.0 omega=0.0
cell s88.c3 module=s88 theta=1.570796326795 amplitude=1.0 omega=0.0
module s89 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s89.c0 module=s89 theta=1.743030498381 amplitude=1.0 omega=0.0
cell s89.c1 module=s89 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s89.c2 module=s89 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s89.c3 module=s89 theta=1.570796326795 amplitude=1.0 omega=0.0
module s90 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s90.c0 module=s90 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s90.c1 module=s90 theta=3.057458382137 amplitude=1.0 omega=0.0
cell s90.c2 module=s90 theta=0.527655302575 amplitude=1.0 omega=0.0
cell s90.c3 module=s90 theta=3.141592653590 amplitude=1.0 omega=0.0
module s91 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s91.c0 module=s91 theta=2.959133931881 amplitude=1.0 omega=0.0
cell s91.c1 module=s91 theta=0.347075779201 amplitude=1.0 omega=0.0
cell s91.c2 module=s91 theta=1.563022669139 amplitude=1.0 omega=0.0
cell s91.c3 module=s91 theta=1.570796326795 amplitude=1.0 omega=0.0
module s92 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s92.c0 module=s92 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s92.c1 module=s92 theta=1.523275701389 amplitude=1.0 omega=0.0
cell s92.c2 module=s92 theta=2.630521944740 amplitude=1.0 omega=0.0
cell s92.c3 module=s92 theta=1.570796326795 amplitude=1.0 omega=0.0
module s93 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s93.c0 module=s93 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s93.c1 module=s93 theta=2.942547437651 amplitude=1.0 omega=0.0
cell s93.c2 module=s93 theta=1.306033614432 amplitude=1.0 omega=0.0
cell s93.c3 module=s93 theta=1.570796326795 amplitude=1.0 omega=0.0
module s94 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s94.c0 module=s94 theta=1.597427543063 amplitude=1.0 omega=0.0
cell s94.c1 module=s94 theta=1.821560711574 amplitude=1.0 omega=0.0
cell s94.c2 module=s94 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s94.c3 module=s94 theta=1.570796326795 amplitude=1.0 omega=0.0
module s95 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s95.c0 module=s95 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s95.c1 module=s95 theta=1.599103705874 amplitude=1.0 omega=0.0
cell s95.c2 module=s95 theta=0.144029839956 amplitude=1.0 omega=0.0
cell s95.c3 module=s95 theta=1.570796326795 amplitude=1.0 omega=0.0
module s96 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s96.c0 module=s96 theta=0.124789796239 amplitude=1.0 omega=0.0
cell s96.c1 module=s96 theta=3.119141039827 amplitude=1.0 omega=0.0
cell s96.c2 module=s96 theta=0.582933104494 amplitude=1.0 omega=0.0
cell s96.c3 module=s96 theta=1.570796326795 amplitude=1.0 omega=0.0
module s97 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s97.c0 module=s97 theta=0.334167906886 amplitude=1.0 omega=0.0
cell s97.c1 module=s97 theta=1.405067414503 amplitude=1.0 omega=0.0
cell s97.c2 module=s97 theta=0.061499755658 amplitude=1.0 omega=0.0
cell s97.c3 module=s97 theta=0.000000000000 amplitude=1.0 omega=0.0
module s98 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s98.c0 module=s98 theta=1.287427579000 amplitude=1.0 omega=0.0
cell s98.c1 module=s98 theta=2.825866791288 amplitude=1.0 omega=0.0
cell s98.c2 module=s98 theta=1.788815846386 amplitude=1.0 omega=0.0
cell s98.c3 module=s98 theta=3.141592653590 amplitude=1.0 omega=0.0
module s99 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s99.c0 module=s99 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s99.c1 module=s99 theta=3.116571576976 amplitude=1.0 omega=0.0
cell s99.c2 module=s99 theta=1.303943567635 amplitude=1.0 omega=0.0
cell s99.c3 module=s99 theta=1.570796326795 amplitude=1.0 omega=0.0
module s100 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s100.c0 module=s100 theta=0.552727857694 amplitude=1.0 omega=0.0
cell s100.c1 module=s100 theta=3.050431752990 amplitude=1.0 omega=0.0
cell s100.c2 module=s100 theta=1.161902152386 amplitude=1.0 omega=0.0
cell s100.c3 module=s100 theta=1.570796326795 amplitude=1.0 omega=0.0
module s101 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s101.c0 module=s101 theta=2.932324726624 amplitude=1.0 omega=0.0
cell s101.c1 module=s101 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s101.c2 module=s101 theta=1.650620120296 amplitude=1.0 omega=0.0
cell s101.c3 module=s101 theta=1.570796326795 amplitude=1.0 omega=0.0
module s102 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s102.c0 module=s102 theta=0.349567111381 amplitude=1.0 omega=0.0
cell s102.c1 module=s102 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s102.c2 module=s102 theta=1.303247526150 amplitude=1.0 omega=0.0
cell s102.c3 module=s102 theta=1.570796326795 amplitude=1.0 omega=0.0
module s103 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s103.c0 module=s103 theta=2.140105985226 amplitude=1.0 omega=0.0
cell s103.c1 module=s103 theta=3.140678174401 amplitude=1.0 omega=0.0
cell s103.c2 module=s103 theta=1.643685176620 amplitude=1.0 omega=0.0
cell s103.c3 module=s103 theta=3.141592653590 amplitude=1.0 omega=0.0
module s104 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s104.c0 module=s104 theta=1.457606665634 amplitude=1.0 omega=0.0
cell s104.c1 module=s104 theta=1.893154631049 amplitude=1.0 omega=0.0
cell s104.c2 module=s104 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s104.c3 module=s104 theta=1.570796326795 amplitude=1.0 omega=0.0
module s105 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s105.c0 module=s105 theta=1.554747079668 amplitude=1.0 omega=0.0
cell s105.c1 module=s105 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s105.c2 module=s105 theta=1.340343859125 amplitude=1.0 omega=0.0
cell s105.c3 module=s105 theta=3.141592653590 amplitude=1.0 omega=0.0
module s106 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s106.c0 module=s106 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s106.c1 module=s106 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s106.c2 module=s106 theta=3.081450330635 amplitude=1.0 omega=0.0
cell s106.c3 module=s106 theta=0.000000000000 amplitude=1.0 omega=0.0
module s107 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s107.c0 module=s107 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s107.c1 module=s107 theta=0.163540692024 amplitude=1.0 omega=0.0
cell s107.c2 module=s107 theta=1.733938882259 amplitude=1.0 omega=0.0
cell s107.c3 module=s107 theta=0.000000000000 amplitude=1.0 omega=0.0
module s108 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s108.c0 module=s108 theta=1.743900665195 amplitude=1.0 omega=0.0
cell s108.c1 module=s108 theta=1.496765863858 amplitude=1.0 omega=0.0
cell s108.c2 module=s108 theta=1.842091487270 amplitude=1.0 omega=0.0
cell s108.c3 module=s108 theta=1.570796326795 amplitude=1.0 omega=0.0
module s109 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s109.c0 module=s109 theta=1.791983985858 amplitude=1.0 omega=0.0
cell s109.c1 module=s109 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s109.c2 module=s109 theta=2.955256222752 amplitude=1.0 omega=0.0
cell s109.c3 module=s109 theta=1.570796326795 amplitude=1.0 omega=0.0
module s110 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s110.c0 module=s110 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s110.c1 module=s110 theta=1.441440555041 amplitude=1.0 omega=0.0
cell s110.c2 module=s110 theta=1.797162805096 amplitude=1.0 omega=0.0
cell s110.c3 module=s110 theta=1.570796326795 amplitude=1.0 omega=0.0
module s111 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s111.c0 module=s111 theta=1.814561392047 amplitude=1.0 omega=0.0
cell s111.c1 module=s111 theta=1.314286561039 amplitude=1.0 omega=0.0
cell s111.c2 module=s111 theta=1.109353847193 amplitude=1.0 omega=0.0
cell s111.c3 module=s111 theta=1.570796326795 amplitude=1.0 omega=0.0
module s112 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s112.c0 module=s112 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s112.c1 module=s112 theta=3.005109600266 amplitude=1.0 omega=0.0
cell s112.c2 module=s112 theta=0.147749845682 amplitude=1.0 omega=0.0
cell s112.c3 module=s112 theta=1.570796326795 amplitude=1.0 omega=0.0
module s113 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s113.c0 module=s113 theta=3.044786740519 amplitude=1.0 omega=0.0
cell s113.c1 module=s113 theta=0.682874344710 amplitude=1.0 omega=0.0
cell s113.c2 module=s113 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s113.c3 module=s113 theta=1.570796326795 amplitude=1.0 omega=0.0
module s114 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s114.c0 module=s114 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s114.c1 module=s114 theta=2.846574005988 amplitude=1.0 omega=0.0
cell s114.c2 module=s114 theta=0.006414743865 amplitude=1.0 omega=0.0
cell s114.c3 module=s114 theta=3.141592653590 amplitude=1.0 omega=0.0
module s115 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s115.c0 module=s115 theta=2.237743935240 amplitude=1.0 omega=0.0
cell s115.c1 module=s115 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s115.c2 module=s115 theta=2.969140509579 amplitude=1.0 omega=0.0
cell s115.c3 module=s115 theta=1.570796326795 amplitude=1.0 omega=0.0
module s116 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s116.c0 module=s116 theta=1.355370816038 amplitude=1.0 omega=0.0
cell s116.c1 module=s116 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s116.c2 module=s116 theta=1.423595760811 amplitude=1.0 omega=0.0
cell s116.c3 module=s116 theta=3.141592653590 amplitude=1.0 omega=0.0
module s117 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s117.c0 module=s117 theta=1.878341692543 amplitude=1.0 omega=0.0
cell s117.c1 module=s117 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s117.c2 module=s117 theta=1.629595756967 amplitude=1.0 omega=0.0
cell s117.c3 module=s117 theta=3.141592653590 amplitude=1.0 omega=0.0
module s118 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s118.c0 module=s118 theta=1.295443040132 amplitude=1.0 omega=0.0
cell s118.c1 module=s118 theta=1.642545328486 amplitude=1.0 omega=0.0
cell s118.c2 module=s118 theta=2.727086273900 amplitude=1.0 omega=0.0
cell s118.c3 module=s118 theta=1.570796326795 amplitude=1.0 omega=0.0
module s119 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s119.c0 module=s119 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s119.c1 module=s119 theta=0.151642268166 amplitude=1.0 omega=0.0
cell s119.c2 module=s119 theta=1.017522087763 amplitude=1.0 omega=0.0
cell s119.c3 module=s119 theta=0.000000000000 amplitude=1.0 omega=0.0
module s120 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s120.c0 module=s120 theta=1.785774614619 amplitude=1.0 omega=0.0
cell s120.c1 module=s120 theta=2.842957190836 amplitude=1.0 omega=0.0
cell s120.c2 module=s120 theta=1.791983596198 amplitude=1.0 omega=0.0
cell s120.c3 module=s120 theta=3.141592653590 amplitude=1.0 omega=0.0
module s121 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s121.c0 module=s121 theta=2.529729294903 amplitude=1.0 omega=0.0
cell s121.c1 module=s121 theta=2.712738513191 amplitude=1.0 omega=0.0
cell s121.c2 module=s121 theta=1.443244246226 amplitude=1.0 omega=0.0
cell s121.c3 module=s121 theta=3.141592653590 amplitude=1.0 omega=0.0
module s122 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s122.c0 module=s122 theta=0.968081298602 amplitude=1.0 omega=0.0
cell s122.c1 module=s122 theta=1.673564798541 amplitude=1.0 omega=0.0
cell s122.c2 module=s122 theta=0.150140572268 amplitude=1.0 omega=0.0
cell s122.c3 module=s122 theta=1.570796326795 amplitude=1.0 omega=0.0
module s123 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s123.c0 module=s123 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s123.c1 module=s123 theta=2.069191960556 amplitude=1.0 omega=0.0
cell s123.c2 module=s123 theta=2.456881121493 amplitude=1.0 omega=0.0
cell s123.c3 module=s123 theta=1.570796326795 amplitude=1.0 omega=0.0
module s124 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s124.c0 module=s124 theta=1.445374320432 amplitude=1.0 omega=0.0
cell s124.c1 module=s124 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s124.c2 module=s124 theta=1.472842933894 amplitude=1.0 omega=0.0
cell s124.c3 module=s124 theta=3.141592653590 amplitude=1.0 omega=0.0
module s125 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s125.c0 module=s125 theta=3.075237663305 amplitude=1.0 omega=0.0
cell s125.c1 module=s125 theta=2.958818876809 amplitude=1.0 omega=0.0
cell s125.c2 module=s125 theta=0.112995237885 amplitude=1.0 omega=0.0
cell s125.c3 module=s125 theta=3.141592653590 amplitude=1.0 omega=0.0
module s126 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s126.c0 module=s126 theta=1.828456023328 amplitude=1.0 omega=0.0
cell s126.c1 module=s126 theta=3.118552107434 amplitude=1.0 omega=0.0
cell s126.c2 module=s126 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s126.c3 module=s126 theta=1.570796326795 amplitude=1.0 omega=0.0
module s127 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s127.c0 module=s127 theta=0.569404335250 amplitude=1.0 omega=0.0
cell s127.c1 module=s127 theta=1.729113247852 amplitude=1.0 omega=0.0
cell s127.c2 module=s127 theta=2.378331830005 amplitude=1.0 omega=0.0
cell s127.c3 module=s127 theta=1.570796326795 amplitude=1.0 omega=0.0
module s128 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s128.c0 module=s128 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s128.c1 module=s128 theta=0.303157145676 amplitude=1.0 omega=0.0
cell s128.c2 module=s128 theta=1.333401620430 amplitude=1.0 omega=0.0
cell s128.c3 module=s128 theta=0.000000000000 amplitude=1.0 omega=0.0
module s129 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s129.c0 module=s129 theta=1.476138386874 amplitude=1.0 omega=0.0
cell s129.c1 module=s129 theta=1.711901283971 amplitude=1.0 omega=0.0
cell s129.c2 module=s129 theta=1.691224476044 amplitude=1.0 omega=0.0
cell s129.c3 module=s129 theta=1.570796326795 amplitude=1.0 omega=0.0
module s130 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s130.c0 module=s130 theta=0.374031129969 amplitude=1.0 omega=0.0
cell s130.c1 module=s130 theta=0.679184646607 amplitude=1.0 omega=0.0
cell s130.c2 module=s130 theta=1.869947471273 amplitude=1.0 omega=0.0
cell s130.c3 module=s130 theta=0.000000000000 amplitude=1.0 omega=0.0
module s131 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s131.c0 module=s131 theta=1.935798259735 amplitude=1.0 omega=0.0
cell s131.c1 module=s131 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s131.c2 module=s131 theta=1.071012327774 amplitude=1.0 omega=0.0
cell s131.c3 module=s131 theta=0.000000000000 amplitude=1.0 omega=0.0
module s132 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s132.c0 module=s132 theta=2.816856979812 amplitude=1.0 omega=0.0
cell s132.c1 module=s132 theta=1.326370137648 amplitude=1.0 omega=0.0
cell s132.c2 module=s132 theta=1.358787855589 amplitude=1.0 omega=0.0
cell s132.c3 module=s132 theta=1.570796326795 amplitude=1.0 omega=0.0
module s133 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s133.c0 module=s133 theta=0.271716664477 amplitude=1.0 omega=0.0
cell s133.c1 module=s133 theta=2.040080538644 amplitude=1.0 omega=0.0
cell s133.c2 module=s133 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s133.c3 module=s133 theta=1.570796326795 amplitude=1.0 omega=0.0
module s134 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s134.c0 module=s134 theta=0.027345500319 amplitude=1.0 omega=0.0
cell s134.c1 module=s134 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s134.c2 module=s134 theta=0.130383373007 amplitude=1.0 omega=0.0
cell s134.c3 module=s134 theta=0.000000000000 amplitude=1.0 omega=0.0
module s135 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s135.c0 module=s135 theta=1.793931521085 amplitude=1.0 omega=0.0
cell s135.c1 module=s135 theta=1.652195366348 amplitude=1.0 omega=0.0
cell s135.c2 module=s135 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s135.c3 module=s135 theta=1.570796326795 amplitude=1.0 omega=0.0
module s136 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s136.c0 module=s136 theta=0.694681564534 amplitude=1.0 omega=0.0
cell s136.c1 module=s136 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s136.c2 module=s136 theta=3.081950934366 amplitude=1.0 omega=0.0
cell s136.c3 module=s136 theta=0.000000000000 amplitude=1.0 omega=0.0
module s137 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s137.c0 module=s137 theta=2.249260850721 amplitude=1.0 omega=0.0
cell s137.c1 module=s137 theta=0.171199127243 amplitude=1.0 omega=0.0
cell s137.c2 module=s137 theta=0.250325891790 amplitude=1.0 omega=0.0
cell s137.c3 module=s137 theta=0.000000000000 amplitude=1.0 omega=0.0
module s138 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s138.c0 module=s138 theta=0.853968119620 amplitude=1.0 omega=0.0
cell s138.c1 module=s138 theta=1.851253443158 amplitude=1.0 omega=0.0
cell s138.c2 module=s138 theta=0.049921775244 amplitude=1.0 omega=0.0
cell s138.c3 module=s138 theta=1.570796326795 amplitude=1.0 omega=0.0
module s139 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s139.c0 module=s139 theta=2.180840681901 amplitude=1.0 omega=0.0
cell s139.c1 module=s139 theta=1.365196536160 amplitude=1.0 omega=0.0
cell s139.c2 module=s139 theta=0.138641405309 amplitude=1.0 omega=0.0
cell s139.c3 module=s139 theta=1.570796326795 amplitude=1.0 omega=0.0
module s140 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s140.c0 module=s140 theta=2.290779616674 amplitude=1.0 omega=0.0
cell s140.c1 module=s140 theta=1.791379706484 amplitude=1.0 omega=0.0
cell s140.c2 module=s140 theta=1.735175407337 amplitude=1.0 omega=0.0
cell s140.c3 module=s140 theta=1.570796326795 amplitude=1.0 omega=0.0
module s141 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s141.c0 module=s141 theta=0.545756979698 amplitude=1.0 omega=0.0
cell s141.c1 module=s141 theta=1.795994409362 amplitude=1.0 omega=0.0
cell s141.c2 module=s141 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s141.c3 module=s141 theta=0.000000000000 amplitude=1.0 omega=0.0
module s142 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s142.c0 module=s142 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s142.c1 module=s142 theta=2.865825258436 amplitude=1.0 omega=0.0
cell s142.c2 module=s142 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s142.c3 module=s142 theta=3.141592653590 amplitude=1.0 omega=0.0
module s143 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s143.c0 module=s143 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s143.c1 module=s143 theta=1.405506829661 amplitude=1.0 omega=0.0
cell s143.c2 module=s143 theta=1.652731548509 amplitude=1.0 omega=0.0
cell s143.c3 module=s143 theta=1.570796326795 amplitude=1.0 omega=0.0
module s144 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s144.c0 module=s144 theta=1.410283898984 amplitude=1.0 omega=0.0
cell s144.c1 module=s144 theta=1.690522873403 amplitude=1.0 omega=0.0
cell s144.c2 module=s144 theta=1.672551372515 amplitude=1.0 omega=0.0
cell s144.c3 module=s144 theta=1.570796326795 amplitude=1.0 omega=0.0
module s145 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s145.c0 module=s145 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s145.c1 module=s145 theta=3.123707124514 amplitude=1.0 omega=0.0
cell s145.c2 module=s145 theta=1.523392589522 amplitude=1.0 omega=0.0
cell s145.c3 module=s145 theta=1.570796326795 amplitude=1.0 omega=0.0
module s146 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s146.c0 module=s146 theta=2.989978092817 amplitude=1.0 omega=0.0
cell s146.c1 module=s146 theta=3.112325220696 amplitude=1.0 omega=0.0
cell s146.c2 module=s146 theta=1.379900477592 amplitude=1.0 omega=0.0
cell s146.c3 module=s146 theta=3.141592653590 amplitude=1.0 omega=0.0
module s147 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s147.c0 module=s147 theta=0.249634986168 amplitude=1.0 omega=0.0
cell s147.c1 module=s147 theta=1.837893371513 amplitude=1.0 omega=0.0
cell s147.c2 module=s147 theta=1.573654164619 amplitude=1.0 omega=0.0
cell s147.c3 module=s147 theta=1.570796326795 amplitude=1.0 omega=0.0
module s148 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s148.c0 module=s148 theta=1.707664943292 amplitude=1.0 omega=0.0
cell s148.c1 module=s148 theta=1.585594680876 amplitude=1.0 omega=0.0
cell s148.c2 module=s148 theta=0.105285033873 amplitude=1.0 omega=0.0
cell s148.c3 module=s148 theta=1.570796326795 amplitude=1.0 omega=0.0
module s149 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s149.c0 module=s149 theta=3.015731640898 amplitude=1.0 omega=0.0
cell s149.c1 module=s149 theta=0.223958360934 amplitude=1.0 omega=0.0
cell s149.c2 module=s149 theta=0.120176361931 amplitude=1.0 omega=0.0
cell s149.c3 module=s149 theta=0.000000000000 amplitude=1.0 omega=0.0
module s150 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s150.c0 module=s150 theta=1.663049643831 amplitude=1.0 omega=0.0
cell s150.c1 module=s150 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s150.c2 module=s150 theta=1.903679893206 amplitude=1.0 omega=0.0
cell s150.c3 module=s150 theta=0.000000000000 amplitude=1.0 omega=0.0
module s151 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s151.c0 module=s151 theta=1.663908366239 amplitude=1.0 omega=0.0
cell s151.c1 module=s151 theta=2.915579414762 amplitude=1.0 omega=0.0
cell s151.c2 module=s151 theta=1.586656217695 amplitude=1.0 omega=0.0
cell s151.c3 module=s151 theta=3.141592653590 amplitude=1.0 omega=0.0
module s152 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s152.c0 module=s152 theta=1.817265182034 amplitude=1.0 omega=0.0
cell s152.c1 module=s152 theta=1.726589894374 amplitude=1.0 omega=0.0
cell s152.c2 module=s152 theta=1.683940851972 amplitude=1.0 omega=0.0
cell s152.c3 module=s152 theta=1.570796326795 amplitude=1.0 omega=0.0
module s153 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s153.c0 module=s153 theta=1.547190357795 amplitude=1.0 omega=0.0
cell s153.c1 module=s153 theta=0.013671658406 amplitude=1.0 omega=0.0
cell s153.c2 module=s153 theta=3.049427525487 amplitude=1.0 omega=0.0
cell s153.c3 module=s153 theta=1.570796326795 amplitude=1.0 omega=0.0
module s154 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s154.c0 module=s154 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s154.c1 module=s154 theta=0.526178976625 amplitude=1.0 omega=0.0
cell s154.c2 module=s154 theta=2.940942723365 amplitude=1.0 omega=0.0
cell s154.c3 module=s154 theta=1.570796326795 amplitude=1.0 omega=0.0
module s155 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s155.c0 module=s155 theta=3.083160390837 amplitude=1.0 omega=0.0
cell s155.c1 module=s155 theta=2.149120598884 amplitude=1.0 omega=0.0
cell s155.c2 module=s155 theta=1.717870225806 amplitude=1.0 omega=0.0
cell s155.c3 module=s155 theta=3.141592653590 amplitude=1.0 omega=0.0
module s156 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s156.c0 module=s156 theta=1.489050757191 amplitude=1.0 omega=0.0
cell s156.c1 module=s156 theta=3.044100454437 amplitude=1.0 omega=0.0
cell s156.c2 module=s156 theta=1.753682174890 amplitude=1.0 omega=0.0
cell s156.c3 module=s156 theta=3.141592653590 amplitude=1.0 omega=0.0
module s157 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s157.c0 module=s157 theta=1.733581006719 amplitude=1.0 omega=0.0
cell s157.c1 module=s157 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s157.c2 module=s157 theta=2.970240676225 amplitude=1.0 omega=0.0
cell s157.c3 module=s157 theta=3.141592653590 amplitude=1.0 omega=0.0
module s158 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s158.c0 module=s158 theta=0.230751795399 amplitude=1.0 omega=0.0
cell s158.c1 module=s158 theta=2.829758653754 amplitude=1.0 omega=0.0
cell s158.c2 module=s158 theta=1.678182287592 amplitude=1.0 omega=0.0
cell s158.c3 module=s158 theta=1.570796326795 amplitude=1.0 omega=0.0
module s159 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s159.c0 module=s159 theta=1.854540245372 amplitude=1.0 omega=0.0
cell s159.c1 module=s159 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s159.c2 module=s159 theta=3.024933153956 amplitude=1.0 omega=0.0
cell s159.c3 module=s159 theta=1.570796326795 amplitude=1.0 omega=0.0
module s160 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s160.c0 module=s160 theta=1.004114080212 amplitude=1.0 omega=0.0
cell s160.c1 module=s160 theta=3.085762192457 amplitude=1.0 omega=0.0
cell s160.c2 module=s160 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s160.c3 module=s160 theta=1.570796326795 amplitude=1.0 omega=0.0
module s161 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s161.c0 module=s161 theta=0.168012164174 amplitude=1.0 omega=0.0
cell s161.c1 module=s161 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s161.c2 module=s161 theta=1.283504442858 amplitude=1.0 omega=0.0
cell s161.c3 module=s161 theta=1.570796326795 amplitude=1.0 omega=0.0
module s162 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s162.c0 module=s162 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s162.c1 module=s162 theta=0.872810591611 amplitude=1.0 omega=0.0
cell s162.c2 module=s162 theta=1.828070079057 amplitude=1.0 omega=0.0
cell s162.c3 module=s162 theta=0.000000000000 amplitude=1.0 omega=0.0
module s163 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s163.c0 module=s163 theta=2.817613345523 amplitude=1.0 omega=0.0
cell s163.c1 module=s163 theta=1.217436509032 amplitude=1.0 omega=0.0
cell s163.c2 module=s163 theta=2.652831796569 amplitude=1.0 omega=0.0
cell s163.c3 module=s163 theta=1.570796326795 amplitude=1.0 omega=0.0
module s164 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s164.c0 module=s164 theta=1.542182337443 amplitude=1.0 omega=0.0
cell s164.c1 module=s164 theta=1.718803493679 amplitude=1.0 omega=0.0
cell s164.c2 module=s164 theta=0.956895822880 amplitude=1.0 omega=0.0
cell s164.c3 module=s164 theta=1.570796326795 amplitude=1.0 omega=0.0
module s165 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s165.c0 module=s165 theta=2.868704139573 amplitude=1.0 omega=0.0
cell s165.c1 module=s165 theta=1.514104570938 amplitude=1.0 omega=0.0
cell s165.c2 module=s165 theta=3.061093562417 amplitude=1.0 omega=0.0
cell s165.c3 module=s165 theta=3.141592653590 amplitude=1.0 omega=0.0
module s166 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s166.c0 module=s166 theta=0.925618146356 amplitude=1.0 omega=0.0
cell s166.c1 module=s166 theta=1.449024808836 amplitude=1.0 omega=0.0
cell s166.c2 module=s166 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s166.c3 module=s166 theta=1.570796326795 amplitude=1.0 omega=0.0
module s167 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s167.c0 module=s167 theta=1.676754982151 amplitude=1.0 omega=0.0
cell s167.c1 module=s167 theta=1.626930803004 amplitude=1.0 omega=0.0
cell s167.c2 module=s167 theta=2.894867213879 amplitude=1.0 omega=0.0
cell s167.c3 module=s167 theta=1.570796326795 amplitude=1.0 omega=0.0
module s168 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s168.c0 module=s168 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s168.c1 module=s168 theta=1.944618103575 amplitude=1.0 omega=0.0
cell s168.c2 module=s168 theta=0.156989513687 amplitude=1.0 omega=0.0
cell s168.c3 module=s168 theta=1.570796326795 amplitude=1.0 omega=0.0
module s169 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s169.c0 module=s169 theta=2.036999989445 amplitude=1.0 omega=0.0
cell s169.c1 module=s169 theta=1.607827233549 amplitude=1.0 omega=0.0
cell s169.c2 module=s169 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s169.c3 module=s169 theta=3.141592653590 amplitude=1.0 omega=0.0
module s170 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s170.c0 module=s170 theta=0.589351561503 amplitude=1.0 omega=0.0
cell s170.c1 module=s170 theta=1.868873232241 amplitude=1.0 omega=0.0
cell s170.c2 module=s170 theta=0.245674831339 amplitude=1.0 omega=0.0
cell s170.c3 module=s170 theta=1.570796326795 amplitude=1.0 omega=0.0
module s171 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s171.c0 module=s171 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s171.c1 module=s171 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s171.c2 module=s171 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s171.c3 module=s171 theta=3.141592653590 amplitude=1.0 omega=0.0
module s172 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s172.c0 module=s172 theta=1.325544592141 amplitude=1.0 omega=0.0
cell s172.c1 module=s172 theta=0.332478470344 amplitude=1.0 omega=0.0
cell s172.c2 module=s172 theta=0.150217566555 amplitude=1.0 omega=0.0
cell s172.c3 module=s172 theta=0.000000000000 amplitude=1.0 omega=0.0
module s173 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s173.c0 module=s173 theta=0.228374782254 amplitude=1.0 omega=0.0
cell s173.c1 module=s173 theta=1.682757409616 amplitude=1.0 omega=0.0
cell s173.c2 module=s173 theta=1.420951423799 amplitude=1.0 omega=0.0
cell s173.c3 module=s173 theta=1.570796326795 amplitude=1.0 omega=0.0
module s174 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s174.c0 module=s174 theta=1.711727848459 amplitude=1.0 omega=0.0
cell s174.c1 module=s174 theta=2.408973337643 amplitude=1.0 omega=0.0
cell s174.c2 module=s174 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s174.c3 module=s174 theta=3.141592653590 amplitude=1.0 omega=0.0
module s175 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s175.c0 module=s175 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s175.c1 module=s175 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s175.c2 module=s175 theta=0.335761645347 amplitude=1.0 omega=0.0
cell s175.c3 module=s175 theta=1.570796326795 amplitude=1.0 omega=0.0
module s176 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s176.c0 module=s176 theta=2.906950208049 amplitude=1.0 omega=0.0
cell s176.c1 module=s176 theta=1.347937883337 amplitude=1.0 omega=0.0
cell s176.c2 module=s176 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s176.c3 module=s176 theta=1.570796326795 amplitude=1.0 omega=0.0
module s177 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s177.c0 module=s177 theta=1.752467166545 amplitude=1.0 omega=0.0
cell s177.c1 module=s177 theta=1.362863581545 amplitude=1.0 omega=0.0
cell s177.c2 module=s177 theta=1.409662616954 amplitude=1.0 omega=0.0
cell s177.c3 module=s177 theta=1.570796326795 amplitude=1.0 omega=0.0
module s178 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s178.c0 module=s178 theta=1.331885820212 amplitude=1.0 omega=0.0
cell s178.c1 module=s178 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s178.c2 module=s178 theta=1.723813961817 amplitude=1.0 omega=0.0
cell s178.c3 module=s178 theta=3.141592653590 amplitude=1.0 omega=0.0
module s179 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s179.c0 module=s179 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s179.c1 module=s179 theta=1.731015792337 amplitude=1.0 omega=0.0
cell s179.c2 module=s179 theta=1.480717144269 amplitude=1.0 omega=0.0
cell s179.c3 module=s179 theta=1.570796326795 amplitude=1.0 omega=0.0
module s180 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s180.c0 module=s180 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s180.c1 module=s180 theta=0.284727466980 amplitude=1.0 omega=0.0
cell s180.c2 module=s180 theta=0.268695697715 amplitude=1.0 omega=0.0
cell s180.c3 module=s180 theta=0.000000000000 amplitude=1.0 omega=0.0
module s181 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s181.c0 module=s181 theta=1.627772219398 amplitude=1.0 omega=0.0
cell s181.c1 module=s181 theta=0.240722264437 amplitude=1.0 omega=0.0
cell s181.c2 module=s181 theta=1.602783158236 amplitude=1.0 omega=0.0
cell s181.c3 module=s181 theta=0.000000000000 amplitude=1.0 omega=0.0
module s182 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s182.c0 module=s182 theta=1.683666287672 amplitude=1.0 omega=0.0
cell s182.c1 module=s182 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s182.c2 module=s182 theta=1.368248507760 amplitude=1.0 omega=0.0
cell s182.c3 module=s182 theta=0.000000000000 amplitude=1.0 omega=0.0
module s183 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s183.c0 module=s183 theta=1.737787986339 amplitude=1.0 omega=0.0
cell s183.c1 module=s183 theta=1.374898513157 amplitude=1.0 omega=0.0
cell s183.c2 module=s183 theta=0.519285767190 amplitude=1.0 omega=0.0
cell s183.c3 module=s183 theta=1.570796326795 amplitude=1.0 omega=0.0
module s184 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s184.c0 module=s184 theta=0.003641288048 amplitude=1.0 omega=0.0
cell s184.c1 module=s184 theta=1.339037414850 amplitude=1.0 omega=0.0
cell s184.c2 module=s184 theta=1.166442814807 amplitude=1.0 omega=0.0
cell s184.c3 module=s184 theta=0.000000000000 amplitude=1.0 omega=0.0
module s185 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s185.c0 module=s185 theta=0.239100599252 amplitude=1.0 omega=0.0
cell s185.c1 module=s185 theta=1.585049593656 amplitude=1.0 omega=0.0
cell s185.c2 module=s185 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s185.c3 module=s185 theta=1.570796326795 amplitude=1.0 omega=0.0
module s186 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s186.c0 module=s186 theta=1.701225876732 amplitude=1.0 omega=0.0
cell s186.c1 module=s186 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s186.c2 module=s186 theta=1.736983205312 amplitude=1.0 omega=0.0
cell s186.c3 module=s186 theta=3.141592653590 amplitude=1.0 omega=0.0
module s187 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s187.c0 module=s187 theta=2.679218177687 amplitude=1.0 omega=0.0
cell s187.c1 module=s187 theta=1.328728450046 amplitude=1.0 omega=0.0
cell s187.c2 module=s187 theta=1.092101563635 amplitude=1.0 omega=0.0
cell s187.c3 module=s187 theta=1.570796326795 amplitude=1.0 omega=0.0
module s188 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s188.c0 module=s188 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s188.c1 module=s188 theta=1.523872281673 amplitude=1.0 omega=0.0
cell s188.c2 module=s188 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s188.c3 module=s188 theta=1.570796326795 amplitude=1.0 omega=0.0
module s189 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s189.c0 module=s189 theta=0.739809865639 amplitude=1.0 omega=0.0
cell s189.c1 module=s189 theta=1.595819524334 amplitude=1.0 omega=0.0
cell s189.c2 module=s189 theta=3.021103259168 amplitude=1.0 omega=0.0
cell s189.c3 module=s189 theta=1.570796326795 amplitude=1.0 omega=0.0
module s190 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s190.c0 module=s190 theta=1.368012298676 amplitude=1.0 omega=0.0
cell s190.c1 module=s190 theta=1.603860457805 amplitude=1.0 omega=0.0
cell s190.c2 module=s190 theta=1.526808808770 amplitude=1.0 omega=0.0
cell s190.c3 module=s190 theta=1.570796326795 amplitude=1.0 omega=0.0
module s191 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s191.c0 module=s191 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s191.c1 module=s191 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s191.c2 module=s191 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s191.c3 module=s191 theta=3.141592653590 amplitude=1.0 omega=0.0
module s192 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s192.c0 module=s192 theta=1.594019585854 amplitude=1.0 omega=0.0
cell s192.c1 module=s192 theta=1.465012583132 amplitude=1.0 omega=0.0
cell s192.c2 module=s192 theta=1.868044325247 amplitude=1.0 omega=0.0
cell s192.c3 module=s192 theta=1.570796326795 amplitude=1.0 omega=0.0
module s193 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s193.c0 module=s193 theta=2.385518317545 amplitude=1.0 omega=0.0
cell s193.c1 module=s193 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s193.c2 module=s193 theta=1.523462353308 amplitude=1.0 omega=0.0
cell s193.c3 module=s193 theta=0.000000000000 amplitude=1.0 omega=0.0
module s194 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s194.c0 module=s194 theta=2.903900902436 amplitude=1.0 omega=0.0
cell s194.c1 module=s194 theta=1.870322133092 amplitude=1.0 omega=0.0
cell s194.c2 module=s194 theta=1.483599215833 amplitude=1.0 omega=0.0
cell s194.c3 module=s194 theta=1.570796326795 amplitude=1.0 omega=0.0
module s195 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s195.c0 module=s195 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s195.c1 module=s195 theta=0.099563863082 amplitude=1.0 omega=0.0
cell s195.c2 module=s195 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s195.c3 module=s195 theta=0.000000000000 amplitude=1.0 omega=0.0
module s196 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s196.c0 module=s196 theta=1.375652644738 amplitude=1.0 omega=0.0
cell s196.c1 module=s196 theta=1.399518521739 amplitude=1.0 omega=0.0
cell s196.c2 module=s196 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s196.c3 module=s196 theta=1.570796326795 amplitude=1.0 omega=0.0
module s197 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s197.c0 module=s197 theta=1.728722243997 amplitude=1.0 omega=0.0
cell s197.c1 module=s197 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s197.c2 module=s197 theta=1.559256681889 amplitude=1.0 omega=0.0
cell s197.c3 module=s197 theta=3.141592653590 amplitude=1.0 omega=0.0
module s198 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s198.c0 module=s198 theta=2.860559883665 amplitude=1.0 omega=0.0
cell s198.c1 module=s198 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s198.c2 module=s198 theta=0.609668006016 amplitude=1.0 omega=0.0
cell s198.c3 module=s198 theta=0.000000000000 amplitude=1.0 omega=0.0
module s199 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s199.c0 module=s199 theta=1.420321519390 amplitude=1.0 omega=0.0
cell s199.c1 module=s199 theta=0.657688215316 amplitude=1.0 omega=0.0
cell s199.c2 module=s199 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s199.c3 module=s199 theta=1.570796326795 amplitude=1.0 omega=0.0
module s200 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s200.c0 module=s200 theta=3.061289611766 amplitude=1.0 omega=0.0
cell s200.c1 module=s200 theta=0.393519800506 amplitude=1.0 omega=0.0
cell s200.c2 module=s200 theta=0.441866692268 amplitude=1.0 omega=0.0
cell s200.c3 module=s200 theta=1.570796326795 amplitude=1.0 omega=0.0
module s201 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s201.c0 module=s201 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s201.c1 module=s201 theta=3.103905778734 amplitude=1.0 omega=0.0
cell s201.c2 module=s201 theta=3.137539486612 amplitude=1.0 omega=0.0
cell s201.c3 module=s201 theta=3.141592653590 amplitude=1.0 omega=0.0
module s202 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s202.c0 module=s202 theta=0.335673704073 amplitude=1.0 omega=0.0
cell s202.c1 module=s202 theta=1.843957480446 amplitude=1.0 omega=0.0
cell s202.c2 module=s202 theta=1.287380017597 amplitude=1.0 omega=0.0
cell s202.c3 module=s202 theta=1.570796326795 amplitude=1.0 omega=0.0
module s203 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s203.c0 module=s203 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s203.c1 module=s203 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s203.c2 module=s203 theta=1.496564345705 amplitude=1.0 omega=0.0
cell s203.c3 module=s203 theta=1.570796326795 amplitude=1.0 omega=0.0
module s204 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s204.c0 module=s204 theta=0.642036602788 amplitude=1.0 omega=0.0
cell s204.c1 module=s204 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s204.c2 module=s204 theta=2.805475696489 amplitude=1.0 omega=0.0
cell s204.c3 module=s204 theta=3.141592653590 amplitude=1.0 omega=0.0
module s205 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s205.c0 module=s205 theta=1.444484460631 amplitude=1.0 omega=0.0
cell s205.c1 module=s205 theta=1.408171427743 amplitude=1.0 omega=0.0
cell s205.c2 module=s205 theta=3.140640550130 amplitude=1.0 omega=0.0
cell s205.c3 module=s205 theta=1.570796326795 amplitude=1.0 omega=0.0
module s206 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s206.c0 module=s206 theta=2.157242333299 amplitude=1.0 omega=0.0
cell s206.c1 module=s206 theta=0.150225666471 amplitude=1.0 omega=0.0
cell s206.c2 module=s206 theta=1.686465213672 amplitude=1.0 omega=0.0
cell s206.c3 module=s206 theta=0.000000000000 amplitude=1.0 omega=0.0
module s207 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s207.c0 module=s207 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s207.c1 module=s207 theta=1.691603472680 amplitude=1.0 omega=0.0
cell s207.c2 module=s207 theta=0.643246064745 amplitude=1.0 omega=0.0
cell s207.c3 module=s207 theta=1.570796326795 amplitude=1.0 omega=0.0
module s208 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s208.c0 module=s208 theta=0.228914516043 amplitude=1.0 omega=0.0
cell s208.c1 module=s208 theta=2.698847520526 amplitude=1.0 omega=0.0
cell s208.c2 module=s208 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s208.c3 module=s208 theta=3.141592653590 amplitude=1.0 omega=0.0
module s209 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s209.c0 module=s209 theta=0.310636006427 amplitude=1.0 omega=0.0
cell s209.c1 module=s209 theta=1.293383322101 amplitude=1.0 omega=0.0
cell s209.c2 module=s209 theta=1.573642788694 amplitude=1.0 omega=0.0
cell s209.c3 module=s209 theta=1.570796326795 amplitude=1.0 omega=0.0
module s210 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s210.c0 module=s210 theta=0.150956892539 amplitude=1.0 omega=0.0
cell s210.c1 module=s210 theta=2.943775838813 amplitude=1.0 omega=0.0
cell s210.c2 module=s210 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s210.c3 module=s210 theta=3.141592653590 amplitude=1.0 omega=0.0
module s211 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s211.c0 module=s211 theta=1.146014547826 amplitude=1.0 omega=0.0
cell s211.c1 module=s211 theta=1.404710445316 amplitude=1.0 omega=0.0
cell s211.c2 module=s211 theta=2.755031056933 amplitude=1.0 omega=0.0
cell s211.c3 module=s211 theta=1.570796326795 amplitude=1.0 omega=0.0
module s212 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s212.c0 module=s212 theta=0.359249343112 amplitude=1.0 omega=0.0
cell s212.c1 module=s212 theta=1.409420677419 amplitude=1.0 omega=0.0
cell s212.c2 module=s212 theta=0.226635299891 amplitude=1.0 omega=0.0
cell s212.c3 module=s212 theta=0.000000000000 amplitude=1.0 omega=0.0
module s213 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s213.c0 module=s213 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s213.c1 module=s213 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s213.c2 module=s213 theta=0.164506007437 amplitude=1.0 omega=0.0
cell s213.c3 module=s213 theta=1.570796326795 amplitude=1.0 omega=0.0
module s214 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s214.c0 module=s214 theta=1.714453782852 amplitude=1.0 omega=0.0
cell s214.c1 module=s214 theta=3.119593525585 amplitude=1.0 omega=0.0
cell s214.c2 module=s214 theta=0.588307222190 amplitude=1.0 omega=0.0
cell s214.c3 module=s214 theta=3.141592653590 amplitude=1.0 omega=0.0
module s215 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s215.c0 module=s215 theta=0.095844483070 amplitude=1.0 omega=0.0
cell s215.c1 module=s215 theta=0.289589242189 amplitude=1.0 omega=0.0
cell s215.c2 module=s215 theta=1.401727310890 amplitude=1.0 omega=0.0
cell s215.c3 module=s215 theta=0.000000000000 amplitude=1.0 omega=0.0
module s216 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s216.c0 module=s216 theta=1.314920376252 amplitude=1.0 omega=0.0
cell s216.c1 module=s216 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s216.c2 module=s216 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s216.c3 module=s216 theta=3.141592653590 amplitude=1.0 omega=0.0
module s217 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s217.c0 module=s217 theta=1.846794876801 amplitude=1.0 omega=0.0
cell s217.c1 module=s217 theta=1.611578208410 amplitude=1.0 omega=0.0
cell s217.c2 module=s217 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s217.c3 module=s217 theta=1.570796326795 amplitude=1.0 omega=0.0
module s218 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s218.c0 module=s218 theta=0.135234301489 amplitude=1.0 omega=0.0
cell s218.c1 module=s218 theta=2.594207561196 amplitude=1.0 omega=0.0
cell s218.c2 module=s218 theta=2.501737129026 amplitude=1.0 omega=0.0
cell s218.c3 module=s218 theta=1.570796326795 amplitude=1.0 omega=0.0
module s219 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s219.c0 module=s219 theta=0.182918476683 amplitude=1.0 omega=0.0
cell s219.c1 module=s219 theta=3.006058835673 amplitude=1.0 omega=0.0
cell s219.c2 module=s219 theta=2.993776137430 amplitude=1.0 omega=0.0
cell s219.c3 module=s219 theta=3.141592653590 amplitude=1.0 omega=0.0
module s220 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s220.c0 module=s220 theta=0.194707420799 amplitude=1.0 omega=0.0
cell s220.c1 module=s220 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s220.c2 module=s220 theta=1.845850352604 amplitude=1.0 omega=0.0
cell s220.c3 module=s220 theta=1.570796326795 amplitude=1.0 omega=0.0
module s221 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s221.c0 module=s221 theta=0.021304415587 amplitude=1.0 omega=0.0
cell s221.c1 module=s221 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s221.c2 module=s221 theta=1.580072541821 amplitude=1.0 omega=0.0
cell s221.c3 module=s221 theta=1.570796326795 amplitude=1.0 omega=0.0
module s222 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s222.c0 module=s222 theta=0.965498654075 amplitude=1.0 omega=0.0
cell s222.c1 module=s222 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s222.c2 module=s222 theta=1.834428940564 amplitude=1.0 omega=0.0
cell s222.c3 module=s222 theta=0.000000000000 amplitude=1.0 omega=0.0
module s223 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s223.c0 module=s223 theta=0.026605774569 amplitude=1.0 omega=0.0
cell s223.c1 module=s223 theta=1.627135398989 amplitude=1.0 omega=0.0
cell s223.c2 module=s223 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s223.c3 module=s223 theta=0.000000000000 amplitude=1.0 omega=0.0
module s224 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s224.c0 module=s224 theta=2.989483981424 amplitude=1.0 omega=0.0
cell s224.c1 module=s224 theta=2.595317195998 amplitude=1.0 omega=0.0
cell s224.c2 module=s224 theta=2.063733070183 amplitude=1.0 omega=0.0
cell s224.c3 module=s224 theta=3.141592653590 amplitude=1.0 omega=0.0
module s225 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s225.c0 module=s225 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s225.c1 module=s225 theta=1.852285135345 amplitude=1.0 omega=0.0
cell s225.c2 module=s225 theta=1.483348118841 amplitude=1.0 omega=0.0
cell s225.c3 module=s225 theta=1.570796326795 amplitude=1.0 omega=0.0
module s226 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s226.c0 module=s226 theta=1.607971431964 amplitude=1.0 omega=0.0
cell s226.c1 module=s226 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s226.c2 module=s226 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s226.c3 module=s226 theta=3.141592653590 amplitude=1.0 omega=0.0
module s227 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s227.c0 module=s227 theta=1.829417913589 amplitude=1.0 omega=0.0
cell s227.c1 module=s227 theta=1.510722959507 amplitude=1.0 omega=0.0
cell s227.c2 module=s227 theta=1.746455052471 amplitude=1.0 omega=0.0
cell s227.c3 module=s227 theta=1.570796326795 amplitude=1.0 omega=0.0
module s228 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s228.c0 module=s228 theta=2.298862636130 amplitude=1.0 omega=0.0
cell s228.c1 module=s228 theta=1.539741727483 amplitude=1.0 omega=0.0
cell s228.c2 module=s228 theta=1.432339093418 amplitude=1.0 omega=0.0
cell s228.c3 module=s228 theta=1.570796326795 amplitude=1.0 omega=0.0
module s229 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s229.c0 module=s229 theta=3.073995212826 amplitude=1.0 omega=0.0
cell s229.c1 module=s229 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s229.c2 module=s229 theta=1.640105057908 amplitude=1.0 omega=0.0
cell s229.c3 module=s229 theta=3.141592653590 amplitude=1.0 omega=0.0
module s230 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s230.c0 module=s230 theta=1.615193063222 amplitude=1.0 omega=0.0
cell s230.c1 module=s230 theta=2.175711179141 amplitude=1.0 omega=0.0
cell s230.c2 module=s230 theta=1.517988874853 amplitude=1.0 omega=0.0
cell s230.c3 module=s230 theta=1.570796326795 amplitude=1.0 omega=0.0
module s231 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s231.c0 module=s231 theta=1.696012180916 amplitude=1.0 omega=0.0
cell s231.c1 module=s231 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s231.c2 module=s231 theta=0.127446542163 amplitude=1.0 omega=0.0
cell s231.c3 module=s231 theta=0.000000000000 amplitude=1.0 omega=0.0
module s232 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s232.c0 module=s232 theta=2.874475403201 amplitude=1.0 omega=0.0
cell s232.c1 module=s232 theta=1.714310010569 amplitude=1.0 omega=0.0
cell s232.c2 module=s232 theta=1.693531776489 amplitude=1.0 omega=0.0
cell s232.c3 module=s232 theta=1.570796326795 amplitude=1.0 omega=0.0
module s233 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s233.c0 module=s233 theta=1.306173245083 amplitude=1.0 omega=0.0
cell s233.c1 module=s233 theta=0.060766936250 amplitude=1.0 omega=0.0
cell s233.c2 module=s233 theta=1.508024308941 amplitude=1.0 omega=0.0
cell s233.c3 module=s233 theta=0.000000000000 amplitude=1.0 omega=0.0
module s234 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s234.c0 module=s234 theta=0.024015185716 amplitude=1.0 omega=0.0
cell s234.c1 module=s234 theta=1.467578813042 amplitude=1.0 omega=0.0
cell s234.c2 module=s234 theta=1.440170756003 amplitude=1.0 omega=0.0
cell s234.c3 module=s234 theta=1.570796326795 amplitude=1.0 omega=0.0
module s235 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s235.c0 module=s235 theta=0.283969277725 amplitude=1.0 omega=0.0
cell s235.c1 module=s235 theta=1.643836595450 amplitude=1.0 omega=0.0
cell s235.c2 module=s235 theta=2.298905759892 amplitude=1.0 omega=0.0
cell s235.c3 module=s235 theta=1.570796326795 amplitude=1.0 omega=0.0
module s236 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s236.c0 module=s236 theta=1.760553416415 amplitude=1.0 omega=0.0
cell s236.c1 module=s236 theta=2.684400485243 amplitude=1.0 omega=0.0
cell s236.c2 module=s236 theta=2.303840799002 amplitude=1.0 omega=0.0
cell s236.c3 module=s236 theta=3.141592653590 amplitude=1.0 omega=0.0
module s237 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s237.c0 module=s237 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s237.c1 module=s237 theta=2.906764905394 amplitude=1.0 omega=0.0
cell s237.c2 module=s237 theta=0.157770969726 amplitude=1.0 omega=0.0
cell s237.c3 module=s237 theta=1.570796326795 amplitude=1.0 omega=0.0
module s238 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s238.c0 module=s238 theta=1.644375961378 amplitude=1.0 omega=0.0
cell s238.c1 module=s238 theta=3.120977638199 amplitude=1.0 omega=0.0
cell s238.c2 module=s238 theta=2.612121658526 amplitude=1.0 omega=0.0
cell s238.c3 module=s238 theta=3.141592653590 amplitude=1.0 omega=0.0
module s239 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s239.c0 module=s239 theta=1.602862327194 amplitude=1.0 omega=0.0
cell s239.c1 module=s239 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s239.c2 module=s239 theta=1.376709713318 amplitude=1.0 omega=0.0
cell s239.c3 module=s239 theta=0.000000000000 amplitude=1.0 omega=0.0
module s240 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s240.c0 module=s240 theta=0.261567871495 amplitude=1.0 omega=0.0
cell s240.c1 module=s240 theta=1.389603953664 amplitude=1.0 omega=0.0
cell s240.c2 module=s240 theta=1.120139457248 amplitude=1.0 omega=0.0
cell s240.c3 module=s240 theta=0.000000000000 amplitude=1.0 omega=0.0
module s241 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s241.c0 module=s241 theta=2.841209237968 amplitude=1.0 omega=0.0
cell s241.c1 module=s241 theta=1.511516533861 amplitude=1.0 omega=0.0
cell s241.c2 module=s241 theta=1.720647737812 amplitude=1.0 omega=0.0
cell s241.c3 module=s241 theta=1.570796326795 amplitude=1.0 omega=0.0
module s242 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s242.c0 module=s242 theta=1.658819436134 amplitude=1.0 omega=0.0
cell s242.c1 module=s242 theta=1.486029375596 amplitude=1.0 omega=0.0
cell s242.c2 module=s242 theta=1.411514964362 amplitude=1.0 omega=0.0
cell s242.c3 module=s242 theta=1.570796326795 amplitude=1.0 omega=0.0
module s243 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s243.c0 module=s243 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s243.c1 module=s243 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s243.c2 module=s243 theta=0.200580860147 amplitude=1.0 omega=0.0
cell s243.c3 module=s243 theta=0.000000000000 amplitude=1.0 omega=0.0
module s244 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s244.c0 module=s244 theta=1.914706049206 amplitude=1.0 omega=0.0
cell s244.c1 module=s244 theta=3.068806337545 amplitude=1.0 omega=0.0
cell s244.c2 module=s244 theta=1.656498613555 amplitude=1.0 omega=0.0
cell s244.c3 module=s244 theta=3.141592653590 amplitude=1.0 omega=0.0
module s245 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s245.c0 module=s245 theta=1.531479454584 amplitude=1.0 omega=0.0
cell s245.c1 module=s245 theta=1.447067437066 amplitude=1.0 omega=0.0
cell s245.c2 module=s245 theta=2.908196421841 amplitude=1.0 omega=0.0
cell s245.c3 module=s245 theta=1.570796326795 amplitude=1.0 omega=0.0
module s246 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s246.c0 module=s246 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s246.c1 module=s246 theta=2.841217690308 amplitude=1.0 omega=0.0
cell s246.c2 module=s246 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s246.c3 module=s246 theta=1.570796326795 amplitude=1.0 omega=0.0
module s247 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s247.c0 module=s247 theta=0.067200101823 amplitude=1.0 omega=0.0
cell s247.c1 module=s247 theta=1.354871347384 amplitude=1.0 omega=0.0
cell s247.c2 module=s247 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s247.c3 module=s247 theta=1.570796326795 amplitude=1.0 omega=0.0
module s248 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s248.c0 module=s248 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s248.c1 module=s248 theta=2.887610508126 amplitude=1.0 omega=0.0
cell s248.c2 module=s248 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s248.c3 module=s248 theta=3.141592653590 amplitude=1.0 omega=0.0
module s249 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s249.c0 module=s249 theta=1.539511166521 amplitude=1.0 omega=0.0
cell s249.c1 module=s249 theta=2.817764067978 amplitude=1.0 omega=0.0
cell s249.c2 module=s249 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s249.c3 module=s249 theta=1.570796326795 amplitude=1.0 omega=0.0
module s250 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s250.c0 module=s250 theta=1.649931020602 amplitude=1.0 omega=0.0
cell s250.c1 module=s250 theta=1.164166091578 amplitude=1.0 omega=0.0
cell s250.c2 module=s250 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s250.c3 module=s250 theta=0.000000000000 amplitude=1.0 omega=0.0
module s251 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s251.c0 module=s251 theta=2.795023891127 amplitude=1.0 omega=0.0
cell s251.c1 module=s251 theta=0.346706429853 amplitude=1.0 omega=0.0
cell s251.c2 module=s251 theta=2.935356647435 amplitude=1.0 omega=0.0
cell s251.c3 module=s251 theta=1.570796326795 amplitude=1.0 omega=0.0
module s252 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s252.c0 module=s252 theta=0.237984258680 amplitude=1.0 omega=0.0
cell s252.c1 module=s252 theta=3.034010410764 amplitude=1.0 omega=0.0
cell s252.c2 module=s252 theta=1.667061663153 amplitude=1.0 omega=0.0
cell s252.c3 module=s252 theta=1.570796326795 amplitude=1.0 omega=0.0
module s253 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s253.c0 module=s253 theta=1.285364612827 amplitude=1.0 omega=0.0
cell s253.c1 module=s253 theta=2.179426904598 amplitude=1.0 omega=0.0
cell s253.c2 module=s253 theta=3.070195671773 amplitude=1.0 omega=0.0
cell s253.c3 module=s253 theta=3.141592653590 amplitude=1.0 omega=0.0
module s254 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s254.c0 module=s254 theta=1.843831082842 amplitude=1.0 omega=0.0
cell s254.c1 module=s254 theta=1.781021486231 amplitude=1.0 omega=0.0
cell s254.c2 module=s254 theta=0.502097311969 amplitude=1.0 omega=0.0
cell s254.c3 module=s254 theta=1.570796326795 amplitude=1.0 omega=0.0
module s255 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s255.c0 module=s255 theta=1.349131159027 amplitude=1.0 omega=0.0
cell s255.c1 module=s255 theta=2.055891314422 amplitude=1.0 omega=0.0
cell s255.c2 module=s255 theta=0.053017288532 amplitude=1.0 omega=0.0
cell s255.c3 module=s255 theta=1.570796326795 amplitude=1.0 omega=0.0
module s256 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s256.c0 module=s256 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s256.c1 module=s256 theta=2.957513767817 amplitude=1.0 omega=0.0
cell s256.c2 module=s256 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s256.c3 module=s256 theta=3.141592653590 amplitude=1.0 omega=0.0
module s257 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s257.c0 module=s257 theta=1.394342159003 amplitude=1.0 omega=0.0
cell s257.c1 module=s257 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s257.c2 module=s257 theta=3.128430648734 amplitude=1.0 omega=0.0
cell s257.c3 module=s257 theta=3.141592653590 amplitude=1.0 omega=0.0
module s258 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s258.c0 module=s258 theta=1.364620577873 amplitude=1.0 omega=0.0
cell s258.c1 module=s258 theta=0.216930600325 amplitude=1.0 omega=0.0
cell s258.c2 module=s258 theta=3.051030292677 amplitude=1.0 omega=0.0
cell s258.c3 module=s258 theta=1.570796326795 amplitude=1.0 omega=0.0
module s259 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s259.c0 module=s259 theta=1.902140632624 amplitude=1.0 omega=0.0
cell s259.c1 module=s259 theta=0.293973104568 amplitude=1.0 omega=0.0
cell s259.c2 module=s259 theta=0.642068513424 amplitude=1.0 omega=0.0
cell s259.c3 module=s259 theta=0.000000000000 amplitude=1.0 omega=0.0
module s260 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s260.c0 module=s260 theta=1.775320989954 amplitude=1.0 omega=0.0
cell s260.c1 module=s260 theta=1.513035084875 amplitude=1.0 omega=0.0
cell s260.c2 module=s260 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s260.c3 module=s260 theta=1.570796326795 amplitude=1.0 omega=0.0
module s261 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s261.c0 module=s261 theta=1.291693054370 amplitude=1.0 omega=0.0
cell s261.c1 module=s261 theta=1.378747503733 amplitude=1.0 omega=0.0
cell s261.c2 module=s261 theta=3.128506640451 amplitude=1.0 omega=0.0
cell s261.c3 module=s261 theta=1.570796326795 amplitude=1.0 omega=0.0
module s262 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s262.c0 module=s262 theta=3.109343379399 amplitude=1.0 omega=0.0
cell s262.c1 module=s262 theta=2.553704674908 amplitude=1.0 omega=0.0
cell s262.c2 module=s262 theta=1.525662168424 amplitude=1.0 omega=0.0
cell s262.c3 module=s262 theta=3.141592653590 amplitude=1.0 omega=0.0
module s263 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s263.c0 module=s263 theta=1.610641167965 amplitude=1.0 omega=0.0
cell s263.c1 module=s263 theta=1.863733859849 amplitude=1.0 omega=0.0
cell s263.c2 module=s263 theta=1.955933937068 amplitude=1.0 omega=0.0
cell s263.c3 module=s263 theta=1.570796326795 amplitude=1.0 omega=0.0
module s264 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s264.c0 module=s264 theta=1.457463666683 amplitude=1.0 omega=0.0
cell s264.c1 module=s264 theta=1.715441635137 amplitude=1.0 omega=0.0
cell s264.c2 module=s264 theta=2.809745648134 amplitude=1.0 omega=0.0
cell s264.c3 module=s264 theta=1.570796326795 amplitude=1.0 omega=0.0
module s265 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s265.c0 module=s265 theta=2.615707203465 amplitude=1.0 omega=0.0
cell s265.c1 module=s265 theta=1.370188815883 amplitude=1.0 omega=0.0
cell s265.c2 module=s265 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s265.c3 module=s265 theta=3.141592653590 amplitude=1.0 omega=0.0
module s266 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s266.c0 module=s266 theta=3.076656309093 amplitude=1.0 omega=0.0
cell s266.c1 module=s266 theta=1.704504082866 amplitude=1.0 omega=0.0
cell s266.c2 module=s266 theta=0.094581975625 amplitude=1.0 omega=0.0
cell s266.c3 module=s266 theta=1.570796326795 amplitude=1.0 omega=0.0
module s267 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s267.c0 module=s267 theta=1.297234422233 amplitude=1.0 omega=0.0
cell s267.c1 module=s267 theta=3.008719783465 amplitude=1.0 omega=0.0
cell s267.c2 module=s267 theta=0.168838039557 amplitude=1.0 omega=0.0
cell s267.c3 module=s267 theta=1.570796326795 amplitude=1.0 omega=0.0
module s268 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s268.c0 module=s268 theta=0.108917097082 amplitude=1.0 omega=0.0
cell s268.c1 module=s268 theta=1.549946688502 amplitude=1.0 omega=0.0
cell s268.c2 module=s268 theta=0.352450227071 amplitude=1.0 omega=0.0
cell s268.c3 module=s268 theta=0.000000000000 amplitude=1.0 omega=0.0
module s269 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s269.c0 module=s269 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s269.c1 module=s269 theta=1.569741938986 amplitude=1.0 omega=0.0
cell s269.c2 module=s269 theta=2.800135561954 amplitude=1.0 omega=0.0
cell s269.c3 module=s269 theta=1.570796326795 amplitude=1.0 omega=0.0
module s270 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s270.c0 module=s270 theta=1.630215231339 amplitude=1.0 omega=0.0
cell s270.c1 module=s270 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s270.c2 module=s270 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s270.c3 module=s270 theta=1.570796326795 amplitude=1.0 omega=0.0
module s271 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s271.c0 module=s271 theta=2.783263432783 amplitude=1.0 omega=0.0
cell s271.c1 module=s271 theta=1.391565141510 amplitude=1.0 omega=0.0
cell s271.c2 module=s271 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s271.c3 module=s271 theta=1.570796326795 amplitude=1.0 omega=0.0
module s272 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s272.c0 module=s272 theta=1.609158093528 amplitude=1.0 omega=0.0
cell s272.c1 module=s272 theta=2.220558666137 amplitude=1.0 omega=0.0
cell s272.c2 module=s272 theta=1.795500051441 amplitude=1.0 omega=0.0
cell s272.c3 module=s272 theta=1.570796326795 amplitude=1.0 omega=0.0
module s273 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s273.c0 module=s273 theta=0.287117348638 amplitude=1.0 omega=0.0
cell s273.c1 module=s273 theta=2.296321947279 amplitude=1.0 omega=0.0
cell s273.c2 module=s273 theta=1.845597112641 amplitude=1.0 omega=0.0
cell s273.c3 module=s273 theta=1.570796326795 amplitude=1.0 omega=0.0
module s274 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s274.c0 module=s274 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s274.c1 module=s274 theta=1.314608869034 amplitude=1.0 omega=0.0
cell s274.c2 module=s274 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s274.c3 module=s274 theta=1.570796326795 amplitude=1.0 omega=0.0
module s275 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s275.c0 module=s275 theta=2.495731768697 amplitude=1.0 omega=0.0
cell s275.c1 module=s275 theta=0.935038647623 amplitude=1.0 omega=0.0
cell s275.c2 module=s275 theta=1.274742743981 amplitude=1.0 omega=0.0
cell s275.c3 module=s275 theta=1.570796326795 amplitude=1.0 omega=0.0
module s276 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s276.c0 module=s276 theta=1.255619123668 amplitude=1.0 omega=0.0
cell s276.c1 module=s276 theta=1.301463504078 amplitude=1.0 omega=0.0
cell s276.c2 module=s276 theta=1.758058132594 amplitude=1.0 omega=0.0
cell s276.c3 module=s276 theta=1.570796326795 amplitude=1.0 omega=0.0
module s277 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s277.c0 module=s277 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s277.c1 module=s277 theta=1.734406794337 amplitude=1.0 omega=0.0
cell s277.c2 module=s277 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s277.c3 module=s277 theta=1.570796326795 amplitude=1.0 omega=0.0
module s278 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s278.c0 module=s278 theta=0.007472593235 amplitude=1.0 omega=0.0
cell s278.c1 module=s278 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s278.c2 module=s278 theta=0.199688260488 amplitude=1.0 omega=0.0
cell s278.c3 module=s278 theta=1.570796326795 amplitude=1.0 omega=0.0
module s279 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s279.c0 module=s279 theta=1.767110623259 amplitude=1.0 omega=0.0
cell s279.c1 module=s279 theta=1.496915753098 amplitude=1.0 omega=0.0
cell s279.c2 module=s279 theta=1.471518861215 amplitude=1.0 omega=0.0
cell s279.c3 module=s279 theta=1.570796326795 amplitude=1.0 omega=0.0
module s280 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s280.c0 module=s280 theta=1.769101506628 amplitude=1.0 omega=0.0
cell s280.c1 module=s280 theta=0.119645122545 amplitude=1.0 omega=0.0
cell s280.c2 module=s280 theta=0.031515514317 amplitude=1.0 omega=0.0
cell s280.c3 module=s280 theta=0.000000000000 amplitude=1.0 omega=0.0
module s281 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s281.c0 module=s281 theta=1.911689672947 amplitude=1.0 omega=0.0
cell s281.c1 module=s281 theta=1.728881548644 amplitude=1.0 omega=0.0
cell s281.c2 module=s281 theta=1.804036156128 amplitude=1.0 omega=0.0
cell s281.c3 module=s281 theta=1.570796326795 amplitude=1.0 omega=0.0
module s282 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s282.c0 module=s282 theta=1.378207561870 amplitude=1.0 omega=0.0
cell s282.c1 module=s282 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s282.c2 module=s282 theta=2.340668815370 amplitude=1.0 omega=0.0
cell s282.c3 module=s282 theta=0.000000000000 amplitude=1.0 omega=0.0
module s283 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s283.c0 module=s283 theta=1.657376892759 amplitude=1.0 omega=0.0
cell s283.c1 module=s283 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s283.c2 module=s283 theta=2.134221976065 amplitude=1.0 omega=0.0
cell s283.c3 module=s283 theta=3.141592653590 amplitude=1.0 omega=0.0
module s284 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s284.c0 module=s284 theta=1.308185330999 amplitude=1.0 omega=0.0
cell s284.c1 module=s284 theta=1.277303693226 amplitude=1.0 omega=0.0
cell s284.c2 module=s284 theta=2.936933827288 amplitude=1.0 omega=0.0
cell s284.c3 module=s284 theta=1.570796326795 amplitude=1.0 omega=0.0
module s285 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s285.c0 module=s285 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s285.c1 module=s285 theta=1.411505911226 amplitude=1.0 omega=0.0
cell s285.c2 module=s285 theta=1.461353467409 amplitude=1.0 omega=0.0
cell s285.c3 module=s285 theta=1.570796326795 amplitude=1.0 omega=0.0
module s286 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s286.c0 module=s286 theta=1.687063922945 amplitude=1.0 omega=0.0
cell s286.c1 module=s286 theta=0.328065569163 amplitude=1.0 omega=0.0
cell s286.c2 module=s286 theta=1.489407065711 amplitude=1.0 omega=0.0
cell s286.c3 module=s286 theta=0.000000000000 amplitude=1.0 omega=0.0
module s287 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s287.c0 module=s287 theta=1.453544798306 amplitude=1.0 omega=0.0
cell s287.c1 module=s287 theta=2.684542893678 amplitude=1.0 omega=0.0
cell s287.c2 module=s287 theta=0.012799997173 amplitude=1.0 omega=0.0
cell s287.c3 module=s287 theta=1.570796326795 amplitude=1.0 omega=0.0
module s288 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s288.c0 module=s288 theta=1.335354143456 amplitude=1.0 omega=0.0
cell s288.c1 module=s288 theta=2.871404250648 amplitude=1.0 omega=0.0
cell s288.c2 module=s288 theta=3.127729483511 amplitude=1.0 omega=0.0
cell s288.c3 module=s288 theta=3.141592653590 amplitude=1.0 omega=0.0
module s289 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s289.c0 module=s289 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s289.c1 module=s289 theta=1.645166499502 amplitude=1.0 omega=0.0
cell s289.c2 module=s289 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s289.c3 module=s289 theta=1.570796326795 amplitude=1.0 omega=0.0
module s290 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s290.c0 module=s290 theta=1.801221435253 amplitude=1.0 omega=0.0
cell s290.c1 module=s290 theta=0.192681594833 amplitude=1.0 omega=0.0
cell s290.c2 module=s290 theta=0.028914137799 amplitude=1.0 omega=0.0
cell s290.c3 module=s290 theta=0.000000000000 amplitude=1.0 omega=0.0
module s291 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s291.c0 module=s291 theta=0.174226853162 amplitude=1.0 omega=0.0
cell s291.c1 module=s291 theta=3.128577354537 amplitude=1.0 omega=0.0
cell s291.c2 module=s291 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s291.c3 module=s291 theta=3.141592653590 amplitude=1.0 omega=0.0
module s292 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s292.c0 module=s292 theta=1.237612383553 amplitude=1.0 omega=0.0
cell s292.c1 module=s292 theta=1.284962477581 amplitude=1.0 omega=0.0
cell s292.c2 module=s292 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s292.c3 module=s292 theta=1.570796326795 amplitude=1.0 omega=0.0
module s293 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s293.c0 module=s293 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s293.c1 module=s293 theta=1.260012054877 amplitude=1.0 omega=0.0
cell s293.c2 module=s293 theta=0.806819173056 amplitude=1.0 omega=0.0
cell s293.c3 module=s293 theta=0.000000000000 amplitude=1.0 omega=0.0
module s294 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s294.c0 module=s294 theta=2.742616864422 amplitude=1.0 omega=0.0
cell s294.c1 module=s294 theta=0.955577528356 amplitude=1.0 omega=0.0
cell s294.c2 module=s294 theta=0.165897807891 amplitude=1.0 omega=0.0
cell s294.c3 module=s294 theta=1.570796326795 amplitude=1.0 omega=0.0
module s295 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s295.c0 module=s295 theta=1.374266487132 amplitude=1.0 omega=0.0
cell s295.c1 module=s295 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s295.c2 module=s295 theta=2.647177001205 amplitude=1.0 omega=0.0
cell s295.c3 module=s295 theta=3.141592653590 amplitude=1.0 omega=0.0
module s296 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s296.c0 module=s296 theta=1.420328432899 amplitude=1.0 omega=0.0
cell s296.c1 module=s296 theta=3.127443031747 amplitude=1.0 omega=0.0
cell s296.c2 module=s296 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s296.c3 module=s296 theta=3.141592653590 amplitude=1.0 omega=0.0
module s297 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s297.c0 module=s297 theta=0.177383961142 amplitude=1.0 omega=0.0
cell s297.c1 module=s297 theta=1.656163981854 amplitude=1.0 omega=0.0
cell s297.c2 module=s297 theta=1.563343393165 amplitude=1.0 omega=0.0
cell s297.c3 module=s297 theta=1.570796326795 amplitude=1.0 omega=0.0
module s298 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s298.c0 module=s298 theta=2.090769360849 amplitude=1.0 omega=0.0
cell s298.c1 module=s298 theta=1.551316345528 amplitude=1.0 omega=0.0
cell s298.c2 module=s298 theta=1.728420842980 amplitude=1.0 omega=0.0
cell s298.c3 module=s298 theta=1.570796326795 amplitude=1.0 omega=0.0
module s299 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s299.c0 module=s299 theta=0.973685699830 amplitude=1.0 omega=0.0
cell s299.c1 module=s299 theta=1.303746587903 amplitude=1.0 omega=0.0
cell s299.c2 module=s299 theta=1.858609815531 amplitude=1.0 omega=0.0
cell s299.c3 module=s299 theta=1.570796326795 amplitude=1.0 omega=0.0
module s300 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s300.c0 module=s300 theta=2.896066882728 amplitude=1.0 omega=0.0
cell s300.c1 module=s300 theta=1.732949908045 amplitude=1.0 omega=0.0
cell s300.c2 module=s300 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s300.c3 module=s300 theta=3.141592653590 amplitude=1.0 omega=0.0
module s301 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s301.c0 module=s301 theta=0.302276506792 amplitude=1.0 omega=0.0
cell s301.c1 module=s301 theta=3.120852928200 amplitude=1.0 omega=0.0
cell s301.c2 module=s301 theta=0.155035714231 amplitude=1.0 omega=0.0
cell s301.c3 module=s301 theta=1.570796326795 amplitude=1.0 omega=0.0
module s302 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s302.c0 module=s302 theta=1.984686898199 amplitude=1.0 omega=0.0
cell s302.c1 module=s302 theta=1.431024349365 amplitude=1.0 omega=0.0
cell s302.c2 module=s302 theta=1.628740636656 amplitude=1.0 omega=0.0
cell s302.c3 module=s302 theta=1.570796326795 amplitude=1.0 omega=0.0
module s303 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s303.c0 module=s303 theta=1.489957257411 amplitude=1.0 omega=0.0
cell s303.c1 module=s303 theta=0.800508385318 amplitude=1.0 omega=0.0
cell s303.c2 module=s303 theta=1.413423295498 amplitude=1.0 omega=0.0
cell s303.c3 module=s303 theta=1.570796326795 amplitude=1.0 omega=0.0
module s304 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s304.c0 module=s304 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s304.c1 module=s304 theta=0.183891612104 amplitude=1.0 omega=0.0
cell s304.c2 module=s304 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s304.c3 module=s304 theta=0.000000000000 amplitude=1.0 omega=0.0
module s305 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s305.c0 module=s305 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s305.c1 module=s305 theta=2.796882719015 amplitude=1.0 omega=0.0
cell s305.c2 module=s305 theta=1.712664877645 amplitude=1.0 omega=0.0
cell s305.c3 module=s305 theta=1.570796326795 amplitude=1.0 omega=0.0
module s306 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s306.c0 module=s306 theta=0.394207503027 amplitude=1.0 omega=0.0
cell s306.c1 module=s306 theta=0.179777462358 amplitude=1.0 omega=0.0
cell s306.c2 module=s306 theta=2.633475912502 amplitude=1.0 omega=0.0
cell s306.c3 module=s306 theta=0.000000000000 amplitude=1.0 omega=0.0
module s307 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s307.c0 module=s307 theta=2.630168238897 amplitude=1.0 omega=0.0
cell s307.c1 module=s307 theta=0.204526817286 amplitude=1.0 omega=0.0
cell s307.c2 module=s307 theta=0.691346096142 amplitude=1.0 omega=0.0
cell s307.c3 module=s307 theta=0.000000000000 amplitude=1.0 omega=0.0
module s308 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s308.c0 module=s308 theta=0.217619190745 amplitude=1.0 omega=0.0
cell s308.c1 module=s308 theta=0.134916719685 amplitude=1.0 omega=0.0
cell s308.c2 module=s308 theta=2.848845386847 amplitude=1.0 omega=0.0
cell s308.c3 module=s308 theta=0.000000000000 amplitude=1.0 omega=0.0
module s309 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s309.c0 module=s309 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s309.c1 module=s309 theta=0.019244458672 amplitude=1.0 omega=0.0
cell s309.c2 module=s309 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s309.c3 module=s309 theta=0.000000000000 amplitude=1.0 omega=0.0
module s310 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s310.c0 module=s310 theta=0.170520581994 amplitude=1.0 omega=0.0
cell s310.c1 module=s310 theta=1.393320775971 amplitude=1.0 omega=0.0
cell s310.c2 module=s310 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s310.c3 module=s310 theta=0.000000000000 amplitude=1.0 omega=0.0
module s311 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s311.c0 module=s311 theta=1.435836842633 amplitude=1.0 omega=0.0
cell s311.c1 module=s311 theta=1.600777879384 amplitude=1.0 omega=0.0
cell s311.c2 module=s311 theta=0.343104196204 amplitude=1.0 omega=0.0
cell s311.c3 module=s311 theta=1.570796326795 amplitude=1.0 omega=0.0
module s312 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s312.c0 module=s312 theta=2.341853901095 amplitude=1.0 omega=0.0
cell s312.c1 module=s312 theta=2.634661952809 amplitude=1.0 omega=0.0
cell s312.c2 module=s312 theta=1.350437628935 amplitude=1.0 omega=0.0
cell s312.c3 module=s312 theta=3.141592653590 amplitude=1.0 omega=0.0
module s313 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s313.c0 module=s313 theta=0.308603921516 amplitude=1.0 omega=0.0
cell s313.c1 module=s313 theta=3.057289875619 amplitude=1.0 omega=0.0
cell s313.c2 module=s313 theta=3.034289674949 amplitude=1.0 omega=0.0
cell s313.c3 module=s313 theta=3.141592653590 amplitude=1.0 omega=0.0
module s314 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s314.c0 module=s314 theta=2.705731069476 amplitude=1.0 omega=0.0
cell s314.c1 module=s314 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s314.c2 module=s314 theta=2.465886079580 amplitude=1.0 omega=0.0
cell s314.c3 module=s314 theta=3.141592653590 amplitude=1.0 omega=0.0
module s315 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s315.c0 module=s315 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s315.c1 module=s315 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s315.c2 module=s315 theta=0.326284524473 amplitude=1.0 omega=0.0
cell s315.c3 module=s315 theta=1.570796326795 amplitude=1.0 omega=0.0
module s316 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s316.c0 module=s316 theta=2.551433951399 amplitude=1.0 omega=0.0
cell s316.c1 module=s316 theta=1.649247757104 amplitude=1.0 omega=0.0
cell s316.c2 module=s316 theta=1.809451994610 amplitude=1.0 omega=0.0
cell s316.c3 module=s316 theta=1.570796326795 amplitude=1.0 omega=0.0
module s317 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s317.c0 module=s317 theta=0.933557182119 amplitude=1.0 omega=0.0
cell s317.c1 module=s317 theta=2.849654619570 amplitude=1.0 omega=0.0
cell s317.c2 module=s317 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s317.c3 module=s317 theta=1.570796326795 amplitude=1.0 omega=0.0
module s318 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s318.c0 module=s318 theta=0.579589940009 amplitude=1.0 omega=0.0
cell s318.c1 module=s318 theta=1.989981472554 amplitude=1.0 omega=0.0
cell s318.c2 module=s318 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s318.c3 module=s318 theta=1.570796326795 amplitude=1.0 omega=0.0
module s319 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s319.c0 module=s319 theta=1.768974931804 amplitude=1.0 omega=0.0
cell s319.c1 module=s319 theta=0.269448466600 amplitude=1.0 omega=0.0
cell s319.c2 module=s319 theta=3.119958158679 amplitude=1.0 omega=0.0
cell s319.c3 module=s319 theta=1.570796326795 amplitude=1.0 omega=0.0
module s320 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s320.c0 module=s320 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s320.c1 module=s320 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s320.c2 module=s320 theta=1.437997304849 amplitude=1.0 omega=0.0
cell s320.c3 module=s320 theta=1.570796326795 amplitude=1.0 omega=0.0
module s321 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s321.c0 module=s321 theta=0.122120306786 amplitude=1.0 omega=0.0
cell s321.c1 module=s321 theta=2.344542602499 amplitude=1.0 omega=0.0
cell s321.c2 module=s321 theta=0.334810726162 amplitude=1.0 omega=0.0
cell s321.c3 module=s321 theta=1.570796326795 amplitude=1.0 omega=0.0
module s322 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s322.c0 module=s322 theta=2.900997852287 amplitude=1.0 omega=0.0
cell s322.c1 module=s322 theta=0.209193645506 amplitude=1.0 omega=0.0
cell s322.c2 module=s322 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s322.c3 module=s322 theta=1.570796326795 amplitude=1.0 omega=0.0
module s323 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s323.c0 module=s323 theta=0.833833830688 amplitude=1.0 omega=0.0
cell s323.c1 module=s323 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s323.c2 module=s323 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s323.c3 module=s323 theta=1.570796326795 amplitude=1.0 omega=0.0
module s324 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s324.c0 module=s324 theta=1.399291869131 amplitude=1.0 omega=0.0
cell s324.c1 module=s324 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s324.c2 module=s324 theta=0.303328736042 amplitude=1.0 omega=0.0
cell s324.c3 module=s324 theta=0.000000000000 amplitude=1.0 omega=0.0
module s325 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s325.c0 module=s325 theta=0.290628702737 amplitude=1.0 omega=0.0
cell s325.c1 module=s325 theta=1.357303429757 amplitude=1.0 omega=0.0
cell s325.c2 module=s325 theta=2.889886425124 amplitude=1.0 omega=0.0
cell s325.c3 module=s325 theta=1.570796326795 amplitude=1.0 omega=0.0
module s326 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s326.c0 module=s326 theta=0.460621721350 amplitude=1.0 omega=0.0
cell s326.c1 module=s326 theta=1.391093577039 amplitude=1.0 omega=0.0
cell s326.c2 module=s326 theta=3.112009112250 amplitude=1.0 omega=0.0
cell s326.c3 module=s326 theta=1.570796326795 amplitude=1.0 omega=0.0
module s327 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s327.c0 module=s327 theta=1.824415848771 amplitude=1.0 omega=0.0
cell s327.c1 module=s327 theta=2.957431731098 amplitude=1.0 omega=0.0
cell s327.c2 module=s327 theta=2.898784328249 amplitude=1.0 omega=0.0
cell s327.c3 module=s327 theta=3.141592653590 amplitude=1.0 omega=0.0
module s328 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s328.c0 module=s328 theta=0.041147745148 amplitude=1.0 omega=0.0
cell s328.c1 module=s328 theta=0.982192128115 amplitude=1.0 omega=0.0
cell s328.c2 module=s328 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s328.c3 module=s328 theta=0.000000000000 amplitude=1.0 omega=0.0
module s329 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s329.c0 module=s329 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s329.c1 module=s329 theta=1.427564922341 amplitude=1.0 omega=0.0
cell s329.c2 module=s329 theta=1.721731385682 amplitude=1.0 omega=0.0
cell s329.c3 module=s329 theta=1.570796326795 amplitude=1.0 omega=0.0
module s330 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s330.c0 module=s330 theta=0.226553865543 amplitude=1.0 omega=0.0
cell s330.c1 module=s330 theta=1.741188966317 amplitude=1.0 omega=0.0
cell s330.c2 module=s330 theta=1.502024336334 amplitude=1.0 omega=0.0
cell s330.c3 module=s330 theta=1.570796326795 amplitude=1.0 omega=0.0
module s331 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s331.c0 module=s331 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s331.c1 module=s331 theta=1.842304003689 amplitude=1.0 omega=0.0
cell s331.c2 module=s331 theta=2.796053171378 amplitude=1.0 omega=0.0
cell s331.c3 module=s331 theta=1.570796326795 amplitude=1.0 omega=0.0
module s332 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s332.c0 module=s332 theta=0.352448961601 amplitude=1.0 omega=0.0
cell s332.c1 module=s332 theta=2.248305298316 amplitude=1.0 omega=0.0
cell s332.c2 module=s332 theta=1.950231285563 amplitude=1.0 omega=0.0
cell s332.c3 module=s332 theta=1.570796326795 amplitude=1.0 omega=0.0
module s333 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s333.c0 module=s333 theta=1.492974025515 amplitude=1.0 omega=0.0
cell s333.c1 module=s333 theta=2.068637838655 amplitude=1.0 omega=0.0
cell s333.c2 module=s333 theta=1.654517194102 amplitude=1.0 omega=0.0
cell s333.c3 module=s333 theta=1.570796326795 amplitude=1.0 omega=0.0
module s334 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s334.c0 module=s334 theta=0.282722546703 amplitude=1.0 omega=0.0
cell s334.c1 module=s334 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s334.c2 module=s334 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s334.c3 module=s334 theta=0.000000000000 amplitude=1.0 omega=0.0
module s335 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s335.c0 module=s335 theta=1.747096742355 amplitude=1.0 omega=0.0
cell s335.c1 module=s335 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s335.c2 module=s335 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s335.c3 module=s335 theta=1.570796326795 amplitude=1.0 omega=0.0
module s336 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s336.c0 module=s336 theta=0.312461872836 amplitude=1.0 omega=0.0
cell s336.c1 module=s336 theta=1.418336639524 amplitude=1.0 omega=0.0
cell s336.c2 module=s336 theta=2.401730925341 amplitude=1.0 omega=0.0
cell s336.c3 module=s336 theta=1.570796326795 amplitude=1.0 omega=0.0
module s337 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s337.c0 module=s337 theta=1.788052799445 amplitude=1.0 omega=0.0
cell s337.c1 module=s337 theta=2.965171263748 amplitude=1.0 omega=0.0
cell s337.c2 module=s337 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s337.c3 module=s337 theta=3.141592653590 amplitude=1.0 omega=0.0
module s338 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s338.c0 module=s338 theta=1.405295807995 amplitude=1.0 omega=0.0
cell s338.c1 module=s338 theta=2.897595724938 amplitude=1.0 omega=0.0
cell s338.c2 module=s338 theta=1.482828679335 amplitude=1.0 omega=0.0
cell s338.c3 module=s338 theta=3.141592653590 amplitude=1.0 omega=0.0
module s339 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s339.c0 module=s339 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s339.c1 module=s339 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s339.c2 module=s339 theta=0.330529008104 amplitude=1.0 omega=0.0
cell s339.c3 module=s339 theta=0.000000000000 amplitude=1.0 omega=0.0
module s340 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s340.c0 module=s340 theta=0.604718960102 amplitude=1.0 omega=0.0
cell s340.c1 module=s340 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s340.c2 module=s340 theta=0.622239037424 amplitude=1.0 omega=0.0
cell s340.c3 module=s340 theta=0.000000000000 amplitude=1.0 omega=0.0
module s341 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s341.c0 module=s341 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s341.c1 module=s341 theta=1.491655744221 amplitude=1.0 omega=0.0
cell s341.c2 module=s341 theta=2.638809690328 amplitude=1.0 omega=0.0
cell s341.c3 module=s341 theta=1.570796326795 amplitude=1.0 omega=0.0
module s342 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s342.c0 module=s342 theta=1.298465263917 amplitude=1.0 omega=0.0
cell s342.c1 module=s342 theta=1.781010130586 amplitude=1.0 omega=0.0
cell s342.c2 module=s342 theta=1.051834724282 amplitude=1.0 omega=0.0
cell s342.c3 module=s342 theta=1.570796326795 amplitude=1.0 omega=0.0
module s343 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s343.c0 module=s343 theta=0.125226005446 amplitude=1.0 omega=0.0
cell s343.c1 module=s343 theta=0.562249375610 amplitude=1.0 omega=0.0
cell s343.c2 module=s343 theta=2.826359688457 amplitude=1.0 omega=0.0
cell s343.c3 module=s343 theta=0.000000000000 amplitude=1.0 omega=0.0
module s344 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s344.c0 module=s344 theta=1.503744504238 amplitude=1.0 omega=0.0
cell s344.c1 module=s344 theta=0.024150168483 amplitude=1.0 omega=0.0
cell s344.c2 module=s344 theta=0.091845286825 amplitude=1.0 omega=0.0
cell s344.c3 module=s344 theta=0.000000000000 amplitude=1.0 omega=0.0
module s345 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s345.c0 module=s345 theta=1.562496336480 amplitude=1.0 omega=0.0
cell s345.c1 module=s345 theta=1.017549450789 amplitude=1.0 omega=0.0
cell s345.c2 module=s345 theta=1.690451371995 amplitude=1.0 omega=0.0
cell s345.c3 module=s345 theta=1.570796326795 amplitude=1.0 omega=0.0
module s346 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s346.c0 module=s346 theta=1.190278928126 amplitude=1.0 omega=0.0
cell s346.c1 module=s346 theta=1.497552139838 amplitude=1.0 omega=0.0
cell s346.c2 module=s346 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s346.c3 module=s346 theta=0.000000000000 amplitude=1.0 omega=0.0
module s347 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s347.c0 module=s347 theta=1.651865529739 amplitude=1.0 omega=0.0
cell s347.c1 module=s347 theta=1.564487906725 amplitude=1.0 omega=0.0
cell s347.c2 module=s347 theta=2.763936670131 amplitude=1.0 omega=0.0
cell s347.c3 module=s347 theta=1.570796326795 amplitude=1.0 omega=0.0
module s348 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s348.c0 module=s348 theta=1.754134662696 amplitude=1.0 omega=0.0
cell s348.c1 module=s348 theta=1.715956594469 amplitude=1.0 omega=0.0
cell s348.c2 module=s348 theta=1.867245090647 amplitude=1.0 omega=0.0
cell s348.c3 module=s348 theta=1.570796326795 amplitude=1.0 omega=0.0
module s349 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s349.c0 module=s349 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s349.c1 module=s349 theta=3.101091829718 amplitude=1.0 omega=0.0
cell s349.c2 module=s349 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s349.c3 module=s349 theta=3.141592653590 amplitude=1.0 omega=0.0
module s350 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s350.c0 module=s350 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s350.c1 module=s350 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s350.c2 module=s350 theta=0.097741372908 amplitude=1.0 omega=0.0
cell s350.c3 module=s350 theta=3.141592653590 amplitude=1.0 omega=0.0
module s351 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s351.c0 module=s351 theta=3.000839405210 amplitude=1.0 omega=0.0
cell s351.c1 module=s351 theta=3.120483834839 amplitude=1.0 omega=0.0
cell s351.c2 module=s351 theta=2.795447909370 amplitude=1.0 omega=0.0
cell s351.c3 module=s351 theta=3.141592653590 amplitude=1.0 omega=0.0
module s352 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s352.c0 module=s352 theta=0.912784538288 amplitude=1.0 omega=0.0
cell s352.c1 module=s352 theta=1.834894105997 amplitude=1.0 omega=0.0
cell s352.c2 module=s352 theta=0.112073453927 amplitude=1.0 omega=0.0
cell s352.c3 module=s352 theta=1.570796326795 amplitude=1.0 omega=0.0
module s353 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s353.c0 module=s353 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s353.c1 module=s353 theta=0.869043865621 amplitude=1.0 omega=0.0
cell s353.c2 module=s353 theta=1.287440312538 amplitude=1.0 omega=0.0
cell s353.c3 module=s353 theta=1.570796326795 amplitude=1.0 omega=0.0
module s354 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s354.c0 module=s354 theta=2.801735190056 amplitude=1.0 omega=0.0
cell s354.c1 module=s354 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s354.c2 module=s354 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s354.c3 module=s354 theta=3.141592653590 amplitude=1.0 omega=0.0
module s355 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s355.c0 module=s355 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s355.c1 module=s355 theta=1.738854937012 amplitude=1.0 omega=0.0
cell s355.c2 module=s355 theta=2.087943843162 amplitude=1.0 omega=0.0
cell s355.c3 module=s355 theta=1.570796326795 amplitude=1.0 omega=0.0
module s356 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s356.c0 module=s356 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s356.c1 module=s356 theta=3.116689970625 amplitude=1.0 omega=0.0
cell s356.c2 module=s356 theta=1.475540504447 amplitude=1.0 omega=0.0
cell s356.c3 module=s356 theta=3.141592653590 amplitude=1.0 omega=0.0
module s357 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s357.c0 module=s357 theta=1.347345559688 amplitude=1.0 omega=0.0
cell s357.c1 module=s357 theta=2.924814558590 amplitude=1.0 omega=0.0
cell s357.c2 module=s357 theta=0.480619274002 amplitude=1.0 omega=0.0
cell s357.c3 module=s357 theta=1.570796326795 amplitude=1.0 omega=0.0
module s358 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s358.c0 module=s358 theta=1.822018447063 amplitude=1.0 omega=0.0
cell s358.c1 module=s358 theta=1.405962271970 amplitude=1.0 omega=0.0
cell s358.c2 module=s358 theta=0.556396318691 amplitude=1.0 omega=0.0
cell s358.c3 module=s358 theta=1.570796326795 amplitude=1.0 omega=0.0
module s359 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s359.c0 module=s359 theta=2.398912122092 amplitude=1.0 omega=0.0
cell s359.c1 module=s359 theta=1.205760880331 amplitude=1.0 omega=0.0
cell s359.c2 module=s359 theta=2.926961019173 amplitude=1.0 omega=0.0
cell s359.c3 module=s359 theta=1.570796326795 amplitude=1.0 omega=0.0
module s360 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s360.c0 module=s360 theta=2.610041569536 amplitude=1.0 omega=0.0
cell s360.c1 module=s360 theta=1.317873408607 amplitude=1.0 omega=0.0
cell s360.c2 module=s360 theta=2.963686975864 amplitude=1.0 omega=0.0
cell s360.c3 module=s360 theta=1.570796326795 amplitude=1.0 omega=0.0
module s361 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s361.c0 module=s361 theta=1.422827041739 amplitude=1.0 omega=0.0
cell s361.c1 module=s361 theta=2.932471479111 amplitude=1.0 omega=0.0
cell s361.c2 module=s361 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s361.c3 module=s361 theta=1.570796326795 amplitude=1.0 omega=0.0
module s362 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s362.c0 module=s362 theta=1.815380326206 amplitude=1.0 omega=0.0
cell s362.c1 module=s362 theta=1.153942814527 amplitude=1.0 omega=0.0
cell s362.c2 module=s362 theta=1.803154976105 amplitude=1.0 omega=0.0
cell s362.c3 module=s362 theta=1.570796326795 amplitude=1.0 omega=0.0
module s363 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s363.c0 module=s363 theta=2.449450506017 amplitude=1.0 omega=0.0
cell s363.c1 module=s363 theta=2.066468797050 amplitude=1.0 omega=0.0
cell s363.c2 module=s363 theta=1.071887021102 amplitude=1.0 omega=0.0
cell s363.c3 module=s363 theta=1.570796326795 amplitude=1.0 omega=0.0
module s364 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s364.c0 module=s364 theta=1.636285815435 amplitude=1.0 omega=0.0
cell s364.c1 module=s364 theta=1.089882359054 amplitude=1.0 omega=0.0
cell s364.c2 module=s364 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s364.c3 module=s364 theta=1.570796326795 amplitude=1.0 omega=0.0
module s365 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s365.c0 module=s365 theta=0.691496370523 amplitude=1.0 omega=0.0
cell s365.c1 module=s365 theta=0.825793589638 amplitude=1.0 omega=0.0
cell s365.c2 module=s365 theta=0.280826934458 amplitude=1.0 omega=0.0
cell s365.c3 module=s365 theta=0.000000000000 amplitude=1.0 omega=0.0
module s366 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s366.c0 module=s366 theta=2.990781593165 amplitude=1.0 omega=0.0
cell s366.c1 module=s366 theta=1.741706830078 amplitude=1.0 omega=0.0
cell s366.c2 module=s366 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s366.c3 module=s366 theta=3.141592653590 amplitude=1.0 omega=0.0
module s367 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s367.c0 module=s367 theta=1.175382624844 amplitude=1.0 omega=0.0
cell s367.c1 module=s367 theta=1.673133152591 amplitude=1.0 omega=0.0
cell s367.c2 module=s367 theta=2.810711876127 amplitude=1.0 omega=0.0
cell s367.c3 module=s367 theta=1.570796326795 amplitude=1.0 omega=0.0
module s368 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s368.c0 module=s368 theta=1.397430644351 amplitude=1.0 omega=0.0
cell s368.c1 module=s368 theta=1.348094693958 amplitude=1.0 omega=0.0
cell s368.c2 module=s368 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s368.c3 module=s368 theta=0.000000000000 amplitude=1.0 omega=0.0
module s369 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s369.c0 module=s369 theta=0.673561252284 amplitude=1.0 omega=0.0
cell s369.c1 module=s369 theta=3.040294739422 amplitude=1.0 omega=0.0
cell s369.c2 module=s369 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s369.c3 module=s369 theta=1.570796326795 amplitude=1.0 omega=0.0
module s370 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s370.c0 module=s370 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s370.c1 module=s370 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s370.c2 module=s370 theta=0.074950266334 amplitude=1.0 omega=0.0
cell s370.c3 module=s370 theta=0.000000000000 amplitude=1.0 omega=0.0
module s371 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s371.c0 module=s371 theta=0.792303411934 amplitude=1.0 omega=0.0
cell s371.c1 module=s371 theta=0.280308996698 amplitude=1.0 omega=0.0
cell s371.c2 module=s371 theta=2.451730623417 amplitude=1.0 omega=0.0
cell s371.c3 module=s371 theta=0.000000000000 amplitude=1.0 omega=0.0
module s372 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s372.c0 module=s372 theta=2.966489729519 amplitude=1.0 omega=0.0
cell s372.c1 module=s372 theta=0.904222274277 amplitude=1.0 omega=0.0
cell s372.c2 module=s372 theta=0.144226401104 amplitude=1.0 omega=0.0
cell s372.c3 module=s372 theta=1.570796326795 amplitude=1.0 omega=0.0
module s373 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s373.c0 module=s373 theta=1.424825571531 amplitude=1.0 omega=0.0
cell s373.c1 module=s373 theta=1.836209293896 amplitude=1.0 omega=0.0
cell s373.c2 module=s373 theta=2.978581431941 amplitude=1.0 omega=0.0
cell s373.c3 module=s373 theta=1.570796326795 amplitude=1.0 omega=0.0
module s374 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s374.c0 module=s374 theta=1.436210340418 amplitude=1.0 omega=0.0
cell s374.c1 module=s374 theta=1.545993191496 amplitude=1.0 omega=0.0
cell s374.c2 module=s374 theta=0.369678052197 amplitude=1.0 omega=0.0
cell s374.c3 module=s374 theta=1.570796326795 amplitude=1.0 omega=0.0
module s375 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s375.c0 module=s375 theta=2.084339198252 amplitude=1.0 omega=0.0
cell s375.c1 module=s375 theta=1.463170130070 amplitude=1.0 omega=0.0
cell s375.c2 module=s375 theta=1.348656599733 amplitude=1.0 omega=0.0
cell s375.c3 module=s375 theta=1.570796326795 amplitude=1.0 omega=0.0
module s376 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s376.c0 module=s376 theta=3.111343932860 amplitude=1.0 omega=0.0
cell s376.c1 module=s376 theta=1.769286387957 amplitude=1.0 omega=0.0
cell s376.c2 module=s376 theta=0.227896702516 amplitude=1.0 omega=0.0
cell s376.c3 module=s376 theta=1.570796326795 amplitude=1.0 omega=0.0
module s377 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s377.c0 module=s377 theta=1.804855643406 amplitude=1.0 omega=0.0
cell s377.c1 module=s377 theta=1.004490899051 amplitude=1.0 omega=0.0
cell s377.c2 module=s377 theta=1.119396564424 amplitude=1.0 omega=0.0
cell s377.c3 module=s377 theta=1.570796326795 amplitude=1.0 omega=0.0
module s378 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s378.c0 module=s378 theta=3.064558771127 amplitude=1.0 omega=0.0
cell s378.c1 module=s378 theta=1.560081332417 amplitude=1.0 omega=0.0
cell s378.c2 module=s378 theta=1.566309426525 amplitude=1.0 omega=0.0
cell s378.c3 module=s378 theta=1.570796326795 amplitude=1.0 omega=0.0
module s379 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s379.c0 module=s379 theta=0.875218041636 amplitude=1.0 omega=0.0
cell s379.c1 module=s379 theta=0.791521488474 amplitude=1.0 omega=0.0
cell s379.c2 module=s379 theta=2.903621843306 amplitude=1.0 omega=0.0
cell s379.c3 module=s379 theta=1.570796326795 amplitude=1.0 omega=0.0
module s380 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s380.c0 module=s380 theta=2.971172602274 amplitude=1.0 omega=0.0
cell s380.c1 module=s380 theta=1.299592479697 amplitude=1.0 omega=0.0
cell s380.c2 module=s380 theta=1.365456673457 amplitude=1.0 omega=0.0
cell s380.c3 module=s380 theta=1.570796326795 amplitude=1.0 omega=0.0
module s381 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s381.c0 module=s381 theta=1.153851050870 amplitude=1.0 omega=0.0
cell s381.c1 module=s381 theta=0.000735750817 amplitude=1.0 omega=0.0
cell s381.c2 module=s381 theta=3.084058596584 amplitude=1.0 omega=0.0
cell s381.c3 module=s381 theta=1.570796326795 amplitude=1.0 omega=0.0
module s382 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s382.c0 module=s382 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s382.c1 module=s382 theta=1.761124294816 amplitude=1.0 omega=0.0
cell s382.c2 module=s382 theta=1.602521682527 amplitude=1.0 omega=0.0
cell s382.c3 module=s382 theta=1.570796326795 amplitude=1.0 omega=0.0
module s383 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s383.c0 module=s383 theta=0.091711439184 amplitude=1.0 omega=0.0
cell s383.c1 module=s383 theta=1.486716406134 amplitude=1.0 omega=0.0
cell s383.c2 module=s383 theta=1.280680356005 amplitude=1.0 omega=0.0
cell s383.c3 module=s383 theta=1.570796326795 amplitude=1.0 omega=0.0
module s384 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s384.c0 module=s384 theta=1.369772061361 amplitude=1.0 omega=0.0
cell s384.c1 module=s384 theta=0.098339121074 amplitude=1.0 omega=0.0
cell s384.c2 module=s384 theta=1.159126008243 amplitude=1.0 omega=0.0
cell s384.c3 module=s384 theta=0.000000000000 amplitude=1.0 omega=0.0
module s385 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s385.c0 module=s385 theta=3.043745759056 amplitude=1.0 omega=0.0
cell s385.c1 module=s385 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s385.c2 module=s385 theta=2.718902022849 amplitude=1.0 omega=0.0
cell s385.c3 module=s385 theta=3.141592653590 amplitude=1.0 omega=0.0
module s386 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s386.c0 module=s386 theta=1.265065787995 amplitude=1.0 omega=0.0
cell s386.c1 module=s386 theta=2.849401269724 amplitude=1.0 omega=0.0
cell s386.c2 module=s386 theta=0.933743047998 amplitude=1.0 omega=0.0
cell s386.c3 module=s386 theta=1.570796326795 amplitude=1.0 omega=0.0
module s387 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s387.c0 module=s387 theta=1.001490685027 amplitude=1.0 omega=0.0
cell s387.c1 module=s387 theta=0.789090533301 amplitude=1.0 omega=0.0
cell s387.c2 module=s387 theta=3.135041840167 amplitude=1.0 omega=0.0
cell s387.c3 module=s387 theta=1.570796326795 amplitude=1.0 omega=0.0
module s388 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s388.c0 module=s388 theta=1.292555218677 amplitude=1.0 omega=0.0
cell s388.c1 module=s388 theta=0.630602016646 amplitude=1.0 omega=0.0
cell s388.c2 module=s388 theta=1.289875202046 amplitude=1.0 omega=0.0
cell s388.c3 module=s388 theta=0.000000000000 amplitude=1.0 omega=0.0
module s389 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s389.c0 module=s389 theta=1.354548487708 amplitude=1.0 omega=0.0
cell s389.c1 module=s389 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s389.c2 module=s389 theta=2.904892410185 amplitude=1.0 omega=0.0
cell s389.c3 module=s389 theta=3.141592653590 amplitude=1.0 omega=0.0
module s390 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s390.c0 module=s390 theta=1.530079928163 amplitude=1.0 omega=0.0
cell s390.c1 module=s390 theta=1.821240052515 amplitude=1.0 omega=0.0
cell s390.c2 module=s390 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s390.c3 module=s390 theta=1.570796326795 amplitude=1.0 omega=0.0
module s391 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s391.c0 module=s391 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s391.c1 module=s391 theta=1.457960728101 amplitude=1.0 omega=0.0
cell s391.c2 module=s391 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s391.c3 module=s391 theta=0.000000000000 amplitude=1.0 omega=0.0
module s392 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s392.c0 module=s392 theta=2.842037005996 amplitude=1.0 omega=0.0
cell s392.c1 module=s392 theta=1.014698793540 amplitude=1.0 omega=0.0
cell s392.c2 module=s392 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s392.c3 module=s392 theta=1.570796326795 amplitude=1.0 omega=0.0
module s393 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s393.c0 module=s393 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s393.c1 module=s393 theta=3.074231956523 amplitude=1.0 omega=0.0
cell s393.c2 module=s393 theta=1.821605976956 amplitude=1.0 omega=0.0
cell s393.c3 module=s393 theta=3.141592653590 amplitude=1.0 omega=0.0
module s394 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s394.c0 module=s394 theta=1.576247333762 amplitude=1.0 omega=0.0
cell s394.c1 module=s394 theta=2.989019965999 amplitude=1.0 omega=0.0
cell s394.c2 module=s394 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s394.c3 module=s394 theta=1.570796326795 amplitude=1.0 omega=0.0
module s395 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s395.c0 module=s395 theta=0.141709624067 amplitude=1.0 omega=0.0
cell s395.c1 module=s395 theta=0.359130166127 amplitude=1.0 omega=0.0
cell s395.c2 module=s395 theta=1.857787778978 amplitude=1.0 omega=0.0
cell s395.c3 module=s395 theta=0.000000000000 amplitude=1.0 omega=0.0
module s396 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s396.c0 module=s396 theta=1.874880489516 amplitude=1.0 omega=0.0
cell s396.c1 module=s396 theta=2.876624308701 amplitude=1.0 omega=0.0
cell s396.c2 module=s396 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s396.c3 module=s396 theta=1.570796326795 amplitude=1.0 omega=0.0
module s397 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s397.c0 module=s397 theta=0.121055839496 amplitude=1.0 omega=0.0
cell s397.c1 module=s397 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s397.c2 module=s397 theta=1.447995090200 amplitude=1.0 omega=0.0
cell s397.c3 module=s397 theta=0.000000000000 amplitude=1.0 omega=0.0
module s398 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s398.c0 module=s398 theta=1.490111290259 amplitude=1.0 omega=0.0
cell s398.c1 module=s398 theta=2.773927742371 amplitude=1.0 omega=0.0
cell s398.c2 module=s398 theta=2.839721646516 amplitude=1.0 omega=0.0
cell s398.c3 module=s398 theta=3.141592653590 amplitude=1.0 omega=0.0
module s399 field=scenes-train belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s399.c0 module=s399 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s399.c1 module=s399 theta=1.512375827399 amplitude=1.0 omega=0.0
cell s399.c2 module=s399 theta=1.427324619979 amplitude=1.0 omega=0.0
cell s399.c3 module=s399 theta=1.570796326795 amplitude=1.0 omega=0.0
