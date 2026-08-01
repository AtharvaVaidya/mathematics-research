#!/usr/bin/env node
// Independent bit-mask replay of the five-point/Fano-line list theorem.

function bits(mask) {
  const result = [];
  for (let point = 0; point < 8; point += 1) {
    if ((mask >>> point) & 1) result.push(point);
  }
  return result;
}

function xor(values) {
  return values.reduce((total, value) => total ^ value, 0);
}

function chooseMasks(size) {
  const result = [];
  for (let mask = 0; mask < 256; mask += 1) {
    if (bits(mask).length === size) result.push(mask);
  }
  return result;
}

const triples = chooseMasks(3);
const fiveSets = chooseMasks(5);
const planeByTriple = new Map();
const planes = new Set();

for (const triple of triples) {
  const [a, b, c] = bits(triple);
  const directions = [0, a ^ b, a ^ c, b ^ c];
  const plane = directions.reduce((mask, point) => mask | (1 << point), 0);
  planeByTriple.set(triple, plane);
  planes.add(plane);
}

if (planes.size !== 7 || triples.length !== 56 || fiveSets.length !== 56) {
  throw new Error("wrong ambient enumeration");
}

let specialCases = 0;
let ordinaryCases = 0;
let admitted = 0;

for (const five of fiveSets) {
  const forbidden = 0xff ^ five;
  const singleton = xor(bits(forbidden));
  if (!((five >>> singleton) & 1)) {
    throw new Error("affine-plane fourth point is not admitted");
  }
  const special = planeByTriple.get(forbidden);
  const otherCoset = five ^ (1 << singleton);

  for (const plane of planes) {
    const allowed = triples.filter(
      (triple) => planeByTriple.get(triple) === plane && (triple & ~five) === 0,
    );
    const expected = plane === special ? 4 : 1;
    if (allowed.length !== expected) throw new Error("wrong local list size");
    admitted += allowed.length;

    if (plane === special) {
      specialCases += 1;
      for (const triple of allowed) {
        if ((triple >>> singleton) & 1) {
          throw new Error("special triangle uses singleton");
        }
        if (triple & ~otherCoset) throw new Error("special triangle leaves coset");
      }
      continue;
    }

    ordinaryCases += 1;
    const triangle = allowed[0];
    if (!((triangle >>> singleton) & 1)) {
      throw new Error("ordinary triangle misses singleton");
    }
    const common = bits(plane & special).filter((point) => point !== 0);
    if (common.length !== 1) throw new Error("wrong line intersection");

    const trianglePoints = bits(triangle);
    for (const difference of bits(plane).filter((point) => point !== 0)) {
      const pairs = [];
      for (let i = 0; i < 3; i += 1) {
        for (let j = i + 1; j < 3; j += 1) {
          if ((trianglePoints[i] ^ trianglePoints[j]) === difference) {
            pairs.push([trianglePoints[i], trianglePoints[j]]);
          }
        }
      }
      if (pairs.length !== 1) throw new Error("difference has wrong multiplicity");
      const includesSingleton = pairs[0].includes(singleton);
      if (includesSingleton === (difference === common[0])) {
        throw new Error("pair-shape classification failed");
      }
    }
  }
}

const result = {
  schema: "five-cdc-five-point-triangle-list-independent-v1",
  five_point_sets: fiveSets.length,
  fano_lines: planes.size,
  special_line_cases: specialCases,
  nonspecial_line_cases: ordinaryCases,
  allowed_local_triangles: admitted,
  result: "PASS",
};
process.stdout.write(`${JSON.stringify(result)}\n`);
