#!/usr/bin/env node
// Independent bit-set replay of rooted_three_pole_signature_factorization.py.

import fs from "node:fs";

const path = process.argv[2] ??
  "scratch/rooted-three-pole-signature-factorization-result.json";
const frozen = JSON.parse(fs.readFileSync(path, "utf8"));
const orbits = [
  [0b00011],
  [0b00101],
  [0b00110],
  [0b01001, 0b10001],
  [0b01010, 0b10010],
  [0b01100, 0b10100],
  [0b11000],
];

function labels(mask) {
  const answer = [];
  for (let orbit = 0; orbit < 7; ++orbit) {
    if ((mask >>> orbit) & 1) answer.push(...orbits[orbit]);
  }
  return answer;
}

function relation(left, right) {
  let answer = 0;
  for (const first of labels(left)) {
    for (const second of labels(right)) {
      if (first === second) answer |= 1;
      else if (first & second) answer |= 2;
      else answer |= 4;
    }
  }
  return answer;
}

const names = new Map([
  [1, "E"], [2, "I"], [4, "D"], [3, "EI"],
  [5, "ED"], [6, "ID"], [7, "EID"],
]);
const profile = {};
const equality = [];
const disjoint = [];
let equalIntersect = 0;
for (let left = 1; left < 128; ++left) {
  for (let right = 1; right < 128; ++right) {
    const value = relation(left, right);
    const name = names.get(value);
    profile[name] = (profile[name] ?? 0) + 1;
    if (value === 1) equality.push([left, right]);
    if (value === 4) disjoint.push([left, right]);
    if (value === 3) ++equalIntersect;
  }
}

const unordered = new Set(
  disjoint.map(([left, right]) =>
    `${Math.min(left, right)},${Math.max(left, right)}`)
);
const expectedEquality = new Set(["1,1", "2,2", "4,4", "64,64"]);
const observedEquality = new Set(equality.map(pair => pair.join(",")));
if (JSON.stringify([...observedEquality].sort()) !==
    JSON.stringify([...expectedEquality].sort())) {
  throw new Error("equality-only classification mismatch");
}
if (disjoint.length !== 26 || unordered.size !== 13 ||
    equalIntersect !== 231) {
  throw new Error("special relation count mismatch");
}
const profileKeys = [...new Set([
  ...Object.keys(profile), ...Object.keys(frozen.relation_profile),
])].sort();
for (const key of profileKeys) {
  if (profile[key] !== frozen.relation_profile[key]) {
    throw new Error(`relation profile differs at ${key}`);
  }
}
if (JSON.stringify(orbits) !== JSON.stringify(frozen.orbit_labels)) {
  throw new Error("orbit list differs from frozen result");
}
if (frozen.disjoint_only_ordered_count !== 26 ||
    frozen.disjoint_only_unordered_count !== 13 ||
    frozen.equal_intersect_ordered_count !== 231 ||
    frozen.status !== "PASS") {
  throw new Error("frozen summary mismatch");
}
console.log(JSON.stringify({
  status: "PASS",
  relation_profile: profile,
  equality_only: equality.length,
  disjoint_only_ordered: disjoint.length,
  disjoint_only_unordered: unordered.size,
  equal_intersect_ordered: equalIntersect,
}));
