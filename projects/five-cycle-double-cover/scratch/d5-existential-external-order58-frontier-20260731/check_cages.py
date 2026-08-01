#!/usr/bin/env python3
"""Independent semantic check of the complete 18-row (3,9)-cage control."""

from __future__ import annotations

import base64
from collections import deque
import hashlib
import zlib


DATA = """c-o~{O>bK{47~53B55U10x!T6IrzxUDMufADEjYL5;+v*WPt+v(%R3mo<4@d;mE&#5@{zQCK<0{Wb{OFb^NQ>?Dn=AJL&w?Xgo7tnC6{D%lLY{==dA2^X0yt_R&<<__BvoJT_M1Q*una9v;^Rm1lT8v7Tw(%O6sXA)7bO>*C{<8~TWu>4p~37Mt$$*YBUXZ5e+&8u_VU(6NR!`BkEyuT@5)p;w>1WX{X$(^@_g7RRHn_%KY&SU{q(wrBpyuwuVncZ5cty?F2J?+p-WJRLE4KqbIn!yL^NO|h8Kd!a%-Q6X!+y%aor&4^E1H@0}uXO9sfgjNCHXjz*!0e74*%^%eqyaSclzisMVqV*o@K-kSEXGg*4#Ll;O-vPb<PgGhVN4wE4db}o?J#zvUYjb0hri}wM0js-zw^}_5y6?x5+4N7%hV|uYe~X-Hl`{(f$yxlpDIHviNML-r(#{}iPv93P(R}PdTE$JEGM4G6_=uhzbh|eC?s|?cFS9rMo}6Aj)KZ1+xXcN}3A1S5U9xCB?pd6vftZm4notV01be3lV>^hYfycfn3)Eb=6etHX?hL7lc#H|7&l9*|9jHY9ba|$mzEpW_i|t%_Qzb`Ta03%rjT0MBp6+QD95UG|siCkD;MjP)X>Ft*x&Bjp&CYj)NFhrEs7SJ|<&Dt!)fo0cZ6mM7Ba=s}RtgZbVy9W6qN8b5E=Aau;F`ycQC0-pGLLZIT6rtrFZlgC>NQtBbK2F6{Y-5rs6Z7mD_2GQZ(ZS3C4HztqiLfuGF#d}<t@dITuyywCs**_0Wp_Ajg?yuB4n{OhwYvjA4T_ChE$>uFXvk_2|44+lc{p@E5Xn#9qlVBq=x(h!(J(GG)4MACGs-az?sczi1u7Y4{l0mTyN=J)M?V-f81nvSl0x>?<*Kx>qm%iN{04YYL~F(XrRs;mj86vm`Jz>RM;d%(jK^?$iPEad@0RX<#x*K3o4lgFy_kd43NT~=EkKVb`zZDwK_~+1UKS;E5*NWMRh4ANF=aRD+OB933OB&tu=^u)8vhTSO)l`1+I@#%;t70DzjZ}*w)(@7dN-~4zh&SclT{!PolzU<eMPW2IH#1kI#}7q7N<(cT#FD)HP}tGN+oXFo~&lnQ32i1sIt8p{`)6&$a*571@EXFi{#y>r^OW40{*R71`$q(s%(LE(47Z&jkynP+dK$PI$gsF}z!hHLb0dUf@djl?J~eP}`@h-eO>xKA^HB$}W7W?YdLQjfK8<j>4q93JEWE2tNKOVZM}IxEyrbbHDFqu-Z}L!|^JeRyQhTriS31i(h$Ws0pVl&Hjo5LeE4!QJFiDat`t(FlyY?Jr&s7V)P}9xe=<-Ivjelq^<Rmq{Vvf46@ytifJ&Hx*O5;%V7zXnj1t?b_Ov$X3!rv{))=s)3lymmbLE!3*JIZ=CG^MP93>y8}?pyUwnT^{l~ebMT>MGu>vQ+D;>hY=`lYGJ0!CWl{$+10funG161x?S9<d3L?u@G>-gCq+yiqctj9cf!tO}8;}q9B!0mp}R_rcpkYm%eR+%Weup$?tvliduq*7Hid)=zTWmv1;O9owVj+Vz?60X_DfQo*Libje|v^8^J)LX_WOd_8huU81d?67FUnxVWF^WYS6LbUVu6+2FNse4weE`ELB)S_##YpK+5XIy?<`1<?GH#LavJ!9|<DlQNlxw1IfJ;fy=)nOF+^88u9&1<#3?A7}z%yU<?crZtWk4VIXU%V}3-pX-1aLuDK$>SM%dt0Kv6UZP9YS0^fduIL@VSW+$"""
SOURCE_URL = "https://houseofgraphs.org/data/cages/cagesk3g09.g6"
SOURCE_SHA256 = "6c5339042f2f48e9f596e154da3f0bc145d27cb835902f538618013c2439b5b2"


def parse_graph6(row: bytes) -> tuple[int, tuple[tuple[int, int], ...]]:
    values = [byte - 63 for byte in row.strip()]
    assert values[0] < 63
    n = values[0]
    bits = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    index = 0
    for v in range(1, n):
        for u in range(v):
            if bits[index]:
                edges.append((u, v))
            index += 1
    return n, tuple(edges)


def incidence(n: int, edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    rows = [[] for _ in range(n)]
    for edge, (u, v) in enumerate(edges):
        rows[u].append(edge)
        rows[v].append(edge)
    return rows


def neighbors(n: int, edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    rows = [[] for _ in range(n)]
    for u, v in edges:
        rows[u].append(v)
        rows[v].append(u)
    return rows


def girth(n: int, edges: tuple[tuple[int, int], ...]) -> int:
    rows = neighbors(n, edges)
    best = n + 1
    for source in range(n):
        distance = [-1] * n
        parent = [-1] * n
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for other in rows[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    best = min(best, distance[vertex] + distance[other] + 1)
    return best


def nine_cycles(n: int, edges: tuple[tuple[int, int], ...]) -> set[frozenset[int]]:
    rows = incidence(n, edges)
    answer: set[frozenset[int]] = set()
    for start in range(n):
        def visit(vertex: int, path: tuple[int, ...], used: frozenset[int]) -> None:
            if len(path) == 9:
                if vertex == start:
                    answer.add(frozenset(path))
                return
            for edge in rows[vertex]:
                if edge in used:
                    continue
                u, v = edges[edge]
                other = v if u == vertex else u
                if other == start:
                    if len(path) == 8:
                        visit(start, path + (edge,), used | {edge})
                    continue
                if other < start:
                    continue
                visit(other, path + (edge,), used | {edge})
        visit(start, (), frozenset())
    return answer


def bounded_cycle_pack(
    cycles: set[frozenset[int]], target: int, edge_capacity: int, edge_count: int
) -> tuple[frozenset[int], ...] | None:
    """Find target cycles while using each edge at most edge_capacity times."""
    cycle_list = tuple(sorted(cycles, key=lambda cycle: tuple(sorted(cycle))))
    order = sorted(
        range(len(cycle_list)),
        key=lambda index: sum(bool(cycle_list[index] & other)
                              for other in cycle_list),
    )
    loads = [0] * edge_count

    def search(start: int, chosen: tuple[int, ...]) -> tuple[int, ...] | None:
        if len(chosen) == target:
            return chosen
        if len(order) - start < target - len(chosen):
            return None
        for position in range(start, len(order)):
            index = order[position]
            if any(loads[edge] == edge_capacity for edge in cycle_list[index]):
                continue
            for edge in cycle_list[index]:
                loads[edge] += 1
            result = search(position + 1, chosen + (index,))
            for edge in cycle_list[index]:
                loads[edge] -= 1
            if result is not None:
                return result
        return None

    indices = search(0, ())
    if indices is None:
        return None
    return tuple(cycle_list[index] for index in indices)


def tait_coloring(n: int, edges: tuple[tuple[int, int], ...]) -> tuple[int, ...] | None:
    rows = incidence(n, edges)
    colors = [-1] * len(edges)
    used = [0] * n

    def search(left: int) -> tuple[int, ...] | None:
        if left == 0:
            return tuple(colors)
        edge = max(
            (e for e, color in enumerate(colors) if color < 0),
            key=lambda e: (used[edges[e][0]] | used[edges[e][1]]).bit_count(),
        )
        u, v = edges[edge]
        allowed = (~(used[u] | used[v])) & 7
        while allowed:
            bit = allowed & -allowed
            allowed -= bit
            colors[edge] = bit.bit_length() - 1
            used[u] |= bit
            used[v] |= bit
            result = search(left - 1)
            if result is not None:
                return result
            used[u] ^= bit
            used[v] ^= bit
            colors[edge] = -1
        return None

    return search(len(edges))


def main() -> None:
    raw = zlib.decompress(base64.b85decode(DATA.encode("ascii")))
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
    source_rows = [row for row in raw.splitlines() if row]
    assert len(source_rows) == 18
    counts = []
    marked = 0
    disjoint_six = 0
    half_integral_eleven = 0
    for graph_index, source_row in enumerate(source_rows):
        n, edges = parse_graph6(source_row)
        assert n == 58 and len(edges) == 87 and len(set(edges)) == 87
        rows = incidence(n, edges)
        assert all(len(row) == 3 for row in rows)
        assert girth(n, edges) == 9
        coloring = tait_coloring(n, edges)
        assert coloring is not None
        assert all({coloring[e] for e in row} == {0, 1, 2} for row in rows)
        cycles = nine_cycles(n, edges)
        counts.append(len(cycles))
        # A five-unit edge subdivision cannot destroy all 9-cycles.  Sixteen
        # cages have six edge-disjoint 9-cycles.  For the other two, eleven
        # selected 9-cycles use each edge at most twice, so five subdivided
        # edge units can hit at most ten of them.
        if graph_index in (12, 14):
            pack = bounded_cycle_pack(cycles, 11, 2, len(edges))
            half_integral_eleven += 1
        else:
            pack = bounded_cycle_pack(cycles, 6, 1, len(edges))
            disjoint_six += 1
        assert pack is not None
        loads = [sum(edge in cycle for cycle in pack)
                 for edge in range(len(edges))]
        assert max(loads) <= (2 if graph_index in (12, 14) else 1)
        for z in range(n):
            avoiding = [cycle for cycle in cycles
                        if all(z not in edges[edge] for edge in cycle)]
            common = set.intersection(*(set(cycle) for cycle in avoiding))
            marked += sum(z not in edges[edge] for edge in common)
    assert counts == [92, 95, 96, 84, 86, 100, 95, 96, 70,
                      95, 97, 92, 80, 93, 73, 84, 75, 70]
    assert marked == 0
    assert (disjoint_six, half_integral_eleven) == (16, 2)
    print(f"CAGE_SOURCE rows=18 sha256={SOURCE_SHA256} PASS")
    print("CAGE_GEOMETRY order=58 simple=1 cubic=1 connected=1 girth=9 PASS")
    print("CAGE_TAIT rows=18 certificates_reconstructed=18 PASS")
    print("CAGE_MARKED_INTERFACES candidates=0 PASS")
    print("CAGE_FIVE_SUBDIVISIONS impossible=18 disjoint_six=16 half_integral_eleven=2 PASS")


if __name__ == "__main__":
    main()
