import { Entity } from "./entity";
import { Keyword, KeywordContainer } from "./keyword";
import { POSData } from "./pos";

export interface Resume extends KeywordContainer {
    name: string,
    entities: Entity[],
    pos_data: POSData,
}