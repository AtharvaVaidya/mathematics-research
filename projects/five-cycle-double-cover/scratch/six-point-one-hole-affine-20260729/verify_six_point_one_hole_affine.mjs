#!/usr/bin/env node
// Independent standard-library replay of the six-point/one-hole audit.

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..");
const referencePath = path.join(
  root,
  "output",
  "jaeger-star-thinning-countermodel-34v",
  "star-good-six-witness.json",
);
const universe = [...Array(8).keys()];

function parity(value) {
  let answer = 0;
  for (let work = value; work; work &= work - 1) answer ^= 1;
  return answer;
}

function key(values) {
  return [...values].sort((a, b) => a - b).join(",");
}

const planeMap = new Map();
for (let first = 1; first < 8; ++first) {
  for (let second = first + 1; second < 8; ++second) {
    const plane = [0, first, second, first ^ second];
    planeMap.set(key(plane), new Set(plane));
  }
}
const planes = [...planeMap.values()].sort((a, b) =>
  key(a).localeCompare(key(b)),
);
if (planes.length !== 7) throw new Error("Fano plane enumeration failed");

function triangle(plane, potential) {
  return [...plane]
    .filter((point) => point !== 0)
    .map((point) => point ^ potential)
    .sort((a, b) => a - b);
}

function admitted(plane, support, missing) {
  return universe.filter((potential) => {
    const local = triangle(plane, potential);
    if (local.some((point) => !support.has(point))) return false;
    return !missing || ![...missing].every((point) => local.includes(point));
  });
}

function affine(points) {
  if (points.length === 0) return false;
  const translated = new Set(points.map((point) => point ^ points[0]));
  for (const left of translated) {
    for (const right of translated) {
      if (!translated.has(left ^ right)) return false;
    }
  }
  return true;
}

function combinations(values, size) {
  const result = [];
  function visit(start, current) {
    if (current.length === size) {
      result.push([...current]);
      return;
    }
    for (
      let index = start;
      index <= values.length - (size - current.length);
      ++index
    ) {
      current.push(values[index]);
      visit(index + 1, current);
      current.pop();
    }
  }
  visit(0, []);
  return result;
}

const pairs = combinations(universe, 2);
const localHistogram = {
  parallel: { 1: 0, 2: 0, 4: 0 },
  skew: { 1: 0, 2: 0, 4: 0 },
};
const configurationCounts = { parallel: 0, skew: 0 };
let admittedTotal = 0;
for (const omitted of pairs) {
  const support = new Set(universe.filter((point) => !omitted.includes(point)));
  for (const missing of pairs) {
    if (missing.some((point) => omitted.includes(point))) continue;
    const type =
      (omitted[0] ^ omitted[1]) === (missing[0] ^ missing[1])
        ? "parallel"
        : "skew";
    configurationCounts[type] += 1;
    const counts = [];
    for (const plane of planes) {
      const points = admitted(plane, support, new Set(missing));
      if (!affine(points)) throw new Error("non-affine local list");
      counts.push(points.length);
      localHistogram[type][points.length] += 1;
      admittedTotal += points.length;
    }
    counts.sort((a, b) => a - b);
    const expected =
      type === "parallel"
        ? [2, 2, 2, 2, 2, 2, 4]
        : [1, 1, 2, 2, 2, 4, 4];
    if (counts.join(",") !== expected.join(",")) {
      throw new Error("unexpected local orbit profile");
    }
  }
}
if (
  configurationCounts.parallel !== 84 ||
  configurationCounts.skew !== 336 ||
  localHistogram.parallel[1] !== 0 ||
  localHistogram.parallel[2] !== 504 ||
  localHistogram.parallel[4] !== 84 ||
  localHistogram.skew[1] !== 672 ||
  localHistogram.skew[2] !== 1008 ||
  localHistogram.skew[4] !== 672 ||
  admittedTotal !== 6720
) {
  throw new Error("local census totals disagree");
}

const rawReference = await readFile(referencePath);
const witness = JSON.parse(rawReference.toString("utf8"));
const vertexCount = witness.vertices;
const edges = witness.edges;
const flow = witness.flow;
const pointLabels = witness.point_labels;
if (vertexCount !== 34 || edges.length !== 51) {
  throw new Error("wrong strict witness dimensions");
}

const incidence = Array.from({ length: vertexCount }, () => []);
const seenEdges = new Set();
edges.forEach(([left, right], edge) => {
  if (left === right) throw new Error("loop in simple witness");
  const edgeKey = `${Math.min(left, right)},${Math.max(left, right)}`;
  if (seenEdges.has(edgeKey)) throw new Error("parallel edge in simple witness");
  seenEdges.add(edgeKey);
  incidence[left].push(edge);
  incidence[right].push(edge);
});
if (incidence.some((row) => row.length !== 3)) {
  throw new Error("witness is not cubic");
}

function reachable(skippedEdge = -1) {
  const reached = new Set([0]);
  const stack = [0];
  while (stack.length) {
    const vertex = stack.pop();
    for (const edge of incidence[vertex]) {
      if (edge === skippedEdge) continue;
      const [left, right] = edges[edge];
      const next = left === vertex ? right : left;
      if (!reached.has(next)) {
        reached.add(next);
        stack.push(next);
      }
    }
  }
  return reached.size;
}
if (reachable() !== vertexCount) throw new Error("witness disconnected");
for (let edge = 0; edge < edges.length; ++edge) {
  if (reachable(edge) !== vertexCount) throw new Error("witness has bridge");
}

const vertexPlanes = incidence.map((row) => {
  const values = row.map((edge) => flow[edge]);
  if (
    values.includes(0) ||
    new Set(values).size !== 3 ||
    (values[0] ^ values[1] ^ values[2]) !== 0
  ) {
    throw new Error("invalid local Fano flow row");
  }
  const plane = planeMap.get(key([0, ...values]));
  if (!plane) throw new Error("unknown local Fano plane");
  return plane;
});

if (pointLabels.length !== edges.length) throw new Error("label count");
pointLabels.forEach(([first, second], edge) => {
  if (first === second || (first ^ second) !== flow[edge]) {
    throw new Error("label difference mismatch");
  }
});
for (let vertex = 0; vertex < vertexCount; ++vertex) {
  for (const point of universe) {
    const degree = incidence[vertex].filter((edge) =>
      pointLabels[edge].includes(point),
    ).length;
    if (degree % 2) throw new Error("point parity failure");
  }
  const points = new Set(
    incidence[vertex].flatMap((edge) => pointLabels[edge]),
  );
  if (points.size !== 3) throw new Error("local labels are not a triangle");
  const potential = [...points].reduce((sum, point) => sum ^ point, 0);
  if (key(points) !== key(triangle(vertexPlanes[vertex], potential))) {
    throw new Error("potential reconstruction failure");
  }
}

function localEquations(points) {
  const base = points[0];
  const equations = [];
  for (let functional = 1; functional < 8; ++functional) {
    if (
      points.every(
        (point) => parity(functional & (point ^ base)) === 0,
      )
    ) {
      equations.push([functional, parity(functional & base)]);
    }
  }
  return equations;
}

function systemRows(support, missing) {
  const variableCount = 3 * vertexCount;
  const rows = [];
  for (let vertex = 0; vertex < vertexCount; ++vertex) {
    const points = admitted(vertexPlanes[vertex], support, missing);
    if (!affine(points)) return { variableCount, impossible: true, rows };
    for (const [functional, rhs] of localEquations(points)) {
      let mask = 0n;
      for (let coordinate = 0; coordinate < 3; ++coordinate) {
        if (functional & (1 << coordinate)) {
          mask |= 1n << BigInt(3 * vertex + coordinate);
        }
      }
      rows.push([mask, rhs]);
    }
  }
  edges.forEach(([left, right], edge) => {
    const value = flow[edge];
    const otherLeft = flow[incidence[left].find((item) => item !== edge)];
    const otherRight = flow[incidence[right].find((item) => item !== edge)];
    const constant = otherLeft ^ otherRight;
    for (let functional = 1; functional < 8; ++functional) {
      if (parity(functional & value)) continue;
      let mask = 0n;
      for (let coordinate = 0; coordinate < 3; ++coordinate) {
        if (functional & (1 << coordinate)) {
          mask ^= 1n << BigInt(3 * left + coordinate);
          mask ^= 1n << BigInt(3 * right + coordinate);
        }
      }
      rows.push([mask, parity(functional & constant)]);
    }
  });
  return { variableCount, impossible: false, rows };
}

function highestBitIndex(value) {
  let index = -1;
  for (let work = value; work; work >>= 1n) index += 1;
  return index;
}

function solveAffine(support, missing) {
  const built = systemRows(support, missing);
  if (built.impossible) return { sat: false, dimension: null };
  const coefficientMask = (1n << BigInt(built.variableCount)) - 1n;
  const rhsBit = 1n << BigInt(built.variableCount);
  const basis = new Map();
  for (const [mask, rhs] of built.rows) {
    let row = mask | (rhs ? rhsBit : 0n);
    while (row & coefficientMask) {
      const pivot = highestBitIndex(row & coefficientMask);
      if (basis.has(pivot)) row ^= basis.get(pivot);
      else {
        basis.set(pivot, row);
        row = 0n;
      }
    }
    if (row === rhsBit) return { sat: false, dimension: null };
  }
  return { sat: true, dimension: built.variableCount - basis.size };
}

const fixedSupport = new Set([0, 3, 4, 5, 6, 7]);
const fixedMissing = new Set([4, 5]);
const literalUsedPairs = new Set(pointLabels.map((pair) => key(pair)));
const literalExpectedPairs = new Set(
  combinations([...fixedSupport].sort((a, b) => a - b), 2)
    .filter((pair) => key(pair) !== key(fixedMissing))
    .map(key),
);
if (
  literalUsedPairs.size !== 14 ||
  [...literalUsedPairs].some((pair) => !literalExpectedPairs.has(pair)) ||
  [...literalExpectedPairs].some((pair) => !literalUsedPairs.has(pair))
) {
  throw new Error("literal cover does not use all fourteen allowed pairs");
}
const fixedResult = solveAffine(fixedSupport, fixedMissing);
if (!fixedResult.sat || fixedResult.dimension !== 1) {
  throw new Error("fixed six-point system mismatch");
}

let fivePasses = 0;
for (const support of combinations(universe, 5)) {
  if (solveAffine(new Set(support), null).sat) fivePasses += 1;
}
if (fivePasses !== 0) throw new Error("strict witness has a five-point lift");

const sixPasses = [];
for (const omitted of pairs) {
  const support = new Set(universe.filter((point) => !omitted.includes(point)));
  for (const missing of combinations([...support].sort((a, b) => a - b), 2)) {
    const result = solveAffine(support, new Set(missing));
    if (result.sat) {
      sixPasses.push({
        omitted,
        missing,
        kind:
          (omitted[0] ^ omitted[1]) === (missing[0] ^ missing[1])
            ? "parallel"
            : "skew",
        dimension: result.dimension,
      });
    }
  }
}
const expectedPassKeys = [
  "0,3|4,5",
  "0,3|6,7",
  "1,2|4,5",
  "1,2|6,7",
  "4,7|0,1",
  "4,7|2,3",
  "5,6|0,1",
  "5,6|2,3",
];
if (
  sixPasses.map((row) => `${row.omitted}|${row.missing}`).join(";") !==
    expectedPassKeys.join(";") ||
  sixPasses.some((row) => row.kind !== "skew" || row.dimension !== 1)
) {
  throw new Error("six-point pass profile mismatch");
}

const report = {
  schema: "six-point-one-hole-affine-independent-js-v1",
  status: "PASS",
  local: {
    configurationCounts,
    localHistogram,
    admittedTotal,
  },
  strictWitness: {
    referenceSha256: createHash("sha256").update(rawReference).digest("hex"),
    graphPremises: "simple cubic connected bridgeless",
    fivePointPasses: fivePasses,
    sixPointOneHolePasses: sixPasses,
    literalAllowedPairTypesUsed: literalUsedPairs.size,
  },
  scope:
    "Independent exact replay for finite loopless cubic fixed-flow systems; not a FiveCDC resolution.",
};
console.log(JSON.stringify(report, null, 2));
