// The pilot stays opt-in and outside release feeds. No graph service or browser script.
import fs from 'node:fs';
import path from 'node:path';

export function loadLineage(root) {
  const file = path.join(root, 'notes/knowledge-lineage/graph.json');
  if (!fs.existsSync(file)) return null;
  const graph = JSON.parse(fs.readFileSync(file, 'utf8'));
  const nodes = new Map(graph.nodes.map(node => [node.id, node]));
  return {
    ...graph,
    trails: graph.trails.map(trail => ({ ...trail,
      steps: trail.steps.map(step => ({ ...step, connections: trail.links.filter(link => link.subject === step.id).map(link => ({ ...link, objectTitle: nodes.get(link.object).title })) })),
    })),
    edges: graph.edges.map(edge => ({ ...edge,
      subjectTitle: nodes.get(edge.subject).title,
      objectTitle: nodes.get(edge.object).title,
    })),
  };
}
