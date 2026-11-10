import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { loadLineage } from '../lib/lineage.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const graph = JSON.parse(fs.readFileSync(path.join(root, 'notes/knowledge-lineage/graph.json'), 'utf8'));

test('lineage evidence is grounded in the frozen input, not just a generated assertion', () => {
  const ids = new Set(graph.nodes.map(n => n.id));
  assert.equal(ids.size, graph.nodes.length);
  const files = new Map(Object.keys(graph.inputs).map(file => [file, execFileSync('git', ['show', `${graph.input_commit}:${file}`], { cwd: root, encoding: 'utf8' })]));
  for (const edge of graph.edges) {
    assert.ok(ids.has(edge.subject) && ids.has(edge.object), edge.id);
    assert.ok(files.get(edge.evidence.path).includes(edge.evidence.passage), edge.id);
    const lines = files.get(edge.evidence.path).split('\n');
    assert.ok(lines.slice(edge.evidence.line_start - 1, edge.evidence.line_end).join('\n').includes(edge.evidence.passage), edge.id);
    assert.ok(!['causes', 'influenced', 'proves-benefit'].includes(edge.predicate));
  }
  assert.equal(graph.claims.length, 17);
  assert.equal(graph.external.length, 12);
  assert.deepEqual(graph.claims.map(c => c.ordinal), Array.from({ length: 17 }, (_, i) => i * 5 + 1));
  assert.equal(graph.candidates.find(c => c.id === 'candidate-bridge').status, 'inferred');
  assert.ok(!graph.edges.some(e => e.id === 'candidate-bridge'));
});

test('reading order never chooses a relationship direction', () => {
  const view = loadLineage(root);
  for (const trail of view.trails) for (const step of trail.steps) {
    for (const link of step.connections) assert.equal(link.subject, step.id);
  }
  const finding = view.trails[0];
  assert.equal(finding.steps[0].connections.length, 0);
  assert.equal(finding.steps[3].connections[0].object, 'finding-prior');
  assert.equal(finding.steps[3].connections[0].predicate, 'revises');
});
