#!/usr/bin/env node
// Independent JavaScript replay of four_pole_two_plus_two_algebra.py.

import fs from "node:fs";

const names = [
  "AA", "AT2", "T2T2", "AT3", "AT4",
  "T2T3", "T2T4", "T3T3", "T3T4", "T4T4",
];
const ends = [
  [0, 0], [0, 1], [1, 1], [0, 2], [0, 3],
  [1, 2], [1, 3], [2, 2], [2, 3], [3, 3],
];

function permutations(values) {
  if (values.length === 0) return [[]];
  const answer = [];
  for (let index = 0; index < values.length; ++index) {
    const remainder = values.slice(0, index).concat(values.slice(index + 1));
    for (const suffix of permutations(remainder)) {
      answer.push([values[index], ...suffix]);
    }
  }
  return answer;
}

const colourPermutations = permutations([0, 1, 2, 3, 4]);
const labels = [];
for (let left = 0; left < 5; ++left) {
  for (let right = left + 1; right < 5; ++right) {
    labels.push((1 << left) | (1 << right));
  }
}

function transformed(mask, permutation) {
  let answer = 0;
  for (let colour = 0; colour < 5; ++colour) {
    if ((mask >> colour) & 1) answer |= 1 << permutation[colour];
  }
  return answer;
}

function wordKey(word) {
  return word.join(",");
}

function canonical(word) {
  let answer = null;
  for (const permutation of colourPermutations) {
    const candidate = word.map((mask) => transformed(mask, permutation));
    let smaller = answer === null;
    if (answer !== null) {
      for (let index = 0; index < candidate.length; ++index) {
        if (candidate[index] === answer.word[index]) continue;
        smaller = candidate[index] < answer.word[index];
        break;
      }
    }
    if (smaller) answer = { key: wordKey(candidate), word: candidate };
  }
  return answer;
}

const allWords = [];
const representativeMap = new Map();
for (const a of labels) for (const b of labels) {
  for (const c of labels) for (const d of labels) {
    if ((a ^ b ^ c ^ d) !== 0) continue;
    const word = [a, b, c, d];
    allWords.push(word);
    const representative = canonical(word);
    representativeMap.set(representative.key, representative.word);
  }
}
const representatives = [...representativeMap.values()].sort(
  (left, right) => {
    for (let index = 0; index < 4; ++index) {
      if (left[index] !== right[index]) return left[index] - right[index];
    }
    return 0;
  },
);
if (representatives.length !== 10) throw new Error("orbit count");
const orbitByKey = new Map(
  representatives.map((word, index) => [wordKey(word), index]),
);
const classes = Array.from({ length: 10 }, () => []);
for (const word of allWords) {
  classes[orbitByKey.get(canonical(word).key)].push(word);
}

const table = Array.from({ length: 10 }, () => Array(10).fill(0));
for (let leftType = 0; leftType < 10; ++leftType) {
  for (let rightType = 0; rightType < 10; ++rightType) {
    let output = 0;
    const rightBuckets = new Map();
    for (const word of classes[rightType]) {
      const key = `${word[0]},${word[1]}`;
      if (!rightBuckets.has(key)) rightBuckets.set(key, []);
      rightBuckets.get(key).push(word);
    }
    for (const leftWord of classes[leftType]) {
      const key = `${leftWord[2]},${leftWord[3]}`;
      for (const rightWord of rightBuckets.get(key) ?? []) {
        const boundary = [
          leftWord[0], leftWord[1], rightWord[2], rightWord[3],
        ];
        output |= 1 << orbitByKey.get(canonical(boundary).key);
      }
    }
    table[leftType][rightType] = output;
  }
}

function has(mask, left, right) {
  if (left > right) [left, right] = [right, left];
  const index = ends.findIndex(
    ([first, second]) => first === left && second === right,
  );
  return ((mask >> index) & 1) !== 0;
}

function lemmaAdmissible(mask) {
  for (let vertex = 0; vertex < 4; ++vertex) {
    const loop = has(mask, vertex, vertex);
    const neighbours = [];
    for (let other = 0; other < 4; ++other) {
      if (other !== vertex && has(mask, vertex, other)) neighbours.push(other);
    }
    if (neighbours.length === 1 && !loop) return false;
    if (loop && neighbours.length === 0) return false;
    if (!loop) continue;
    let extension = false;
    for (const other of neighbours) {
      if (has(mask, other, other)) extension = true;
    }
    for (let first = 0; first < neighbours.length; ++first) {
      for (let second = first + 1; second < neighbours.length; ++second) {
        if (has(mask, neighbours[first], neighbours[second])) extension = true;
      }
    }
    if (!extension) return false;
  }
  return true;
}

function compose(left, right) {
  let output = 0;
  for (let i = 0; i < 10; ++i) if ((left >> i) & 1) {
    for (let j = 0; j < 10; ++j) if ((right >> j) & 1) {
      output |= table[i][j];
    }
  }
  return output;
}

const allowed = [];
for (let mask = 1; mask < 1024; ++mask) {
  if (lemmaAdmissible(mask)) allowed.push(mask);
}
const exceptionalFour = [0x119, 0x2b, 0x53];
const exceptionalFive = [0x2e4, 0x3a4, 0x3c4];
const exceptional = new Set([...exceptionalFour, ...exceptionalFive]);
const counts = {};
for (const target of [...exceptionalFour, ...exceptionalFive]) {
  let total = 0;
  let withoutExceptionalFactor = 0;
  for (const left of allowed) for (const right of allowed) {
    if (compose(left, right) !== target) continue;
    ++total;
    if (!exceptional.has(left) && !exceptional.has(right)) {
      ++withoutExceptionalFactor;
    }
  }
  counts[`0x${target.toString(16)}`] = [total, withoutExceptionalFactor];
}

const resultPath = new URL(
  "./four-pole-two-plus-two-algebra-result.json",
  import.meta.url,
);
const frozen = JSON.parse(fs.readFileSync(resultPath, "utf8"));
const frozenTable = frozen.singleton_composition_table.map((row) =>
  row.map((cell) =>
    cell.reduce((mask, name) => mask | (1 << names.indexOf(name)), 0)
  )
);

if (allWords.length !== frozen.ordered_boundary_words) {
  throw new Error("word count mismatch");
}
if (classes.map((row) => row.length).join(",") !==
    frozen.orbit_representatives.map((row) => row.orbit_size).join(",")) {
  throw new Error("orbit-size mismatch");
}
if (JSON.stringify(table) !== JSON.stringify(frozenTable)) {
  throw new Error("composition-table mismatch");
}
if (allowed.length !== frozen.published_lemma_admissible_nonempty_signatures) {
  throw new Error("lemma-filter mismatch");
}
for (const [target, [total, withoutExceptionalFactor]] of Object.entries(counts)) {
  const rows = frozen.factorizations[target];
  if (rows.length !== total) throw new Error(`factor count mismatch ${target}`);
  if (rows.filter((row) => !row.has_exceptional_factor).length !==
      withoutExceptionalFactor) {
    throw new Error(`exceptional-factor mismatch ${target}`);
  }
}

console.log(JSON.stringify({
  status: "PASS",
  words: allWords.length,
  orbit_sizes: classes.map((row) => row.length),
  lemma_admissible_masks: allowed.length,
  factorization_counts: counts,
}));
