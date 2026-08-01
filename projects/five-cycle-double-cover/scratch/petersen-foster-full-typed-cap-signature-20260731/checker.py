#!/usr/bin/env python3
"""Semantic checker for six literal Petersen--Foster typed-cap witnesses."""

from __future__ import annotations

import base64
from collections import deque
import hashlib
import zlib


PETERSEN = (
    (0, 1), (1, 2), (2, 3), (0, 4), (3, 4),
    (0, 5), (1, 6), (2, 7), (5, 7), (3, 8),
    (5, 8), (6, 8), (4, 9), (6, 9), (7, 9),
)
LCF = (17, -9, 37, -37, 9, -17) * 15
PORT_NAMES = (1, 17, 89)
PAIRS = (18, 17, 6, 6, 24, 5)
COMPONENT_SIZES = (337, 419, 523, 383, 611, 469)

# Six consecutive 1,335-byte D5 label words, one for each typed-state bit.
WITNESS_B85 = (
    "c-rlm%dTZ75<~|GBoGr21OER@d#zw!tK_y@>K?hJlFPU5Ihzgnh>VP++Szl|e%76PoOb8fZJu4%nfKf~=c&ElHBYZ)^mg`cW$n|}"
    "E_d*-w0#GE_}psgv-08gwN7;rzujF{J8hrQ%j#pcareBu!G^W%ReE9NxU;n}$GP+Nx^6veHD~9$yH{uP!+U$Ue2mgZpA8#%{q{ZB"
    "{Zt-}ve!Km%Q<FZI2*OXS*3Hvyc)eaM`P8v9L%wYb-q+*UwgUV>ZjH<`#n4#p2^Q=-V4I41&8Kn?6P~sl2RJ3@dcmn;yAv=dAz|~"
    "V^R1L2Ua1v{C$?rm&yV65Y&c$7njb)zBWrG#MrQKYu?e!$g0T*FYem(^sZ9-#8Jb}*?iY#0>PQ?G>@@3H;4EOE}q5@o*c8LRhopo"
    "yt8)YY3B#;tuGH>mb;dCbRSsXaRxh&rp-pc%sI;v2l5UY>RBG+k$h{+lLcZj*|tAtz}OH0EN1szj5mQMk9@i61Re(y`@RAbqi@@U"
    "tpXEKh{L0q5Ys>~&Gvba;a4{IlwL8z&};!jLP)o+u2TkkxtJ7RUa#125+a=7YyQJn0?v;*&ziRlP;^8j*3Z?6a~~v{)Fl=ee+2(1"
    "xIoTaqbWpBD~_P5<V;Lr{&FoQ5~V&x#vu^o6R;AKloJOSeX<=#hlMB(h32sUR@*^#ipeS??Yw=ya19~lw^?L-In_D=LfAEm@ZdEw"
    "r1OI}OoDYWz9+mmaYk^k@f4MOTMUZ9Hbrai2NPj0aC>6!!#k*Z9JaLYJD)SbUMdY#m^ce_g;=l+ZrGOiO8O~ifyCLh8HTB+Y}w8J"
    "AO*ZTbk0oTU^~XF4GYGTpdvP4Tb_yt_ofaZ6p;kv8b~(Y_yPv-lrWP&Oe6!d$zsRQk`TC&h?80^qt+z~4~9a?z9_|O8D&y%z+={X"
    "`obPo2f6U7k>Fu?fImXPSS~&Y4id_uDXG8?SSM{(gF-5AtXqakY_L)+N>bvHfDwGQx>6!*D;|M*nXCRSZBo=$M-{n`D^{|&b+`2J"
    "h(-g^p;ZG$OQ>1rOGLN+GiY;PIHR4lh@$)j#%^jP9KQ-JD-;<zx@jfXgQe1DAUN}tiLpordB13pFcd*%4FlvI3$==E<4K7_3c!JF"
    "3|MNE2)XalODk@s-i%~{Dta~Nmhviqph1Q#mI@#W(nCdMNjSi^C3BweNc`Z<#}}SPOhv>bGq2;qV0H*xTyVR9;VrW&=W316Aw(_w"
    "L&3_Uc6oZCA1zARnG9T=H(wwVeCoT4rA>fS<@ykqae?oocuX}h?xn8a%_Ac1?)A~;<LYCYF#ZVs&?Y%^jTO*!?;1g?I3yuiNIM4N"
    "$gb)SyT`SO*=bTvnrERFyURa<Hm|6}`eIO0dk3~@?ZG6SYY814^Wl^>qp{9R(N%E?_G)>k@N5gShFIh`TCpWgBV}*fyq1H$Z5Xb!"
    "@hfeL(Ri)RVe#})t@R|Rhz(?815$+<C%ndGps3@Tc;gHFA3bOOFj30h4=Y=2^QcuZ3+u{f*F-@D<bd~&kPIBHOo~d{M9e5KSRLKd"
    "c91ZlJZAvH-or#Z<Y1SJj1p+sVdri*hboB9M5g5=k-fD2>Yr5A*R1ic>tK0WL!lG38MP!$!$)za+0u)ACn1@vr8*XHgcSw?P1kDl"
    "YkSKfz>ije)U?oQKGMgQ8J9NS|LSgoKoQOM!Y?nEtdieF{88EooIcYJqHIF$E2PivSf|jiMG?9a*06BgYT8THx&lJ_S8YZ=nme>z"
    "(S2)UB?3xJuq4DS6&7e;7YhB6+~aI_3jSaD+TKa?UJnd>dbG7pGK7NY(O*sN@BBc6u8+En1Fc_aTATsYwP01cmM^aDaK2I|ya~np"
    ">fXK<MpBDi@mT_<NXvlNPGhq-Fcf8~70zT086S=zWNg?hJV~_>tvzME{rI#zG68UAd)d__2ZJFRMrgg4C`hZ@o+A6<<tv40vK5}^"
    "VR)y?B~AMzku(^T3X*inL0|JUzo|$#+y!0Iw0{T+qTAHhZ}PdX$v(lW%r7$Z8;b}8)NySzkV10@wY{@inDve*EI$Q*KkYkpwUiTK"
    "W9S%YNs!2&TD}e|8QSpD#8Q7z5JPy3#6lKnGn^b@rxyOG&6D3WdDIr$5KCQ|$uRp1hiY@L^%yh)vwdolRbtJ8un+BD)aIF=##r_X"
    "qXMx+lBoWl;F;}B1*Sq70orSrJ?c!Q-tDD|Tyj4{xPZPn+DK@Q(JdPDDj1@=jv#ypESZnhU1z?;^9}CVFmXo?EAb}HBcjmGK;iUw"
    "zvTp5IaAW(r|ujUcDA*A%~Ip)&yb#>+y<5=+1}9pm2T$5Z%DT=e}?o7Yu}JAY^$)$IP!Z)|F<EX-Rc{S|GOc5ID~#fdivQnq|ftO"
    "8@8VH%aFc9BW1lIef|vTIB)ZpEdRrhE_40;kY4tiH@+b~GU^-B%P&K^V*h7Izdu9z{YMY!Jrss7KSR0;dWQ7eXgMDI4C%ITxeGXd"
    "np07<1!^90VihMT;#2<^($5>j1n8fJbW7xoqfhCmv)_$Zl;u#rIbgKEP@94Nr#21T`jgrOU{Ra*)#*{>o@fUL)!#$<A47W7mwHCg"
    "{GAr!V9}e`XYRzJ|LUi5zDui-X^aB!EX_ACud|zd@ogBoV^7b6ZyMesT3EDesAWDP^^3kp%_Jx%jg-XWkw>fVp2&#+m)}5B<ER?a"
    "S}nGT`sOA%;f9M8q^wuImLOJ=iF6FLZG}mHgXj{}HrJi3n?<MJ7Y`ZPD}|X(fGYpk5hf9?Fkv94+D^pY%|^OQhKOl3S}IGc4O8aT"
    "76EoG+v2G7PL_@Q8FlmqjwO<;dPnHYV#$o$kPM`!ynB*2uPzmYM=FY2PPfM8OLjSt!?sx!f#)N6iUj`p6^!3>9U%pzqd#ADwe)v+"
    "Yo}k?(@JXF1`{6LAE7=AZge?C&DLpf*U=$eJa49ti46!hY-p{%aaclnH-_H7%HWxLq=TyRVHXv0y6L+Mc)jH5D;9(kmiIHw#;h&W"
    "{CRT!#+>v6O^Qab5UZnK^Ii$2*|q~$c<`6*u+le=gax9Z%yo&<X(vO}>!#M(tH9UUMhO;9bWSwi8*6QNEkmPOq#Tbnc$=k{KUR2)"
    "Ln8A}65p-ByCs$NQgmB_do!0}KmZm6?N<_0OhwRyQM<h5tmxf<6qYeJ%IeK4_9g-TrodOLuYceY$P8Zw86it@X|&(i80l>+o;Y!e"
    "kH)r*(ACC%^4GhW8WsNTaprwfLDWvE>8|qE$k1AZgx%~X8RM1aj3#>7u&yMNcO&I*nI+_gr^G`g>VUg41k$`T%|W(#BAb3!6{^tg"
    "WTMO>5Wnv>f8TBXPj{R3-RJ%F-KPEZFYh*M|K)D8o{XS>+-;uUcbmWOHvd2FHva{PeTvu"
)


def make_graph() -> tuple[int, tuple[tuple[int, int], ...]]:
    foster: set[tuple[int, int]] = set()
    for u in range(90):
        for v in ((u + 1) % 90, (u + LCF[u]) % 90):
            foster.add((min(u, v), max(u, v)))
    edges = []
    for copy in range(10):
        edges.extend((89 * copy + u - 1, 89 * copy + v - 1)
                     for u, v in foster if 0 not in (u, v))
    used = [0] * 10
    for u, v in PETERSEN:
        a = 89 * u + PORT_NAMES[used[u]] - 1
        b = 89 * v + PORT_NAMES[used[v]] - 1
        used[u] += 1
        used[v] += 1
        edges.append((min(a, b), max(a, b)))
    assert len(foster) == 135 and used == [3] * 10
    return 890, tuple(sorted(edges))


def incidence(n: int, edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    rows = [[] for _ in range(n)]
    for edge, (u, v) in enumerate(edges):
        rows[u].append(edge)
        rows[v].append(edge)
    return rows


def adjacency(n: int, edges: tuple[tuple[int, int], ...], skip: int = -1,
              omit: int = -1) -> list[list[tuple[int, int]]]:
    rows = [[] for _ in range(n)]
    for edge, (u, v) in enumerate(edges):
        if edge != skip and omit not in (u, v):
            rows[u].append((v, edge))
            rows[v].append((u, edge))
    return rows


def connected(n: int, edges: tuple[tuple[int, int], ...], skip: int = -1,
              omit: int = -1) -> bool:
    rows = adjacency(n, edges, skip, omit)
    start = next(v for v in range(n) if v != omit)
    seen, todo = {start}, [start]
    while todo:
        for v, _ in rows[todo.pop()]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return len(seen) == n - (omit >= 0)


def bridges(n: int, edges: tuple[tuple[int, int], ...], skip: int = -1,
            omit: int = -1) -> list[int]:
    rows = adjacency(n, edges, skip, omit)
    start = next(v for v in range(n) if v != omit)
    tin, low, found = [-1] * n, [-1] * n, []
    timer = 0

    def visit(u: int, parent_edge: int) -> None:
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        for v, edge in rows[u]:
            if edge == parent_edge:
                continue
            if tin[v] >= 0:
                low[u] = min(low[u], tin[v])
            else:
                visit(v, edge)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    found.append(edge)

    visit(start, -1)
    assert sum(value >= 0 for value in tin) == n - (omit >= 0)
    return found


def girth(n: int, edges: tuple[tuple[int, int], ...], skip: int = -1,
          omit: int = -1) -> int:
    rows = adjacency(n, edges, skip, omit)
    best = n + 1
    for source in range(n):
        if source == omit:
            continue
        distance, parent_edge = [-1] * n, [-1] * n
        distance[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, edge in rows[u]:
                if distance[v] < 0:
                    distance[v] = distance[u] + 1
                    parent_edge[v] = edge
                    queue.append(v)
                elif parent_edge[u] != edge:
                    best = min(best, distance[u] + distance[v] + 1)
    return best


def petersen_not_tait() -> bool:
    rows = incidence(10, tuple(PETERSEN))
    colors = [-1] * 15

    def search() -> bool:
        if -1 not in colors:
            return True
        edge = colors.index(-1)
        for color in range(3):
            if all(colors[other] != color for vertex in PETERSEN[edge]
                   for other in rows[vertex] if other != edge):
                colors[edge] = color
                if search():
                    return True
                colors[edge] = -1
        return False

    return not search()


def factor_component(n: int, edges: tuple[tuple[int, int], ...],
                     rows: list[list[int]], labels: bytes,
                     pair: int, root: int) -> set[int]:
    active = [((label & pair).bit_count() == 1) for label in labels]
    assert active[root]
    component, todo = {root}, [root]
    while todo:
        edge = todo.pop()
        for vertex in edges[edge]:
            local = [other for other in rows[vertex] if active[other]]
            assert len(local) in (0, 2)
            for other in local:
                if other not in component:
                    component.add(other)
                    todo.append(other)
    return component


def main() -> None:
    n, edges = make_graph()
    rows = incidence(n, edges)
    assert len(edges) == len(set(edges)) == 1335
    assert all(u != v for u, v in edges) and all(len(row) == 3 for row in rows)
    assert connected(n, edges) and not bridges(n, edges)
    assert all(not bridges(n, edges, skip=edge) for edge in range(1335))
    assert girth(n, edges) == 10 and petersen_not_tait()
    print("GRAPH vertices=890 edges=1335 simple=1 cubic=1 edge_connectivity=3 girth=10 non_tait=1")

    z, root = 0, 552
    ports = tuple(rows[z])
    assert ports == (0, 1, 2)
    assert tuple(edges[edge] for edge in ports) == ((0, 1), (0, 81), (0, 89))
    assert edges[root] == (363, 400)
    assert connected(n, edges, omit=z) and not bridges(n, edges, omit=z)
    assert girth(n, edges, omit=z) == 10
    assert connected(n, edges, skip=root, omit=z)
    print("CORE vertices=889 degree2=3 degree3=886 connected=1 bridgeless=1 girth=10 root_deleted_connected=1")

    raw = zlib.decompress(base64.b85decode(WITNESS_B85.encode("ascii")))
    assert len(raw) == 8010
    assert hashlib.sha256(raw).hexdigest() == (
        "d4db26db13658c2f369ff606e41870cc6535553d92ce4ddc9713158cdc3ce4a0"
    )
    names = ("01", "01", "02", "02", "12", "12")
    slots_wanted = ((0, 1), (0, 1), (0, 2), (0, 2), (1, 2), (1, 2))
    mask = 0
    for bit in range(6):
        labels = raw[1335 * bit:1335 * (bit + 1)]
        assert all(label.bit_count() == 2 for label in labels)
        assert all(labels[a] ^ labels[b] ^ labels[c] == 0 for a, b, c in rows)
        pair = PAIRS[bit]
        component = factor_component(n, edges, rows, labels, pair, root)
        slots = tuple(i for i, edge in enumerate(ports) if edge in component)
        assert slots == slots_wanted[bit]
        inactive = labels[ports[next(i for i in range(3) if i not in slots)]]
        if bit % 2 == 0:
            assert inactive == pair
            mode = "in"
        else:
            assert inactive & pair == 0
            mode = "out"
        assert len(component) == COMPONENT_SIZES[bit]
        mask |= 1 << bit
        print(f"STATE bit={bit} physical={names[bit]} mode={mode} pair={pair} component={len(component)} PASS")
    assert mask == 63
    print("TYPED_MASK 63 FULL PASS")
    print("PASS")


if __name__ == "__main__":
    main()
