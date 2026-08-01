#!/usr/bin/env node

import fs from "node:fs";

const resultPath = new URL(
  "./rooted-cycle-translation-blockers-result.json",
  import.meta.url,
);
const frozen = JSON.parse(fs.readFileSync(resultPath, "utf8"));

const labels = [];
const even = [];
for (let value = 0; value < 32; value += 1) {
  const size = value.toString(2).replaceAll("0", "").length;
  if (size === 2) labels.push(value);
  if (size % 2 === 0) even.push(value);
}
if (labels.length !== 10 || even.length !== 16) {
  throw new Error("bad D5/even-subspace construction");
}

function members(support) {
  return labels
    .map((_, index) => index)
    .filter((index) => (support & (1 << index)) !== 0);
}

function connected(support) {
  const rows = members(support);
  if (rows.length === 0) return false;
  const reached = new Set([rows[0]]);
  const stack = [rows[0]];
  while (stack.length > 0) {
    const first = stack.pop();
    for (const second of rows) {
      if (!reached.has(second) && (labels[first] & labels[second]) !== 0) {
        reached.add(second);
        stack.push(second);
      }
    }
  }
  return reached.size === rows.length;
}

function blocker(support) {
  for (const shift of even) {
    if (shift === 0) continue;
    let admissible = true;
    for (const index of members(support)) {
      if (!labels.includes(labels[index] ^ shift)) {
        admissible = false;
        break;
      }
    }
    if (admissible) return false;
  }
  return true;
}

function endpoints(label) {
  const result = [];
  for (let vertex = 0; vertex < 5; vertex += 1) {
    if ((label & (1 << vertex)) !== 0) result.push(vertex);
  }
  if (result.length !== 2) throw new Error("non-edge label");
  return result;
}

function degreeProfile(support) {
  const degrees = [0, 0, 0, 0, 0];
  for (const index of members(support)) {
    const [left, right] = endpoints(labels[index]);
    degrees[left] += 1;
    degrees[right] += 1;
  }
  return degrees.sort((left, right) => right - left).join(",");
}

function isBipartite(support) {
  const adjacency = [[], [], [], [], []];
  for (const index of members(support)) {
    const [left, right] = endpoints(labels[index]);
    adjacency[left].push(right);
    adjacency[right].push(left);
  }
  const colour = [null, null, null, null, null];
  for (let start = 0; start < 5; start += 1) {
    if (colour[start] !== null) continue;
    colour[start] = 0;
    const stack = [start];
    while (stack.length > 0) {
      const vertex = stack.pop();
      for (const other of adjacency[vertex]) {
        if (colour[other] === null) {
          colour[other] = 1 - colour[vertex];
          stack.push(other);
        } else if (colour[other] === colour[vertex]) {
          return false;
        }
      }
    }
  }
  return true;
}

function characterized(support) {
  const profile = degreeProfile(support).split(",").map(Number);
  if (profile.includes(0)) return false;
  if (!isBipartite(support)) return true;
  return profile.join(",") === "4,1,1,1,1";
}

const connectedRows = [];
const blockers = [];
const mismatches = [];
for (let support = 1; support < 1 << 10; support += 1) {
  if (!connected(support)) continue;
  connectedRows.push(support);
  if (blocker(support)) blockers.push(support);
  if (blocker(support) !== characterized(support)) mismatches.push(support);
}

const minimal = blockers.filter((support) =>
  members(support).every((index) => !blocker(support ^ (1 << index))),
);
const profiles = {};
for (const support of minimal) {
  const profile = degreeProfile(support);
  profiles[profile] = (profiles[profile] ?? 0) + 1;
}

const replay = {
  characterization_mismatches: mismatches.length,
  connected_blockers: blockers.length,
  connected_supports: connectedRows.length,
  even_shift_universe: even.length,
  inclusion_minimal_connected_blockers: minimal.length,
  label_universe: labels.length,
  minimal_blocker_degree_profiles: Object.fromEntries(
    Object.entries(profiles).sort(),
  ),
  nonempty_supports: (1 << 10) - 1,
  schema: "five-cdc-rooted-cycle-translation-blockers-v1",
};

if (JSON.stringify(replay) !== JSON.stringify(frozen)) {
  throw new Error(
    `replay mismatch\nobserved=${JSON.stringify(replay)}\nfrozen=${JSON.stringify(frozen)}`,
  );
}
console.log("PASS rooted cycle translation blocker replay");
