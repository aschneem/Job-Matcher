export interface Script {
    name: string
    actions: Action[]
    headless: boolean
}

export enum ActionType {
    Nav = "Nav",
    Click = "Click",
    Fill = "Fill",
    Press = "Press",
    Sleep = "Sleep",
    SetResult = "SetResult",
    Loop = "Loop",
    Evaluate = "Evaluate",
    Back = "Back",
}

export enum KeyType {
    string = "string",
    RegEx = "RegEx",
}

export interface Action {
    action: ActionType
    actionValue?: string
    targetKey?: string
    targetGetBy?: string
    targetRole?: string
    targetKeyExact?: boolean
    targetKeyType?: KeyType
    loopActions?: Action[]
}