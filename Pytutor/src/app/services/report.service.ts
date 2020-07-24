import { Injectable } from '@angular/core';
import { Professor } from '../classes/professor';

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  professors: Professor[] = [];

  public loadReport() {
    var reportpage = <HTMLIFrameElement>document.getElementById("reportpage");
    var profUsername = <HTMLInputElement>document.getElementById("profUsername");
    var reportInputForm = document.getElementById("reportInputForm");
    reportpage.src = `http://pytutor.ddns.net/${profUsername.value}/pages/report.html`;
    console.log(reportpage.src);
    reportpage.classList.remove("hidden");
    reportInputForm.classList.add("hidden");
  }

  constructor() { }
}
