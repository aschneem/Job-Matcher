export interface SearchConfig {
    url: string,
    skip: boolean,
    extraDelay?: number,
    searchBoxGetBy?: string,
    searchBoxKey?: string,
    searchButtonGetBy?: string,
    searchButtonRole?: string,
    searchButtonKey?: string,
    searchButtonKeyExact?: boolean,
    jobPostsCSSSelector: string,
    jobPostsContentCSSSelector: string,
    headless: boolean,
    name: string,
    runData: RunData,
}

export interface RunData{
    search_status: string,
    search_start_time?: string,
    search_end_time?: string,
}