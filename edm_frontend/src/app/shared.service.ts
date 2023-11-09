import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  public isExpanded: boolean = false;
  public sidebarWidth = '48px';
  constructor() { }
  
}
