import { Component, Input } from '@angular/core';
import { Compare } from '../models/compare';
import { NgFor, NgIf, SlicePipe } from '@angular/common';

@Component({
  selector: 'app-compare-section',
  standalone: true,
  imports: [
    NgIf,
    NgFor,
    SlicePipe
  ],
  templateUrl: './compare-section.component.html',
  styleUrl: './compare-section.component.scss'
})
export class CompareSectionComponent {
  @Input() compareData?: Compare
  
  maxDisplay: number = 10;

  displayAllSuggestions: boolean = false;
  displayAllIntersection: boolean = false;
  displayAllResume: boolean = false;
  displayAllPost: boolean = false;

  toggleSuggestions() : void{
    this.displayAllSuggestions = true;
  }

  toggleIntersection(): void {
    this.displayAllIntersection = true;
  }

  toggleResume(): void {
    this.displayAllResume = true;
  }

  togglePost(): void {
    this.displayAllPost = true;
  }

  min(a: number,b: number): number {
    if (a <= b){
      return a;
    }
    return b;
  }

}
