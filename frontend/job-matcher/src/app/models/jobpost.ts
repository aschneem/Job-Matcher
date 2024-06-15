import { Entity } from "./entity";
import { Keyword, KeywordContainer } from "./keyword";
import { MatchData } from "./matchdata";
import { POSData } from "./pos";

export interface JobPost extends KeywordContainer{
    contentID: string,
    entities: Entity[],
    match_data: MatchData,
    pos_data: POSData,
    postLink: string,
    search: string,
    searchName: string,
    timestamp: string,
    url: string,
}