import { Component, Input } from '@angular/core';
import { JobPost } from '../models/jobpost';
import { Resume } from '../models/resume';
import { Keyword, KeywordContainer } from '../models/keyword';
import { NgFor, NgIf, SlicePipe } from '@angular/common';
import { emitDistinctChangesOnlyDefaultValue } from '@angular/compiler';

@Component({
  selector: 'app-keyword-display',
  standalone: true,
  imports: [
    NgFor,
    NgIf,
    SlicePipe,
  ],
  templateUrl: './keyword-display.component.html',
  styleUrl: './keyword-display.component.scss'
})
export class KeywordDisplayComponent {
  @Input() data?: KeywordContainer;
  @Input() key?: string;
  maxDisplayed = 10;
  showAll = false;

  toggleShowAll() {
    if (this.maxDisplayed > 10){
      this.maxDisplayed = 10;
      this.showAll = false;
    } else {
      this.maxDisplayed = this.getKeywords().length;
      this.showAll = true;
    }
  }

  getKeywords() : Keyword[] {
    const key = this.key;
    const data = this.data;
    if (!key || !data){
      return []
    }
    if (key === 'text_rank') {
      return data.text_rank;
    }
    if (key === 'rakeResults') {
      return data.rakeResults;
    }
    return [];
  }

  min(a:number, b:number): number {
    return Math.min(a, b);
  }

  truncate(value:number): string {
    return (''+value).substring(0,6);
  }
}
