import { Injectable } from '@angular/core';
import { Professor } from '../classes/professor';

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  professors: Professor[] = [];

  public loadReport() {
    // Look up better way to do this.
    var profUsername = <HTMLInputElement>document.getElementById("profUsername");
    window.location.replace(`http://pytutor.ddns.net/${profUsername.value}/pages/report.html`);
  }

  constructor() { }
}
