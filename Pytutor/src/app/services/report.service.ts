import { Injectable } from '@angular/core';
import { Professor } from '../classes/professor';

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  professors: Professor[] = [];

  public loadReport() {
    var reportpage = <HTMLIFrameElement>document.getElementById("reportpage");
    var reportProfUsername = <HTMLInputElement>document.getElementById("reportProfUsername");
    var reportInputForm = document.getElementById("reportInputForm");
    reportpage.src = `http://pytutor.ddns.net/${reportProfUsername.value}/pages/report.html`;
    reportpage.classList.remove("hidden");
    reportInputForm.classList.add("hidden");
  }

  constructor() { }
}
