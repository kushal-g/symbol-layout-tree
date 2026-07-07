import { StreamLanguage } from '@codemirror/language'
import { stex } from '@codemirror/legacy-modes/mode/stex'

export const stexLanguage = StreamLanguage.define(stex)
