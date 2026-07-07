export interface NarrationTerm {
  term: string
  narration: string
  pos: number
}

export interface Narration extends NarrationTerm {
  id: string
}
