import { Component } from '@angular/core';
import { SharedService } from '../service/shared.service';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent {

  constructor(public sharedService: SharedService) { }
}
