import { Token } from "./token";

export interface POSData{
    [key: string]: Token[];
}

export const DISPLAY_POS: string[] = ['VERB', 'PROPN', 'NOUN', 'ADV', 'ADJ'];