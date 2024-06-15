import { Compare } from "./compare"
import { MatchData } from "./matchdata"

export interface ResumePostCompare {
    postID: string
    resume: string
    searchName: string
    postUrl: string
    postTitle: string
    postText: string
    resumeText: string
    entities: Compare
    nounCompare: Compare
    properNounCompare: Compare
    verbCompare: Compare
    adverbCompare: Compare
    adjectiveCompare: Compare
    textRankCompare: Compare
    rakeCompare: Compare
    match_data: MatchData
}