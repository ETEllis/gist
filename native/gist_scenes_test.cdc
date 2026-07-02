# gist_scenes_test.cdc -- native training data (phases-only).
# Each module: c0..c2 evidence phases, c3 the teacher label pole.
# Labels computed BY the C runtime: converged (40x0.25) fixed-
# pyramid singular. Deterministic generator seed 202.
field scenes-test dt=0.125 gain=1.0 deadband=0.5

module s0 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s0.c0 module=s0 theta=1.700090682884 amplitude=1.0 omega=0.0
cell s0.c1 module=s0 theta=1.775418192788 amplitude=1.0 omega=0.0
cell s0.c2 module=s0 theta=1.852412428699 amplitude=1.0 omega=0.0
cell s0.c3 module=s0 theta=1.570796326795 amplitude=1.0 omega=0.0
module s1 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s1.c0 module=s1 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s1.c1 module=s1 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s1.c2 module=s1 theta=1.420487653924 amplitude=1.0 omega=0.0
cell s1.c3 module=s1 theta=1.570796326795 amplitude=1.0 omega=0.0
module s2 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s2.c0 module=s2 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s2.c1 module=s2 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s2.c2 module=s2 theta=1.423051762885 amplitude=1.0 omega=0.0
cell s2.c3 module=s2 theta=1.570796326795 amplitude=1.0 omega=0.0
module s3 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s3.c0 module=s3 theta=1.767567851031 amplitude=1.0 omega=0.0
cell s3.c1 module=s3 theta=1.176719047272 amplitude=1.0 omega=0.0
cell s3.c2 module=s3 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s3.c3 module=s3 theta=1.570796326795 amplitude=1.0 omega=0.0
module s4 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s4.c0 module=s4 theta=1.627100610902 amplitude=1.0 omega=0.0
cell s4.c1 module=s4 theta=1.700149894672 amplitude=1.0 omega=0.0
cell s4.c2 module=s4 theta=2.071487463692 amplitude=1.0 omega=0.0
cell s4.c3 module=s4 theta=1.570796326795 amplitude=1.0 omega=0.0
module s5 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s5.c0 module=s5 theta=1.702593449915 amplitude=1.0 omega=0.0
cell s5.c1 module=s5 theta=2.244474995237 amplitude=1.0 omega=0.0
cell s5.c2 module=s5 theta=3.002378425489 amplitude=1.0 omega=0.0
cell s5.c3 module=s5 theta=3.141592653590 amplitude=1.0 omega=0.0
module s6 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s6.c0 module=s6 theta=1.795940204438 amplitude=1.0 omega=0.0
cell s6.c1 module=s6 theta=0.815964033467 amplitude=1.0 omega=0.0
cell s6.c2 module=s6 theta=3.005584778559 amplitude=1.0 omega=0.0
cell s6.c3 module=s6 theta=1.570796326795 amplitude=1.0 omega=0.0
module s7 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s7.c0 module=s7 theta=0.145148126908 amplitude=1.0 omega=0.0
cell s7.c1 module=s7 theta=1.667482601588 amplitude=1.0 omega=0.0
cell s7.c2 module=s7 theta=1.341890562690 amplitude=1.0 omega=0.0
cell s7.c3 module=s7 theta=1.570796326795 amplitude=1.0 omega=0.0
module s8 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s8.c0 module=s8 theta=1.375261379439 amplitude=1.0 omega=0.0
cell s8.c1 module=s8 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s8.c2 module=s8 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s8.c3 module=s8 theta=1.570796326795 amplitude=1.0 omega=0.0
module s9 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s9.c0 module=s9 theta=0.364664790025 amplitude=1.0 omega=0.0
cell s9.c1 module=s9 theta=0.735042856324 amplitude=1.0 omega=0.0
cell s9.c2 module=s9 theta=2.942111471078 amplitude=1.0 omega=0.0
cell s9.c3 module=s9 theta=1.570796326795 amplitude=1.0 omega=0.0
module s10 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s10.c0 module=s10 theta=1.550868049991 amplitude=1.0 omega=0.0
cell s10.c1 module=s10 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s10.c2 module=s10 theta=1.940073731475 amplitude=1.0 omega=0.0
cell s10.c3 module=s10 theta=0.000000000000 amplitude=1.0 omega=0.0
module s11 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s11.c0 module=s11 theta=1.551494857368 amplitude=1.0 omega=0.0
cell s11.c1 module=s11 theta=0.012632683772 amplitude=1.0 omega=0.0
cell s11.c2 module=s11 theta=2.816512299791 amplitude=1.0 omega=0.0
cell s11.c3 module=s11 theta=1.570796326795 amplitude=1.0 omega=0.0
module s12 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s12.c0 module=s12 theta=1.611953271297 amplitude=1.0 omega=0.0
cell s12.c1 module=s12 theta=1.225129481640 amplitude=1.0 omega=0.0
cell s12.c2 module=s12 theta=2.306883016421 amplitude=1.0 omega=0.0
cell s12.c3 module=s12 theta=1.570796326795 amplitude=1.0 omega=0.0
module s13 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s13.c0 module=s13 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s13.c1 module=s13 theta=0.080797608070 amplitude=1.0 omega=0.0
cell s13.c2 module=s13 theta=2.806484695834 amplitude=1.0 omega=0.0
cell s13.c3 module=s13 theta=1.570796326795 amplitude=1.0 omega=0.0
module s14 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s14.c0 module=s14 theta=2.131186331163 amplitude=1.0 omega=0.0
cell s14.c1 module=s14 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s14.c2 module=s14 theta=1.069553188175 amplitude=1.0 omega=0.0
cell s14.c3 module=s14 theta=0.000000000000 amplitude=1.0 omega=0.0
module s15 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s15.c0 module=s15 theta=0.196899398574 amplitude=1.0 omega=0.0
cell s15.c1 module=s15 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s15.c2 module=s15 theta=0.209554136877 amplitude=1.0 omega=0.0
cell s15.c3 module=s15 theta=1.570796326795 amplitude=1.0 omega=0.0
module s16 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s16.c0 module=s16 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s16.c1 module=s16 theta=1.460954200312 amplitude=1.0 omega=0.0
cell s16.c2 module=s16 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s16.c3 module=s16 theta=1.570796326795 amplitude=1.0 omega=0.0
module s17 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s17.c0 module=s17 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s17.c1 module=s17 theta=1.206006409202 amplitude=1.0 omega=0.0
cell s17.c2 module=s17 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s17.c3 module=s17 theta=0.000000000000 amplitude=1.0 omega=0.0
module s18 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s18.c0 module=s18 theta=1.465509411945 amplitude=1.0 omega=0.0
cell s18.c1 module=s18 theta=2.155445637595 amplitude=1.0 omega=0.0
cell s18.c2 module=s18 theta=1.505054260491 amplitude=1.0 omega=0.0
cell s18.c3 module=s18 theta=1.570796326795 amplitude=1.0 omega=0.0
module s19 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s19.c0 module=s19 theta=2.191045416241 amplitude=1.0 omega=0.0
cell s19.c1 module=s19 theta=2.355103821808 amplitude=1.0 omega=0.0
cell s19.c2 module=s19 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s19.c3 module=s19 theta=3.141592653590 amplitude=1.0 omega=0.0
module s20 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s20.c0 module=s20 theta=1.671303386382 amplitude=1.0 omega=0.0
cell s20.c1 module=s20 theta=0.272641673902 amplitude=1.0 omega=0.0
cell s20.c2 module=s20 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s20.c3 module=s20 theta=1.570796326795 amplitude=1.0 omega=0.0
module s21 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s21.c0 module=s21 theta=1.788874687963 amplitude=1.0 omega=0.0
cell s21.c1 module=s21 theta=3.082844969817 amplitude=1.0 omega=0.0
cell s21.c2 module=s21 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s21.c3 module=s21 theta=1.570796326795 amplitude=1.0 omega=0.0
module s22 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s22.c0 module=s22 theta=0.308562768038 amplitude=1.0 omega=0.0
cell s22.c1 module=s22 theta=0.225019326145 amplitude=1.0 omega=0.0
cell s22.c2 module=s22 theta=1.745304722276 amplitude=1.0 omega=0.0
cell s22.c3 module=s22 theta=0.000000000000 amplitude=1.0 omega=0.0
module s23 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s23.c0 module=s23 theta=2.566253924053 amplitude=1.0 omega=0.0
cell s23.c1 module=s23 theta=1.021469000018 amplitude=1.0 omega=0.0
cell s23.c2 module=s23 theta=1.427620076897 amplitude=1.0 omega=0.0
cell s23.c3 module=s23 theta=1.570796326795 amplitude=1.0 omega=0.0
module s24 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s24.c0 module=s24 theta=1.575361916715 amplitude=1.0 omega=0.0
cell s24.c1 module=s24 theta=1.584188962087 amplitude=1.0 omega=0.0
cell s24.c2 module=s24 theta=1.709263819341 amplitude=1.0 omega=0.0
cell s24.c3 module=s24 theta=1.570796326795 amplitude=1.0 omega=0.0
module s25 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s25.c0 module=s25 theta=0.275812797895 amplitude=1.0 omega=0.0
cell s25.c1 module=s25 theta=3.006787006799 amplitude=1.0 omega=0.0
cell s25.c2 module=s25 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s25.c3 module=s25 theta=1.570796326795 amplitude=1.0 omega=0.0
module s26 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s26.c0 module=s26 theta=1.984252419741 amplitude=1.0 omega=0.0
cell s26.c1 module=s26 theta=1.643193236986 amplitude=1.0 omega=0.0
cell s26.c2 module=s26 theta=1.593015759108 amplitude=1.0 omega=0.0
cell s26.c3 module=s26 theta=1.570796326795 amplitude=1.0 omega=0.0
module s27 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s27.c0 module=s27 theta=0.824428994497 amplitude=1.0 omega=0.0
cell s27.c1 module=s27 theta=3.032561949426 amplitude=1.0 omega=0.0
cell s27.c2 module=s27 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s27.c3 module=s27 theta=3.141592653590 amplitude=1.0 omega=0.0
module s28 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s28.c0 module=s28 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s28.c1 module=s28 theta=2.856248246995 amplitude=1.0 omega=0.0
cell s28.c2 module=s28 theta=1.360513688568 amplitude=1.0 omega=0.0
cell s28.c3 module=s28 theta=1.570796326795 amplitude=1.0 omega=0.0
module s29 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s29.c0 module=s29 theta=1.732989621626 amplitude=1.0 omega=0.0
cell s29.c1 module=s29 theta=1.505433402765 amplitude=1.0 omega=0.0
cell s29.c2 module=s29 theta=1.515564996747 amplitude=1.0 omega=0.0
cell s29.c3 module=s29 theta=1.570796326795 amplitude=1.0 omega=0.0
module s30 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s30.c0 module=s30 theta=0.058619980101 amplitude=1.0 omega=0.0
cell s30.c1 module=s30 theta=0.275915520039 amplitude=1.0 omega=0.0
cell s30.c2 module=s30 theta=1.797324311096 amplitude=1.0 omega=0.0
cell s30.c3 module=s30 theta=0.000000000000 amplitude=1.0 omega=0.0
module s31 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s31.c0 module=s31 theta=2.966673726257 amplitude=1.0 omega=0.0
cell s31.c1 module=s31 theta=0.671850260932 amplitude=1.0 omega=0.0
cell s31.c2 module=s31 theta=0.197317966302 amplitude=1.0 omega=0.0
cell s31.c3 module=s31 theta=1.570796326795 amplitude=1.0 omega=0.0
module s32 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s32.c0 module=s32 theta=2.891009829577 amplitude=1.0 omega=0.0
cell s32.c1 module=s32 theta=2.222216438109 amplitude=1.0 omega=0.0
cell s32.c2 module=s32 theta=1.439037897856 amplitude=1.0 omega=0.0
cell s32.c3 module=s32 theta=3.141592653590 amplitude=1.0 omega=0.0
module s33 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s33.c0 module=s33 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s33.c1 module=s33 theta=2.947314227428 amplitude=1.0 omega=0.0
cell s33.c2 module=s33 theta=1.498257796248 amplitude=1.0 omega=0.0
cell s33.c3 module=s33 theta=3.141592653590 amplitude=1.0 omega=0.0
module s34 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s34.c0 module=s34 theta=1.867251180324 amplitude=1.0 omega=0.0
cell s34.c1 module=s34 theta=0.217858479559 amplitude=1.0 omega=0.0
cell s34.c2 module=s34 theta=1.807572230524 amplitude=1.0 omega=0.0
cell s34.c3 module=s34 theta=0.000000000000 amplitude=1.0 omega=0.0
module s35 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s35.c0 module=s35 theta=1.870725628112 amplitude=1.0 omega=0.0
cell s35.c1 module=s35 theta=1.776138755141 amplitude=1.0 omega=0.0
cell s35.c2 module=s35 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s35.c3 module=s35 theta=1.570796326795 amplitude=1.0 omega=0.0
module s36 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s36.c0 module=s36 theta=0.929251137943 amplitude=1.0 omega=0.0
cell s36.c1 module=s36 theta=2.925987594251 amplitude=1.0 omega=0.0
cell s36.c2 module=s36 theta=2.806894493981 amplitude=1.0 omega=0.0
cell s36.c3 module=s36 theta=3.141592653590 amplitude=1.0 omega=0.0
module s37 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s37.c0 module=s37 theta=2.973296224989 amplitude=1.0 omega=0.0
cell s37.c1 module=s37 theta=1.287179531513 amplitude=1.0 omega=0.0
cell s37.c2 module=s37 theta=0.203363632614 amplitude=1.0 omega=0.0
cell s37.c3 module=s37 theta=1.570796326795 amplitude=1.0 omega=0.0
module s38 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s38.c0 module=s38 theta=1.140455423226 amplitude=1.0 omega=0.0
cell s38.c1 module=s38 theta=1.427231966924 amplitude=1.0 omega=0.0
cell s38.c2 module=s38 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s38.c3 module=s38 theta=0.000000000000 amplitude=1.0 omega=0.0
module s39 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s39.c0 module=s39 theta=1.792948278979 amplitude=1.0 omega=0.0
cell s39.c1 module=s39 theta=1.357182049709 amplitude=1.0 omega=0.0
cell s39.c2 module=s39 theta=1.740172520592 amplitude=1.0 omega=0.0
cell s39.c3 module=s39 theta=1.570796326795 amplitude=1.0 omega=0.0
module s40 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s40.c0 module=s40 theta=0.299788968471 amplitude=1.0 omega=0.0
cell s40.c1 module=s40 theta=1.353701710032 amplitude=1.0 omega=0.0
cell s40.c2 module=s40 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s40.c3 module=s40 theta=1.570796326795 amplitude=1.0 omega=0.0
module s41 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s41.c0 module=s41 theta=1.429302819408 amplitude=1.0 omega=0.0
cell s41.c1 module=s41 theta=1.489952160370 amplitude=1.0 omega=0.0
cell s41.c2 module=s41 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s41.c3 module=s41 theta=1.570796326795 amplitude=1.0 omega=0.0
module s42 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s42.c0 module=s42 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s42.c1 module=s42 theta=3.032238673660 amplitude=1.0 omega=0.0
cell s42.c2 module=s42 theta=3.001621474126 amplitude=1.0 omega=0.0
cell s42.c3 module=s42 theta=3.141592653590 amplitude=1.0 omega=0.0
module s43 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s43.c0 module=s43 theta=2.593491842670 amplitude=1.0 omega=0.0
cell s43.c1 module=s43 theta=1.718714673672 amplitude=1.0 omega=0.0
cell s43.c2 module=s43 theta=1.659924878223 amplitude=1.0 omega=0.0
cell s43.c3 module=s43 theta=1.570796326795 amplitude=1.0 omega=0.0
module s44 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s44.c0 module=s44 theta=1.477815971828 amplitude=1.0 omega=0.0
cell s44.c1 module=s44 theta=1.792440977019 amplitude=1.0 omega=0.0
cell s44.c2 module=s44 theta=1.382382999249 amplitude=1.0 omega=0.0
cell s44.c3 module=s44 theta=1.570796326795 amplitude=1.0 omega=0.0
module s45 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s45.c0 module=s45 theta=0.159059442566 amplitude=1.0 omega=0.0
cell s45.c1 module=s45 theta=0.639859629526 amplitude=1.0 omega=0.0
cell s45.c2 module=s45 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s45.c3 module=s45 theta=1.570796326795 amplitude=1.0 omega=0.0
module s46 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s46.c0 module=s46 theta=1.313407824919 amplitude=1.0 omega=0.0
cell s46.c1 module=s46 theta=1.297065680547 amplitude=1.0 omega=0.0
cell s46.c2 module=s46 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s46.c3 module=s46 theta=0.000000000000 amplitude=1.0 omega=0.0
module s47 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s47.c0 module=s47 theta=0.458637606787 amplitude=1.0 omega=0.0
cell s47.c1 module=s47 theta=0.189212884038 amplitude=1.0 omega=0.0
cell s47.c2 module=s47 theta=1.483149308469 amplitude=1.0 omega=0.0
cell s47.c3 module=s47 theta=0.000000000000 amplitude=1.0 omega=0.0
module s48 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s48.c0 module=s48 theta=1.614550761643 amplitude=1.0 omega=0.0
cell s48.c1 module=s48 theta=1.494431583698 amplitude=1.0 omega=0.0
cell s48.c2 module=s48 theta=1.277357221577 amplitude=1.0 omega=0.0
cell s48.c3 module=s48 theta=1.570796326795 amplitude=1.0 omega=0.0
module s49 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s49.c0 module=s49 theta=1.293952799088 amplitude=1.0 omega=0.0
cell s49.c1 module=s49 theta=1.813531666658 amplitude=1.0 omega=0.0
cell s49.c2 module=s49 theta=1.434184015785 amplitude=1.0 omega=0.0
cell s49.c3 module=s49 theta=1.570796326795 amplitude=1.0 omega=0.0
module s50 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s50.c0 module=s50 theta=3.113024839593 amplitude=1.0 omega=0.0
cell s50.c1 module=s50 theta=0.262213359851 amplitude=1.0 omega=0.0
cell s50.c2 module=s50 theta=1.301726192985 amplitude=1.0 omega=0.0
cell s50.c3 module=s50 theta=1.570796326795 amplitude=1.0 omega=0.0
module s51 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s51.c0 module=s51 theta=1.375412954735 amplitude=1.0 omega=0.0
cell s51.c1 module=s51 theta=2.803369029247 amplitude=1.0 omega=0.0
cell s51.c2 module=s51 theta=2.251275937116 amplitude=1.0 omega=0.0
cell s51.c3 module=s51 theta=3.141592653590 amplitude=1.0 omega=0.0
module s52 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s52.c0 module=s52 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s52.c1 module=s52 theta=1.751258873416 amplitude=1.0 omega=0.0
cell s52.c2 module=s52 theta=1.825706379301 amplitude=1.0 omega=0.0
cell s52.c3 module=s52 theta=1.570796326795 amplitude=1.0 omega=0.0
module s53 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s53.c0 module=s53 theta=2.919373144190 amplitude=1.0 omega=0.0
cell s53.c1 module=s53 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s53.c2 module=s53 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s53.c3 module=s53 theta=1.570796326795 amplitude=1.0 omega=0.0
module s54 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s54.c0 module=s54 theta=1.872515831661 amplitude=1.0 omega=0.0
cell s54.c1 module=s54 theta=1.079956367464 amplitude=1.0 omega=0.0
cell s54.c2 module=s54 theta=2.876467673789 amplitude=1.0 omega=0.0
cell s54.c3 module=s54 theta=1.570796326795 amplitude=1.0 omega=0.0
module s55 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s55.c0 module=s55 theta=0.172490470465 amplitude=1.0 omega=0.0
cell s55.c1 module=s55 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s55.c2 module=s55 theta=1.810924325817 amplitude=1.0 omega=0.0
cell s55.c3 module=s55 theta=1.570796326795 amplitude=1.0 omega=0.0
module s56 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s56.c0 module=s56 theta=1.836171024489 amplitude=1.0 omega=0.0
cell s56.c1 module=s56 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s56.c2 module=s56 theta=0.016904573652 amplitude=1.0 omega=0.0
cell s56.c3 module=s56 theta=1.570796326795 amplitude=1.0 omega=0.0
module s57 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s57.c0 module=s57 theta=1.356383182078 amplitude=1.0 omega=0.0
cell s57.c1 module=s57 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s57.c2 module=s57 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s57.c3 module=s57 theta=0.000000000000 amplitude=1.0 omega=0.0
module s58 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s58.c0 module=s58 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s58.c1 module=s58 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s58.c2 module=s58 theta=1.576692562046 amplitude=1.0 omega=0.0
cell s58.c3 module=s58 theta=3.141592653590 amplitude=1.0 omega=0.0
module s59 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s59.c0 module=s59 theta=1.836690994564 amplitude=1.0 omega=0.0
cell s59.c1 module=s59 theta=1.351181844695 amplitude=1.0 omega=0.0
cell s59.c2 module=s59 theta=1.323994374989 amplitude=1.0 omega=0.0
cell s59.c3 module=s59 theta=1.570796326795 amplitude=1.0 omega=0.0
module s60 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s60.c0 module=s60 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s60.c1 module=s60 theta=1.609872426647 amplitude=1.0 omega=0.0
cell s60.c2 module=s60 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s60.c3 module=s60 theta=0.000000000000 amplitude=1.0 omega=0.0
module s61 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s61.c0 module=s61 theta=1.667446334003 amplitude=1.0 omega=0.0
cell s61.c1 module=s61 theta=0.968851514740 amplitude=1.0 omega=0.0
cell s61.c2 module=s61 theta=1.971001512559 amplitude=1.0 omega=0.0
cell s61.c3 module=s61 theta=1.570796326795 amplitude=1.0 omega=0.0
module s62 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s62.c0 module=s62 theta=1.682174368116 amplitude=1.0 omega=0.0
cell s62.c1 module=s62 theta=1.286884262000 amplitude=1.0 omega=0.0
cell s62.c2 module=s62 theta=1.591180373210 amplitude=1.0 omega=0.0
cell s62.c3 module=s62 theta=1.570796326795 amplitude=1.0 omega=0.0
module s63 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s63.c0 module=s63 theta=1.364925710977 amplitude=1.0 omega=0.0
cell s63.c1 module=s63 theta=2.799707906162 amplitude=1.0 omega=0.0
cell s63.c2 module=s63 theta=1.353356814991 amplitude=1.0 omega=0.0
cell s63.c3 module=s63 theta=1.570796326795 amplitude=1.0 omega=0.0
module s64 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s64.c0 module=s64 theta=1.719666657487 amplitude=1.0 omega=0.0
cell s64.c1 module=s64 theta=2.432295584342 amplitude=1.0 omega=0.0
cell s64.c2 module=s64 theta=0.599285643697 amplitude=1.0 omega=0.0
cell s64.c3 module=s64 theta=1.570796326795 amplitude=1.0 omega=0.0
module s65 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s65.c0 module=s65 theta=1.763716788332 amplitude=1.0 omega=0.0
cell s65.c1 module=s65 theta=0.322836047467 amplitude=1.0 omega=0.0
cell s65.c2 module=s65 theta=0.871595953184 amplitude=1.0 omega=0.0
cell s65.c3 module=s65 theta=0.000000000000 amplitude=1.0 omega=0.0
module s66 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s66.c0 module=s66 theta=0.339645163448 amplitude=1.0 omega=0.0
cell s66.c1 module=s66 theta=1.516178218494 amplitude=1.0 omega=0.0
cell s66.c2 module=s66 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s66.c3 module=s66 theta=1.570796326795 amplitude=1.0 omega=0.0
module s67 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s67.c0 module=s67 theta=1.845277548278 amplitude=1.0 omega=0.0
cell s67.c1 module=s67 theta=0.139652875188 amplitude=1.0 omega=0.0
cell s67.c2 module=s67 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s67.c3 module=s67 theta=0.000000000000 amplitude=1.0 omega=0.0
module s68 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s68.c0 module=s68 theta=0.227725083839 amplitude=1.0 omega=0.0
cell s68.c1 module=s68 theta=0.695164706059 amplitude=1.0 omega=0.0
cell s68.c2 module=s68 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s68.c3 module=s68 theta=1.570796326795 amplitude=1.0 omega=0.0
module s69 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s69.c0 module=s69 theta=2.843201529697 amplitude=1.0 omega=0.0
cell s69.c1 module=s69 theta=0.002929992684 amplitude=1.0 omega=0.0
cell s69.c2 module=s69 theta=0.491642750819 amplitude=1.0 omega=0.0
cell s69.c3 module=s69 theta=0.000000000000 amplitude=1.0 omega=0.0
module s70 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s70.c0 module=s70 theta=1.669715316865 amplitude=1.0 omega=0.0
cell s70.c1 module=s70 theta=0.245327042547 amplitude=1.0 omega=0.0
cell s70.c2 module=s70 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s70.c3 module=s70 theta=0.000000000000 amplitude=1.0 omega=0.0
module s71 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s71.c0 module=s71 theta=1.444218914580 amplitude=1.0 omega=0.0
cell s71.c1 module=s71 theta=1.757317770794 amplitude=1.0 omega=0.0
cell s71.c2 module=s71 theta=1.857508762992 amplitude=1.0 omega=0.0
cell s71.c3 module=s71 theta=1.570796326795 amplitude=1.0 omega=0.0
module s72 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s72.c0 module=s72 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s72.c1 module=s72 theta=1.642944256266 amplitude=1.0 omega=0.0
cell s72.c2 module=s72 theta=0.423790035863 amplitude=1.0 omega=0.0
cell s72.c3 module=s72 theta=1.570796326795 amplitude=1.0 omega=0.0
module s73 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s73.c0 module=s73 theta=1.817650235115 amplitude=1.0 omega=0.0
cell s73.c1 module=s73 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s73.c2 module=s73 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s73.c3 module=s73 theta=3.141592653590 amplitude=1.0 omega=0.0
module s74 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s74.c0 module=s74 theta=3.016959216643 amplitude=1.0 omega=0.0
cell s74.c1 module=s74 theta=1.344875081832 amplitude=1.0 omega=0.0
cell s74.c2 module=s74 theta=0.263443848083 amplitude=1.0 omega=0.0
cell s74.c3 module=s74 theta=1.570796326795 amplitude=1.0 omega=0.0
module s75 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s75.c0 module=s75 theta=1.374916770091 amplitude=1.0 omega=0.0
cell s75.c1 module=s75 theta=1.572034827295 amplitude=1.0 omega=0.0
cell s75.c2 module=s75 theta=0.038904789509 amplitude=1.0 omega=0.0
cell s75.c3 module=s75 theta=1.570796326795 amplitude=1.0 omega=0.0
module s76 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s76.c0 module=s76 theta=1.994973896089 amplitude=1.0 omega=0.0
cell s76.c1 module=s76 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s76.c2 module=s76 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s76.c3 module=s76 theta=1.570796326795 amplitude=1.0 omega=0.0
module s77 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s77.c0 module=s77 theta=2.939789656290 amplitude=1.0 omega=0.0
cell s77.c1 module=s77 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s77.c2 module=s77 theta=0.012432619002 amplitude=1.0 omega=0.0
cell s77.c3 module=s77 theta=3.141592653590 amplitude=1.0 omega=0.0
module s78 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s78.c0 module=s78 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s78.c1 module=s78 theta=1.421036118411 amplitude=1.0 omega=0.0
cell s78.c2 module=s78 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s78.c3 module=s78 theta=3.141592653590 amplitude=1.0 omega=0.0
module s79 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s79.c0 module=s79 theta=1.694806647558 amplitude=1.0 omega=0.0
cell s79.c1 module=s79 theta=0.317038612140 amplitude=1.0 omega=0.0
cell s79.c2 module=s79 theta=1.719153546140 amplitude=1.0 omega=0.0
cell s79.c3 module=s79 theta=0.000000000000 amplitude=1.0 omega=0.0
module s80 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s80.c0 module=s80 theta=1.727103576971 amplitude=1.0 omega=0.0
cell s80.c1 module=s80 theta=1.617411303283 amplitude=1.0 omega=0.0
cell s80.c2 module=s80 theta=2.927999510884 amplitude=1.0 omega=0.0
cell s80.c3 module=s80 theta=1.570796326795 amplitude=1.0 omega=0.0
module s81 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s81.c0 module=s81 theta=0.876857121856 amplitude=1.0 omega=0.0
cell s81.c1 module=s81 theta=0.096700608597 amplitude=1.0 omega=0.0
cell s81.c2 module=s81 theta=1.769843700600 amplitude=1.0 omega=0.0
cell s81.c3 module=s81 theta=0.000000000000 amplitude=1.0 omega=0.0
module s82 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s82.c0 module=s82 theta=1.354897782103 amplitude=1.0 omega=0.0
cell s82.c1 module=s82 theta=0.910973417145 amplitude=1.0 omega=0.0
cell s82.c2 module=s82 theta=1.285126284305 amplitude=1.0 omega=0.0
cell s82.c3 module=s82 theta=1.570796326795 amplitude=1.0 omega=0.0
module s83 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s83.c0 module=s83 theta=1.591063844692 amplitude=1.0 omega=0.0
cell s83.c1 module=s83 theta=1.597765586403 amplitude=1.0 omega=0.0
cell s83.c2 module=s83 theta=0.067389399251 amplitude=1.0 omega=0.0
cell s83.c3 module=s83 theta=1.570796326795 amplitude=1.0 omega=0.0
module s84 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s84.c0 module=s84 theta=1.672753731585 amplitude=1.0 omega=0.0
cell s84.c1 module=s84 theta=2.453840794112 amplitude=1.0 omega=0.0
cell s84.c2 module=s84 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s84.c3 module=s84 theta=3.141592653590 amplitude=1.0 omega=0.0
module s85 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s85.c0 module=s85 theta=0.246915028529 amplitude=1.0 omega=0.0
cell s85.c1 module=s85 theta=1.779609803297 amplitude=1.0 omega=0.0
cell s85.c2 module=s85 theta=1.530985497349 amplitude=1.0 omega=0.0
cell s85.c3 module=s85 theta=1.570796326795 amplitude=1.0 omega=0.0
module s86 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s86.c0 module=s86 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s86.c1 module=s86 theta=1.729197246412 amplitude=1.0 omega=0.0
cell s86.c2 module=s86 theta=1.786557718389 amplitude=1.0 omega=0.0
cell s86.c3 module=s86 theta=1.570796326795 amplitude=1.0 omega=0.0
module s87 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s87.c0 module=s87 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s87.c1 module=s87 theta=1.491327043277 amplitude=1.0 omega=0.0
cell s87.c2 module=s87 theta=1.764413448259 amplitude=1.0 omega=0.0
cell s87.c3 module=s87 theta=1.570796326795 amplitude=1.0 omega=0.0
module s88 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s88.c0 module=s88 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s88.c1 module=s88 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s88.c2 module=s88 theta=1.351661479348 amplitude=1.0 omega=0.0
cell s88.c3 module=s88 theta=0.000000000000 amplitude=1.0 omega=0.0
module s89 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s89.c0 module=s89 theta=0.910485862570 amplitude=1.0 omega=0.0
cell s89.c1 module=s89 theta=1.077768341751 amplitude=1.0 omega=0.0
cell s89.c2 module=s89 theta=3.102004123818 amplitude=1.0 omega=0.0
cell s89.c3 module=s89 theta=1.570796326795 amplitude=1.0 omega=0.0
module s90 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s90.c0 module=s90 theta=1.420141139112 amplitude=1.0 omega=0.0
cell s90.c1 module=s90 theta=1.430103389645 amplitude=1.0 omega=0.0
cell s90.c2 module=s90 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s90.c3 module=s90 theta=1.570796326795 amplitude=1.0 omega=0.0
module s91 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s91.c0 module=s91 theta=1.563581345983 amplitude=1.0 omega=0.0
cell s91.c1 module=s91 theta=1.645407705822 amplitude=1.0 omega=0.0
cell s91.c2 module=s91 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s91.c3 module=s91 theta=1.570796326795 amplitude=1.0 omega=0.0
module s92 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s92.c0 module=s92 theta=2.049620496815 amplitude=1.0 omega=0.0
cell s92.c1 module=s92 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s92.c2 module=s92 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s92.c3 module=s92 theta=0.000000000000 amplitude=1.0 omega=0.0
module s93 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s93.c0 module=s93 theta=2.356124163409 amplitude=1.0 omega=0.0
cell s93.c1 module=s93 theta=1.351049180780 amplitude=1.0 omega=0.0
cell s93.c2 module=s93 theta=1.283765663445 amplitude=1.0 omega=0.0
cell s93.c3 module=s93 theta=1.570796326795 amplitude=1.0 omega=0.0
module s94 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s94.c0 module=s94 theta=1.143528686751 amplitude=1.0 omega=0.0
cell s94.c1 module=s94 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s94.c2 module=s94 theta=1.275894627192 amplitude=1.0 omega=0.0
cell s94.c3 module=s94 theta=3.141592653590 amplitude=1.0 omega=0.0
module s95 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s95.c0 module=s95 theta=1.753288132033 amplitude=1.0 omega=0.0
cell s95.c1 module=s95 theta=0.102272558222 amplitude=1.0 omega=0.0
cell s95.c2 module=s95 theta=3.026746536419 amplitude=1.0 omega=0.0
cell s95.c3 module=s95 theta=1.570796326795 amplitude=1.0 omega=0.0
module s96 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s96.c0 module=s96 theta=2.920661741663 amplitude=1.0 omega=0.0
cell s96.c1 module=s96 theta=0.229650558454 amplitude=1.0 omega=0.0
cell s96.c2 module=s96 theta=1.443041627725 amplitude=1.0 omega=0.0
cell s96.c3 module=s96 theta=1.570796326795 amplitude=1.0 omega=0.0
module s97 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s97.c0 module=s97 theta=1.585085216475 amplitude=1.0 omega=0.0
cell s97.c1 module=s97 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s97.c2 module=s97 theta=3.051024858212 amplitude=1.0 omega=0.0
cell s97.c3 module=s97 theta=3.141592653590 amplitude=1.0 omega=0.0
module s98 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s98.c0 module=s98 theta=2.793227412980 amplitude=1.0 omega=0.0
cell s98.c1 module=s98 theta=2.150499808475 amplitude=1.0 omega=0.0
cell s98.c2 module=s98 theta=1.610077852313 amplitude=1.0 omega=0.0
cell s98.c3 module=s98 theta=3.141592653590 amplitude=1.0 omega=0.0
module s99 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s99.c0 module=s99 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s99.c1 module=s99 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s99.c2 module=s99 theta=2.587378736414 amplitude=1.0 omega=0.0
cell s99.c3 module=s99 theta=3.141592653590 amplitude=1.0 omega=0.0
module s100 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s100.c0 module=s100 theta=1.366104223173 amplitude=1.0 omega=0.0
cell s100.c1 module=s100 theta=1.049281385294 amplitude=1.0 omega=0.0
cell s100.c2 module=s100 theta=1.753252984148 amplitude=1.0 omega=0.0
cell s100.c3 module=s100 theta=1.570796326795 amplitude=1.0 omega=0.0
module s101 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s101.c0 module=s101 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s101.c1 module=s101 theta=1.089104011597 amplitude=1.0 omega=0.0
cell s101.c2 module=s101 theta=1.419536020806 amplitude=1.0 omega=0.0
cell s101.c3 module=s101 theta=0.000000000000 amplitude=1.0 omega=0.0
module s102 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s102.c0 module=s102 theta=1.599806593923 amplitude=1.0 omega=0.0
cell s102.c1 module=s102 theta=0.125356861907 amplitude=1.0 omega=0.0
cell s102.c2 module=s102 theta=2.170726492022 amplitude=1.0 omega=0.0
cell s102.c3 module=s102 theta=0.000000000000 amplitude=1.0 omega=0.0
module s103 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s103.c0 module=s103 theta=2.318593224888 amplitude=1.0 omega=0.0
cell s103.c1 module=s103 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s103.c2 module=s103 theta=0.272109626357 amplitude=1.0 omega=0.0
cell s103.c3 module=s103 theta=3.141592653590 amplitude=1.0 omega=0.0
module s104 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s104.c0 module=s104 theta=0.011024958388 amplitude=1.0 omega=0.0
cell s104.c1 module=s104 theta=3.119086516197 amplitude=1.0 omega=0.0
cell s104.c2 module=s104 theta=1.358678130233 amplitude=1.0 omega=0.0
cell s104.c3 module=s104 theta=1.570796326795 amplitude=1.0 omega=0.0
module s105 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s105.c0 module=s105 theta=3.042301396170 amplitude=1.0 omega=0.0
cell s105.c1 module=s105 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s105.c2 module=s105 theta=2.082716234863 amplitude=1.0 omega=0.0
cell s105.c3 module=s105 theta=1.570796326795 amplitude=1.0 omega=0.0
module s106 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s106.c0 module=s106 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s106.c1 module=s106 theta=1.339105173034 amplitude=1.0 omega=0.0
cell s106.c2 module=s106 theta=0.823488393144 amplitude=1.0 omega=0.0
cell s106.c3 module=s106 theta=0.000000000000 amplitude=1.0 omega=0.0
module s107 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s107.c0 module=s107 theta=0.436828345500 amplitude=1.0 omega=0.0
cell s107.c1 module=s107 theta=1.699628680213 amplitude=1.0 omega=0.0
cell s107.c2 module=s107 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s107.c3 module=s107 theta=1.570796326795 amplitude=1.0 omega=0.0
module s108 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s108.c0 module=s108 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s108.c1 module=s108 theta=1.773686398979 amplitude=1.0 omega=0.0
cell s108.c2 module=s108 theta=1.699503267977 amplitude=1.0 omega=0.0
cell s108.c3 module=s108 theta=1.570796326795 amplitude=1.0 omega=0.0
module s109 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s109.c0 module=s109 theta=2.421863703885 amplitude=1.0 omega=0.0
cell s109.c1 module=s109 theta=1.406595123743 amplitude=1.0 omega=0.0
cell s109.c2 module=s109 theta=1.759835605873 amplitude=1.0 omega=0.0
cell s109.c3 module=s109 theta=1.570796326795 amplitude=1.0 omega=0.0
module s110 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s110.c0 module=s110 theta=0.042171154136 amplitude=1.0 omega=0.0
cell s110.c1 module=s110 theta=2.355343617092 amplitude=1.0 omega=0.0
cell s110.c2 module=s110 theta=0.339105909739 amplitude=1.0 omega=0.0
cell s110.c3 module=s110 theta=1.570796326795 amplitude=1.0 omega=0.0
module s111 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s111.c0 module=s111 theta=2.441987354637 amplitude=1.0 omega=0.0
cell s111.c1 module=s111 theta=1.338279550837 amplitude=1.0 omega=0.0
cell s111.c2 module=s111 theta=0.468455781293 amplitude=1.0 omega=0.0
cell s111.c3 module=s111 theta=1.570796326795 amplitude=1.0 omega=0.0
module s112 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s112.c0 module=s112 theta=1.691105473009 amplitude=1.0 omega=0.0
cell s112.c1 module=s112 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s112.c2 module=s112 theta=1.683736561911 amplitude=1.0 omega=0.0
cell s112.c3 module=s112 theta=3.141592653590 amplitude=1.0 omega=0.0
module s113 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s113.c0 module=s113 theta=1.842672656893 amplitude=1.0 omega=0.0
cell s113.c1 module=s113 theta=2.792838177430 amplitude=1.0 omega=0.0
cell s113.c2 module=s113 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s113.c3 module=s113 theta=1.570796326795 amplitude=1.0 omega=0.0
module s114 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s114.c0 module=s114 theta=1.749326903945 amplitude=1.0 omega=0.0
cell s114.c1 module=s114 theta=1.544995434634 amplitude=1.0 omega=0.0
cell s114.c2 module=s114 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s114.c3 module=s114 theta=1.570796326795 amplitude=1.0 omega=0.0
module s115 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s115.c0 module=s115 theta=1.635619612378 amplitude=1.0 omega=0.0
cell s115.c1 module=s115 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s115.c2 module=s115 theta=1.503699411750 amplitude=1.0 omega=0.0
cell s115.c3 module=s115 theta=3.141592653590 amplitude=1.0 omega=0.0
module s116 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s116.c0 module=s116 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s116.c1 module=s116 theta=1.591774204026 amplitude=1.0 omega=0.0
cell s116.c2 module=s116 theta=2.891067149836 amplitude=1.0 omega=0.0
cell s116.c3 module=s116 theta=3.141592653590 amplitude=1.0 omega=0.0
module s117 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s117.c0 module=s117 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s117.c1 module=s117 theta=1.397639220257 amplitude=1.0 omega=0.0
cell s117.c2 module=s117 theta=0.467681855280 amplitude=1.0 omega=0.0
cell s117.c3 module=s117 theta=0.000000000000 amplitude=1.0 omega=0.0
module s118 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s118.c0 module=s118 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s118.c1 module=s118 theta=2.655403685543 amplitude=1.0 omega=0.0
cell s118.c2 module=s118 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s118.c3 module=s118 theta=3.141592653590 amplitude=1.0 omega=0.0
module s119 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s119.c0 module=s119 theta=1.274015688193 amplitude=1.0 omega=0.0
cell s119.c1 module=s119 theta=1.309840039572 amplitude=1.0 omega=0.0
cell s119.c2 module=s119 theta=0.207500960358 amplitude=1.0 omega=0.0
cell s119.c3 module=s119 theta=0.000000000000 amplitude=1.0 omega=0.0
module s120 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s120.c0 module=s120 theta=0.336170135946 amplitude=1.0 omega=0.0
cell s120.c1 module=s120 theta=1.692691509455 amplitude=1.0 omega=0.0
cell s120.c2 module=s120 theta=1.695380439476 amplitude=1.0 omega=0.0
cell s120.c3 module=s120 theta=1.570796326795 amplitude=1.0 omega=0.0
module s121 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s121.c0 module=s121 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s121.c1 module=s121 theta=2.812289875739 amplitude=1.0 omega=0.0
cell s121.c2 module=s121 theta=1.316970497272 amplitude=1.0 omega=0.0
cell s121.c3 module=s121 theta=3.141592653590 amplitude=1.0 omega=0.0
module s122 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s122.c0 module=s122 theta=1.410150832018 amplitude=1.0 omega=0.0
cell s122.c1 module=s122 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s122.c2 module=s122 theta=0.303689698751 amplitude=1.0 omega=0.0
cell s122.c3 module=s122 theta=1.570796326795 amplitude=1.0 omega=0.0
module s123 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s123.c0 module=s123 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s123.c1 module=s123 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s123.c2 module=s123 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s123.c3 module=s123 theta=3.141592653590 amplitude=1.0 omega=0.0
module s124 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s124.c0 module=s124 theta=1.566167881069 amplitude=1.0 omega=0.0
cell s124.c1 module=s124 theta=3.029826488750 amplitude=1.0 omega=0.0
cell s124.c2 module=s124 theta=1.106863827778 amplitude=1.0 omega=0.0
cell s124.c3 module=s124 theta=3.141592653590 amplitude=1.0 omega=0.0
module s125 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s125.c0 module=s125 theta=0.308184872848 amplitude=1.0 omega=0.0
cell s125.c1 module=s125 theta=1.475257690497 amplitude=1.0 omega=0.0
cell s125.c2 module=s125 theta=1.433219190571 amplitude=1.0 omega=0.0
cell s125.c3 module=s125 theta=1.570796326795 amplitude=1.0 omega=0.0
module s126 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s126.c0 module=s126 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s126.c1 module=s126 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s126.c2 module=s126 theta=2.931971445271 amplitude=1.0 omega=0.0
cell s126.c3 module=s126 theta=3.141592653590 amplitude=1.0 omega=0.0
module s127 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s127.c0 module=s127 theta=0.508751353845 amplitude=1.0 omega=0.0
cell s127.c1 module=s127 theta=2.872230452700 amplitude=1.0 omega=0.0
cell s127.c2 module=s127 theta=1.582007981549 amplitude=1.0 omega=0.0
cell s127.c3 module=s127 theta=1.570796326795 amplitude=1.0 omega=0.0
module s128 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s128.c0 module=s128 theta=2.904079078829 amplitude=1.0 omega=0.0
cell s128.c1 module=s128 theta=0.260009860411 amplitude=1.0 omega=0.0
cell s128.c2 module=s128 theta=1.337263472203 amplitude=1.0 omega=0.0
cell s128.c3 module=s128 theta=1.570796326795 amplitude=1.0 omega=0.0
module s129 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s129.c0 module=s129 theta=2.925720630559 amplitude=1.0 omega=0.0
cell s129.c1 module=s129 theta=2.156336922572 amplitude=1.0 omega=0.0
cell s129.c2 module=s129 theta=2.613846913107 amplitude=1.0 omega=0.0
cell s129.c3 module=s129 theta=3.141592653590 amplitude=1.0 omega=0.0
module s130 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s130.c0 module=s130 theta=2.803109606414 amplitude=1.0 omega=0.0
cell s130.c1 module=s130 theta=1.355952017467 amplitude=1.0 omega=0.0
cell s130.c2 module=s130 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s130.c3 module=s130 theta=1.570796326795 amplitude=1.0 omega=0.0
module s131 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s131.c0 module=s131 theta=1.325243614565 amplitude=1.0 omega=0.0
cell s131.c1 module=s131 theta=1.561680657720 amplitude=1.0 omega=0.0
cell s131.c2 module=s131 theta=2.904813179814 amplitude=1.0 omega=0.0
cell s131.c3 module=s131 theta=1.570796326795 amplitude=1.0 omega=0.0
module s132 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s132.c0 module=s132 theta=2.451139639632 amplitude=1.0 omega=0.0
cell s132.c1 module=s132 theta=2.359590527818 amplitude=1.0 omega=0.0
cell s132.c2 module=s132 theta=1.544203819411 amplitude=1.0 omega=0.0
cell s132.c3 module=s132 theta=3.141592653590 amplitude=1.0 omega=0.0
module s133 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s133.c0 module=s133 theta=1.503201953544 amplitude=1.0 omega=0.0
cell s133.c1 module=s133 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s133.c2 module=s133 theta=0.552771552463 amplitude=1.0 omega=0.0
cell s133.c3 module=s133 theta=1.570796326795 amplitude=1.0 omega=0.0
module s134 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s134.c0 module=s134 theta=2.306711487533 amplitude=1.0 omega=0.0
cell s134.c1 module=s134 theta=1.795654000259 amplitude=1.0 omega=0.0
cell s134.c2 module=s134 theta=0.042043535297 amplitude=1.0 omega=0.0
cell s134.c3 module=s134 theta=1.570796326795 amplitude=1.0 omega=0.0
module s135 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s135.c0 module=s135 theta=1.320916428693 amplitude=1.0 omega=0.0
cell s135.c1 module=s135 theta=1.480668615254 amplitude=1.0 omega=0.0
cell s135.c2 module=s135 theta=1.360735678573 amplitude=1.0 omega=0.0
cell s135.c3 module=s135 theta=1.570796326795 amplitude=1.0 omega=0.0
module s136 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s136.c0 module=s136 theta=3.001856543595 amplitude=1.0 omega=0.0
cell s136.c1 module=s136 theta=1.772334825507 amplitude=1.0 omega=0.0
cell s136.c2 module=s136 theta=0.195361464121 amplitude=1.0 omega=0.0
cell s136.c3 module=s136 theta=1.570796326795 amplitude=1.0 omega=0.0
module s137 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s137.c0 module=s137 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s137.c1 module=s137 theta=2.424049776658 amplitude=1.0 omega=0.0
cell s137.c2 module=s137 theta=0.662329823107 amplitude=1.0 omega=0.0
cell s137.c3 module=s137 theta=1.570796326795 amplitude=1.0 omega=0.0
module s138 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s138.c0 module=s138 theta=3.013155961076 amplitude=1.0 omega=0.0
cell s138.c1 module=s138 theta=1.499583748189 amplitude=1.0 omega=0.0
cell s138.c2 module=s138 theta=1.014621316743 amplitude=1.0 omega=0.0
cell s138.c3 module=s138 theta=1.570796326795 amplitude=1.0 omega=0.0
module s139 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s139.c0 module=s139 theta=0.295238647830 amplitude=1.0 omega=0.0
cell s139.c1 module=s139 theta=2.318520216231 amplitude=1.0 omega=0.0
cell s139.c2 module=s139 theta=1.604347646646 amplitude=1.0 omega=0.0
cell s139.c3 module=s139 theta=1.570796326795 amplitude=1.0 omega=0.0
module s140 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s140.c0 module=s140 theta=2.814569092462 amplitude=1.0 omega=0.0
cell s140.c1 module=s140 theta=2.190603155761 amplitude=1.0 omega=0.0
cell s140.c2 module=s140 theta=2.444080807878 amplitude=1.0 omega=0.0
cell s140.c3 module=s140 theta=3.141592653590 amplitude=1.0 omega=0.0
module s141 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s141.c0 module=s141 theta=2.866965256134 amplitude=1.0 omega=0.0
cell s141.c1 module=s141 theta=2.873206474306 amplitude=1.0 omega=0.0
cell s141.c2 module=s141 theta=1.360923939495 amplitude=1.0 omega=0.0
cell s141.c3 module=s141 theta=3.141592653590 amplitude=1.0 omega=0.0
module s142 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s142.c0 module=s142 theta=0.076083285013 amplitude=1.0 omega=0.0
cell s142.c1 module=s142 theta=0.096524791425 amplitude=1.0 omega=0.0
cell s142.c2 module=s142 theta=0.876847593282 amplitude=1.0 omega=0.0
cell s142.c3 module=s142 theta=0.000000000000 amplitude=1.0 omega=0.0
module s143 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s143.c0 module=s143 theta=0.833434265681 amplitude=1.0 omega=0.0
cell s143.c1 module=s143 theta=1.671153166267 amplitude=1.0 omega=0.0
cell s143.c2 module=s143 theta=0.278366127110 amplitude=1.0 omega=0.0
cell s143.c3 module=s143 theta=1.570796326795 amplitude=1.0 omega=0.0
module s144 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s144.c0 module=s144 theta=1.729265076051 amplitude=1.0 omega=0.0
cell s144.c1 module=s144 theta=1.433200171198 amplitude=1.0 omega=0.0
cell s144.c2 module=s144 theta=0.025887351185 amplitude=1.0 omega=0.0
cell s144.c3 module=s144 theta=1.570796326795 amplitude=1.0 omega=0.0
module s145 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s145.c0 module=s145 theta=1.019270712734 amplitude=1.0 omega=0.0
cell s145.c1 module=s145 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s145.c2 module=s145 theta=0.000000000000 amplitude=1.0 omega=0.0
cell s145.c3 module=s145 theta=1.570796326795 amplitude=1.0 omega=0.0
module s146 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s146.c0 module=s146 theta=0.061977034188 amplitude=1.0 omega=0.0
cell s146.c1 module=s146 theta=1.678937465750 amplitude=1.0 omega=0.0
cell s146.c2 module=s146 theta=1.655187606587 amplitude=1.0 omega=0.0
cell s146.c3 module=s146 theta=1.570796326795 amplitude=1.0 omega=0.0
module s147 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s147.c0 module=s147 theta=0.882642863861 amplitude=1.0 omega=0.0
cell s147.c1 module=s147 theta=1.539083084258 amplitude=1.0 omega=0.0
cell s147.c2 module=s147 theta=1.667269512660 amplitude=1.0 omega=0.0
cell s147.c3 module=s147 theta=1.570796326795 amplitude=1.0 omega=0.0
module s148 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s148.c0 module=s148 theta=0.108606731960 amplitude=1.0 omega=0.0
cell s148.c1 module=s148 theta=0.572847780555 amplitude=1.0 omega=0.0
cell s148.c2 module=s148 theta=2.929281346339 amplitude=1.0 omega=0.0
cell s148.c3 module=s148 theta=0.000000000000 amplitude=1.0 omega=0.0
module s149 field=scenes-test belief=0.0 prior=0.0 precision=1.0 action-gain=1.0
cell s149.c0 module=s149 theta=3.141592653590 amplitude=1.0 omega=0.0
cell s149.c1 module=s149 theta=0.076720979174 amplitude=1.0 omega=0.0
cell s149.c2 module=s149 theta=0.303277109289 amplitude=1.0 omega=0.0
cell s149.c3 module=s149 theta=0.000000000000 amplitude=1.0 omega=0.0
