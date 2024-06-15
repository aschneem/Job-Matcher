import { Component, Input } from '@angular/core';
import { SearchConfig } from '../models/search';
import { NgFor, NgIf, UpperCasePipe } from '@angular/common';

@Component({
  selector: 'app-search-config-details',
  standalone: true,
  imports: [
    NgFor,
    NgIf,
    UpperCasePipe
  ],
  templateUrl: './search-config-details.component.html',
  styleUrl: './search-config-details.component.scss'
})
export class SearchConfigDetailsComponent {
  @Input() searchConfig?: SearchConfig


}
