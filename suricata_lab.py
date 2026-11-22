from pathlib import Path
import json
import base64
import zlib
import pandas as pd
import streamlit as st


# Úplná kopie laboratorního suricata.yaml
_SURICATA_YAML_B85 = (
    "c-ri}YkT8HmL~X}zXDCRSCX5c?wM)UbnVKSN;|vqqDsl-s`2AT4U(XQN)liJpd@;0_qXqP&m|%Nl1in^HQPHo)iY@k2*f>3oa=kO`pen7"
    "x6$F?uoK5|r_+lrmt{6i>LeN$`82y(mPwrzc{I&t=^%QON6BQ8@sqlU>f4lx&F5)eSJ5P`#$`6j@|!4`&8VhgfpS%pQQ6z9;wt*lbUB+v"
    "lVZHYS5o&l$)iykO^andiIRFq-`>{sq8je+Q^9IbX_p3Bv7hGqv!qU|dcV=XeJc~MlKE_KThC`0%oW;QA4qhcRMAbEr}QkHM5C1-^^3v5"
    ";Q65As=G_eiar}gU3$}{I(zj0qRTp6M2AC~k7-fP{nyE;Sk}?1Se8+q*7rsE2_JOslCm0hqNo?mi!zO>MLN!=**K!kjncYKOB#DgvzC^1"
    "l#IvJ)$uAyXfhUQi3XB<oYLns^<`RB@l9DQ7hGW!egEOz`SttrE9&4+hX(`tfAoL*htGcQ^6OsX{WnL0!)GrZE5V=B>lYi}KF9a+`O$^~"
    "Nxq^P!qf9VU!8w^fA&^i{L8;uDgCJR-hcT0)z!uI<@v`yoqxQf7p?Cu-#z;Fk8iiXeD(fv`^&5IxAgb+_h)b3g)hV2Ywa%|Yx&|>-)?#N"
    "^6i`R_gCvL-+g%X?GKlqd%dmd^Y?EqwtmYmH+@NO7e!e&_ZSxC;={))jPAvO&i41`Z{NQB@ao*X`4@Zj;p5rMx9<7j>CvHlarwPHJ38{C"
    "w?_x`zi?do{PaM|zJ5bhzB;=)bM5`~ufAjb!^4CA;mNV?%GbWb+W2?p@6Z3_`t<DJg*^V#pWmLnx2Gr1Uwotc;p6$M5BB)@^yEYa@WxNW"
    "Pp1dZ4*Jx)XNNyG$->bvx=d&3xQ>VxES5wWiBhI{GMc4K3_z7qqL$NSIjf^tadQKbImt@;q$pPd+HUy@&m*D<QiT$&j40=bDv1`eWK4AH"
    "HYH+`O{1*dsiM57jj+(G`>ei=5+SyWg#ONxIni&ShfHokpozGZ*<_ODQXb?yo-suS@tI|LN*|Z>C6TB>N4p$T*JA4KFxn@&woktt@!iMh"
    "zMB=JWENFK+*`D_!_Tm%WI86pXq8q>7cnJSPR-oWr!<1uB-*8Wqe`iQNwtT1>av(s+(%b1srlpk+iZNR4JI@t%f*E0I$t~~rgA{#?5kn)"
    "g1<VOOlTFx#Uzc=JHEkaowyQ|?#Zh%mUqLbE|)2P_ex&KN7158r`ZFVl24=W6A*Qp(jBc~hkg<fr>k#7D_P$rwCHIvk#SR#^Q@|{1GE#`"
    "Y5Fyg5z)RV$_dqcnbOd!YMDm8qobqK4ZVz|H?%$V`GB8y-FU0IOq01aMLqT7l~-=K(_~g*yy?R@<$F9{6tir+5{l5Hiz!YP3u>^ai<q`i"
    "QQAjnOSg(Xp?yb_C;J!sT8iV&<H{cYUoT1%T3y%JAo?*WbDFSWM8xYa5$)koL0zStcQISiS*oHqj?N#bhZ(aNGyIm5vEr%4VZw3XOP4EO"
    "@P|=#OS@+h6{Ek>QS8V=xwqqJe_7F9&qjW)FQz5+Vo(*^3gii$ymWl~Sdqyh!|Pr|Z*fld>tbIT#$$T^QV&qdU9VS*G%BXbD(vEv7WBN_"
    "b997wkLbQw&TxD`rGt*rAmKg|In$%0qG56!6)#AY&9hljVmDsqME!}JOp~e}&^!7r<{v{{tJcxQ|7=2s;aB({En1p4iuO<zqZrb@zFDHt"
    "UbLfs?)0ObWu84;%U;|80h9-m8=^ux9UjE_L!IVTMxBVx`3SxSheWfHXX8)k#v~$2zo+LD!=t7BkIN75BW9&)9ud6+9sA6nS{>Ct{$8yr"
    "`u6X>XMYcR{dd|z+4{`jJpZ*K8fd%voSWo5IH#kM#q}+HKB3-QQ6>Jr3oij7a8zSHQ7Z2$B&wbfDX(z>l>I0j+zk3$*EfxZtr>sB<@3wn"
    "gd}rf#cOP|(Q-OXvCsRM#nFm5?|yJ_d&1dk2QgiP#_dMrmJa?wG*1&cm)*Q@-?@sr1A8Wq;wt-v=Ig+oI+FH(j8l5vrEity(r%@{u*3L<"
    "#X)B3LN~=K=pW{IHY@H~Frmq#K4mm@w?v|4ePubpyWhF#keRGk)Sw;KuG_-NIGgdiSusv#r}lhClRXoeAR=a9QB<-^`8iR?^Lbj5&@o>1"
    "qcfbne)O^=QHrYQZ=!=##W@IN-w0kmdS6g+x=7GOpDv=&(oR}01sNcjV@Qku#?3RK&xlb-aAVO5D&^<VCwB>*daxy02k+dWn>xCEOQNpC"
    "!5uwkvEb0Z0*^>+)baCg{IjH5<zu-h(RpG_xI+4OG0Sx4V(&@8+p@@uWi|6lMZ(d9mSdJxbz}Z`6IJr!@3Y0Sx{Y>qgYEUB5)b;(_%_M&"
    "boTefazy3m!2?N4f0rZaTWC(N)CD41%3t6e_%2SOkKA=MIf%OWPZ!b}oiW-y3Ey4v`L?>XANZ(QrFN8R)xXv&)^E2}jghU_D?_Df<&X7R"
    "@tLpkQ%d{Swl->|&zKKQiIKz~I5<>jUwgT)tOK32CEfA10L(LKEqlSv5oThZJP`e(4Ful)AQ-~gvMz`eWAD$1<j_qmoSim8AKic-Er`RT"
    "T~XCf;1jfFrbqd5KBE0j^h@?Tcqi`a0sf)cV$zFd=eWY3Ui*ify1T^f$tMUK7V}(5?U-Smr@`7>ptU%CNXE6}lcdfodJ*vpOob>_XyUT@"
    "a^9K`rchtd+gHYgVa4d;M;mU`;IHM$Xaz|jz5jwqrVALeo7L&O+WV(YpKR_$wn&L}LAOzOxlmDtSxULQQA2_HC$wv#zb(^ph1CzPf}K%P"
    "k8k;Y*>M|#tEp~<V=C@x*RaSyj2jVZnzYGsEE*!y=U8ndk>tcCLZy_{stK$3&a4XJE$8W+g}Eyc(jcEj(-{#Aj3JvZW+|A{)St+zkiARe"
    "<MXF|8i8gqA?91|HoKv7Q6^KUkDS_RLKL=Gu^KMecz)7`At?!Y9X|Lpp?(VS(8;ShjlQC=9zUBn;HW7$c60}4Qq!lDWMc3Re7kpC4R7-C"
    "Y&k)j3%Ma_%IahSHJ@!<bjFRx-r|B=tHcp9RoD3{^1{`yuG0gz=jzI=L$s7E9?&>M+5~U27$*x6!)Yx32Z<!(ROC18W~~hGW4t#e%Qf<n"
    "WNTs;>s9occ3br3m3u?t84>JgXKW>|v&oK%!ZeM<(t1gdHWi&{TvuSM`0(6ho_Vo?RNVqs@VFLMQ(6=eRCTU=7$JmWG2M5ypJ8R~Xf9aL"
    "pjVK>t0hFTD*Eqf`YGD|wk-DCEW0nSl20j*s7g~B3AdWlpS&xm=?Zh4j7z%aX%FTVM8br5IcmZ4Z|K`6Srua2hy$*|K@I%W%9h=C)LnJc"
    "GTZd&G)-!fqpYLuU7W4+!qiRWU2$`wDw;Q$ib3=zW*~(t;YB!zpPil_pKhu-#^Axty1JpWivApv&~l%Y#E0WAn$HC|DkjB~3192Pt3A*`"
    "*Bt;=5N+FgFpR-5<U6ximg5v9CTT@)Ma})@!qmmMtHC6rR_MR63q;#Q<@}xPG(bfTl7sGe6-v9mJP6?`m4s$~$!^oxV!E6OjW5%?EEV2c"
    "<V~JXC1AWKSP6~-CCGKK3I(gh(JGGFLzYf#h99QWp}Tb)J#%z{ci%l-2a8md{y3W|IvLYToIOu)45HHIo!7M~PP_h=6{ge|ZMA`(twI9K"
    "t>}89S6v;JHlZWx!j=+Ll?3H{WwP`9O7dyVD!rm`+vF(=W?`>f6YYwoSxKJ+)n!tnAFKah*jf$Vxgtd{ZM^4ejb+7gy-a3dwW_Cdn}~)w"
    "Wy42M7p;8GJFVHB1@5|>BqKM%4fWEype9sO6NSj3;45$~S0ud2y8DsIULCeKvK>nZf|cJ=v2501r>TfqB&%7G=*`*EQOSKdS<V;O%32aj"
    "^KDY4&rUYi6gNcPljslGw`?Rz9wIyf)wP<WBr`cekwut`y|SfU_k#HOT6Vhh_px5O!qM)G2=Z#rD@!)jEevTe5nJn)l6}2hO|ZC07S&qS"
    "<4+J@+jF~KHO~qPN4p?eu(&CoT%|XB2KQQZhrGk)y19E`3Rt_gAeJOq(RAB~s!zwJXmBU3c4(io{tb7secHzv8*b}Rr#;p;0T&`l+zI+K"
    "1LuP7Nxycpbig*!el*F~IPe~nrCiXdt(%R!Eo2$S%d!M@fEL*CJA6S1C(xEPdU&_F&T=_Rhn;ohtu^IlQtq>9S<Lx4zGDi8HC&EyLr*qT"
    "BfD{3_6gX+4ZR9GP$u`%SWUEiLq+ty$p(b)QaXDi5Tv2#7O;%&Jw1`0vZXm3V`~Fo?cz}}S+zGjB%Z%5>3Xi*l>KhQ0pJT5-)|)`u7x%s"
    "_%$tf^01LC+^3_ez=@1oB=U)E{g{p}`TOYNGlX-krC&L^jV-Q?veme%Y}KZ8qgB<(%?%w=AxXmDV8Km46W&&OLDLsq=vMC6j+oRHYhA+)"
    "Bu4vS?aRHM!xkp8s9c2*N{vX4M5jx1m<0Y-ZM*5<W+>M<TNLKWD!NVXQmbtzf#wwKyV$N$2w32~VL)tFwKFM;#SYCei;+n#;)0UQD`NC^"
    "s-PeALu+c&YJJ=sdoQ5LQy3(x;I8HeZ3?Sm0E_OXt4b;nu`_ObWu~L%5^Q28KYM96?`-bS7v0=3CTyO}R_$S&$zxXMnsla)HYB{|>BEBf"
    "cp4?lq?x$eKsIaDf`OOIe9Tr+-CTXQWBG2&a?y*wx!C{V)y4kR%ZpYWs)G`-ryn`flQW)zmoH(L5P?Z*Z&hNg;E+t0C4V1?&?3XM2iK}&"
    "l+q5(AQ0s&B~>`GS#_IEoDTH8=xQpl47a{d*)+)1nzbp#Sgt|p1YiC<<4|7UF!;h7*_E*Klk}zpy=m~Bp-9|ZQ?C(MQOhJvXRT=Og~Nf`"
    "o`(=YS@_HwE6+=SIwxr@+k(cwcJ(k<!CEN#@GhHxd)KXCvYcFNm0PZsp|%(9Je7l4Azs|aqRL@Q?YNlfu3=O2eL9=1?@Q&}%5=t?Q#aEt"
    "?Z4<azGrfjPpVs}0ND0j^|yDWBFfL}DvGFnl-A?D)>=eIgXogm9JU6#y(g_2w)E?<p0u~%hJGCnqO&%iH&jgzE9KL5KCo4V^DEo5Cw%Yv"
    "!Mftr_6dbjNfZEK)AJ(F>VmBW%s4*2+rM@6w{Jww-Ci{PN^S?yk8F~X0&UW>R=m$0;_JZblyfA-+S_ba6|SMp#D49fZB_B|wxFAWg-sZ2"
    ";l;-?qo){tR5+C+AFH~|Tz@tXNqKIiCTgc+8<0G4)TqTLH09OC(N5Q{F5Vlu=Qq5vsoXFN(u><k+4wMK=Cav*3ak7i4TNJSTZ!{0d@Zz$"
    "Ur^62x8`TOtZL$(nf<7o&nZzVW=mOyFg>Ck;7M?=w$B#x9S;e#?(_xZn*`ccn8MSra;=vYS9D#9XKVWclCBM-pU%c`jfu~5p{M;wAG}TS"
    "n`Ls7_F?9_rGxSdkMQUAX@%7TQzME-HeaN2ufmLhA1p!qpQ8c-bP1AD)%c@Y(8*5!ul67dW^gfQp?*%Mo*5o~tQDc9eekMUUHg`xs$!}t"
    ")>^Ou0`@V6+}XaMLMK{Cz0m&V={<Ze-IB|K_nl=RaA62ntC&r+sN7*JS1%X1VN>HntH5`-T4Ob+fg|ymdV(*p*1S(0k7;1B_BMv`^M(!|"
    "`x7_ncQ%CM%~C?3htAl^<_4-#XOY`Tjd~4o)TTh<0T)sZT}j~sY#rBDC3fYk*{}|*4Xixbnxqj2Rc`q($*X&shpiMp!q(l=O}><PUfQ$Z"
    "yW3{LgAUQFR<r5`!~_}Lvd*s02eC&<#`Bz%C0*q(W5U&1KU^!%zOY<e#v758R;D-RI}T#p`o^tu(&l+&Q_}!`vR?G9{-4_;!W0YBua^z&"
    "X&O{t9k>d)n#D%PzBiBbqV-NLkm#p`Zc_SRKN>@=+mGfC{V0cQP!s!9Kh!@5Cw|^I@^Mtps(<PopyJZi+e;V>@=9e=uX?V)dD9d2F{zgD"
    "{8FEYHBzeuTcli{$NV*WIc^a9^eS>5sN!vkUfDHdEY^mbs8!dGXCL3cdH<cBCv;V7S87qM&Cg)V<x?%$OR+E9CoPta<yvO~56Uc=^`Rah"
    "+QYgHdYET@qn&;D3}2gbD*jHUHL4nu%nm-1HaI)hWK{I8$ua*^;olRgNZL<kwQQU*F)3(3{(If5LZ3-Z`YV|&u+hZF$bRWN$6LGi?n$^I"
    "*&(jE1!*kfG@d6n*;tjmJ$dH#8^2@OQM^&1yWxsDYZ}LKgW!#C)A1*oTL`~qL?S7mx+O_A9}Bn5CfUhpo8PCNA2Ri$KaNhHtx*K(GAg2F"
    "rH}mxdqk?rB4D)G?k;w;hVGr+*TlT0#$C1);p3|LF%-BJ6NG>>Ov;)?f!S;r?eNbXR9Oill0-ODP@hqC&Du6N>w=6nO^hVh$V^w_qlao1"
    "&_jHx2mf5<78{JJTj~rm?4fQp1LshQFD>`T=8P)bDN}6iohNCg;;5RpdEs7@5dK3%unuL^VKf?#iAd8?C;l?dChi>eqlfD`u9K4O4P{L4"
    "^LjHSQ?lhaGE-B-%dLG`vh&_5u8aO-O~>m^gHIi&BtK5thk=R{Pkh6MYGSdn1?17#x8s!QbkMRnggS&j^`V`m@9NcBeQ+Ki4*m}BXdmAs"
    "xpLfnCfd}Q7-up<P{0;y>iQatWxbnF4Xmnub54HVd}~pQtP1409<n0c&Dc7n;rVA}JNR69Nw8xb1VA(83{0m&JS^?F!91I%1J>_TQ|r9%"
    "nkYx5XrPUL1PljAO};n|wzbo=hh@?{TZ9C-4u6%C@K-*q!Y}i>O~*DVT5+02?LA00T3tftY#v^?T#_tTrbt~Bypu2X@n&vEA`nRuPOsH{"
    "i|)Pjrl>Q%rzTYKf;Rb>L}mKDzR%=_rDa)S(-z};hRq-sAU(ZC{nv2gzs}f0mqQG*ad>Cd%{j|HHDoI8K=9yGIXVq~j<UKg*kl(^ZtHN?"
    "@_Az=rlas>W6l1y%)%CClO%k*C>om}DcfScUo<~6?~;6F`ZATrl(COqt*ha~@!pQN)xU1}U<Hw*oaQ@-Q;ys0)%Pzij5>v~McaM^UAKgw"
    "GW$K)R_$~e?XH_{yxZ|#iF8nJi{;I2<6>cdB@)7;cV{onb7B2-CV9*8VUr-_Z;|E+scu82{BQLJKZUA-ZK+x}F6vF>y}Df4&YHdmWDl`k"
    "vuvKxt#`=Y3E(#H+Zj8Qg_81>ixPOMn<^w*72#d*8r4B<^`m$A=ez9NLG&M(?L@VyPp=ssB}vJ_E|qr6S?}rHA)5Juj{X3rJ5|@v$Q#bY"
    "JSkt`Oib0ihfbIIH5O(tpYYj+vT}q_Xg)PhuP*c()=}$ukh*uPG<|w)?%rvJ@a?sffJXsMpTH@Yn55PVI_AY~_;Ybn{cSdUveE5V?B&Pl"
    "&S%H|X37kvROTj;eRI=XEur31_lvfpnI-#C*BT&+ZIVFU-qqL%M-IY6Z;_LM4!9uct1&G-je(S4@>wLIJ}`urH_TDouu{5Ni<Ainy72Jw"
    "Tq<mQFiB^1QZ+9C^Ml}bY7uJdB8q%RqOmM6bcuM(KzjZqEsH=yw&u>!%ZY5q77XJ2FnZBz{*#&g_aCk{wBe(P*nXJBPBwwg7ZOp()6nlu"
    "XbpL+I2fC>=1+oe-kGn9grI3y6fu(|hpX>9^s(4vpX$4$<gJz51q<F2BLapLx+P0-L|{>i{x4z+Sh*H_K4o604#+Td)f^(izMlX2;{4;A"
    "cjxb~&ffCEt6-(4>W0{AVyR$`6DOg%r1xU(#QhnHm)^yTLv3>n0tV*8EV-%J95)EvCxg&2n0A7Y&AvJ|PuU_oT6)8Zvaa4mnFSkG)AHQ|"
    "g`-d`QKd`u<|hV5CFdZj#>A*`q`{xEG#q&QtRH8Qx@SB&YCvt&z^fluX}zT$sllx9d=A9-LhU%^ei*LXsG8?BmN@54wYRF4ttZh!ektYi"
    "X1$9gNm<K^#4%R6acnZQVlJ|mPnVX8nx)(%bV50(m@Fl-fJ7}i<$+?T65W#CqMtgdQ;fObT4bj8`bQO&k3#34?D3%y^u96naSIz1MGyDy"
    "LiRbVMT0?Ox}1Z*_?$&Y>OKq~c=IS8BAAh0&m^{*U3)o<lRbxf9dYH0q>ONtNf0*BwZKpg(-L{ZIa{~l?E4*chK9A=@kn&9b?K!vho-o7"
    "ZmExO9*$J-ReO>iM$Ra_2z|?55<NvDkw|qeA>T{ou%1Z_s;FRhWOO?kZ>&X&Jl)WzX5e+Lp#jtMUWP<-MC2@E6{v(N$I(|g0=M-Za-1K("
    "$$~em)8(f%KP3u6+k3tMzca2dZ}{(E$-kW9e1~?BtnZEl6%TF(L9{MbYVcJ)_^NiR>A5wATX4~d8W3l@FN4~`oTY+?e8myz;ks;90^pg!"
    "rY=<bU*!N;7<^Uv=y`T?7SW_}ReJ;p*XJ|vl6iy86y_cKm3YNimQxuS>0_F+Lb9=CxU$Q_^Qlsc*hyLA{=zXEEMXzw5A3_eEK_s9_i&0<"
    "@Iu4r#n&kJHNW}4qr+!c!i`Jc11nN8a~>*zWT(&swq1m-fnFk>U{&PK9f<y^s&qb@tp*eN;8s6K^KrRa)Xr^)>W2E;0v}O5Un|<9SfYA1"
    "1&uq><W~=ihVnk{<26pCpS(e|QSSLPqN|Vo|ILUBY?6953N`x91T~%fAl7PXF?PzG^&`Fw)HTh7Uhj*6y~gHQ6DW$QtE}rbPM4$IFr+Rw"
    "Z4uJ0fS|fGqMzX5&zD6qyMa3Ib}sG?MjDBCzi0>k<{aiQ`{l$3xAAFYQHggp)%RnTPlz?^2d0&vH9kFG6NiG$kbcb<PV{E~LlCoLW!2K{"
    "7f$`u49<!@oqjn9KarsKusv~uS~E`ff;9lKy@x<?z~|%eSzqZYywa#Wb*zFtXU0y0@;nGY^zFM4^j}V5vr~juCZ20}x?7I9x{B}()w4eg"
    "j=+!qRd}y5@=Rm3Xm0^}W>FS*8AR5)32xKz4w+Vs#c_nOCp`g_AztEoB0w^xx-&Y>QLJM&=8e%y{w4S@<|*K!!Xrf+W6&Fv<HD_nd?jcz"
    "^k=Mbx=bQiyy^L4(_LY=8x3MHP>4kdlZJRgF{_s4IL@pI;)=vBctewmb45HuS1cg`Nz*Re7E~yPP#ClOuyi46^+6bZ=265BDT1nawsR0)"
    "s&Yexz)A_MYATmRkI|(bbk(5TAh0sEcn`kH6%kVqo&~<n*tgOj`ik9}!+q{PV|$RgN#A7&Z;^%*wBzi|Zw)9tFrEA8$mrXP*H}KG&`Irf"
    "5qqYIzC0WTkGvDQTWKH?&8ByKorA(k?4v={p#gSmz0WFUTUJ4c95sN=K5Ba|^hS$mEFTX$3bn#oMscggOu!V8NC-37t!AVExD?tY9H1C+"
    "1X@{jd<+~M_7K~5lSpXrvQh^<VatgZf&D`+0*zgYS!{aBRTUKfXG6DKGTKlu8&xDRAuvIK0fbQDGz01z=e&x<$R}fL=tCZbq^YdU^?`-T"
    "E=3VxzIm74?S&zibcBH~Q<(PaA6314fzqX^_23435~$Epp|I$vcq@S#Mf_xX(T9dO#v4w3IE6(6!J<2Hz<i1ZF+zp{SJG+HZ_H~Yfp%3L"
    "I5A3m;Sr>|5(+K1gtGSEpB<e(^JM`ic@BH9i7Mi33RQ*{O)3>+m|{D|P#i_0$x=L0Q&$1wM@s0RlL9L9l1U%5vs3Yi?uAHUzVaV(z$Tds"
    "8f@8^j+#9rTnJMpXlvLRH57uOijkd~Q#US+;!kE+Sc|O?@ec%`YyLeV`tkSX!w6!<n=iJ~0an5aVn)rT3)dEtC$!M9xJWj8)Adk{GnO|5"
    "R!A0H90g<%!&N~;9UnwKAkypF4`Jxs@EwYlccc&3U8W&*l7e4SqGMCV@k#S)$v(;%{HBSi@hftL7~5s;B}ftN{dT0f<wh~rzHvSC1w~3i"
    "1ziVhCpRaUvq?%M&7|5wbaG~0Om39c;B8YW;hg`DHqh4~io7WWuDpxC^==S-gu6NId`9WZgUA-yph_nd>q!*^-Ij)++vKAB*j-gWG7)19"
    "m|soZdRx{{3JwA`aAQDC`%AW9$YyUSv3veFhmAYDlXd6aUUT!e&>CK|dydgChD4hgOBxVASDAR(xT$H?_Cb&kWh31ffT8CHg<uM^9WY<_"
    "DaU$-OpmElc-wQ-xH`c&1R7Me%voScC%^N&M&DJ#TnU}98&(sP5-h!~XU==L%~3b`*+2^W!91H=c5~CfutF}K0x6DtXP`8d6GBHOz?k4g"
    "D;7!u{LyS^HC{E4z-V_IG=g$^3JoUp(<K>=X9df)%wF^Ek{eieN@G((&_oAJ+B|GXo3FQea1EdA!L{bQH3$?zdQV}?H}H&9fih~MkS!~v"
    "i(c!kw=taz;xE`?ni(E<{dohl(orH1%mC6z=4oqhs|OkS+m8Z2vL37==Z(<!79=t}j6_5MXxI9kV@9k0g<<hu48x-TKLo>~|GzLS{;OkH"
    "NSHfRpv<5O@l=(BD0b8(u48MiE>TQXaO{Y2=$Kchusouu;0`$#P<mtp*oxAZs?V;7_ZK=2S%&qort4#6Y*8wKLnyw4)iu0Gg|}Ai_FUS4"
    "s$vI5y`2D+ij92SMO2Iq@YxtNboIkXuUIyfY*7Vw#ppC%#335P`e_ugcj|*Fy?kjOvxw=I!bi^s3({DLKJC<ae7np)nQ3#G|B@{h>O-<^"
    "l?K1<DsewIFH>uItn=_I{^u=}^Mh0;BehI)%-=*14Sw}vaTTrAS|%nOU+N7O6RAwcOS<M~^b+yN3&GgZi~)w!pHG}=*6f`!8Lu?GK`QAC"
    "436P5K}b@=KD8NZWg2!AqaVY^M2)~$f*Hh^l((qTqy)lo!cn-e@5~qVYG6<$i&?<ZsVNJ7XKcNfDtI$gsa7F6Fm+HB-8O5#Jq(w`*;N*3"
    "2YU^P)WjB5%gmuGz^{9vsA<btAoOH8$?db5hcJh#4(>O^hSGl|>N|RN0$<4JZI&+|fZtlDbGEv9t}<C^FYnXjQ{b1?!!U+Xm$8@`@EH@n"
    "e>ynX|KA7n*Y7sH*w6B;_HSp|=-J7p&ss11X9F!Y2p&3J={W3CyY8ykR5gGF5Y$6&2VAJ@_JVBJN)g)AdhF4r{m$Cg(posg2aNUMA^O<q"
    "(4|w>qtv!B>>N@>%xH$O!(tZ({|4*_vC$A5iYe3sPJPEahd&aF>z~e9FDkT6q18eVVwD&i2z>O@Vf^giXFhg~N=3~uV+7Zk#0ro+9oAn7"
    "L?akA?Jm?Bfg>LaAzV*hxGxQM88s{CrP7^?S4KZkT#9x)urZ@Uc%dgR@)-V2eF2B`pQtVy;qj_Y!Oj)gDyS}<3?7;KaMD?~Y##}wX4O}y"
    "QCS0MhB5X43Qi0#D<;I&8dfEk>)ys@S*GOM?nbO_fk-ikjH6~vnWRNAN$kz5OJ$_@#c5cMu5%fY()TQ3**ZfCDLBZM^>ZAgvRpWa-@anX"
    "tB+9-`L~vBAyPY-+U9~B2pQu^XeTNSUTN9>Sxv6iJsS^iY&LX^KwhzoEJ*oHn#kUQ#V&KCjk7JpLe53~?&dI6V`I2xE>JkD!cOa*dHM4C"
    "?T7EK-_p){OIO4lgn4`&YKnB=;{ViHn;YBi>h%(RSg6aJO99b0b*2aZ?Fe)!y}lLkC#ecW)N0xVy}i3V<Ds{Z&3Y95g)S#7(JY0^)P!ca"
    "h3nAB*qS5o&V}$mW)_rbTVL<y)V==j@!i=~ICs5p^2`X?{p!^)`s$MY|GTbh`L*ixi1m-34-Ue{75r;+T|a%5{S3dApT4^MnF#OhSJUBF"
    "v%ToQeKq+#{mA#=(9)HaI)l+AeNY<(8>y6LZkyMQJ6Y8+g7FGYfKR>Dxc9}|?Zd_O>o;$&&OdJ2az->ltC+)PqU&s#lSplBgxANg#2ub{"
    "cPJ)I`bW!57hU{x*={xqP%D6<oR)Ja5vU=nsShm%a1Nk_9F<u*r3cAPUQ{*5L-d@VuU8@v5fvtd$j$f@RC&CugV^n!e-jglm%a>%7<6p5"
    "p+)0-P)-je2^nbJ*m9nyir9jZ6T~mE%~9lhz1tj?5rfNt+O*EV&~1Cqg$9WqVtf6F!K|ljv!)6V;o_0<N=(#R&@#ChdmGyS!%YuwtvT)d"
    "U!t!j;c42~5rOA_#FDugj=y=x_(<_-+R#cPeb4bQ$hiSUDT53w*fQ(H5iOslQTJ?ehxoJ!9YZN3bhGLz13Wdn5cMAkp%CAv^*mXiD(viw"
    "*ViB4y#H>XS%QSQWr(6`0an)aLd29#GF6~3S!2GJX)>Vc$rneJ_&n3)<xrV5%FWD=gQyF=W!GySJ%IBVQedZHt32#9qRJxxCQ^$TOhm7*"
    "FV0^6;rz<H)Bt;x%rGzBAaAaBP~HhQt~D?K?>8@6)%!ZNnEFu%&v898nzGnaI20icA*pT$oxs^R(~wrD+TzubiT;FC3A5<;(ec1W+RQ+J"
    "BdOVMqUdYu)wMt(HasXmmc*JlH4&&v1*VymooxH^v2~5=#*1aMw%R*~Y8M%={pH0EUsmzo=FNI%S^lYkY)<nj2AL%Kc*&p;GUl}=tZr#("
    ";EB3qHmXc6qlr8jtal_GEvB?Z)t@5`mk@FqpDL1)_Yq5avn1YOUpIbCLfPaVf*GoaA0~?dl!2CwgcC?;n6EYaF%?sXg?0%SA1+<QnpN0a"
    "iU&i~@=Jl8<R=hiMcC{F`er+pJbhy0#Qg1+HZ7<Jx?%>Ru9vxUW#_7*Hy{6~PxrK1Yq5lB=1w-U<dmAE#9}av+wX7_LG#&%KdMt!N@6hS"
    "S1`)vc@xqXzV8_LsK_VNGPw!UGgfMC7Gnv{oqEB5qg|SM6lTd1UOi%_?u4<ZeRZqk4a`JhA{z=qddeJSqfJ32z}9n^v4&CB5iKvuyITNa"
    "$oP|j?sEVh_VHbjO<-9O)qHgiHxKISx4c#<)cfK*c$eA^s+J>{#B!`T0jOTSz{8cF&)F4}Iuu-rq6Dj@pVxQCZf9WU4VvVQ88D9a0R@71"
    "I4%||*`orkC$2qgX+S(7J;@eTvnmd$;oJ`FANc0t68rV)>_Q#R*{sBI?O2dIXuCDBfmESgjqi@bL44%Ng7|96YFlO5R{&v=2n=xrRlAIV"
    "R*H=v@LBDN)l07&<LlwaFi-NOBmjX@*fmQ-@fVT1K30u*tKORJk|?y(YWYMie8juq#+UxFBL;N|t%sQ%dVG!M6|PCqrp8<aYK3HeuW<X7"
    "GGJYfl0>(=z|&(R6>VbRH%)^pb!{T_B5_~CQ})EJz;AieSwNt{5(FCymlzGUHhHY++$%hT#-@rnp%!(5SZOB22GA(h=9oyYHfceeNJ_B)"
    "Nl%?kLe9dws~^JlN2#lP!8tUj(j(ckwX<fs7y@q5MI|mP*#jpB-#k-Lyxs^Cp!0Hk^!%AkOfUspg#CPo(H*k51530#W*6y7QybtOsTRt+"
    "XSM1iI?k#(bJk{QR_l!B^eR)`Q=?z5(ZhrF1>*y2=jw<v<|290H=@~w>=I|W6QD&iputn@nyk>sJZkj*@c8iHIo0Eh_KKne@QVafU=&b3"
    "$)*nD6xkmNVqfNRZh7IFS{nKC?kEl?Tw2shKOo+*S}E~kycPsN1ero$DP?btJH}=OXq&~5IlvHNrRe5J!_X7&*337K9rIlz{7D|D4)INc"
    "#%WJ)8;LAa*GKI;9CuU8t0fAmkd{%u?##;_qw5FrtZD(?z}XyninNt)H;Niiug^|Sk54;+Z;zV;3j(G}=2<mf!i~|T199?OtgnMxOJN1g"
    "F#(Q6602keU*|I9xO?J&h4jpexrK%GjN0gp({E0yNA=Ae^rLH10DA+X>fQ+1xBFOpD5l`nQs=i5vW|8wwcPg`Y;&wEfTbjw*jSmzBqFCA"
    "g3rvTK=0<+?JHWrFy<!?gL2*s;(+1H=Ec^c4c`VX44G)?H4utp2cJxM5RQRHv!Ink@7PfWP^+x9uqs?jG+i;~OR+1xox109SnlYO4eYDf"
    "_ixA1&Z@E9bS+oGP^4N{hx{?r=`<=8cu*JYH?8@mnBu$b1)ZQd__G;#Mc2oJ`dL?;bk@kBcY5Z8aM6ncb|0VEskh61S*2Tijd(n)v4>sF"
    "%XZ*-s4B2DA<OdylIda<w=ze8GZIEg-9ObggLW`;k41=fAKddi;(*OrWPWRNI~f-UCWkt(L(S}H<9%ny@9_tsuY&!n*22`aMq%60>~t>v"
    "kcylwj$)m4S99r?vhX(gAqMRqWhVGPJR3ht51t=R4^K{<qz3&Y3tYH6{`?9SUue(0B4V_{ec87q=j^`?v8=CrfRp{cTu57&&eWwa`u@it"
    "Y)@tLLF1{z6<OwGI?KfO#qbQgakWe*bGV3u6+lCDd$Uup+;&BIvoBb^`_E5bC?z-Ae0%R23)2ALegU)Z`~_Qjmi6gw=}Q_qj^|Gi!&;)v"
    "mMiG98^LLSHgWlD!y>Z1teaLLJ?aWU90u)(mwO%@A#;MV07uKb4BujxwXQLBAt*!7%^7H~KkBn|T1O6r6&lUHedpyT))(WXa1sg3fmX1a"
    "<;Zrs7ZQ;6Tx?RaCA@1lY1`=W@X>KRRo5n35{v)ZBqp%_jnCo7KZ`1++B#Kh?1kUHJ)HLIS0Dc*%!D4I@hzQ<TvMPzi(F=4-gKlDz6rj*"
    "{KL0T`Fc{MnuJ`vD10rCa|Dy}&f$xOz4axkPoqW&>rr^Y=U5A+C%ei;0OXCx(M_sJU1lrG)24icI8M^C#uf~hTcxj-B9Kawh*9SC5TOzy"
    "scTqK7`uWc_`WgVCSL#}0SvQPze&<jrk!^xUl9^`gmQ90pe_0Bb(i{7S0H^r=tBl6Gcb<0bQ7v+7X5SM=CrawL)x!wW(K=zIR>IVv?FX9"
    "(k|~kjlIJ}xV3V#(poJ%a)ma$|A$r+qgr3iccK|0e(5G>Da!3=;zU;dDBc%N2ZN$wbLtorh&^MsE%jw;0-UcEkh^~t$}IXj+93)QdP{Ap"
    "-#!sXsZAw>qTDWT(uG*UE8$;M{kX1*;bM-nbcQ!=X`aqw*GwR(Ts7D?i-jFGvXd_ux-W*nh-~pQe}JrY`Am6CErEMiEqfDo0M|`EVV|&o"
    "-TchfTLn198{`GZ0J^0*0obzdZ74Uohb-)aU8)QQA6~q3Mnb_G+LZGQISkcD1=dXZ))^4kGXNGx2-spFmwUm;r%MjXUTMl#H(G~kXsug1"
    "SL#Qrzcg7(h#${MI&E0(&%sal<pqxpm&0W)jJYV$gduLOvs{@UE_bTv{n^DE$N%P>S_yS!NMc+rAlqh@#uLDu-$JvII~I3nxm*O$HRAon"
    "5palOU23i!v|+WIhT$ILniR5o%8*c2#k9`KzsXmUANGOhZ<>^|RbQq^Lf@;E--3l#VFfNemyQ(9oc2+j;ruMkiu?weu_)a3cF=FPX&2Vi"
    "!G15_5YZG*8>eVG;{3_F3-V-<#XO(PYsWNL1R`}Ni^(TcktVa4T{cw7h!iEtYc5LKy5&lZ(-*J)u*T)E0@yf?Xcx!w%KcOwGm~5~P*;_Z"
    "Bi<sV6geCoMyy|=${eGleQB^x7}D@~G(0#M9N=`ne3LpqY1L=EfAccZe%T6x{b9*@u}%%5G~-Zx<+Y$$cMO>_P8|>HjY0-R0;m&b@>CAi"
    "#;Qs~M^K^u4gAzvMpMaQ>Yj4|BKyJmxd_6J+X11Dt8*eMj)>l8ViM>H--}+{XSHY{TuJG$rJ*&3P*Sq5si$xi>-w+9qqDkpOnj>QJat>X"
    "GQ9^U%*%b*Rvl~l2(2k}j?y!tstm7w+EPcXI;gNNw-fZ;MqQ7J_1ICn0Ne7eA<#u~{E17XH?Nl@znvZ&sHX4T)ep8KC+S@_PMwC_0s=`)"
    "27o}e@cpyZ3OlIRlgY^Z9YZIw-?xvgswxiWiCtV0ot6jmCNXb=W(1F1tbK_wf`vO1LkNB&NVvjPilMWSk{y?Q79?0J??oR~^~30?=s(vx"
    "@}FGiZTgT*=m-EYf;x7XjLhFDI2@?A5nUxXV6^LAE$54mRrQ*G;=X4k^6tvnh8(J2Fpl`{?#@`-iE!swLGuOlQ9wqi<$M>I&FkB#zr;<-"
    "UF#naJm;n0V>bM@=&{j!x$uM;OX6bW0v_N#VY4IKFcm@#kg+YqNaElGiHr9uHh`ydMaXM_(NAXMC9HRz4kdF0fHMXQn>TiCQ|>8dfYO^C"
    "grUzDML{f%{vqzEUt^<pJc{clPNXflHdx1~HY8k{k~_??ndVL%)+f{po0R_J`aAKSA0Hp~uO2kR*P?d$o*RVODjX*?DUVj`aI5tbR`6>r"
    "<wG1a<7$9q!ISHtgpuK2_nFUm?XC<gfcO98Tx7I5$LfR-E2Ir8EVD&;DT(X@7g?@{4|D9(1E2xht_i%Jh}AX0+Y+j|fHR@RdqM3rR6hE?"
    "YT_!<N?3eDWpQr1bYIYaUVZ#<q3X%KhF>qU5LagxK?^jRp?5|>3}dp8p#T&M&{KSS0GYlCeFt&~`fwxGPD!CC&Vh;;@1S~|<|{}^6Dq&h"
    "tBzyuHt`gS8RL#eXPq-?B8G0doEul`<{R^|JMbxYTl+5h+*M;+f5Y7obbO71Z9T}JIgpQ>v`0?U7p);2^P-oWAbvq-p5v-#*@%r3ZN?Q3"
    "*Ztt?+XHXNWU-|$wha~xYQZ$Z<pO2sPT*tb;5QiyC(yxmJ3gf%P(aM*#98Upm0<w9G?(HDx1w{B9x)nYCkP@u{0f_s4YVU_`97P}w@wxe"
    ")W3(%o<DznbogxD{L-z*;v~YVx1-bU|8EV9{~xsruBj~k2U!RMjr))A65w@BNba5CDuDYNUloSkL0d+!>g*iuay-Vn70pU9-|J%&cYFwz"
    "xy#&&6TjXHfyAW8&ERs9H9u4-VCH<VsO(e0rwWc~;*qdih}}=C36Tum3mhnNoV;)F8a*~oq`AhFyWaVO(9*cuxwE;>i^pvLx+T|b{`k5g"
    "A%2$TeW!F4uZqyP0hxo|;y<bp`;-^=wwVB<#R&+&7|w)`Dg<)M=2WWIL1=@xNe*8;X772_zOi}tbXZ6d1WC?*EE0Nv635gzHjnbHC-~{-"
    "_X|$%KYVt-=;Sue?H8U`*NVt%oejK$o>n-v`pm-2%kwGVLrQ<$(VGD=^bbCU<Jk!yAqT3vV+XQ!xEgJaqZfe07yS?&4LZGSxKxJ9TmUka"
    "_+u%8;E${<M6b@SMqR;X=&Gi>5a3n;+leu)@r2o26OpZA1K`qVVL{DN^W@93ivWu7B1jr6N@c?=T9$C$^E{C#CTY}kFvF)4By$-?#|Hu_"
    "xJhyglKaYCbU$Nk3nG8$jx@>oR38&}suH0DKSD2trEB5<$%*-mVh5U`1C3CIlOa;dMsFF$|H4x8HZ%tsYw)t6-}Tu43^ZDjv`3Y)c2zJ}"
    "8SJ^3W#g5^-NpLDN#1@vnL2H#FR~oQO5D0&^4Zt2tJwJNhd3wTFD@fYhbv`2QDs*$H?iigE088#PUGPccleQ5I-Q-$BBTt`Ts@EUz5haW"
    "4_ysG>8kGV*r-@+5RHI&L~l(+7UQ^eF=)Y&G({S#1-&B86o)cNQjM4VBnv21<-N74U5zg9a;To8O}i^~I=V>n;1)$FZ@7*_g@frtu0qw{"
    "*6A!y>#boy<#hB&$dK<eo0&cO$%KT`({BzA`uO*d|2^V=kNMvd{`Zvsea8Pj=YL=DzuyEg-w&~+E#b7&oSpq!ejlbu*%<wVkLQ*D@{kd9"
    "ok~gl!qd1e7TGvv-EHjgb~`>@z>|x<Q)pe!?95;odiText1#bT<-%GTeXSpc>@xdEbuJqYLks#En`72O=-ZK4gOGG+>s&Qc5N$1nghX3k"
    "634jpU654rOSjO;$+1_UeP>t=|8aJ_{~u>3VH(6rbVrhG5W2@%;c#pNH0HVq{0T+GItH46eQQ_2bBW?Ym2^~z10MKmavX=9Xe#^vnw)HU"
    ">k-^;MY%dDyyt~Su!fV&GFQ2-5_WeO>V1&4foa81aGhNm2jsC-{ExogRct;qLgEro_d6RB|EW7JR_*$0Lv!`%SE>*Xmv-bbH~C>xWjmU!"
    "ZO3DwR&BXRh9ft^FcOg4#x)Htk%O)(358EQR6C%%Oi8w>eM|-Dq{Zj>z7L`gYFXgArFltV?EEWRl@+De@&^`xK`;t%>q9<pjTLD&jR6Ss"
    "3Vgtw_@z^|sbyV-U=lSsse#4<Y#{X+VS5dg{|Kp}14Cusc`L}Mch)}BU5G=8ES)oEe*K1%E!@cYvmvJgF)R#L<N<oTJ3UDY^-Y;x{_$<o"
    "*@D~P5Eu2hoUN>LZS1?x&|Kfb6DhBwm76Q|Nsdv&#docWJ*qJ$3^!kNz@;C?&*-|_ofC_FbSS>D9D~ZHF~t<VRPcied6LajU3E0B<-JCq"
    "gT%>d@|RR|k6wveChOJ9^N$xVf5k+}{k$BRu;C!;r}g6TyE&ahyQebD_BLF~!eM7qLhbgrSY@|JR(!A}IzSv}Dz^7lpRz#ftjQFNvt=+#"
    "1IHIcN5f-R*o{UvwH4>Z$x;?`Oq0d-&Q{g!qw{i`phN=*=$~~>;F4ov8&IZAl=<^C%@eeLoS<(ae~(h?&y!_?a`<vO7=4Zq^06y!kG8HU"
    "=S}-HM-nJrM=p&8JHm#iQ5j>r+`=>pv>c2zBh69~e#=j7@1C9>uYbRZY)hTdznT24Q0HZcaVxaRzBR%?=lM}SS?UnB_93iFUTo_mgW<4x"
    "$BwEvYo_577K_DcsbH^Qk4^8=EySZ@K5{I*k)$vW@P@@Jll$1?!8Y!`EvtI@?&{)+WY#B@4rO^%5Wjo#?mT)W38l=W1Fy19m?s`@BQEKL"
    "24<1hx)6M|3k5Gn9V>dLi=5nRC;1Zm&uX~<8skL$Z5a3#am^f|%0XpIpco0ss<Q^xqLKtCY5^lUod$T1=zPp$3PF9_14EVd3gB{}-@6&H"
    "gWo1qitF}o%Yvw5%#62$763(PuieCmi#Jn~>Z^7QYdx_gmas|&Cy?X8n^LrN4sTudBs<5{<#Oy4;5zRUpTQE2VS6orNCAsC-X~1J!mwMi"
    "1*0E6z7?Y{d|@~Yk3A8#w5l67UX}`bAJllsV6@n^TqpclrSz6Q{{%AkbFfFk%431HMY3KL>q}@yA1p#2DABXJ2=b#d)FLbHTYWHtvR2*5"
    "tQYphL;530N^yfeXcyLo*-+SONVM3=B-OLxSkD;0Py(IB%4jAa_2DEwPE8YkrE`-rreYu`Mv*0TZqNvSsvRRA^W7o_f7Y9F>XcSajkVJL"
    ";9GL+AZ^gW!P;A`fDTx`7LmKD+&$;v3GSI}o~+ZwrUFYugko|0YeoOV!-FSD5+5#(|7kJ=)%}IkI>>eX#RES6rXQW0oPPce`SwdV^`}fC"
    "s#I=b&;Xv?K9#*KbJ-L^dQr4hM98PrXVrHNS)hJQsF>ugwmQr}y)par)^$+DrRB?BPJWx3K=C&AJV5&-%JY#^UcS`)0CbVsIs}-hN^z)o"
    "iP9m=qsdf<nk&q|ajqfH0xWeazWzVkc<Kj1rIIl&+NnZpZ{pEg{|izwJ7E02Y1P#}AhI9b%!8YO@0MYWiA^Ky-Vc>#T7{XmO3ORC7&R~G"
    "Jn)H^j)5;xf2zh1-)e3Q{~o-9xq39cgisH(ek3;tNUf4psRv-T!C_)aoy!W^t@!JiWc7q8qvo+su0@A=&6WIb(PB*Z!~R8p9_V`}3V?Rk"
    "Hup@*{`#)D%Si6;YnlIMFaOx?Wl%MQFz4y&Y+sh>12Lx&2c330fzxNO#2Xh;N;J)1mHGdWAYg7{>)S)$tnGfQIrJ4}r*m;yQJi=%z#RVZ"
    "4{x~js-CbMSGVvpkeo!RaN^3`HxEw;kSIPlYmK~=0BYJLXAZ9KBJ62MVBTdp+=Kg~iO<G;c4~Aw1N!;q^7`cZK>j%Oe;mpm&*(`|9UeWm"
    "LeH;H`_b6~9%<J{&arKDTL%=lO&h{o(v9h-Zgo0envlMko6(RAnpv-Vk}1@@avPc9H&F_Z;y*Z2ti?7QTPxRU%PVHMT(z~ixvY%i*o>=N"
    "Z#?*DjlFxktDD<6`OE;@jT}DPFwiD>@}fJdqz;_HbZ>hz{u{A?+Qc5UT4MKK=LP8D$0e{>V?%tLNS}oRhI2B99`-Qdq#$9<?V6glo<Me0"
    "oy6sjuU%@Jbqmy>`CR}Tze6S9D~;rAvtQ;3{womeg23fl(1H^9PbHgGy4e!`t@-j&Pf4W$kZ=RuH+@~}(r;FPscL1#kpMxfi-_LI(KjdG"
    "JbQlh;%LKJ>IHTGx-O<I-7WfCjKElh*yg5Xm&gQlzPTwm{UMwOIJeYt;V?Bc&+8?RPw$z!U7JHD=8Kp*b4vW!w`&t{ba?Xo<i+tbIzj6b"
    "P~A`C#yMz=e{*(`04X0^qWQcvo0}+8v_9!u2opfjl86}42`BlRDdt%~uRt7Nqykifi1Uu}3a(dchx6nDXG+saAeSpHc(^X6cL`Gh;<Rr$"
    "n^?uVYXx&llS#9#I*eq}H1ZY<TrLr+`lb$mMkHi++u4&b(qLjgIHr6porwixcej7QAbNsi-Ve~wX_T5KaVzm}BDYDbz6+K3=`e~TmIc1*"
    "M~BhB>EA!MD6FPEZcw8TFTB{+cm9(5et7VNxe=)ZI9luHdEx`2WV;nh0m^2Dn?U9__j9uZEq%EPjU&P3u3=bj|NFbM<^|Fy3PKpWvlIH*"
    "M~$FzIl4;*4`w{kwQA{7l8B9R)tXkrHV-KfQKf7ad?HC^nR;O-dgXl3O_IKhI|#(NwgNnCMfVBkSO~jnp_}172m}uXsEc;lorp&Wevx}7"
    "{o?QX?k1tPc~Lhm;q5B)?OkS27O`k(auYEIHM)$tB=H=_KM&RpnjxaeL{4x)vs+zrku-ne!ZMnz(Q38~vZgPo0~p(_!{Y><#93`08Yo>}"
    "hy7qLYaME!xWN<z`HEG25_X?MI=1NY9@7v#rX31QKo7&{^zdkNjVzz|Y9aL>I+IeCYc?(sciBH!n6XA>THFu7Yol<(HKe=diH@U$C4ttZ"
    "AIfb%9e#5(IDGbEa5y;FKRO}OcLY#A`oH}b{ir(}9(I3T`??_{w1f>`>Nk`YJ|i;pw#f~FMK3J4L2}qw^7DkX_hjlCM_E=q-@X!SFW{VQ"
    "i*vw>^JtO7EoGVlorsG6YpFIam0^jzD<-2QdyJ0E<rE}R1vls+BydN8oFqe&TykomVqL<(#aGe2pmiFOzW7o`yNx`ST1L%ZQp93jIDpAK"
    "&)&R>c4-Qe8K=z@zyWqplXXMKIm&>$ZYVd*tYvfPS2grR?|RSWafB3mm<u|;O@zS=^gMQOE4_9{bLmlWuj%;S!he@J5z>23yP{R<4yY`X"
    "D+8#)0Sh#?2okctnfh4{?x}v$8$0G~DMRVNfU5uwG+$e+v~m^N*5finxV;H*T@-lSEBD|ibXF?LiNa;P`|#@9A1;Xl!b)od&DG0`{WllU"
    "8)*MMlJj>^)J1<H$~)?ZK9xL7kIv058mWZwAaxu~S8k4jbVvGpP$e;4wZ-B4<g&mVE_lHi2Uc*r3$ZIZG)d|8KI#vyJq;*IeBUInC|lo5"
    "mCL(;)T<Uy+On1K9bN@4!FGCfw`8Fk()NCm=|z|RiB^}531Erme1CDQR*($_x2Nrkqkz3|{K4^2_+(Lt8|&e-;};DVuwn!s{Ynv!4Nvvu"
    "*{ieY94-Ox(;C|dEBKQB>*#@pC_#6##jou8$;pdDZ@sMC6EQPAW_tPCG8=DyJGmV{@@<uE@$=$`vxzs6{=){T;}_rbX)T<I_8+!OwJY4p"
    "O1^z{cJa?}plsK>&9%`pjq||5*PQO2nmjD*b-vbiQssx{Vx)SjiAR)z@pi9+GI8i}1e0z@<T=KfSTn{=^vy6#!{Y(r#J;A`<khXu9wtTv"
    "`<g+}644`R920IFCVc@aoMw{=vhf(;_$ISo&sy|HQfEmT#}dG+-FhK8`tq>``0!0BUhfJ)R}_3BYDAV|tDrNYn6_YDAD?EeSOfoQJ^Ifk"
    "=({4a`~G@IFR6}*;E1!OZ<<8dKx`r{wi6-TuD&XWu%`DsrePEC*`Rk=)Fi>UDrQSfAkWF$1-jq;Vo7o7z!<xO0cWA74a;eE0ZsxSr&JQ9"
    "lq?Hsl$ZwEDGmbaQCt-tNu8CxDIE~^E4F^c?zQPJI_AsD8I*%vCGAM6?Sx^kc+R?T59$U8U0wDQ>bi`{F7zP`iMS;(9JaPbb(s&lmFrM>"
    "OIEnL*to_x_<Kb|==6Tm|7o0@i@>vkDv@{c_BU-$8~nJ;Ey_=0@9-qZXUI&BN+@Htb;g-M_S}@ka)EfvPOn_%aYB2u$55`Nq+G%;E~7s?"
    "6`~;_5(y^jlqa$em_AOs=bY*|F|0Ue!spNWGGf#jg)?J4eaTC=`|<6YcW<t)-(P(E@UkDV0~)`G^8!^m_zKbe&fp8n`1sl#OHI1WApvke"
    "Dr(ST!_KBlJvbHa9+lnUZG>^Of0vZ|G&lS1A#!K(<RKF#01R0t!PsRJWjhhBEJ(F>uA4d6=fvQS6^SHFHI485RT*<r`{8fo-faJNxj1nW"
    "T~=2+kjUH02XPRc=bP<3dNPDI*~y45q58HAW0tnnS+1CR<PzI18EZK=2ohC53@!&@9zd$i1r2k`m!hiiZKqeIc~z8gGshR-dM>-70!t`k"
    "yvT$WD&C|1a#@%p6L?M)Op<hNcoe%5tKU2k@vA)-p+)PPODcfyyG~CNDpE7t3PcMwXF<l(&`k@zcCdylm?B|;^|aHYKP6J#?<SYejNZvD"
    "&&|TdkB<1b-d-!)sTveq0cRS5Mhx!fnjF#3A=1EhJ3Sd#>^_voRP2X&Qhge%H6*JH{~5gZi7tHh#Xw{*G+MJq_4F%EnNhebf7LCA3HA6j"
    "Nf1Xzov`IGt5BEoMLYMW@(x@D?qI_Xapie|>Y~$Yfn0&3LIK$@nw8yu)-Y`(jf5gH4wqJB5WTdo^zyvdL?uLL${W)~SbIzm=q%-oay5uP"
    "<OU4g5A(yfdZPZ%B+aMyimJM)@`1-k@C`zx;bVJU#hj>kbMYM~N2>YuCR0oeL49aUE-Lwu6Vo2MG|7DlSdseVg#Z5EqaWUWc>mq?yR$#@"
    "Xv7n{xmIj%=qddRIx*;UPzYr}#H{L}mv^yQRI}mll;S~Blh8d?tLrN7lRTSFp+#2LnK04Fj+EU21?cp2XD0v{)$bJb00?WrS5jrk4yHQ;"
    ">5C=GS=NP_)f6ejav<cKj7E?Zg-BTQp{ZZP?wf6JfmfEWz+B(cM9?@Y%Rc}oD@XneF^J>Vg9yqF$gUzJ8OX-_wWLT3&S0e2Y#a{3SS1a5"
    "F2=Z{6J$I_JVWY0F*`le9U1T&D@l-9&JGz{Nz$asW=PGks2Su`LS7}q_DurK7`?^9%op%12T+vk;|<xNOh{w4hv~hz``>^{D-`4snPM(9"
    "?GQ(##xd?^y7Y3vPYbfZI{ad)(!Fn|4@t%(yF-bGJ0PuZ3z{Okv?ON}oA3>%*`dz#T<IO`N@5*$6eJCs1P8EM3lthKcji}ax?rN&a6$M4"
    "<ZT49;L;CM7?zD)!LNxXFbp+UWqXUsu;nl`u-sCCRPdH@4TbM`EzwgRsnt+&JYe`~{5+!LGfOpPBCX|Ok&t-tgzp2-HwG2y!B?L}s;9M$"
    "l6}RM;DvjAb)g{E37C=Kf2f$H1x!rkHYo>N`B`HSA87|uArlw7Ng8sCSd)wJ^f(<`ux|#TXX@eU;YoCVo6%e4jK(vJj96r<%YDwEH?)^n"
    "m6f9o1On*JP9}c^2U7d&x+(+l!K`Y&!g$9@ZY+TR{F@J06P@`Ust+>K(UhC3n`Spq=V|INvkZCm;J6{hv*#<(QfeqO#F27Zj*plTZLH~8"
    "j#vsNkC5+Y{4pXMOi^oR5@|O81iB_pbQqAYE*bnxd^IGR*`g7ZOAuNhZZjrZO5BCqLM~YhpAez0tife(E%Cz&UNy3FgKX>PY(rqJRU=E^"
    "ddeD=pc|M{$ZptkuZ6WXWw0d0>?~>4W1US#Wj2AvAbfnf+%fHmVm?r$^bRx`kT^W&jG52bL_L__jQRGP1Q=<W^o@bidn~OO0}F|yx<xV;"
    "JlN-V%_3;-yR>+7al~>sLY%bWOGR;om8qfCz(`x4bb6AFk^#<D_5cjfO<H7&t|*Vp+qcILWBXKl$*Fs_uT=S4;vbIOAMr~V(#zFgKA(&_"
    "of+LaV-{+$wIuw+kl!aJXTNgxo-k=|M-@3hb15gP?-Q&`hf->hZmsO-TwD{&^%;_~uh({8s?g1akQS6>;haby%Ilw;4^94*FZG9f-f{V&"
    "*L9K(Kv+8)o?ksuiu>-8wDvX=F%ocuNN`QiVS-Yi@pA|5a{&~X3<u8lDY0D0qx3ep%Zk#e)LM{0S<3J}Z$iJwy2*|>sGk9QdUJkJ3s+8H"
    "ROQ6+I^@3c_R1r;JQ}Q<^>{!7K<0+|H40|;wXeH|OvKc^n9Av$vw4>UB+fv{xwjekhOf2RY_Hz{a1=}&CWh3yA(uHvXudnvrXnP=eM9&u"
    "RR-o^Awo?LhXT&Vdd<w!Bo8JF-3taB?UD=+oo~VlPxjH->-3rqsT_CB{cbR)!CEVFQvk#kHUd;7*8#uZEnQRqz@$H<oHn_u0?yu`<7UP|"
    "3>jDZ<|6u-8Vn@yPVVm*7xN9Pe2ktoG$<Kyzl(ieXiz`Y{wfUW5j**Yj~lJAgDnm%4yQdGfbT>vf4mikz#u!k%wHVK#*7oX8dp`ONnFC+"
    "$_l2&#)}xApD0wR`o_MRzDWc@>zswhF(d9`l*>@jsw$O1klkRwZvO7egt5!AT$QYes$KHNIh+-&xu9AkRkd<Yu4kOim!}eOkyNtVm%;1M"
    "q%kN51s+MMtpJyC>yqw5x<rjbB~aYw`bfpp*5oM`l|!>?)xv>}Nd-oy1~VdabeEQb7d$YfeH<1tTi0jm<*CNkPV=t@BgK?cfG#$)t06;T"
    "3SWLa2l4V)v~&p}#6_gy0Q~7#KzxH|v8!7le%o5<D@|l~6#^+BsdX+fy6Dwq^M3mt$*i6J*wG=jBDIn%b9RT97iuVm0ObwSyrCe3MjtL|"
    "uN0q<FOH}YG*<=&S|$@>E$L&TG+=By(CvRpRk~*eU+@G9#gh$tmf}XYU>lWpi^|AD$03r3dsc~+ga@$6L;oB`KOLw;*8x1aMip^dKj~jF"
    "U68l6{-$ez=00CO=<o1vysL^CF?y9gY5uxhEFTUJ!XJnFBP%njWS)!*`{0hKN1}ggPmeww^8>kAX*nE!GVE-_*b}2&9FpoLY~B|`;x*(L"
    "kBz6P=Q=(-@c2m0guP}j0*E*Un{JxpG}Ks;7yyYF!l&CNOeZSH0rs&_#k(3+Z#I5wUsldtWLH%htZ}nu_ZYZNggZO^ji|<+s@JtM5|7Wj"
    ")19S=A2^T0o=Bp^!_9vgda2aadVJs?KGE&)aB%2e91ZY)@^@EW9AY`;`BB$7DY|~ll6+G?PEObR5em_3-gX<`9d3O294`llC-RP7vUKma"
    "Z?73yEl@ge+?-f&=&tM`$xk3_PkT`In71f8S19Nbw4mi65LZ~vw-XABCbg-;y(wUeO{XWyEC<(Z-rC%afgU}#m)R$xL^8>BJvQq$Olnpu"
    "%F2erebZZBdM9`LC~(<vG8=GNab%dOtSys8gM+}R0yUraOjPv|_zjV~M=7qmPOqVi;!(A}XsQiaJxKp+SeodrbV-#pxAV%DhN?&Y@I(@^"
    "=?P}oA>ZpfO<9M4-VoQ68lviWmL{cXeq0lRJ)yF0^PvlaKwqJ-G*BaTm{@n2a~YoU^xo4K#6qyKXTsV`?U(js?zuYOydJ5F@k3Y4Q>j~p"
    "@Hl$|uin<qv_1DiCQz~FWj455tbWyI-PX`X+1Ld@=pwE19WYC|x((jDTKdkA<JA$q`_TJq0(RGaaznC$G|Fcoxw&EI@w?PFY=cUC<4}F}"
    "McEV91`@3J7PvW~29@b%_5i#95&~)dG`Q4<2Tf;e{CS7mE&jOdeJkRQ`rkh3^8BY<n;i@-yfuNNtk>oj+?xK%I#l<%^+U)v4Lj21bO3R~"
    "9tJ^V5PNldMOvc6?x5q<c=l*%D`JXMj<aIdLRnMxr{s7!J}(eGXX)Y=Zjt=G04c3_`cnzwV)RWtG6FR%5(bt_>sq9mrsgi0g{drE=E@!_"
    "i48_fF~WJhX(-<*V-k7v<--uoS=Whme~vYe=+xIfKMoqMpg1TyX0cJh4vM9+m{k^X4r2GGw`cE(;#bZC8bjYzUt(e;_EhuE`5)dh$k|N8"
    "wp9Z>a&nwlQ2@LHRp{=hEIy?<Dqu@ir6L7G1mj9!{israL_NN0$(G`%2y4F4M^J<0hU7K5KU5q?5gox!a|qVw&K<KAk{_7n$j`j<H2B;U"
    "L8UrL@18tM+ueu+oybj_!(PoGL_6Crt8m2`xRtWdQVXaE<znC@1%cQZJKEjH$9!ori@Os%;}CtHYQ`kaTovSnbA|14H0^U5+AkPyoE^&&"
    "VjXJVO|=&4H3&8)XT+>Nbd<Pd_zqKyY9@U?Hjl2p?ivTv!Z=T+oavjbC)F(^tpd!0Ix{OPV)u4%n@vgFtGwe@7!DQOSX7ha#Zo^8B-kF!"
    "vI?fv-DSmkH_(oIWE00-W9c#ZezIh8y+$j0?a>C6cJ0u+;NDJv?%rZj8uO1~`Q4gndwhGPvt&`Fc3;zyYA=n+Fl#JSnX|$fw!8=XAnLL&"
    "y6YZxf{Q-pHrlHqy{N>8J(w$`)TIefOmwOdM_o3WKaQ+ShrvS&*;Z9-!^&+yoApV-$wGL4p+Y?Y>T=@-$XN<TxXbxMm%fU6RJza)W{{IG"
    "AbAKprW8WGL@qMKUph8LO~6TQ*1WOgAK_yn4q{1N;~pAk<#;()$5Y(V^W>A`BxOMz+CKLHn{HXLzDQi0vZ|Fe&rCX4TC?{chi&#io623i"
    "T}cLnEHo8yo3o^JX-b&F;}T`|gPpM4sW<M4GZh;WejNbM6X(v_65AVniGiOi6y!Y{!*_&v3rp8jap;@UM{yma4X8Xp6rL_TJJ4+NsNF!9"
    "Y)g13az9Y6>ahK^QR(_e&FcMg-_R*uIj?qZ<k^P)K5O;&*%Lc_`s@08_?ZqnuldhT@NYh)t)5^X{FmrT$Hk_YzlMtbdI?(Sj$R=R@K>){"
    "^roEPJQ|IVPeo(VMEz}o+I&eUU*|D&9I0%haM2JgqRr~B0Fz*Y=&?alCpj&i(4{A(z<6>!Ueehl*94|Hd&V_yNMOV2G?${%C2eh__2T#q"
    "zQ!j{=%AVJkf44&k&j>Bq<YF|B>@M^s&;EJd+f53X%kEHk0qw+3H6R#G8pe?VuygY>^_nCh@<odPpHo22(p{nGA~XXyDGcp33d5TjXP;&"
    "Ui1DVnqBP)l_K+&))FY!guhT7m;fAyC7)6+0{ItkX}1hhu)9N9mnB^9PAlcn&QmH~i0Lr$B6O@N4K&J33m$#4R0m!Mwj+*nMzhpyh(U5E"
    "N{uuOw24r`e3L|hxRO?Tw8+MvNQP_Hvw?K{Pf9nEYL$;;utk|qTiu#E4a?=CHv6`zxDta#BK~tj_w<VZiHSerQR-QDq$)s32|o}gj`bv@"
    "Mk<(Yl<5uUzvCQoXp)@>_~gs#0<dzG$DARZuh14i0&&4pj_|3Y%fGzminwg}H4wtBg40L7-amW!hgJ;+oW6OMz7_a$M+rd|x5S_Z%F8dJ"
    "VAHIG-GmkLMTiHYZYfWp+M*RgSEcD$HiC;KbG^i$%omm4L{LkmNiE#8d(ZI<qKlOTXL^zpu3xzSC-g*IF8KDZX0RH<DV;@8h|;Vo-5i=B"
    "b{RjZW^^$o=IHcUi;H;@3)4`3KB51QaxjnaF#m5+q7ACo&sF;+lqiY}n(80pA%C+Kc=Xe$hgD#^$Ec!%uRy5L0jy^Un=HD{#lE{|X$ZCc"
    "x-h7e+hzVq70k5x4m?N{kmx=AjJTj^7i$1yRrQljtRfN741InUpHSgrTK=_3B=MPHPyeSLqzB9jM~N$q&T8^$Bc>Xc6kFwEXlkGD=|2du"
    "_Jq0pM{(CSPm%)^6Htv!bGQ{)tx@C&Luk#v^?p|&*4F#APxAHN*BeggQyQbS+*QD~FR0n&6jYbc&ox8R$apzZ?`>!c*H7A0w$B<`+{RuT"
    "OkB?`=6#!Ib2aXKOzw9=OboLZ6h5ipQ+funAc<rRxIV<r;|->}@(Gox_kkNgm9lqA><xJ)e1uLcT54<bj;oF(pqTM^>C$$bAiGYBapLb1"
    ")cu5YWwj_kj;(nfev-k#)UlWoant`iT_j?7&pO+52YIGv==MsjysTqRo<d&*S4XhTJdVnf$x~o7f-mXZkXAYRu_YIL=HgX|W$JpsA}idE"
    "-*eZx6xVLX7~}ePU(f;r*@>&7t+HTP+=#IHqQ#D`IfB!wnPEsj3dC1Q)P%l0p-W+|=@*)ax}_h#Pr?Y&1LcmXm>`>WI;O6R)>CwCHGDs&"
    "R1&}luy;swi!_snC!@mbzuA_^8_(7oG68Z6MQMWj{z^#Skl|;n73fV}N-gVBQH<7RpW_Fl)jk&>>W=$gV9r0jei=PG_~y7D9S;uo`q53Y"
    "&^oE8`i@%d996JE)(8PV)@SE2&RCW~N0w@dEN53@^%Z@T*X%sXq;($UZaOWr(AK?fukVAxo5^mFvHVdQ>U?G;aSxwM|J$8hRr<l?ZaQt}"
    "H3+(0-4-(j$AT|3$7ONWWV|0X-8~f9t?BKt?s6%v@fV1~3wrj0_T^y&|KlAA)7$YDI~0<KEP=M0?X9)j+tje8i}LP}9YMj-T)|g}HZf!z"
    "4vOK_^q?egOBkgA7!}YzKu-h@0%E#3EfFgz=$@KxJqL!R)C~I?{{<fq`KtvBp$HRljg&&g;HAv>kMvIxpr6QlXUcRA^6d4Fm=BMq;=S^W"
    "?M(93PT!B$7*=qo&}ClJOkPJnyt*(I%Rn>P07WVK*Q@i7=dV6oUwrs@bqSr-if-J8VYKtp@#zVBgC3v!yaVd8b9{PyEPtWJfk5#5>CbT1"
    "2xd79q!gU#6KPyV7=-w<&x_!f(l$DKf9Ahs=lhfAFTM#bP;~q5L47|q&9aS%yR>0IFHW8x^|@9Z5dO4rAOXN#`p+52vx66ht%2NdbDtZ@"
    "cjxcV|8%}#D5$ZqHh5q|S-+5NRIK|~oFUx}_JyGLF}RS_@;M(G4e;@S2QwPbEOe*gYC@NqFL$WnDgvh(YgKgD?3l33^K`~JGS$HWN4W}p"
    "LR|h^_UMU#i_X>o#ePLjVYYEITP0xwIp?jXTPp)XkhI2u8#daQN2~YgHlG|0leqAXuIQ|z%VjamM33C-xG+9DyK1%>EwkCg$NUR$4r>U)"
    "<il6a&I6Z?nYuT!HaPI~kp@%4c-JtzIeX@c8=koxga3nMk;2Bq*{AQ56??Ly^EX8?X?pKkHcD&3a{I1|B|L0`I8}xXh`Oq6o2Qd(Imch{"
    "j~88;gqe1k62e~zU&=G}rce+77R@>4&yhsu%B7V^in*$5u}A~HnZ!c{RSVe0g0Zb4>B~Mkvd?aPxW~HH&22Pa%wv|q9-s;I`jA_Axr*Bm"
    "U$z!KP4i#lqewsE<EEakZq;-p2NAWwaADn`=HQSylx3|<>oPBmR(-ssxl*8QgjFWtFkB=N!m8YN_zdi3mkx4Wg~mgo9_GqUN3kxm(b52P"
    "Y>ZTs3r$72Fu*#f=_ZkMiuzPzpET3UdXLN_$H-6!%I*)MIaixcojefFelEn})3cd6;;PqETdE#&$f1OKrX_^V$mheoQOvePll<H>>H<{n"
    "G%`u2png6;l|uqp_LurhYu+_GDQ}i6?*^*7Dmv(E9HzKZT0ECdo|}PzMgAq8HE1M>UkhzL22Ul#X2?ulA)$+M2q6B12WZ&jlx61{V7Ozi"
    "?eP&@UFh7z!G`nk<k3qQZ=!b>@BHyFgf(dI8c==Apk=D)QLi|4`5Oe4aZIG3*NXGJ7uAW-CMD37MkOHX8~AOmkAehZta|IQ#bp9ziK_9j"
    "nRuV>SDbp)gF{-p##kWSF;0si53i(^Mn5hU|Im_bR}#T&JIy)X!5z4YcB}rpf7_q*@B6Dg`Rv1790QHOy1*9B<)Ig+6m1U-cYXqS<+(UM"
    "Z$Df^*)W?~3*nBFsD4nupOm9EZ#2@|2in8v?@)prhD^uXN#pu~qc{y)THU+ZE$wCr2spY)d<`M){8L)$%Y?mu`<Lj=YaiguSQqdxZ{y6n"
    "Ky|~=SC&XGSi>>%4Uwdfu(v7hPsFVwSM_bPPR64tgy|ZkdX9;efQvf2xoeyJy)?>0k6|NZcxB*{=5m%iR1j@lIpm;M>hRz>1P_!$43Be&"
    "beIwy)&20%lC(CNe&b2$ghVH!X{LAJ{!LQ!YZ5CtF}PUvP@L74$<zDuyBCUwR5L%=rJdOoK3WcOg|o8{x5#U~B|4!xlP)>EtP&(VXMD)z"
    "!dGs^ctY7@G(au#8DA8#$6o!rM(jhmAyE|e#$59o-5+#<3|>Rru);ZGzL*?hh!(TX*(uC9<<{W1m7xoX*FwS}lvuH2?uE3R6%0&hC;>FI"
    "v7v5q-wfPDLzua4*+YLqWRyZ9h;XS}BB#*+8Uk*%^dPC+YlPpRhv~yY@+AvUD&zijA~!x=-g>-<t%His8=W5aqZf3CX%^69P6bLoPmZB6"
    "IzD)Ye}UTjjQ+>}KF0?yRDH6XY_9U~m?}9vki3sLlYv@;gWfcp*WCUfoLd>a%L0Xi2Yz;8F@avng)KYqSJ8g^8imr!P8f#?9vD{&;lr6j"
    "-i<udZ>Pdi0|x-Ad`RikEjTdAoPBvygVh8yCPWew-omp5fo(b!fx!3B_DkSu@Ae<JtF<uhAbU?Yx<Jjx+P<mH<#y(H00GLeBqTi}i+ac`"
    "RhmAHU8fkFo69seQp9j>ab3h<2b%e8vV1&SPEtda3><cP5r_WKKcix;IPN^CLp{1ImUYHxK#1`|jD~TdL`?wGP~Xl)LQp_;Kq_GD70ELD"
    "RhpFSK9YKVGPJQ^@_itWtI%Mth;EI$7Oi@ATf{GmGO0+w?E7VGVAIPd@u#Z0;gjwki0`|s(-aZ}dy3~UYIJWa*T(lN<ei|N_X8Xd7Ih(A"
    ")^gNcAqQaIYeCCk8Znq4q(KO<(@t}vB%=Ge*h1+V?aR=a8sBGCFkO(AI5_3D02n@#bP+nLjZ()3>8dSR^#fK~wW2T^(0p{|rW&+()b7CT"
    "3-(?>SJi_a&55vxlm$eVx7Ohx2=!hz;jZrz$U~+Z?^GsgYlUoT>jRV!Y>sR#-sY*;m*)&&lNU>pM-c{+aZHxf0hv^9D+b*zBpz3z1ym9g"
    "q$3)W1L3eFK|DN%0E3-Q)#+Dq$#-n&Jse7Set?Z2STviCj;R_H6x+_393u83XrRP3k4w}Y5m&JLZ2`vTT|vzA9_vncr|kwCo6~a#TMgUL"
    "p*ce5!|@=G?f1RG+Kzu@iwAq!ZD;N*%uVaFWj#UW5|Eo%ZV~WW&L>?SVIp-YNQ9<?27rx0$GrrVq)icz7t0tfxH;#NVSW&;5g~Ql;T2+d"
    "sa#~`WW7sK5uC#XZko)qS@_)A9>Fc6qb?8*4CCd+4}6{W^x{Q~&XErt5x#Zi01k&LF+jD%rVn&lcQniDE^OXngUq$EFOiq<%VY3(Mm5~{"
    "xgs9!*Z^Gb&L$H!+X`k9D?A08P(q8i(?i96XD{%L)w}RKUpsCYWIfwh9-OhhZ}q6LV8U;#O^jWE^m7>fL?YbJBA4+!=9J9Tdn^P?8Md;G"
    "Y}%~>{YJIQN9qq9+n#7QB2Zzj+%W2<`QoHHm>zT+S%9@OhyCOJY5#fuo9O4pYXPS0rVrFf@Se?&!4(c$Nrj=fLyg@8gzM+lTgRiD&XM0Y"
    "_f>12niXyD5X6Wesll;3O04&0FJh=MfWNOo^Jt~P=ibPT%S4Gn%w}yD_2tK@_4-V0;WR|>gVN=7k7TSon8Wy}8@#dEIu4#~o}=gqi@tTq"
    "sn>`RA0Cf}2L}VVJLM_TfHT<Y0Sj~0;WW&FwRK-Swg~H!v3*B8Hr8J2Xd9Cr936Y&o9i{}V@<ZBLV=CQ15&Gei+fu6h^~nh;OzY+Mh9{q"
    "IJaX)baM&_<L6Zop)%!6!VHmnTkzzTCBSrLH`ymd>5up}<JuHh{K#yZwsRfORHFmYWub<niG!KOOSCCuT42N~W?}Q_q*X1e^i>)b{H;S5"
    "3f+&C@$qCf5Q({I4$5e@oP^^#7@TV3OvDbg^^QL})GA-ER_RCfn&*ZM7Sm=H4v?H<Y&qXp6Av|+-6yLm0PV25al?5gv2t**VO#VKtVByg"
    "#2c$~B%B-5DRWWTda@SAnKo^M2W{C<33SrTLH0dfXkqvx4PP3|pipc6tS~s5Jxr05O(Z}tLHSA>+^NDQC8?$v@01hvU^jsHp3*@ehPEuB"
    "ond>O=PSN5=;F<DBOZflY>|vI4Ce6S-M3taF9b&=brrZUxjTpk<Xmv+bec*S?`Jqhhukj~%h*ZsK01(inS^~C8dAQb&hW)O7~G#}TrRMz"
    "jfLHBz$@O%T$+JRz7Jy3bdrHu-Dkq0W>Nvy$2Sw-Fjs}5E&xuNuM)_ef{0-`2$E<4|5_#-GQC^~n>zKWj6_%oOqwn&jgm+||H@!GlP=V-"
    "3Nm3X7qw(Kh0mTjPXs1Z#qZ9hY8_y8|DdxmZInl^MR%@I&0to@#mgB~gR+9TsxjT7QVkOGiGIefVxl-m9p@CUOOO{X3DaIbQ0@3n@7?fJ"
    "R1~$V)`So<pz<09vOyhNUJdTw(5FefgyK)kW5~3Tje$y^+}-G3;>XrE1Uvlkz^^(kr=MiEgYd<AbF(Z4^*a5rPb|{I`=M*ddh^!livv&6"
    "Os^E#(5#AK>P~0)p6xmShm3aFLr^3!=4UL$s@1I-&1us9T4{DI{NXgtyiJ_#Ioyk;#2tQamuSK58)aRw{YY)D<fHZVT;?h<e6|mf+SQ)4"
    "!MW_`T2lv#pczBG|1Wb|r9;=eRkn@9W=_X5uI_Y)h$^<a8~S90A7tzNiqU+*csAwu+cG5TT_+&u%E2J75MS(kGqrSeK9dUWCVwrVmi0?1"
    "MqQH341a9SR^&T}LXXcj0OO&>{aj5bN5vkiOuS;=r?o1TAvxSA{~@k024iapbl$)IV>2XD)5aLww5pllD=|l00LK}rqaJZ_#A#3sKb-$?"
    "ZnC+{d%*#7HCSpENtpTp70$U6g$VN+{)-UAC3`xWG?6W8fozT6M6W-5{PFDLt0<lmsVzT6|3a(7fBfsavyXq+r++X15XFDB9x-VB#Nc%e"
    "pocf0fajYD+uO`kFUU~R20GW#I3V=~rfTw3oFQ;634951gro~%RCmPhz-j4{V63dV6wRF?`A8V2LB8bC*~^#b7gwyFtwcL*=|+7sNJX+E"
    "j$HIEPakTD9QC0+A94+W{QbYfdDssfAB=EWDUMg+yc&K_oH$tFIh?)I@KkmfwM#?ag~_`E3+Y_K)bQ?B+39F@MFn6gE7peWt@rO)vwzG%"
    ")9H*kiL3gic$Pu#cJFuA<J@u!HRdQ|Hf?AH!N(eGKO=@xF`g$0NR+K4z`oU|c1i?iF5rWrA*xv6@MBiRYv;vg;R`q53kR*FO*Y`5vVHWT"
    "!*TLD9FO`XS-f=fjZz2pAuOgp^`_khtIY_EV(t`ITuc^@qI2nU)fXVbZo@i09lZi;l28A}=TZ}!a839v8=ns%u@sFbl|7N3hGpCnSB7`C"
    "?B!u}#AV!Gg-Huf+|Dq1mrsFWZFUv@WvYWbt%<CC60PtU);7Mv_3f?$0#ieTCp0lv6D!LAG;GUG{T)9#XuE{VUgVS|x|Mfoi7CK^8Cy!e"
    "qgKZxP(#uyF?I|8HrwfolVke;_v@q)P=(tytlBcSX=pqM!&<5!iyAldROh)FMSlxyhlfEWBL2=e%N3vU>1@ePrtYZa!32<`Dq-nTr2*0!"
    "rcAIR$-~;<IS^hmkREKn!G5XQ;%4SVm1lkK#zbUJ-$V1m(EkoYr`PEHo0kTOAyPlWFk!wyTB{as07hCQ=`ET0dRlAjYYf6v8tpoK4j%zS"
    "q(L{M=?He>Pq=7_*o#w|sFg%y0f4ortu_YJ;4{t_C7!mS*-;<S87f&*#ugjQgQF41s>iOmZbLK4d0nRIx0kP?!^3}5Y2%gwS(smn!AUe4"
    "V=Odb;{=5i8Dmxc(UO`35^p&P+@j3ny5;VOcQ9ldzO3cOaQSX<K?~G?c}>w4h6#_)icT{dOjKdtx3D+C`tNsoJ`O3^11_@;`mihh%4vPe"
    "32)fa#_(T!jlJSlP~hs%A@q%_im1fbYJ;47Z2^b5ZqE;w@NVQ3*#-lPChZv-Fw_->ew|AO2k-ewSHW#vlk~E`e?wm{M+2Jf{n;|R$;#}P"
    "Uy6Nkv!+FtKbS1?yqV*2&;=kxM+-XKZ0n62O5P;eO$TrxqB%JDw=U7ahBlg>9!a%6Gg-^5<9vyh@Y3^C>Eq?4Pz(0Cbaf6oO>hZswdF6="
    "$DQrAD-x}19L`x^7&P&!Vh@r+s*%W(F@TG!rDn+OIbFZ{O-8--ls`^|=K$gwiHFpKy~aT*8!lTW_AgekM3T8kl5D|YWb{qnJl6!~r<kio"
    "Fu;85G)+QINkA26KJ5=TlW_q*foOk+TG`RI`{qE><MM*JC9yeDmO9obYn0O)pQ9Z_nC(P9_jb=gC;46t);1U_qfMq4Y|z_X%?Cg)G3|Ww"
    "+daieSZJHy6KCGBNO5SROCWqY(M26~`39e}*Cp)N6JR87+Q(9pZf4&T-on_}gXk5Tlc?bvSuZRbUG_=1(WG<~|DOMlI@vukr7iF9rUudX"
    "hPPy7ftT3yeqR%f_}V*j+Ztz6sZet(<c;$wJ>SWuq7mixqquxvG^@DQ|H|)Y_Tbr$q*D{hEw#h0YXmL+gVa+$fNVu2|3|)Iax2=Rp4-hs"
    ">|X!K&){(<%#f|Dx=~@G?DMP|FN>wfP*T<|OMPqNZZCQ%ek%ToB+1NDgozkrew@LcKQk$5?hcQo92IiZ7vKWph2SbGnuy#3gEc|3IxZ&6"
    "y%1YtqFGKvv%u8eA4x@(jR1S82jap+=^(>S$MO}g;BB>m9ncW<aXN8D^I~gB)4I5_AZ<g>yD;rdByhFj*j2f48LG#^+L+(b8p7)=4(>Cj"
    "qzp*(&IT4_$8Gkiu_tuSS3&<fQOL!}A0ci2_Tse)=u8N_Lxkn)lpVnNg#jpT?tC21rR60v8mb#Drs{Av6u-_F2a#ZIcA{SUZady`Uwr;R"
    "=&g9sX51^~+#4+!^A20e>+6qi-hbD$91R5)v`U3d$T{JrE9#g#F6Gz+_Ok_pK>We|{rw=Xi^YJ5+deJ(WI3*@{l)YeI*<L%Vp^&_r9A=0"
    "xcl4P(0N0<qYIU!`PpenxB?DUmo8_$sFPq}+#R#ek?1181bS~D#~jF8(E&Esq0_{ffYlm097NjK%m_aa<ks{$3k#<)_j66aZEfru)L#`K"
    "(~=}eM<-hd10YA<sUsL&Ly;C-R}{^Ze<Evp^vyTze!B&iQc=BHAoZy|CGyl9Kw38Xyp6U%acOm4Gd6uIy!%<q**=HSf2+zd@g_tc%kecf"
    "Qa_r|is1?VD^D1(wjTi-{P%0sBRgrkk&V?y|6ujkN7q{G(OUI^`vF(K1@z$2>QAitlP~D~)2lzV>QBFXa<)~^5I^+qh~%%`_aCmJkLNEx"
    "ynA>4{?+-by~g&##u_%Zgl$D4iBZD`IV7x7CZwA6c+v3&F0bTj=)Y_O-`;OhgY^|;!zIhoj;tD2Xh7VXG$qs2S1tYtIx%ibtAq46U9v1<"
    "=U!Ya9@nMmh!s^YFo^s%jLC1rnfw;4$>a0`7)B4!*$y>yL>;YMlkByxy*6Vv)^JlhPv&&Kh}HQGc%9EOJKo~liGFjwXFKBqW*V6Fjgz>>"
    "pd3o}i-z}FuXW|Lo^7B5k8&!TS(T{47#(pcC@*Oc1)JXQzSyJ1qC-;ep6uCKhgw7Pdi!u=sF-+y@YyvM;NQD{IlmOt^=u)P1kWWjfU`OB"
    "4lf7neNOFvnoaOz$57z|wUX*6Rq4bSYfU%S(6HkUAazLGFYIW0oO$A}Tq;MUE(o;6CmQN{{=ohmmO6|pgM@l`aG*0o+$a4_w-tZNK0l1Z"
    "FPgf6WyDIQBH7wqeAA8MSSYn>RCwFX1$xs?Gu44XX$FA8;$<Zbw7||}gLKf3;t6+zT16j+Vm|#yRD^MOY<LzV>Z54g>_{ir{oO%&cRVn!"
    "rDSM-5S?8`KYst_<@e6T#f(hwyCVryvo@-hnLiILQLGFMV(xTtV7Y*oEg;Ps(U-a_RKLNO0b4O7(q8dF!v2Nu(-Pt+9|VX9kn&5ND)`u|"
    "(p;98>k?(D<i^Pv%A{j>Zf`DL|G0hZ)TQ^9&%hEd(*EFkXVr1|gyI^AN^qpu-db_S#WDJ3^r)tHxeo!J6~#hwa$>)lf?9m^z4psCUY*Wn"
    "Rcrs3t^FZkmvB^LoFKPgBmt!NxQl7A!?`^@JvbOT%{Yq2RwakYQqfq74!LZn)5#Ms-{V`mqJ9)iiIhQDB+j)8G;Rz9t`{;LbfUb!BrZT)"
    "rj3LQFPcCztt~iplchKgQWIH2a*AjR=IlR-9OHbk&j(@mtS@=d4Is|!kkIxilhr04piY2url%-Rd5hGnw>Ldlo6Nnxx_H~j;V%A@!5AlL"
    "m4)NrI6#fW;wpXCcZn6O(wIgUYkAhxbUb3LRm0!_HXF>};VRSgiQ&!dK-L7AP=hZ_cnVzk!;c(o5%X-CL00rm!ptmLB4<PW6rGvt_D=^t"
    "+a2y8e<HzfltgwmlJ<AqgZQ{>-}1lhcg|tVrOv5+SA7P1MN*3xTH~e^7zCz8k{{5rVo7X<DHjz`8S}L7K+2Q4ojk$!P90V>@LR+4{G$E1"
    "VQpL|g9UXuXN{d@JB>o`bUcEZN8Qs?|Ne(}XVlyz)dW^P00*Wu#GMJP4VSv(K=Q07O7nf>jscBuj8*<vPpxy~@&D7>)wH$^1krnbg>f%2"
    "NRE@#3FKB<3W3rVLQf?GB~pxFZ5c}@&A;!?yqVb#%SjKtCGvjn?C$LBn>XFAj%@4U@j;LYipfqmU4=>|a$eB&{6p;%MN&JKaKw=jai>U{"
    "<7-;(S{p{i?Amp;YcZ1gjD}G6sX^$C@(dr0)-Y(tpKndK@7=3JZ|1c#nP%&HYHMRM)p!9C{bL%}7fDWXJ(75;7HR;DMSRy%X75l)R>4?7"
    "0!qR|B_^IF*F;s`PyFyB5EFyg5y_fIuI)#qRGt<Dl1TuiZ9`Bu%A!CVgrcU)Otu%EOcGvt1NBLSYh{GNk#C1dpd7<p(}*CWMQ9I5*rj_A"
    "ld!r%ExY|<Kzd<2iy|gXI9f{`cJkmdtfPcGq4|1-Tj8jL@<3;Ely4JghN>6Q`B?RVV^n*Ta3%SSr~M4a1dY>vE87~pdR{gmd<?f84goaH"
    "HbS7die5uW6XxTQs7O><H(A8q>m|t<lu3h89&}qnThrrSN`^`LS273UlmUxqyLklPGFlyN;PK^K*?0l}N(%7en3N!{<}XTFNAfMDLduoL"
    "mFECkYw|2+b=K9E0$?5Q>)p>!-<bv=>oJohy*)d+#&~+rNTpTc3!kx(#lal|&%z*Gv;c=ebhUe|Ycgr$Q?Rv4;c`|lN~UB9-U8?nmX2Pv"
    "@!w*Wjst%*LSBYW=cfTlS>%r-bP2x~<#};YUKStAWpPzr71!nUeNr^t0cHCZK1k?2BMZxPqajjql7`T&FfktmEuB1NZjzcwts!NM(nfj_"
    "<OoA%y(oMyipxa3$@HSpY~^7VID^qsw`_zGQNy`|9Z)u`p<6W^aZZa!EActAN&qY+NEY!e@J-KO+2ClxZZqR5XFTQE^xglfT13zTw({w;"
    "NSHzM%zielQpq4h_fTv;R*@c2=0t)KsT<<R37TA@?waK&oGGm5Tbo4T&-DT_JobZ<ljNyk?gL}T1)HRc=<l9QvxSsJ-<MIEWt0Zty=d!V"
    "Lv-4RyQaw+U3X7=1LDX=s7({k&St1ur(|3$zkSXBw;X7dHwXPu?Ad4APRzK-9HU;5)eq&bEl0nCzj3V;E(A^!QyDI@$B3>#5pu$5m}(2J"
    "aQgdPDMU(`yV87T96RcrH1q`c;Ht-mcH2u*LDud6w63jonQjTjFLdF_k-o1s?h-s^X(efrxtM-zzm_=|&1#7>mw^yRliRPFT>4>i!+OV8"
    "wKk}G%_(v0c*U9o&dn%~8YFJS2Y<B!Hdwro%w8c_g%2?xpR-sUunaQ7ZKs5EURufXh9(?0CW+K55~5*{GXX-R<497Hu4|LdQ2#gC*}=`m"
    "I{kCpB=W!85hLlE2_gC-VsXQhfLhf$PR7f3uPG2PM-IPgkTmchBGUutsr@4EXVz#FT{g&TV?^9!o^I7Co)<jkP+^?%o8OlG;5sIo<PUHo"
    "F*TPd44`3ZwCNXS8rv`)vR2NRgD{`ezPS`FL7g04(P_BJyTUG!jO1qij9Owu2c5$x?f_{zQVoI0*43+UgjA1x=Kycgnuf0P>r1-Gkm^!9"
    "d_I4z)-L&Uflq${B6R$H"
)


def _kompletni_suricata_yaml() -> str:
    """Vrátí původní, neupravený konfigurační soubor v textové podobě."""
    return zlib.decompress(base64.b85decode(_SURICATA_YAML_B85)).decode("utf-8")


ROOT = Path(__file__).resolve().parent
D = ROOT / "data"
st.set_page_config(page_title="Suricata IPS – reálná laboratoř", page_icon="🛡️", layout="wide")
st.title("Pokročilá konfigurace Suricata IPS")
st.caption("Praktická realizace transparentního inline IPS, testování útoků a analýza výsledků")
st.markdown("**Autoři:** Oryna Borovyk (bor0250), David Kunčík (kun212)")

metrics = json.loads((D / "metrics.json").read_text(encoding="utf-8"))
eve = json.loads((D / "eve_prehled.json").read_text(encoding="utf-8"))
choices = ["Přehled", "Topologie a konfigurace IPS", "Pravidla Suricaty", "Simulace útoků", "Výkon a stabilita", "Analýza EVE", "EveBox a screenshoty", "Závěr a zdroje"]
panel = st.sidebar.radio("Obsah projektu", choices)

if panel == "Přehled":
    st.header("Úvod a cíl projektu")
    st.markdown("""
    Cílem projektu bylo vytvořit a prakticky ověřit systém prevence průniků (IPS)
    s využitím nástroje Suricata. Nepracovali jsme pouze se simulací: sestavili jsme
    skutečnou laboratorní síť, vložili zařízení se Suricatou přímo do komunikační cesty,
    připravili vlastní detekční a blokovací pravidla a provedli bezpečnostní i výkonnostní testy.

    Základním rozdílem je, že IDS síťovou komunikaci vyhodnocuje a vytváří upozornění,
    zatímco inline IPS může vybraný provoz na základě pravidel také zablokovat.
    V laboratoři jsme si tento rozdíl ověřili zejména na skenování portů,
    ICMP a HTTP požadavcích připomínajících SQL injection, XSS a průchod adresářů.
    """)

    st.subheader("Co jsme chtěli ověřit")
    st.markdown("""
    - Zda Suricata dokáže transparentně předávat provoz mezi dvěma fyzickými rozhraními, aniž by na nich potřebovala IP adresu
    - Jak se liší chování detekčních (alert) a blokovacích (drop) pravidel při skutečných testech
    - Jaké události lze doložit pomocí EVE JSON a EveBoxu
    - Jak nasazení ovlivňuje TCP/UDP propustnost, latenci, spotřebu CPU a RAM a stabilitu
    """)

    st.subheader("Současný stav a použité technologie")
    st.markdown("""
    Suricata je otevřený systém pro analýzu síťového provozu, který podporuje
    IDS i IPS. V našem řešení využíváme režim AF_PACKET pro transparentní
    přenos a kontrolu paketů přímo v síťové cestě. Události Suricata zapisuje
    do EVE JSON; pro detailní procházení alertů používáme EveBox.
    """)

    st.subheader("Praktický postup projektu")
    st.markdown("""
    **1. Realizace sítě:** Cisco L3 switch, útočný Linux, cílový Windows a
    dvourozhranový Linux se Suricatou

    **2. Nasazení IPS:** konfigurace obousměrného předávání AF_PACKET, vymezení
    chráněné sítě, zapnutí logování a příprava vlastních pravidel

    **3. Bezpečnostní ověřování:** připravenými Python skripty jsme řízeně
    simulovali TCP skenování a různé HTTP požadavky. HTTP testy proběhly nejprve
    s detekční sadou IDS a následně s blokovací sadou IPS; samostatně jsme
    ověřovali také blokování ICMP

    **4. Měření a analýza:** testy iPerf2, ping, sledování CPU/RAM a kontrola
    výstupů Suricaty i EveBoxu
    """)
    st.info("**Vlastní přínos:** reálné zapojení a konfigurace IPS, vlastní laboratorní pravidla a testy, vyhodnocení naměřených dat a jejich přehledná prezentace ve Streamlitu.")

    with st.expander("Rozsah výsledků a metodická omezení"):
        st.markdown("""
        Výsledky se vztahují k této konkrétní laboratorní sestavě, nikoli ke všem
        možným konfiguracím Suricaty. Při vyšší UDP zátěži vznikaly ztráty
        v zachytávací vrstvě; u TCP se vyskytly timeouty při ukončování
        některých spojení. Přímý srovnávací experiment se stejnou sítí bez IPS
        nebyl proveden. Z těchto důvodů nevyvozujeme univerzální výkonový limit
        ani přesné zpoždění způsobené samotnou Suricatou.
        """)

elif panel == "Topologie a konfigurace IPS":
    st.header("Topologie, realizace a konfigurace IPS")
    st.markdown("""
    Laboratoř byla sestavena ze tří fyzických notebooků a
    24portového L3 switche Cisco Catalyst C3850. Switch rozdělil síť do
    dvou VLAN a zajišťoval směrování mezi nimi. Útočný počítač byl umístěn
    do simulované vnější sítě, Windows do chráněné vnitřní sítě.

    Suricata IPS ležela fyzicky mezi portem 10 switche a cílovým počítačem.
    Neprováděla směrování mezi VLAN; na svých dvou síťových rozhraních
    neměla IP adresu. Komunikaci obousměrně kontrolovala a předávala
    pomocí AF_PACKET v režimu `copy-mode: ips`.
    """)

    st.subheader("IP Adresace/VLAN")
    st.table(pd.DataFrame([
        {"VLAN": 20, "Síť": "Simulovaná vnější síť", "Subnet": "10.20.0.0/16", "Port switche": "20", "Koncové zařízení": "Linux 10.20.0.100"},
        {"VLAN": 10, "Síť": "Chráněná vnitřní síť", "Subnet": "10.10.0.0/16", "Port switche": "10", "Koncové zařízení": "Windows 10.10.0.100 přes IPS"},
    ]))

    st.subheader("Cesta testovacího provozu")
    st.code(
        "Útočný Linux 10.20.0.100 (VLAN 20)\n"
        "   ↓ port 20\n"
        "Cisco Catalyst C3850 – směrování mezi VLAN 20 a VLAN 10\n"
        "   ↓ port 10\n"
        "Suricata IPS: enx6c6e071f144e ↔ enp2s0 (bez IP adres)\n"
        "   ↓\n"
        "Cílový Windows 10.10.0.100 (VLAN 10)",
        language="text"
    )
    st.caption("Zpětná komunikace prochází stejnou cestou opačným směrem. Jde o simulaci hranice vnější/vnitřní sítě, nikoli o napojení na skutečný internet.")

    st.image(
        str(ROOT / "assets" / "schema_zapojeni_vlan10_vlan20_16.png"),
        caption="Schéma skutečné laboratorní topologie. VLAN 10 i VLAN 20 používají masku /16.",
        use_container_width=True,
    )

    st.subheader("Použitá zařízení")
    st.dataframe(pd.DataFrame([
        {"Zařízení": "Cisco Catalyst C3850", "Systém": "L3 switch", "Úloha": "VLAN 10 a 20, SVI brány a směrování"},
        {"Zařízení": "Lenovo ThinkPad L380", "Systém": "Linux Mint", "Úloha": "Útočný / testovací počítač, 10.20.0.100"},
        {"Zařízení": "Lenovo IdeaPad Gaming 3 15ACH6", "Systém": "Linux Mint + Suricata 8.0.7", "Úloha": "Transparentní inline IPS bez IP na průchozích rozhraních"},
        {"Zařízení": "Lenovo V310-15IKB", "Systém": "Windows 10", "Úloha": "Chráněný cíl, 10.10.0.100"},
    ]), hide_index=True, use_container_width=True)


    st.subheader("Hardwarové prostředky počítače se Suricatou")
    st.markdown("""
    IPS běželo na notebooku **Lenovo IdeaPad Gaming 3 15ACH6 (typ 82K2)**
    s operačním systémem **Linux Mint**. Skutečnou hardwarovou konfiguraci
    jsme ověřili příkazy `lscpu`, `free -h`, `lspci`, `lsusb` a `ethtool` přímo
    na zařízení, na kterém proběhly experimenty.
    """)
    st.dataframe(pd.DataFrame([
        {"Komponenta": "Notebook", "Zjištěné údaje": "Lenovo IdeaPad Gaming 3 15ACH6, typ 82K2"},
        {"Komponenta": "Procesor", "Zjištěné údaje": "AMD Ryzen 5 5600H, 6 fyzických jader / 12 logických procesorů"},
        {"Komponenta": "Operační paměť", "Zjištěné údaje": "5,6 GiB celkové kapacity hlášené Linuxem (free -h)"},
        {"Komponenta": "Interní síťová karta (enp2s0)", "Zjištěné údaje": "Realtek RTL8111/8168/8211/8411 – gigabitový Ethernet, ovladač r8169"},
        {"Komponenta": "USB síťová karta (enx6c6e071f144e)", "Zjištěné údaje": "Realtek RTL8153 – gigabitový Ethernet, ovladač r8152"},
        {"Komponenta": "Úložiště", "Zjištěné údaje": "NVMe SSD Samsung 980"},
        {"Komponenta": "Operační systém", "Zjištěné údaje": "Linux Mint, Suricata 8.0.7"},
    ]), hide_index=True, use_container_width=True)
    st.caption(
        "Obě síťové karty mají gigabitové označení, ale výpis po skončení experimentů "
        "neobsahuje skutečnou vyjednanou rychlost linky během měření. "
        "Uvedených 5,6 GiB je hodnota hlášená systémem, nikoli údaj o velikosti osazených modulů RAM."
    )
    st.markdown("""
    Při desetiminutovém měření stability zabírala Suricata přibližně **450 MiB
    operační paměti RSS** a její průměrné vytížení bylo zhruba **72,15 %
    jednoho logického CPU** podle `pidstat`. Tyto hodnoty popisují samotný
    proces Suricaty, nikoli využití celé kapacity notebooku.
    """)

    st.subheader("Konfigurace transparentního inline IPS")
    st.markdown("""
    Samotné směrování mezi VLAN 20 a VLAN 10 provádí Cisco Catalyst C3850.
    Po směrování do VLAN 10 prochází komunikace dvěma fyzickými rozhraními
    počítače se Suricatou. Ta provoz nesměruje ani nepřekládá adresy:
    kontroluje pakety a v režimu AF_PACKET IPS je předává na druhé rozhraní,
    pokud je aktivní pravidlo nezablokuje.

    Průchozí síťová rozhraní nemají vlastní IP adresy. Suricata tedy stojí
    přímo v cestě k chráněnému zařízení, nikoli na samostatném monitorovacím portu.
    """)
    cfg = json.loads((D / "suricata_config_summary.json").read_text(encoding="utf-8"))
    m1, m2 = st.columns(2)
    m1.metric("Verze Suricaty", cfg["generovana_verze_v_komentari"].replace("Suricata ", ""))
    m2.metric("Režim", "AF_PACKET IPS")

    st.subheader("Nastavení síťových rozhraní")
    interface_roles = {
        "enx6c6e071f144e": "Směrem ke switchi (port 10 / VLAN 10)",
        "enp2s0": "Směrem k cílovému Windows",
    }
    st.dataframe(pd.DataFrame([
        {
            "Rozhraní": item["rozhrani"],
            "Zapojení": interface_roles.get(item["rozhrani"], ""),
            "Předávání do": item["preposila_do"],
            "Režim": item["rezim"],
            "Vlákna": item["vlaken"],
            "Cluster ID": item["cluster_id"],
            "Typ clusteru": item["typ_clusteru"],
        }
        for item in cfg["af_packet_interfaces"]
    ]), hide_index=True, use_container_width=True)
    st.markdown("""
    Pro každé rozhraní je v YAML definováno `copy-mode: ips` a jako
    `copy-iface` druhá síťová karta. Příjem a předávání proto fungují
    obousměrně. Nastavení `threads: 1` určuje jedno zachytávací vlákno
    na každé straně, `cluster-type: cluster_flow` přiřazuje pakety toku
    ke stejnému zpracování.
    """)

    st.subheader("Síťové skupiny, logování a načítání pravidel")
    net_tab, log_tab, rules_tab = st.tabs(["Síťové proměnné", "Výstupní logy", "Pravidla a soubory"])
    with net_tab:
        st.code(
            'vars:\n  address-groups:\n'
            '    HOME_NET: "[10.10.0.0/16]"\n'
            '    EXTERNAL_NET: "!$HOME_NET"',
            language="yaml",
        )
        st.write("`HOME_NET` vymezuje chráněnou vnitřní síť VLAN 10. "
                 "`EXTERNAL_NET` představuje adresy mimo tuto síť, tedy také "
                 "testovací Linux ve VLAN 20. Členění do VLAN ale zajišťuje "
                 "switch, nikoli samotné proměnné v Suricatě.")
    with log_tab:
        st.dataframe(pd.DataFrame([
            {"Soubor": "eve.json", "Účel": "Strukturované bezpečnostní i provozní události pro analýzu a EveBox"},
            {"Soubor": "fast.log", "Účel": "Stručný čitelný přehled alertů"},
            {"Soubor": "stats.log", "Účel": "Statistiky zpracování paketů a čítače zachytávání"},
        ]), hide_index=True, use_container_width=True)
        st.write(f"Výstupy se ukládají do `{cfg['logovaci_slozka']}`; "
                 f"interval statistik je {cfg['statistiky_interval_s']} sekund. "
                 "Detailní laboratorní alerty zobrazujeme na stránkách "
                 "Analýza EVE a EveBox a screenshoty.")
    with rules_tab:
        st.markdown("""
        `suricata.yaml` odkazuje na standardní a vlastní soubory signatur.
        V průběhu testování jsme přepínali sady IDS/IPS i jednotlivé
        signatury; dodaný YAML je proto snímek konfigurace, nikoli
        doklad stejného aktivního stavu během všech experimentů.
        """)
        st.code("\n".join(f"- {name}" for name in cfg["pravidla_v_yaml"]), language="text")
        st.write("Soubory `classification.config` a `reference.config` poskytují "
                 "metadata pravidel; `threshold.config` slouží k případné "
                 "konfiguraci omezení četnosti upozornění. Podrobnosti "
                 "vlastních signatur uvádí stránka **Pravidla Suricaty**.")

    with st.expander("Zobrazit výňatek skutečného souboru suricata.yaml"):
        st.code((D / "suricata_config_excerpt.yaml").read_text(encoding="utf-8"), language="yaml")
        st.caption("Výňatek je převzat z dodané kopie konfigurace; aktivace "
                   "jednotlivých sad se během testů měnila.")


    st.subheader("Předzpracování provozu a HTTP inspekce")
    st.markdown("""
    Suricata nevyžaduje samostatné konfigurační *preprocesory* ve stylu
    Snortu. Místo nich obsahuje integrované mechanismy předzpracování:
    **defragmentaci IP**, **sledování síťových toků**, **rekonstrukci TCP streamů**
    a **aplikační parser HTTP (libhtp)**. V dodaném `suricata.yaml` jsou tyto
    mechanismy nakonfigurované; nejsou zde uvedené žádné samostatné externí
    HTTP preprocesory.

    Parser **libhtp** převádí HTTP komunikaci do strukturovaných polí, nad
    nimiž lze vyhodnocovat signatury. V našich vlastních pravidlech se pro
    GET používalo zejména `http.uri.raw` a pro POST `http.request_body`.
    To umožnilo testovat SQL injection, XSS a průchod adresářů v různých
    podobách vstupu. Pole `http.uri.raw` je původní reprezentace URI;
    při jejím použití se nespoléháme na normalizovanou podobu adresy.
    """)
    st.dataframe(pd.DataFrame([
        {"Mechanismus": "Defragmentace IP", "Konfigurace": "defrag.memcap: 32 MiB", "Význam": "Sestavování fragmentovaných IP paketů"},
        {"Mechanismus": "Rekonstrukce TCP", "Konfigurace": "stream.inline: yes; reassembly.depth: 1 MiB", "Význam": "Kontrola dat rekonstruovaných z TCP spojení v inline režimu"},
        {"Mechanismus": "HTTP parser libhtp", "Konfigurace": "app-layer.protocols.http.enabled: yes", "Význam": "Rozpoznání a zpracování HTTP komunikace"},
        {"Mechanismus": "Profil parseru HTTP", "Konfigurace": "libhtp.personality: IDS", "Význam": "Výchozí způsob interpretace HTTP; neznamená provoz Suricaty pouze v IDS režimu"},
        {"Mechanismus": "Těla HTTP požadavků/odpovědí", "Konfigurace": "request-body-limit: 100 KiB; response-body-limit: 100 KiB", "Význam": "Maximální rozsah těla zpracovávaného při inspekci"},
        {"Mechanismus": "Dvojité dekódování URL", "Konfigurace": "double-decode-path: no; double-decode-query: no", "Význam": "Dodatečné dvojité dekódování cesty a parametrů URL nebylo zapnuto"},
        {"Mechanismus": "Inspekce HTTP body v IPS", "Konfigurace": "http-body-inline: auto", "Význam": "Automatická volba režimu inspekce HTTP těla pro inline IPS"},
        {"Mechanismus": "Dekompresní vrstvy odpovědi", "Konfigurace": "response-body-decompress-layer-limit: 2", "Význam": "Limit počtu vrstev dekomprese HTTP odpovědi"},
    ]), hide_index=True, use_container_width=True)
    st.caption(
        "Hodnoty odpovídají předanému konfiguračnímu souboru; jeho aktivní stav "
        "se mohl mezi laboratorními testy měnit. Označení 'IDS' u libhtp je profil parseru, "
        "nikoli akce pravidel alert/drop."
    )
    st.markdown(
        "Podrobnosti: [Oficiální dokumentace Suricata 8.0.7 – HTTP parser libhtp]"
        "(https://docs.suricata.io/en/suricata-8.0.7/configuration/suricata-yaml.html#configure-http-libhtp)."
    )

    st.subheader("Úplný konfigurační soubor Suricaty")
    st.write("Vedle výňatků je k dispozici také **celá původní kopie `suricata.yaml` "
             "(2 389 řádků)**, včetně komentářů a nepoužitých sekcí. "
             "Jde o archivní snímek konfigurace, ne o záruku "
             "stejného nastavení během všech etap testování.")
    st.caption("Upozornění: zveřejnění kompletní konfigurace zpřístupňuje také "
               "laboratorní IP adresy, názvy síťových rozhraní a umístění souborů pravidel.")
    uplna_konfigurace = _kompletni_suricata_yaml()
    with st.expander("Zobrazit nebo stáhnout kompletní suricata.yaml"):
        st.download_button(
            "Stáhnout originální suricata.yaml",
            data=uplna_konfigurace,
            file_name="suricata.yaml",
            mime="application/x-yaml",
            key="kompletni_suricata_yaml",
        )
        if st.checkbox("Zobrazit všech 2 389 řádků konfigurace", value=False):
            st.code(uplna_konfigurace, language="yaml")

    st.subheader("Jak jsme ověřili funkčnost")
    st.markdown("""
    Nejprve jsme ověřili síťovou komunikaci přes vložené IPS. Následovaly
    testy ICMP, skenování TCP portů a dvě fáze HTTP testování:
    IDS s upozorněními, následně IPS s blokováním vybraných požadavků.
    Reálné zásahy potvrzují události `blocked` v exportu EVE a screenshoty
    EveBoxu. Nakonec jsme pomocí iPerf2 a `ping` měřili propustnost,
    odezvu a stabilitu při dlouhodobé TCP zátěži.
    """)

    st.subheader("Fotodokumentace fyzického zapojení")
    photos = json.loads((ROOT / "assets" / "photos" / "photos.json").read_text(encoding="utf-8"))
    cols = st.columns(2)
    for i, p in enumerate(photos):
        with cols[i % 2]:
            st.image(
                str(ROOT / "assets" / "photos" / p["file"]),
                caption=p["caption"],
                use_container_width=True,
            )
    st.caption("Fotografie dokládají skutečně sestavenou laboratoř; konkrétní čísla portů a VLAN vycházejí z dokumentace zapojení.")

elif panel == "Simulace útoků":
    st.header("Simulace útoků a testovací Python skripty")
    st.markdown("""
    Tato část vysvětluje, jak vznikala testovací síťová komunikace, jak jsme
    zajistili opakovatelnost jednotlivých pokusů a jak jsme porovnávali odpověď
    klienta s bezpečnostními událostmi Suricaty. Všechny pokusy proběhly
    ve fyzické laboratoři: Linux `10.20.0.100` odesílal provoz
    přes L3 switch a transparentní IPS na Windows `10.10.0.100`.

    HTTP server na Windows naslouchal na portu `8080` a neprováděl žádnou SQL
    operaci, nevykonával JavaScript ani neotevíral testované souborové cesty.
    Generované HTTP požadavky proto představují vzory pro ověření signatur,
    nikoli úspěšné zneužití zranitelné webové aplikace.
    """)

    st.subheader("Postup a použité nástroje")
    st.markdown("""
    Testování probíhalo v naší izolované laboratorní síti. Na útočném
    Linuxu jsme spouštěli připravené Python skripty, které odesílaly přesně
    definované TCP nebo HTTP požadavky na cílový Windows. Na Windows běžel
    jednoduchý testovací HTTP server na portu 8080, který přijatý obsah
    nevykonával jako skutečný útok. Tím jsme mohli bezpečně porovnávat,
    co IDS pouze zaznamená a co IPS skutečně zablokuje.

    Skripty zaznamenávaly výsledky pokusů; jejich interpretaci jsme ověřovali
    proti logům EVE JSON a rozhraní EveBox. Samotný timeout klienta
    jsme nepovažovali za dostatečný důkaz blokování.
    """)
    st.dataframe(pd.DataFrame([
        {"Typ testu":"TCP skenování", "Použitý skript":"tcp_scanner_v4.py", "Princip":"Řízené TCP connect pokusy na 12 vybraných portů; rychlé/pomalé profily a kontrola obnovy komunikace"},
        {"Typ testu":"Základní HTTP", "Použitý skript":"http_attack_lab_v1.py", "Princip":"Série známých HTTP požadavků pro porovnání reakcí IDS a IPS"},
        {"Typ testu":"Pokročilé HTTP", "Použitý skript":"http_advanced_v2.py", "Princip":"20 postupných scénářů: neškodné požadavky, SQLi/XSS/traversal vzory, varianty kódování a GET/POST (formulář/JSON)"},
        {"Typ testu":"HTTP cíl", "Použitý skript":"windows_http_lab_server.py", "Princip":"Kontrolovaný HTTP server pro GET/POST, bez vykonávání testovaných vstupů"},
    ]), hide_index=True, use_container_width=True)
    
    st.subheader("Testovací scénáře HTTP")
    cases=pd.read_csv(D/"http_test_cases.csv")
    columns=[c for c in ["index", "case", "family", "method", "expected_match", "expected_sid"]
             if c in cases.columns]
    st.dataframe(cases[columns],use_container_width=True,hide_index=True)
    st.caption("Tabulka uvádí 20 připravených scénářů a očekávané signatury. "
               "Individuální pozorované výsledky nevyvozujeme pouze z očekávání nebo "
               "z poslední dodané konfigurace; ty vyžadují párování s testovacími záznamy.")


    st.subheader("Ukázky ze skutečných zdrojových kódů")
    st.caption("Výňatky pocházejí z původních skriptů a jsou bez úprav samotného kódu. "
               "Jde o vybrané části funkcí, nikoli o samostatně spustitelné programy. "
               "Pro přehlednost uvádíme jen jejich podstatnou logiku.")
    snippets = ROOT / "assets" / "ukazky_kodu"
    http_tab, eve_tab, tcp_tab, server_tab = st.tabs([
        "HTTP požadavky", "Párování s EVE", "TCP skener", "Server na Windows"
    ])
    with http_tab:
        st.markdown("""
        **Zdroj:** `http_advanced_v2.py`, funkce `run()`.

        Skript postupně prochází definované scénáře. Do URL každého požadavku
        vkládá náhodný identifikátor běhu (`rid`) a jméno scénáře (`labcase`).
        Následně naváže HTTP spojení, odešle požadavek `GET` nebo `POST`,
        zaznamená odpověď či chybu a uloží výsledek do JSON.
        Tyto identifikátory usnadňují pozdější spojení konkrétního testu s
        událostí zaznamenanou Suricatou.
        """)
        st.code((snippets / "http_odesilani.py").read_text(encoding="utf-8"), language="python")
        st.markdown("""
        **Příklady reálných scénářů:** `baseline` (neškodný vstup),
        `sql_encoded` (URL-kódovaný SQLi vzor), `xss_encoded` (XSS vzor),
        `trav_encoded` (průchod adresářů), dále `POST` s formulářovým nebo JSON tělem.
        Skript obsahuje **20 připravených scénářů** včetně kontrolních požadavků.
        """)
    with eve_tab:
        st.markdown("""
        **Zdroj:** `http_advanced_v2.py`, funkce `match_event()` a `analyze()`.

        Při analýze se kontroluje zdrojová a cílová IP adresa, cílový port a
        časové okno. Pokud je ve výpisu dostupná HTTP URL, skript hledá shodu
        `rid`/`labcase`; alternativně používá zdrojový TCP port.
        Tím omezuje riziko, že bude náhodný alert přiřazen nesprávnému pokusu.
        """)
        st.code((snippets / "http_parovani_eve.py").read_text(encoding="utf-8"), language="python")
        st.markdown("""
        Výsledek klienta (`HTTP_RESPONSE`, `TIMEOUT` či `NETWORK_ERROR`) je
        **odlišný od závěru o zásahu IPS**. Ten skript vyhodnocuje až z
        odpovídajícího EVE alertu a pole `alert.action`.
        """)
        st.code((snippets / "http_vyhodnoceni.py").read_text(encoding="utf-8"), language="python")
        st.caption("`blocked` = potvrzený blokovací alert; `allowed` = upozornění na povolený provoz; "
                   "bez odpovídajícího alertu zůstává daný výsledek neověřený. "
                   "Jeden alert s akcí allowed však nemusí sám o sobě znamenat, "
                   "že byla povolena celá HTTP transakce.")
    with tcp_tab:
        st.markdown("""
        **Zdroj:** `tcp_scanner_v4.py`, funkce `attempt()`.

        Nejde o nízkoúrovňový SYN skener. Skript se pokouší navázat běžná
        **TCP spojení pomocí `socket.connect()`** na předem určené porty.
        Rozlišuje úspěšné spojení (`OPEN`), aktivní odmítnutí (`CLOSED`),
        timeout (`TIMEOUT`) a další chyby. Ukládá také čas zahájení,
        dobu trvání, zdrojový port a identifikátor pokusu.
        """)
        st.code((snippets / "tcp_pokus.py").read_text(encoding="utf-8"), language="python")
        st.write("Časování portových pokusů řídí okolní funkce `run_scan()` a zvolený "
                 "profil `fast`/`slow`. Samotný stav `TIMEOUT` nelze bez dalších "
                 "záznamů přisuzovat zásahu IPS.")
    with server_tab:
        st.markdown("""
        **Zdroj:** `windows_http_lab_server.py`, třída `Handler`.

        Server přijímá požadavky `GET` a `POST`. U `POST` pouze přečte
        přijaté tělo a při běžném zpracování odpoví stavem HTTP `200`.
        Odeslané SQLi, XSS ani traversal řetězce nijak neinterpretuje.
        Tím slouží jako kontrolovaný cíl pro testování **síťové inspekce**.
        """)
        st.code((snippets / "http_server_windows.py").read_text(encoding="utf-8"), language="python")

    st.subheader("Jak číst výsledek konkrétního testu")
    st.markdown("""
    1. **Odeslání:** například `sql_encoded` vytvoří HTTP požadavek z Linuxu
       `10.20.0.100` na Windows `10.10.0.100:8080` a přidá identifikátory testu.
    2. **Kontrola:** Suricata na průchozím IPS porovná požadavek s právě
       aktivní sadou pravidel. Ve fázi IDS používala HTTP sada `alert`,
       ve fázi IPS měla odpovídající signatura akci `drop`.
    3. **Záznam:** skript zaznamená odpověď nebo timeout; Suricata nezávisle
       zapíše detekci do `eve.json`.
    4. **Vyhodnocení:** oba záznamy se spárují podle testovacích identifikátorů,
       adres, portů a času. **Blokování potvrdí až odpovídající
       `alert.action=blocked`**, případně další nezávislé ověření.

    Konkrétní příklad signatury **SID `1000121`** a blokované události je
    zachycen na stránce **EveBox a screenshoty**. Úplný přehled testovacích
    scénářů, obě varianty HTTP pravidel a jejich SID jsou na stránce
    **Pravidla Suricaty**.
    """)

elif panel == "Pravidla Suricaty":
    st.header("Detekční a blokovací pravidla Suricaty")
    st.write("Pravidla se během experimentů měnila a jednotlivé sady se aktivovaly postupně. "
             "Přehled proto popisuje použité varianty, nikoli stav všech pravidel v jediném okamžiku.")

    st.markdown("""
    Každé pravidlo je identifikováno číslem SID a určuje podmínku,
    při které má Suricata reagovat. Akce `alert` vytvoří upozornění,
    zatímco `drop` je v inline IPS určena k blokování odpovídajícího provozu.
    Níže uvádíme skutečné dodané signatury, nikoli jen ilustrační příklady.
    """)

    st.subheader("HTTP testování: IDS/IPS")
    t_ids, t_ips, t_compare = st.tabs(["1. fáze: IDS", "2. fáze: IPS", "Srovnání signatur"])
    with t_ids:
        st.markdown("**IDS sada (`http_lab_ids.rules`)** – všechny dodané HTTP signatury "
                    "používají akci `alert`. Účelem bylo nejdříve ověřit detekci bez "
                    "blokování samotnými HTTP pravidly.")
        st.write("Podle průběhu laboratorních testů tato fáze převážně pouze upozorňovala; "
                 "vyskytla se jedna výjimka v pozorovaném chování. Protože všechny "
                 "signatury v dodané IDS sadě mají akci `alert`, nelze bez konkrétního "
                 "protokolu příčinu této výjimky připsat právě IDS sadě.")
    with t_ips:
        st.markdown("**IPS sada (`http_lab_ips.rules`)** – devět pravidel pro SQLi, XSS "
                    "a průchod adresářů bylo změněno z `alert` na `drop`. "
                    "Kontrolní pravidlo SID `1000100` zůstalo typu `alert`.")
        st.write("Ve druhé fázi se ověřovalo skutečné blokování vybraných "
                 "HTTP požadavků. Důkazem jsou také autentické záznamy s akcí "
                 "`blocked` v EVE JSON a screenshot z EveBoxu u SID `1000121`.")
    with t_compare:
        st.dataframe(pd.read_csv(D/"http_sady_porovnani.csv"),
                     hide_index=True,use_container_width=True)
        st.caption("Srovnání je odvozeno přímo ze dvou předaných souborů pravidel; "
                   "nepotvrzuje současnou aktivaci obou sad.")

    st.subheader("Katalog použitých pravidel")
    df=pd.read_csv(D/"pravidla_inventar.csv")
    files=sorted(df["soubor"].dropna().unique().tolist())
    choice=st.selectbox("Soubor s pravidly", files)
    sub=df[df["soubor"]==choice]
    st.dataframe(sub[["sid", "akce", "protokol", "zprava"]],
                 use_container_width=True,hide_index=True)
    with st.expander("Zobrazit text pravidel z vybraného souboru"):
        st.code("\n".join(sub["puvodni_pravidlo"].fillna("").tolist()), language="text")


elif panel == "Výkon a stabilita":
    st.header("Výkonové testy na skutečném zapojení")
    tab1, tab2, tab3, tab4 = st.tabs(["TCP", "UDP", "Latence", "CPU a RAM"])

    with tab1:
        tcp = pd.read_csv(D / "tcp_timeseries.csv")
        sel = st.selectbox(
            "TCP experiment",
            sorted(tcp.experiment.dropna().unique().tolist()),
            index=0,
        )
        d = tcp[tcp.experiment == sel]
        st.subheader("Propustnost TCP v čase")
        st.line_chart(
            d.pivot_table(index="end_sec", columns="device", values="mbps").sort_index(),
            x_label="Čas od začátku experimentu [s]",
            y_label="Propustnost [Mbit/s]",
        )
        st.dataframe(
            pd.read_csv(D / "tcp_summary.csv").query("experiment == @sel"),
            hide_index=True,
            use_container_width=True,
        )
        st.caption("Závěrečný Windows report obsahoval timeouty při ukončování TCP; hlavní 600s přenos byl stabilní")

    with tab2:
        udp = pd.read_csv(D / "udp_tests.csv")
        st.dataframe(udp, use_container_width=True, hide_index=True)
        st.subheader("Skutečná odesílaná rychlost UDP")
        st.bar_chart(
            udp.set_index("id")["actual_send_mbps"],
            x_label="Test UDP (identifikátor pokusu)",
            y_label="Odesílaná rychlost [Mbit/s]",
        )
        st.warning("U vysoké UDP zátěže nelze spolehlivě určit celkovou ztrátovost kvůli rozděleným reportům")

    with tab3:
        latency = pd.read_csv(D / "latency.csv")
        st.subheader("Průměrná a maximální odezva ICMP")
        rtt = latency.set_index("label")[["rtt_avg_ms", "rtt_max_ms"]].rename(
            columns={"rtt_avg_ms": "Průměrná RTT", "rtt_max_ms": "Maximální RTT"}
        )
        st.bar_chart(
            rtt,
            x_label="Podmínky měření",
            y_label="Doba odezvy RTT [ms]",
        )
        st.dataframe(latency, use_container_width=True, hide_index=True)

    with tab4:
        cpu = pd.read_csv(D / "suricata_cpu_memory.csv")
        st.subheader("Využití CPU Suricaty")
        st.line_chart(
            cpu.set_index("elapsed_sec")["cpu_total_pct"],
            x_label="Čas od začátku měření [s]",
            y_label="Využití CPU [% jednoho logického CPU]",
        )
        st.subheader("Spotřeba operační paměti Suricaty")
        st.line_chart(
            cpu.set_index("elapsed_sec")["rss_mib"],
            x_label="Čas od začátku měření [s]",
            y_label="Paměť RSS [MiB]",
        )
        st.caption("CPU podle pidstat je vyjádřeno jako procento jednoho logického CPU")

elif panel == "Analýza EVE":
    st.header("Vlastní analýza laboratorních událostí")
    st.caption("Reálná data z dodaného eve.json; filtrujeme laboratorní pravidla SID 1000000–1000999 ze dne 17. 11. 2026. Jde o počty alertů, ne počet unikátních útoků.")
    a,b,c=st.columns(3)
    a.metric("Lab alerty",eve["pocet_laboratornich_alertu"])
    b.metric("S akcí blocked",eve["laboratorni_akce"].get("blocked",0))
    c.metric("S akcí allowed",eve["laboratorni_akce"].get("allowed",0))
    df=pd.read_csv(D/"eve_alerty_laboratorni.csv")
    sigs=pd.read_csv(D/"eve_signatury_laboratorni.csv")
    st.subheader("Nejčastější laboratorní signatury")
    st.bar_chart(sigs.head(12).set_index("signatura")["celkem"])
    cas=pd.read_csv(D/"eve_laboratorni_v_case.csv")
    st.subheader("Alerty v čase")
    st.bar_chart(cas.set_index("hodina")["pocet"])
    x,y=st.columns(2)
    with x:
        akce=st.multiselect("Akce",sorted(df.akce.unique().tolist()),default=sorted(df.akce.unique().tolist()))
    with y:
        sid=st.selectbox("Signatura",["Všechny"]+[f"{r.sid} – {r.signatura}" for r in sigs.itertuples(index=False)])
    filtered=df[df.akce.isin(akce)]
    if sid!="Všechny":filtered=filtered[filtered.sid==int(sid.split(" ")[0])]
    st.write(f"Zobrazeno **{len(filtered)}** laboratorních alertů")
    st.dataframe(filtered,use_container_width=True,hide_index=True)
    st.caption("Historický export má více než 25 tisíc opakovaných diagnostických alertů `SURICATA Ethertype unknown`; přehled se proto zaměřuje na vlastní laboratorní SID.")
    with st.expander("Rozdělení všech typů událostí v původním EVE"):
        st.dataframe(pd.read_csv(D/"eve_udalosti_typy.csv"),use_container_width=True,hide_index=True)

elif panel == "EveBox a screenshoty":
    st.header("EveBox – důkazy skutečné detekce a blokování")
    st.write("EveBox využíváme jako hotové rozhraní pro detailní zkoumání událostí Suricaty. "
             "Vlastní část projektu tvoří fyzické IPS, testování a vyhodnocení ve Streamlitu.")
    st.info("Screenshoty byly pořízeny nad filtrovaným archivním výřezem EVE JSON ze 17. 11. 2026; "
            "zobrazované počty nejsou počty útoků ani statistikou celého původního logu")
    imgdir = ROOT / "assets" / "screenshots_evebox"
    descriptions = json.loads((imgdir / "screenshots.json").read_text(encoding="utf-8"))
    available = [item for item in descriptions if (imgdir / item["filename"]).is_file()]
    if available:
        tabs = st.tabs([item["tab"] for item in available])
        for tab, item in zip(tabs, available):
            with tab:
                st.subheader(item["title"])
                st.write(item["description"])
                st.image(str(imgdir / item["filename"]), use_container_width=True,
                         caption=f"Screenshot EveBoxu: {item['filename']}")
    else:
        st.warning("Screenshoty nejsou k dispozici ve složce assets/screenshots_evebox/.")

else:
    st.header("Závěrečné vyhodnocení projektu")
    st.success("Hlavní cíl byl splněn: sestavili jsme reálné síťové zapojení, zprovoznili transparentní inline Suricata IPS a experimentálně ověřili detekci, blokování i výkon.")

    st.subheader("Vyhodnocení dosažených cílů")
    st.markdown("""
    **Praktická realizace:** Na fyzických zařízeních Lenovo a switchi Cisco Catalyst C3850
    jsme vytvořili dvě oddělené sítě VLAN 20 (simulované vnější prostředí)
    a VLAN 10 (chráněná síť). Switch směroval provoz mezi VLAN a Suricata
    jej kontrolovala na cestě k Windows jako **transparentní dvourozhranový bridge
    bez IP adres na průchozích rozhraních**. Funkčnost zapojení dokládá
    fotodokumentace, konfigurace a provedené experimenty.

    **Detekce a blokování:** Pomocí připravených Python skriptů jsme simulovali
    TCP skenování a řízené HTTP požadavky představující příklady SQL injection,
    XSS a průchodu adresářů. HTTP testování proběhlo nejprve s pravidly
    **IDS (`alert`)**, následně s pravidly **IPS (`drop`)**. Záznamy v EVE JSON
    a ukázky v EveBoxu potvrzují skutečně blokované události, mimo jiné u ICMP,
    skenování portů a HTTP požadavků. Ne všechny varianty HTTP vstupu však
    vlastní signatury zachytily; ukázalo se omezení jednoduchých pravidel.

    **Výkon:** Při čtyřech souběžných TCP spojeních jsme během desetiminutového
    experimentu naměřili přibližně **949 Mbit/s** bez dlouhodobého poklesu
    propustnosti. V opakovaném 30sekundovém UDP testu byla potvrzena nulová
    ztrátovost při **210 Mbit/s**. Při vyšší zátěži kolem **262 Mbit/s** však
    přibylo **27 030 `capture.kernel_drops`**, takže výsledek nelze zobecnit
    jako bezchybný provoz při libovolné frekvenci paketů.

    **Latence a provozní stabilita:** Ping testy nevykázaly ztráty ICMP
    paketů ani výrazný nárůst RTT při současném TCP provozu. Paměť procesu
    Suricata se v dlouhodobém monitoringu držela okolo **450 MiB**;
    služba po testu zůstala aktivní a systemd nehlásil automatický restart.
    """)

    st.subheader("Hlavní naměřené výsledky")
    a, b, c, d = st.columns(4)
    a.metric("TCP – 10 minut", "≈ 949 Mbit/s")
    b.metric("UDP – bez ztrát", "210 Mbit/s")
    c.metric("ICMP ztráty", "0 %")
    d.metric("RAM Suricaty", "≈ 450 MiB")
    st.caption("TCP: 4 spojení, 600 s. UDP: 30 s, 1200B datagramy a 1MiB buffer příjemce. Hodnoty platí pro konkrétní laboratorní sestavu.")

    st.subheader("Omezení experimentů")
    st.markdown("""
    - **UDP:** při vyšší zátěži vznikaly ztráty.
      Rozdělené reporty Windows iPerf2 neumožňují určit spolehlivou celkovou
      ztrátovost nejvyšších UDP testů.
    - **TCP:** při ukončování některých spojení iPerf2 hlásil timeouty,
      ačkoliv vlastní desetiminutový přenos měl stabilní propustnost.
    - **Latence:** druhý ping test částečně přesahoval interval TCP zátěže.
      Chybí také samostatné referenční měření stejné sítě bez vloženého IPS;
      nelze tedy vyčíslit přesnou režii způsobenou Suricatou.
    - **Bezpečnostní testy:** HTTP požadavky byly laboratorními vzory,
      nikoliv útoky proti skutečně zranitelné webové aplikaci. Počty alertů
      navíc nejsou počty unikátních útoků a pravidla nejsou univerzální
      ochranou před všemi variantami SQLi, XSS nebo traversal.
    """)

    st.subheader("Vlastní přínos a názor autorů")
    st.markdown("""
    Za hlavní přínos považujeme **kompletní realizaci a ověření fyzického IPS**:
    návrh VLAN a zapojení zařízení, konfiguraci obousměrného AF_PACKET,
    přípravu a střídání sad pravidel IDS/IPS, použití Python skriptů
    k reprodukovatelnému generování testovacího provozu a společné
    vyhodnocení výsledků z Linuxu, Windows a Suricaty. Pro samostatnou technickou dokumentaci
    jsme připravili **Streamlit web** s grafy a výběrem laboratorních událostí;
    pro detailnější prohlížení logů jsme použili existující nástroj **EveBox**.

    Na základě testů považujeme Suricatu za vhodný nástroj pro demonstrační
    inline ochranu i pro výuku síťové bezpečnosti: umožnila nám názorně
    porovnat detekci a skutečné blokování. Zároveň se ukázalo, že účinné
    pravidlo musí být dobře navržené a otestované a že výkon IPS závisí
    nejen na datové propustnosti, ale také na charakteru provozu
    a počtu zpracovávaných paketů.
    """)


    st.subheader("Rozdělení práce mezi autory")
    st.markdown("""
    Na projektu jsme spolupracovali v rámci návrhu, sestavení laboratorního
    prostředí, testování a přípravy technické dokumentace. Hlavní odpovědnosti
    byly rozděleny následovně:
    """)
    st.dataframe(pd.DataFrame([
        {"Činnost": "Návrh projektu a laboratorního řešení", "Hlavní odpovědnost": "David Kunčík (kun212)"},
        {"Činnost": "Fyzické zapojení zařízení a konfigurace Suricaty", "Hlavní odpovědnost": "Oryna Borovyk (bor0250)"},
        {"Činnost": "Provedení bezpečnostních a výkonnostních testů", "Hlavní odpovědnost": "Oryna Borovyk s asistencí Davida Kunčíka"},
        {"Činnost": "Zpracování a publikace webové dokumentace", "Hlavní odpovědnost": "David Kunčík (kun212)"},
    ]), hide_index=True, use_container_width=True)
    st.markdown("""
    **Oryna Borovyk** se podílela především na praktické realizaci laboratorní
    sítě, konfiguraci IPS a provádění experimentů. **David Kunčík** připravil
    návrh řešení, asistoval při testování a zpracoval výsledky do samostatné
    webové dokumentace ve Streamlitu. Oba jsme tedy přispěli k praktickému
    ověření navrženého systému, každý se zaměřením na jinou část projektu.
    """)

    st.subheader("Použité zdroje")
    st.markdown("""
    - [Oficiální dokumentace Suricata](https://docs.suricata.io/)
    - [EveBox – dokumentace](https://evebox.org/docs/)
    - [Streamlit – dokumentace](https://docs.streamlit.io/)
    - Vlastní laboratorní konfigurace, pravidla, Python skripty, fotografie, EVE JSON a výsledky testů ze 17. 11. 2026.
    """)

st.divider()
