export class Correo  {
	_id :     string;
    url:      string; 
    idCorreo: string;
    titulo:   string;
    donde:    string;
    urlOk:    string; 
    summary:  string;
    pagina:   string;
    corpus:   {palabra: string,frecuencia:number} [];
    fecha:    Date;
    control:  string;
    decision: string;
    observaciones: string;
    SI: number;
    NO: number;
    urlDonde: string;
    company: string;
    isSended: boolean;
    numeroCorreo: number;
    modelos: {modelo:string,decisionPRED:string,porcentPRED:number} [];
    porcentPREDAvg : number;
}   
