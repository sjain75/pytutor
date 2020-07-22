import { Injectable } from '@angular/core';
import { Professor } from '../classes/professor';

const submit = document.getElementById("#submit");
const profUsername = document.getElementById("#profUsername");
const reportInputForm = document.getElementById("#reportInputForm");
const reportpage = document.getElementById("reportpage");

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  professors: Professor[] = [];

  public loadReport() {
    // Look up better way to do this.
    window.location.replace(`http://pytutor.ddns.net/${profUsername}/pages/report.html`);
  }

  constructor() { }
}
