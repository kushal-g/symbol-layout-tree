import type { NarrationTerm } from './types/narration'

export interface Example {
  name: string
  latex: string
  narrations: NarrationTerm[]
}

export const EXAMPLES: Example[] = [
  {
    name: 'PEMDAS',
    latex: String.raw`2 + 3 \times 4 - 6 \div 2`,
    narrations: [
      { term: String.raw`3 \times 4`, narration: 'Multiplication is evaluated before addition and subtraction', pos: 1 },
      { term: String.raw`6 \div 2`, narration: 'Division is also evaluated before addition and subtraction', pos: 1 },
    ],
  },
  {
    name: 'Fraction',
    latex: String.raw`\frac{a+b}{c-d}`,
    narrations: [
      { term: 'a+b', narration: 'Numerator', pos: 1 },
      { term: 'c-d', narration: 'Denominator', pos: 1 },
    ],
  },
  {
    name: 'Matrix (7x10)',
    latex: String.raw`\begin{pmatrix} a_{1,1} & a_{1,2} & a_{1,3} & a_{1,4} & a_{1,5} & a_{1,6} & a_{1,7} & a_{1,8} & a_{1,9} & a_{1,10} \\ a_{2,1} & a_{2,2} & a_{2,3} & a_{2,4} & a_{2,5} & a_{2,6} & a_{2,7} & a_{2,8} & a_{2,9} & a_{2,10} \\ a_{3,1} & a_{3,2} & a_{3,3} & a_{3,4} & a_{3,5} & a_{3,6} & a_{3,7} & a_{3,8} & a_{3,9} & a_{3,10} \\ a_{4,1} & a_{4,2} & a_{4,3} & a_{4,4} & a_{4,5} & a_{4,6} & a_{4,7} & a_{4,8} & a_{4,9} & a_{4,10} \\ a_{5,1} & a_{5,2} & a_{5,3} & a_{5,4} & a_{5,5} & a_{5,6} & a_{5,7} & a_{5,8} & a_{5,9} & a_{5,10} \\ a_{6,1} & a_{6,2} & a_{6,3} & a_{6,4} & a_{6,5} & a_{6,6} & a_{6,7} & a_{6,8} & a_{6,9} & a_{6,10} \\ a_{7,1} & a_{7,2} & a_{7,3} & a_{7,4} & a_{7,5} & a_{7,6} & a_{7,7} & a_{7,8} & a_{7,9} & a_{7,10} \end{pmatrix}`,
    narrations: [
      { term: 'a_{1,1}', narration: 'Top-left corner: row 1, column 1', pos: 1 },
      { term: 'a_{4,5}', narration: 'An interior entry: row 4, column 5', pos: 1 },
      { term: 'a_{7,10}', narration: 'Bottom-right corner: row 7, column 10', pos: 1 },
    ],
  },
  {
    name: 'Camera Matrix (rotation + translation)',
    latex: String.raw`\begin{pmatrix} r_{1,1} & r_{1,2} & r_{1,3} & t_1 \\ r_{2,1} & r_{2,2} & r_{2,3} & t_2 \\ r_{3,1} & r_{3,2} & r_{3,3} & t_3 \end{pmatrix}`,
    narrations: [
      { term: 'r_{1,1}', narration: 'Rotation block R, which encodes the camera’s orientation', pos: 1 },
      { term: 't_1', narration: 'Translation vector t, which encodes the camera’s position', pos: 1 },
    ],
  },
  {
    name: 'Quadratic Formula (increasing complexity)',
    latex: String.raw`\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}`,
    narrations: [
      { term: String.raw`\pm`, narration: 'Two roots: one with +, one with -', pos: 1 },
      { term: 'b^2 - 4ac', narration: 'The discriminant, determines the number of real roots', pos: 1 },
      { term: '2a', narration: 'Twice the leading coefficient', pos: 1 },
    ],
  },
  {
    name: 'Taylor Series (even more complex)',
    latex: String.raw`\sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n`,
    narrations: [
      { term: String.raw`f^{(n)}(a)`, narration: 'nth derivative of f evaluated at a', pos: 1 },
      { term: 'n!', narration: 'n factorial, normalizes the nth derivative term', pos: 1 },
      { term: '(x-a)^n', narration: 'Distance from the expansion point, raised to the nth power', pos: 1 },
    ],
  },
]
