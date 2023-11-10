import { Component } from '@angular/core';
import { SharedService } from '../service/shared.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  title: string = 'Employee Data Management';
  showFiller = false;
  constructor(public sharedService: SharedService) { }
  toggleSidebar() {
    this.sharedService.isExpanded = !this.sharedService.isExpanded;
    if (this.sharedService.isExpanded) this.sharedService.sidebarWidth = '160px';
    else this.sharedService.sidebarWidth = '64px';
  }
}
