import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ServiceMain {
  
  private address = environment.API_BASE_URL;
  constructor(private http: HttpClient) { }


  handle_post_requests(userObject: any, endpoint: string) {
    console.log(`${this.address}/${endpoint}`);
    return this.http.post<any>(`${this.address}/${endpoint}`, userObject)
  }
}
