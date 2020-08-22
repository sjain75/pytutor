import { Injectable } from '@angular/core';
import { Professor } from '../classes/professor';

@Injectable({
  providedIn: 'root'
})
export class HomeService {
  professors: Professor[] = [];

  public loadHome() {
    var homepage = <HTMLIFrameElement>document.getElementById("homepage");
    var homeProfUsername = <HTMLInputElement>document.getElementById("homeProfUsername");
    var homeInputForm = document.getElementById("homeInputForm");
    homepage.src = `http://pytutor.ddns.net/${homeProfUsername.value}/pages/home.html`;
    homepage.classList.remove("hidden");
    homeInputForm.classList.add("hidden");
  }

  constructor() { }
}
