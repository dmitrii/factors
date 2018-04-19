import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class FactorService {
  public API;
  public FACTORS_API;

  constructor(private http: HttpClient) { 
    if (window.location.hostname == "localhost") {
      this.API = "//localhost:8080"; // development mode
    } else {
      this.API = "//" + window.location.hostname;
    }
    this.FACTORS_API = this.API + "/factors";
  }

  getAll(): Observable<any> {
    return this.http.get(this.FACTORS_API);
  }

  get(number: string) {
    return this.http.get(this.FACTORS_API + '/' + number);
  }
}
