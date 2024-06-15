export interface Keyword {
    keyword: string,
    score: number
}

export interface KeywordContainer {
    text_rank: Keyword[],
    rakeResults: Keyword[],
}