export class Professor {
    private _name: string;
    private _link: string;

    constructor(name:string, link:string) {
        this._name=name;
        this._link=link;
    }

    get name() {
        return this._name;
    }

    get link() {
        return this._link;
    }
}