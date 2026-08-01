#!/usr/bin/env node
// Independent JavaScript replay of the complete 12-vertex fixed-flow profile.

import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..", "..");
const reportPath = path.join(
  root,
  "output",
  "oum-combined-choice-12v",
  "all-flow-orbits.json",
);
const source = JSON.parse(await readFile(reportPath, "utf8"));
const flowRows = source.flow_orbits;
if (flowRows.length !== 900) throw new Error("wrong flow-orbit count");

const W = [...Array(8).keys()];
const edges = [
  [0, 6], [0, 7], [0, 8], [1, 6], [1, 7], [1, 9],
  [2, 6], [2, 10], [2, 11], [3, 7], [3, 10], [3, 11],
  [4, 8], [4, 9], [4, 10], [5, 8], [5, 9], [5, 11],
];
const incidence = Array.from({ length: 12 }, () => []);
edges.forEach(([left, right], edge) => {
  incidence[left].push(edge);
  incidence[right].push(edge);
});
if (incidence.some((row) => row.length !== 3)) throw new Error("not cubic");

function parity(value) {
  let answer = 0;
  for (let work = value; work; work &= work - 1) answer ^= 1;
  return answer;
}

function sortedKey(values) {
  return [...values].sort((a, b) => a - b).join(",");
}

const planeMap = new Map();
for (let first = 1; first < 8; ++first) {
  for (let second = first + 1; second < 8; ++second) {
    const plane = new Set([0, first, second, first ^ second]);
    planeMap.set(sortedKey(plane), plane);
  }
}
if (planeMap.size !== 7) throw new Error("plane enumeration");

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

const pairs = combinations(W, 2);

function translated(points, shift) {
  return points.map((point) => point ^ shift).sort((a, b) => a - b);
}

const fiveRepMap = new Map();
for (const support of combinations(W, 5)) {
  const representative = W.map((shift) => translated(support, shift))
    .sort((left, right) => sortedKey(left).localeCompare(sortedKey(right)))[0];
  fiveRepMap.set(sortedKey(representative), representative);
}
const fiveRepresentatives = [...fiveRepMap.values()].sort((left, right) =>
  sortedKey(left).localeCompare(sortedKey(right)),
);

const pairRepMap = new Map();
for (const omitted of pairs) {
  const support = W.filter((point) => !omitted.includes(point));
  for (const missing of combinations(support, 2)) {
    const images = W.map((shift) => [
      translated(omitted, shift),
      translated(missing, shift),
    ]).sort((left, right) =>
      `${sortedKey(left[0])}|${sortedKey(left[1])}`.localeCompare(
        `${sortedKey(right[0])}|${sortedKey(right[1])}`,
      ),
    );
    const representative = images[0];
    pairRepMap.set(
      `${sortedKey(representative[0])}|${sortedKey(representative[1])}`,
      representative,
    );
  }
}
const pairRepresentatives = [...pairRepMap.values()].sort((left, right) =>
  `${sortedKey(left[0])}|${sortedKey(left[1])}`.localeCompare(
    `${sortedKey(right[0])}|${sortedKey(right[1])}`,
  ),
);
if (fiveRepresentatives.length !== 7 || pairRepresentatives.length !== 63) {
  throw new Error("translation orbit count");
}

function localTriangle(plane, potential) {
  return [...plane]
    .filter((point) => point !== 0)
    .map((point) => point ^ potential);
}

function allowed(plane, support, missing) {
  return W.filter((potential) => {
    const triangle = localTriangle(plane, potential);
    if (triangle.some((point) => !support.has(point))) return false;
    return !missing || ![...missing].every((point) => triangle.includes(point));
  });
}

function affineRows(points) {
  if (!points.length) return null;
  const base = points[0];
  const translatedPoints = new Set(points.map((point) => point ^ base));
  for (const left of translatedPoints) {
    for (const right of translatedPoints) {
      if (!translatedPoints.has(left ^ right)) throw new Error("local non-affine");
    }
  }
  const rows = [];
  for (let functional = 1; functional < 8; ++functional) {
    if (
      points.every(
        (point) => parity(functional & (point ^ base)) === 0,
      )
    ) {
      rows.push([functional, parity(functional & base)]);
    }
  }
  return rows;
}

function highestBit(value) {
  let answer = -1;
  for (let work = value; work; work >>= 1n) answer += 1;
  return answer;
}

function soluble(flow, support, missing) {
  const variableCount = 36;
  const rows = [];
  const planes = incidence.map((incident) => {
    const values = incident.map((edge) => flow[edge]);
    if (
      values.includes(0) ||
      new Set(values).size !== 3 ||
      (values[0] ^ values[1] ^ values[2]) !== 0
    ) {
      throw new Error("not a nowhere-zero flow");
    }
    const plane = planeMap.get(sortedKey([0, ...values]));
    if (!plane) throw new Error("bad local plane");
    return plane;
  });
  for (let vertex = 0; vertex < 12; ++vertex) {
    const localRows = affineRows(allowed(planes[vertex], support, missing));
    if (localRows === null) return false;
    for (const [functional, rhs] of localRows) {
      let mask = 0n;
      for (let bit = 0; bit < 3; ++bit) {
        if (functional & (1 << bit)) {
          mask |= 1n << BigInt(3 * vertex + bit);
        }
      }
      rows.push([mask, rhs]);
    }
  }
  edges.forEach(([left, right], edge) => {
    const value = flow[edge];
    const otherLeft = flow[incidence[left].find((candidate) => candidate !== edge)];
    const otherRight = flow[incidence[right].find((candidate) => candidate !== edge)];
    const offset = otherLeft ^ otherRight;
    for (let functional = 1; functional < 8; ++functional) {
      if (parity(functional & value)) continue;
      let mask = 0n;
      for (let bit = 0; bit < 3; ++bit) {
        if (functional & (1 << bit)) {
          mask ^= 1n << BigInt(3 * left + bit);
          mask ^= 1n << BigInt(3 * right + bit);
        }
      }
      rows.push([mask, parity(functional & offset)]);
    }
  });
  const coefficientMask = (1n << BigInt(variableCount)) - 1n;
  const rhsBit = 1n << BigInt(variableCount);
  const basis = new Map();
  for (const [mask, rhs] of rows) {
    let row = mask | (rhs ? rhsBit : 0n);
    while (row & coefficientMask) {
      const pivot = highestBit(row & coefficientMask);
      if (basis.has(pivot)) row ^= basis.get(pivot);
      else {
        basis.set(pivot, row);
        row = 0n;
      }
    }
    if (row === rhsBit) return false;
  }
  return true;
}

const orbitProfile = new Map();
const labelledProfile = new Map();
for (const row of flowRows) {
  const flow = row.flow;
  const five = fiveRepresentatives.some((support) =>
    soluble(flow, new Set(support), null),
  );
  const sixHole = pairRepresentatives.some(([omitted, missing]) =>
    soluble(
      flow,
      new Set(W.filter((point) => !omitted.includes(point))),
      new Set(missing),
    ),
  );
  const general = row.successful_potentials > 0;
  if (five && !sixHole) throw new Error("five does not imply six-hole");
  if (sixHole && !general) throw new Error("six-hole does not imply general");
  const profileKey = `five=${Number(five)},six_hole=${Number(sixHole)},general=${Number(general)}`;
  orbitProfile.set(profileKey, (orbitProfile.get(profileKey) || 0) + 1);
  labelledProfile.set(
    profileKey,
    (labelledProfile.get(profileKey) || 0) + row.gl3_orbit_size,
  );
}

const expectedOrbit = {
  "five=0,six_hole=0,general=0": 64,
  "five=0,six_hole=0,general=1": 18,
  "five=0,six_hole=1,general=1": 252,
  "five=1,six_hole=1,general=1": 566,
};
const expectedLabelled = {
  "five=0,six_hole=0,general=0": 10752,
  "five=0,six_hole=0,general=1": 3024,
  "five=0,six_hole=1,general=1": 42336,
  "five=1,six_hole=1,general=1": 94080,
};
for (const [profileKey, expected] of Object.entries(expectedOrbit)) {
  if (orbitProfile.get(profileKey) !== expected) throw new Error("orbit profile");
}
for (const [profileKey, expected] of Object.entries(expectedLabelled)) {
  if (labelledProfile.get(profileKey) !== expected) {
    throw new Error("labelled profile");
  }
}

console.log(
  JSON.stringify(
    {
      schema: "six-point-one-hole-all-flow-12v-independent-js-v1",
      status: "PASS",
      flowOrbits: flowRows.length,
      translationOrbitRepresentatives: {
        fiveSets: fiveRepresentatives.length,
        sixPointOneHolePairs: pairRepresentatives.length,
      },
      orbitProfile: Object.fromEntries([...orbitProfile].sort()),
      labelledFlowProfile: Object.fromEntries([...labelledProfile].sort()),
      scope: "Independent exact fixed-flow census on one graph; not a FiveCDC resolution.",
    },
    null,
    2,
  ),
);
