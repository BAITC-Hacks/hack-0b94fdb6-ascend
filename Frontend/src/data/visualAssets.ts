import brandMark from '../assets/brand/freedom-graph.png'
import critical from '../assets/priority/critical.jpeg'
import high from '../assets/priority/high.jpeg'
import medium from '../assets/priority/medium.jpeg'
import low from '../assets/priority/low.jpeg'
import minimal from '../assets/priority/minimal.jpeg'

// Order matches riskIndex and translated labels. Source files remain unchanged.
export const priorityArtwork = [critical, high, medium, low, minimal] as const
export { brandMark }
