import { Component } from '@angular/core';
import { SearchService } from '../services/search.service';
import { SearchConfig } from '../models/search';
import { SearchConfigDetailsComponent } from '../search-config-details/search-config-details.component';
import { NgFor, NgIf, UpperCasePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FileUploadComponent } from '../file-upload/file-upload.component';

@Component({
  selector: 'app-search-config',
  standalone: true,
  imports: [
    NgFor,
    NgIf,
    SearchConfigDetailsComponent,
    UpperCasePipe,
    RouterLink,
    FileUploadComponent
  ],
  templateUrl: './search-config.component.html',
  styleUrl: './search-config.component.scss'
})
export class SearchConfigComponent {
  constructor(private searchService: SearchService) {}

  searches: SearchConfig[] = [];
  selectedSearchConfig?: SearchConfig;

  ngOnInit(): void {
    this.getSearchConfigs();
  }

  getSearchConfigs(): void {
    this.searchService.getSearchConfigs()
      .subscribe(searches => this.searches = searches);
  }

  startSearch(name: string): void {
    this.searchService.runSearchConfig(name).subscribe(
      response => console.log(response)
    );
  }

  runAllSearches(): void {
    this.searchService.runAllSearches().subscribe(
      response => console.log(response)
    );
  }

  onSelect(searchConfig: SearchConfig): void {
    this.selectedSearchConfig = searchConfig;
  }

  uploadResume(fileList: FileList){
    if (fileList.length > 0) {
      const file = fileList.item(0);
      if (!file){
        return;
      }
      this.searchService.uploadSearch(file).subscribe(search => {
        this.searches.push(search);
      })
    }

  }
}
